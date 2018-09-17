import pandas as pd

from datapackage_utilities import building


df = pd.read_csv('archive/demand.csv')

# set the names
df['name'] = df['bus'].apply(lambda row: row + '-electricity-load')

# set the profile names
df['profile'] = df['bus'].apply(lambda row: row + '-load-profile')

# necessary
df.set_index('name', inplace=True)

building.write_elements('load.csv', df)
