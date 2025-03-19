# Copyright (c) 2024-2025 Cary Miller
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.

from functools import lru_cache
from collections import defaultdict
import pytest

from apis.tools import parsed_file_or_url
from apis.api_tools import NonDictArgs, ValidDataBadResponse
from apis.nws import call, _validator, altered_raw_swagger, config
# TODO: consider making call behave like _validator.
# The behavior of the two is currently maybe surprising / inconsistent.
# but the code is currently minimal.
# but the change will be a one-liner.
from test_data.nws import test_parameters

import jsonschema
from apis.nws import DateOrderError

# a product as returned from the /products endpoint...
# {'@id': 'https://api.weather.gov/products/fafb7493-158a-4ff5-9ccb-7667e92508c1',
#  'id': 'fafb7493-158a-4ff5-9ccb-7667e92508c1',
#  'issuanceTime': '2025-01-22T18:42:00+00:00',
#  'issuingOffice': 'KBGM',
#  'productCode': 'RR2',
#  'productName': 'Hydro-Met Data Report Part 2',
#  'wmoCollectiveId': 'SRUS51'}
# TODO: note the issuanceTime is recent.
# I suppose a product has a limited lifetime.
# This feeds into the sequential API call idea.
# So...
# - grab a few random products
# - grab an id from one of them.
# - call that particular product

# TODO: also
# recall that observations disappear after a couple of months.
# So...
# Set a date for fetching observations 2-3 days in the past from today.
#            prerequest
# and then verify that we get some observations.
#            postrequest


# TODO: similar for alerts?????
# Keep hitting until we find one?
#            postman can do this but with considerable complexity.
#            Well, maybe not much more than we will do.
#            Maybe no more than we will do.
#
# BTW Include an optional `next_thing` var.
# and NOTE:  This means each `thing` needs a unique id.

class ThingSequence:
    def __init__(self, thingList):
        self.thingList = thingList
        for thing in self.thingList:
            thing.id = 'some unique id'
    def run_it(self, config):
        for thing in self.thingList:
            thing.run_it(thing.config)

global_env = {'a': 1, 'b': 'x'}
from copy import deepcopy
class Thing:
#     Inspired by Postman.
#     _id # unique amongst Things
#     endpoint, verb
#     parameters
#     code:  prerequest, postrequest
#     nextThing
#     environment(s)
# but wait.
# Postman has its many different environments.
# Shall we do the same here?
# Maybe start with two.

#     # Things Postman cannot do
#     api_base   # because we can easily do more than one.
#     def __init__(self, endpoint, verb, parameters, code, nextThing, environment):
#         self.endpoint = endpoint
    def __init__(self, config):
        self.config = config
        self.env =  {'a': 2}  # the most local environment

    def run_it(self, config):
      try:
        # update env
        env = {}
        for d in global_env, self.env:
            env.update(deepcopy(d))
        # run prerequest code
        self.config.code.prerequest(env)
        # call the endpoint
        # do not bother with validation because Postman does not.
        # HA!
        # NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO 
        # NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO 
        # NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO 
        # Do not fall into the trap of slavishly copying Postman.
        # Do optional validation as usual.
        # AHA!    brainwave!!! 
        # Validation can be done in prerequest code if desired.
        # NOTE
        # This suggests the possibility of NOT running the endpoint if
        # validation fails.
        # NOTE Postman runs the endpoint with or without error in prerequest
        # code.  We could do that, of course
        # BUT
        # do we want to?
        # If we don't then we get into issues of 
        self.config.code.postrequest(env)
      finally:
        globals().update(locals())


class Code:
    # TODO: how does environment fit?
    def __init__(self, pre, post):
        self.prerequest = pre
        self.postrequest = pre


t1 = Thing([])
#t1.run_it([])

# NOTE:  This will be a lot of work.
# But it will (I hope) be easier with the new Postman-inspired organization.
# ================================================================== #
# ================================================================== #

# {pre,post}request functions
# Next step...
# Have the two functions print out the endpoint, verb and environment.  DONE
# Next step after that...
# Define functions like in test_data.    DONE
# Next step after that...
# Assign a unique id to each (endpoint, verb, parameters) tuple
# and have an optional nextCall in the environment.


# Common tests
# Predicates
# ======================================================================= #

