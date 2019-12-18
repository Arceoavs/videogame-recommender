import os
import pandas as pd
import sqlalchemy
from sqlalchemy.dialects import postgresql
from utilities import engine

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/giantbomb/releases.csv'))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';', quotechar='|')

# Drop guid and game_name column
df = df.drop(['guid', 'game_name'], axis=1)

df.to_sql('stage_releases', engine, schema='giantbomb', if_exists='replace', index=False, dtype={
  'release_date': sqlalchemy.types.TIMESTAMP,
  })