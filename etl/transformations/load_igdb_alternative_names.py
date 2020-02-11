import os
import pandas as pd
import sqlalchemy
from utilities import engine

'''
Loads igdb aliases/alternative names from csv file into stage_alternative_names table of schema igdb.
'''

file_name = 'alternative_names'
file_dir = 'igdb'

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../datasets/{file_dir}/{file_name}.csv'))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';', quotechar='|')

df.to_sql(f'stage_{file_name}', engine, schema=file_dir, if_exists='replace', index=False, dtype={
    'game': sqlalchemy.types.INT # Pandas type inference is double, but ids are ints
  })