# TODO: feel free to add functions that return not just True, False but also
# slightly more complex things like a short list or a number.
# TODO: function to verify status code in a list (or specific number)
# TODO: function to verify parameter appears in response.json()

def always_true(response):
    return True

def is_success(response):
    return response.is_success and response.status_code == 200

def is_not_empty(response):
    return response.json() is not None

def is_fail(response):
    return not is_success(response)

def is_graph(response):
    return list(response.json()) == ['@context', '@graph']

def has_non_empty_observationStations(response):
    rj = response.json()
    return len(rj['observationStations']) > 1

def is_FeatureCollection(response):
    return response.json()['type'] == 'FeatureCollection'
 
def is_empty_FeatureCollection(response):
    assert is_FeatureCollection(response)
    return response.json()['features'] == [] 

def is_non_empty_FeatureCollection(response):
    assert is_FeatureCollection(response)
    return not is_empty_FeatureCollection(response)

def is_funky(response):
    rj = response.json()
    keys = list(rj)
    feats = rj['features']
    for feat in feats:
        pass
    1/0


# Endpoint tests
# ======================================================================= #
def setup_endpoint_verb_post_request():
    test_code = defaultdict(lambda: {})

    # ################ (endpoint, verb)-tests ################ #
    for ev in [
            ('/products', 'get'), 
            ('/products/types/{typeId}', 'get'),
        ]:
        test_code[ev]['good'] = [
                is_graph,
            ]

    for ev in [
            ('/alerts/active', 'get'),
            ('/stations/{stationId}/observations', 'get'),
        ]:
        test_code[ev]['good'] = [
                is_FeatureCollection,
            ]

    ev = ('/zones/forecast/{zoneId}/observations', 'get')
    test_code[ev]['good'] = [
            is_non_empty_FeatureCollection,
        ]

    ev = ('/zones/forecast/{zoneId}/stations', 'get')
    test_code[ev]['good'] = [
            is_non_empty_FeatureCollection,
            has_non_empty_observationStations,
        ]

    # ################ (endpoint, verb, params)-tests ################ #
    # Test one (endpoint, verb) with one set of args.
    ev = ('/stations/{stationId}/observations', 'get')
    args = {'stationId': 'CO100', 'end': '2024-09-17T18:39:00+00:00', 'start': '2024-09-18T18:39:00+00:00'}
    arg_key = str(sorted(list(args.items())))
    test_code[ev][arg_key] = [is_empty_FeatureCollection, ]  # OK!!!!!!

    # Test one (endpoint, verb) with one set of args.
    # Same endpoint.
    args = {'stationId': 'CO100', 'limit': '100'}
    arg_key = str(sorted(list(args.items())))
    test_code[ev][arg_key] = [is_non_empty_FeatureCollection, ]  # OK!!!!!!

    # Test one (endpoint, verb) with one set of args.
    # Test specific to one (endpoint, verb, args) combination.
    ev = ('/alerts/active', 'get')
    args = {'limit': '100'}
    arg_key = str(sorted(list(args.items())))
    test_code[ev][arg_key] = [is_non_empty_FeatureCollection, ]  # OK!!!!!!

    # Insert empty list   TODO: rm?
    for ev in test_code:
        assert 'good' in test_code[ev]
        if 'bad' not in test_code[ev]:
            test_code[ev]['bad'] = []
    blah = defaultdict(lambda: dict(good=[], bad=[]))
    for ev in test_code:
        blah[ev] = test_code[ev]

    return blah
    #
    # TODO: add tests for bad params here   DONE
    # priority: medium
    # difficulty: low


def setup_generic_post_request():
    test_code = {}
    test_code['good'] = [is_success, is_not_empty, ] 
    test_code['bad'] = [always_true, ] 
    return test_code
    # NOTE: The good/bad distinction is already something like the
    # Postman thing of grouped/sequential calls.


if 1:
    # generic tests
    post_request_generic = setup_generic_post_request()

    # (endpoint, verb)-specific tests
    post_request_endpoint = setup_endpoint_verb_post_request()
    assert post_request_endpoint[('ep', 'v')] == dict(good=[], bad=[])

    # TODO: also
    # tests for parameters having specific qualities, eg non-dict ??
    # That will be maybe back in the generic tests.  Yes.


# The new test +
# ======================================================================= #
from datetime import date, timedelta
import json
from jinja2 import Environment, PackageLoader, select_autoescape, DictLoader

