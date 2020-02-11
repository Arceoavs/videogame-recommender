import os
import pandas as pd
from utilities import engine

'''
Loads giantbomb games from csv file into stage_games table of schema giantbomb.
Data quality issues are resolved.
'''

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/giantbomb/games.csv'))

print(f'Loading file {file_path} into database...')

missing_values = [',', '.', '..', '...', '....', '-', '--', '---']
df = pd.read_csv(file_path, sep=';', quotechar='|', na_values=missing_values)

# Drop guid column
df = df.drop(['guid'], axis=1)

print(df.dtypes)

df.to_sql('stage_games', engine, schema='giantbomb', if_exists='replace', index=False)