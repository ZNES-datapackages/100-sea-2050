import pandas as pd

from datapackage_utilities import building

df = pd.read_csv('archive/demand.csv')

# set the names
df['name'] = df['bus'].apply(lambda row: row + '-electricity-load')

# set the profile names
df['profile'] = df['bus'].apply(lambda row: 'el-profile-' + row)

# necessary
df.set_index('name', inplace=True)

df_seq = pd.read_csv('archive/load_profile.csv', parse_dates=True, index_col=0)

building.write_sequences('load_profile.csv', df_seq)

building.write_elements('load.csv', df)
