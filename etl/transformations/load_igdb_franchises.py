import os
import pandas as pd
import sqlalchemy
from sqlalchemy.dialects import postgresql
from utilities import engine, liststringToList

file_name = 'franchises'
file_dir = 'igdb'

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../datasets/{file_dir}/{file_name}.csv'))
print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';', quotechar='|')

df['games'] = df.games.apply(liststringToList)


df.to_sql(f'stage_{file_name}', engine, schema=file_dir, if_exists='replace', index=False, dtype={
    'games': postgresql.ARRAY(sqlalchemy.types.INT)
  })