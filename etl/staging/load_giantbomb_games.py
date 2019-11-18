import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://videogamer:pwned-by-headshot-1337@localhost:5432/videogames')

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../datasets/giantbomb/games.csv'))

missing_values = [',', '.', '..', '...', '....', '-', '--', '---']
df = pd.read_csv(file_path, sep=';', quotechar='|', na_values=missing_values)

# Drop guid column
df = df.drop(['guid'], axis=1)

print(df.dtypes)

df.to_sql('stage_games', engine, schema='giantbomb', if_exists='replace', index=False)