def test_another():
  try:
    """
    test_more_new continues the basic testing paradigm I established 3 months
    ago.
    Move towards something different, more like Postman.
    Run a sequence of calls, using values from the environment.
    Set and fetch environment values using {pre,post}-request functions.
    also
    Introduce the next_request environment var.
    """
    # Scenario 1.  Request alerts for different regions until finding
    # a non-empty one.
    # Scenario 2.  Request observations 2-3 days in the past.
    # Scenario 3.  products expire?...
    #              So check the list of current products.
    #              Grab a productid
    #              Fetch info for that product. 
    #              Good, because involves two endpoints.
    # 
    # Scenario 2.  Request observations 2-3 days in the past.
    # 'end':     '2024-09-17T18:39:00+00:00', 
    environment = {'next_request': None}
    foo = pre_request_recent_obs(environment)
    assert foo is None
    assert 'start' in environment
    assert 'end' in environment
    foo = pre_request_set_region(environment)
    assert 'region' in environment
    # OK.  Setting environment values is easy enough.

    # How to get that value into a parameter?
    # Here's how...
    start_end_template = """{
        "stationId": "CO100",
        "end":     "{{ end }}", 
        "start":   "{{ start }}"
    }"""
    region_template = """{
        "region":     "{{ region }}"
    }"""
    productid_template = """{
        "productId":     "{{ productId }}"
    }"""

    mapping = dict(start_end=start_end_template,  region=region_template,   ) 
    dl = DictLoader(mapping)
    env = Environment( loader=dl, autoescape=select_autoescape())

    t = env.get_template('start_end')
    r = t.render(environment)
    print(r)
    e = json.loads(r)

    tr = env.get_template('region')
    rr = tr.render(environment)
    print(rr)
    er = json.loads(rr)

  finally:
    globals().update(locals())

# TODO: same as above with an ordinary function instead of templates.
def region_dict(region):
    return {"region": region}





def product_sequence():
  try:
    """
    This does the job of running sequential endpoints.
    Not in the way  of Postman but much more compactly.
    """
    # Find a current product.
    N = 10
    params = dict(limit=N)

    response = call('/products', 'get', params)
    rj = response.json()
    ks = list(rj)
    rg = rj['@graph']
    i = random.choice(range(N))
    thing = rg[i]
    productId = thing['id']
    print(f'Found a current product: {productId}')

    # Fetch a current product.
    params = dict(productId=productId)
    response = call('/products/{productId}', 'get', params)
    rj = response.json()
    productName = rj['productName']
    print(f'productName: {productName}')
  finally:
    globals().update(locals())


def pre_request_recent_obs(environment):
    # all about the side effects.
    today = date.today()
    environment['start'] = (today - timedelta(days=3)).strftime('%Y-%m-%dT18:11:22')
    environment['end'] = (today - timedelta(days=2)).strftime('%Y-%m-%dT18:11:22')

def pre_request_set_region(environment):
    environment['region'] = 'rrrrrrrrrrrrrrrr'


def get_all_zones():
    response = call('/zones', 'get', {})
    return response
    # 403 Forbidden status code.
    # wtf
    #gaz = get_all_zones() 


import random
from county_codes import (
#        id2state_name, id2county_name, county_name2id,
    state_name2id, county_ids, abrev2state_name, state_name2abrev,
)

stop_words = 'Eastern Western Central Northern Southern County'
stop_words = stop_words.split()

def find_active_alert():
    """Call /alerts/active on random states until an alert is found.
    """
    states = list(abrev2state_name)
    while True:
        state = random.choice(states)
        print(state)
        if state not in abrev2state_name:
            continue
        state_long = abrev2state_name[state]
        params = {'area': [state]}
        response = call('/alerts/active', 'get', params)
        rj = response.json()
        if (not 'features' in rj) or (not rj['features']):
            continue  # to next random state.
        cid_set = set()
        feats = rj['features']
        for feat in feats:
            props = feat['properties']
            event = feat['properties']['event']
            ad = feat['properties']['areaDesc']
            ad_parts = ad.split(';')
            for part in ad_parts:
                for word in stop_words:
                    if word in part:
                        part = part.replace(word, '')
                part = part.strip()
                key = f'{part} County'
                if state_long not in county_ids:
                    continue
                if key in county_ids[state_long]:
                    cid = county_ids[state_long][key]   # eg '16059'
                    print('  ', cid)
                    cid_set.add(cid)
            print(state, event, ad)
        if not cid_set:
            continue
        print(cid_set)
        print()
        globals().update(locals())
        break
    return cid_set


