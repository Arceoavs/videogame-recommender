import os
import pandas as pd
from utilities import engine

'''
Loads giantbomb platforms from csv file into stage_platforms table of schema giantbomb.
'''

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/giantbomb/platforms.csv'))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';', quotechar='|')

print(df.dtypes)

df.to_sql('stage_platforms', engine, schema='giantbomb', if_exists='replace', index=False)