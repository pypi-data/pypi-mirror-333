import os
url = 'https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt'
fpath = '~/local/gov/fips.txt'

with open(os.path.expanduser(fpath)) as fh:
    data = fh.readlines()

states = data[16:67]
counties = data[72:]


long_ones = []
for row in states:
    sp = row.split()
    if len(sp) > 2:
        long_ones.append(sp)

def split_plus(row):
    sp = row.split()
    if len(sp) == 2:
        return tuple(sp)
    return (sp[0], ' '.join(sp[1:]))

id2state_name = dict(split_plus(row) for row in states)
id2county_name = dict(split_plus(row) for row in counties)
county_name2id = dict((v,k) for (k,v) in id2county_name.items())
state_name2id = dict((v.title(),k) for (k,v) in id2state_name.items())


nd = {}
for row in counties:
    sr = row.split()
    (code, name) = split_plus(row)
    if code.endswith('000'):
        state_name = name
        nd[name] = {}
    else:
        (code, county_name) = split_plus(row)
        nd[state_name][county_name] = code
county_ids = nd




def all_states():
    import csv
    import os
    state_file = "~/local/info/states.csv"
    with open(os.path.expanduser(state_file)) as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader if row][1:]
    return dict([(v,k) for (k,v) in rows])
abrev2state_name = all_states()
state_name2abrev = dict((v,k) for (k,v) in abrev2state_name.items())


