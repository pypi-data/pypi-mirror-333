"""
Plot data for every US county.
#https://altair-viz.github.io/user_guide/transform/lookup.html#user-guide-lookup-transform
"""
import altair as alt
from vega_datasets import data
import random
from test_nws import find_active_alert
cid_set = find_active_alert()
import test_nws


counties = alt.topo_feature(data.us_10m.url, 'counties')

ud = data('unemployment')
cs = data('us_10m')
randomizing = True
randomizing = False
if randomizing:
    ud['rate'] = [random.random() for v in ud['rate']]

#for i in range(111): ud.at[i, 'rate'] = 0.99


for (index, row) in df.iterrows():
    rid = str(int(row['id']))
    if rid in cid_set:
        ud.at[index, 'rate'] = 0.99


chart = alt.Chart(counties).mark_geoshape().encode(
    color='rate:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(ud, 'id', ['rate'])
).properties(
    projection={'type': 'albersUsa'},
    width=500, height=300
)


chart.save('counties.html')   # visible in the browser


assert list(cs) == ['type', 'transform', 'objects', 'arcs']
assert cs['type'] == 'Topology'
assert cs['transform'] == {'scale': [0.003589294092944858, 0.0005371535195261037], 'translate': [-179.1473400003406, 17.67439566600018]}
obs = cs['objects']
assert list(obs) == ['counties', 'states', 'land']
xc = obs['counties']
xs = obs['states']
xl = obs['land']
arcs = cs['arcs']

udids = ud['id']
assert sum([len(str(x))==4 for x in udids]) == 314 
assert sum([len(str(x))==5 for x in udids]) == 2904
assert len(udids) == 314 + 2904



