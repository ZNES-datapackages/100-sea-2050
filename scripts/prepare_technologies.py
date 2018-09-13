import pandas as pd

from datapackage_utilities import building

config = building.get_config()

def annuity(capex, n, wacc):
    return capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)

df = pd.read_csv('archive/techno-economic-assumptions.csv', index_col=0)
df.drop('source (c,l,e)', axis=1, inplace=True)

types = config['sources']

element_dfs = {t: building.read_elements(t + '.csv') for t in types}

buses = config['buses']

data = dict(zip(types, [{},{},{}]))

df.index = df.index.str.replace(' ', '_')

for idx, row in df.iterrows():
    for b in buses:
        element_name = idx + '_' + b
        element = dict(row)

        # add tech specific data
        if row['type'] == 'dispatchable':
            if 'ror' in idx:
                edge_parameters = {'summed_max': 4000}
            else:
                edge_parameters = {}
            element.update({
                'capacity_cost': annuity(
                    row['costs in US/kW'], row['lifetime'], 0.07) * 1000,
                'capacity_potential': None,
                'bus': b,
                'tech': idx,
                'edge_parameters': edge_parameters})

        if row['type'] == 'volatile':
            element.update({
                'capacity_cost': annuity(
                    row['costs in US/kW'], row['lifetime'], 0.07) * 1000,
                'capacity_potential': None,
                'bus': b,
                'tech': idx,
                'profile': element_name + '-profile'})

        if row['type'] == 'storage':
            element.update({
                'bus': b,
                'tech': idx,
                'capacity_ratio': 0.2,
                'capacity_cost': annuity(
                    row['costs in US/kW'], row['lifetime'], 0.07) * 1000,
                'loss': 0})

        data[row['type']][element_name] = element

# write elements to CSV-files
for element_type in element_dfs:
    path = building.write_elements(
            element_type + '.csv',
            pd.DataFrame.from_dict(data[element_type], orient='index'))