def test_more_new():
  try:
    """
    Run a bunch of individual api calls with...
    - multiple (endpoint, verb)
      - good, bad data
    """
    for (endpoint, verb) in test_parameters:
        print(endpoint, verb)
        test_data = test_parameters[(endpoint, verb)]

        for params in test_data['good']:
            do_good_one((endpoint, verb), params)

        for params in test_data['bad']:
            do_bad_one((endpoint, verb), params)
  finally:
    globals().update(locals())



def do_good_one(ev, params):
    """
    - validate
    - run the call with params
    - run the post_funcs
    """
    print('   good params       ', params)
    (endpoint, verb) = ev
    validator = _validator(endpoint, verb)
    assert validator.is_valid(params)
    print('   ok valid')
    response = call(endpoint, verb, params)
    post_funcs = get_post_funcs((endpoint, verb), 'good', params)
    for func in post_funcs:
        assert func(response)
        print('   ok test .......', func.__name__)
    print('   ok call verified')
    print()

def do_bad_one(ev, params):
    # Eliminate bad parameters before making the call.
    # If appropriate:
    #     make the call
    #     run the post_funcs
    (endpoint, verb) = ev
    print('   bad param(s)       ', params)
    validator = _validator(endpoint, verb)
    making_the_call = validate_baddies(params, validator)
    if not making_the_call:
        return
#        continue
    response = call(endpoint, verb, params)
    post_funcs = get_post_funcs((endpoint, verb), 'bad', params)
    for func in post_funcs:
        assert func(response)
        print('   ok bad test .......', func.__name__)
    print('   ok bad param verified')
    print()



def get_post_funcs(endpoint_verb, good_or_bad, args):
    assert type(endpoint_verb) is tuple
    assert len(endpoint_verb) == 2
    assert good_or_bad in 'good bad'.split()
    (endpoint, verb) = endpoint_verb
    generic = post_request_generic[good_or_bad] 
    pre = post_request_endpoint[(endpoint, verb)][good_or_bad]
    ev = endpoint_verb
    arg_key = str(sorted(list(args.items())))
    test_code = post_request_endpoint
    if arg_key in test_code[ev]:
        tce = test_code[ev][arg_key]
    else:
        tce = []
    return generic + pre + tce


def test_get_post_funcs():
    endpoint_verb = ('/stations/{stationId}/observations', 'get')
    good_or_bad = 'bad'
    args = {'stationId': 'CO100', 'end': '2024-09-17T18:39:00+00:00', 'start': '2024-09-18T18:39:00+00:00'}
    funcs = get_post_funcs(endpoint_verb, good_or_bad, args)
    fnames = [f.__name__ for f in funcs]
    assert fnames == ['always_true', 'is_empty_FeatureCollection']

    # Test for another set of args.   Same endpoint.
    args = {'stationId': 'CO100', 'limit': '100'}
    funcs = get_post_funcs(endpoint_verb, good_or_bad, args)
    fnames = [f.__name__ for f in funcs]
    assert fnames == ['always_true', 'is_non_empty_FeatureCollection']

    endpoint_verb = ('/alerts/active', 'get')
    args = {'limit': '100'}
    funcs = get_post_funcs(endpoint_verb, good_or_bad, args)
    fnames = [f.__name__ for f in funcs]
    assert fnames == ['always_true', 'is_non_empty_FeatureCollection']

    endpoint_verb = ('/alerts/active', 'get')
    args = {'limit': '100'}
    funcs = get_post_funcs(endpoint_verb, 'good', args)
    fnames = [f.__name__ for f in funcs]
    assert fnames == ['is_success', 'is_not_empty', 'is_FeatureCollection', 'is_non_empty_FeatureCollection']

    args = {'area': ['WY'], 'limit': 50}
    arg_key = str(sorted(list(args.items())))

    funcs = get_post_funcs(endpoint_verb, 'good', args)
    fnames = [f.__name__ for f in funcs]
    assert fnames == ['is_success', 'is_not_empty', 'is_FeatureCollection']


test_get_post_funcs()
test_get_post_funcs()
test_get_post_funcs()


