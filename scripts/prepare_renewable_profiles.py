import pandas as pd

from datapackage_utilities import building

df_seq = pd.read_csv('archive/volatile_profile.csv', parse_dates=True, index_col=0)

building.write_sequences('volatile_profile.csv', df_seq)
