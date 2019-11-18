import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://videogamer:pwned-by-headshot-1337@localhost:5432/videogames')

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../datasets/giantbomb/releases.csv'))

df = pd.read_csv(file_path, sep=';', quotechar='|')

# Drop guid and game_name column
df = df.drop(['guid', 'game_name'], axis=1)

print(df.dtypes)

df.to_sql('stage_releases', engine, schema='giantbomb', if_exists='replace', index=False)