def validate_baddies(params, validator):
    """
    Eliminate bad parameters before making the call.
    Some args are expected to work OK in the call despite failing validation.
    eg  '100' instead of 100.
    We make an effort to identify these and go ahead and make the call.
    """
    making_the_call = True
    try:
        validator.validate(params)  
    except jsonschema.exceptions.ValidationError as exc:
        eargs = exc.args
        ez = eargs[0]
        parts = ez.split()
        making_the_call = False

        if ez == f"'{params}' is not of type 'object'":
            print('   ok NonDictArgs .......', params)
        elif ez == f"{params} is not of type 'object'":
            print('   ok NonDictArgs .......', params)
        elif ez.endswith("is a required property"):
            print(f'   ok missing required property {parts[0]}')
        elif " is not of type " in ez:
            print('   ok Validation..TypeError .......', exc.args[0])
            # TODO: note this type of error often is accepted by the
            # endpoint and returns a good response.
            making_the_call = True
        elif " is not one of " in ez:
            print('   ok Validation..EnumError .......', exc.args[0])
        elif " does not match " in ez:
            print('   ok Validation..RegexError .......', exc.args[0])
        else:
            print('   ok ValidationError .......', exc.args[0])
            print('   ok ValidationError .......', exc.args[0])
            print('   ok ValidationError .......', exc.args[0])
            print('   ok ValidationError .......', exc.args[0])
            print('   ok ValidationError .......', exc.args[0])
            making_the_call = True

        print('   ok bad param verified')
        print()

    except DateOrderError as exc:
        print('   ok DateOrderError .......', exc.args[0])
        print('   ok bad param verified')
        print()
        # go ahead and make the call.  It will work but return nothing.
        making_the_call = True
    return making_the_call


# Original tests
# =========================================================



def demo_current_alerts(area='CO', zone='COZ040', event='Red Flag Warning'):
  try:
    denver_zone = 'COZ040'
    params = dict(zone=zone)
    params = dict(area=area, event=event)
    params = dict(area=area)
    endpoint, verb = '/alerts/active', 'get'
    response = call(endpoint, verb, params).json()
    feats = response['features']    # The interesting part
    return feats
  finally:
    cp = [a['properties'] for a in feats]
    for a in cp:
        az = a['affectedZones']
        ac = a['category']
        ae = a['event']
        ah = a['headline']
        ad = a['description']
        ax = a['areaDesc']
        ae = a['event']
        ae = a['event']
        print(ah)
        print('='*55)
        print(ad)
        print('='*55)
        print(' ' + ax.replace(';', '\n'))
        print()
        print()
    globals().update(locals())
#     return response['features']    # The interesting part
#     return response['type']        # 'FeatureCollection'
#     return response['title']       # string
#     return response['@context']    # list of stuff
#     return response['updated']     # timestamp


def demo_nws_series():
  try:
    """ Get a series of observations suitable for putting in a pandas DF,
    and then a jupyter notebook.
    """
    import pandas
    # Data
    endpoint = '/stations/{stationId}/observations'
    stationId = 'KRCM'   # OK
    stationId = 'CO100'   # OK
    params = {                                # OK
        'stationId': stationId, 
#         'start': '2024-11-13:59:00+00:00', 
#         'end': '2024-11-14:59:00+00:00', 
        'limit':   50,
    }
    # Seems it may require recent timestamps.
    validator = _validator(endpoint, 'get')
    assert validator.is_valid(params)

    response = call(endpoint, 'get', params)
    assert response.status_code == 200

    # Extract desired data from response.
    final = []
    feats = response.json()['features']
    assert feats
    for ft in feats: 
        pt = ft['properties']
        for key in [ '@id', '@type', 'elevation', 'station', 'rawMessage', 'icon', 'presentWeather', 'cloudLayers', 'textDescription', ]:
            pt.pop(key)
        for key in pt:
            if type(pt[key]) is dict:
                pt[key] = pt[key]['value']
        final.append(pt)

    # Convert to dataframe.
    df = pandas.DataFrame(final)
#    assert df.shape[0] > 10
    assert df.shape[1] == 15
    return df
  finally:
    globals().update(locals())


def test_current_alerts():
    # Because returning a value from a test generates a pytest warning.
    demo_current_alerts()


def test_nws_series():
    # Because returning a value from a test generates a pytest warning.
    demo_nws_series()

