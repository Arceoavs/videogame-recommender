import os
import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy.dialects import postgresql
from utilities import engine, liststringToList

file_name = 'games'
file_dir = 'igdb'

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../datasets/{file_dir}/{file_name}.csv'))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';', quotechar='|')

# Convert numeric timestamp to date
df['first_release_date'] = pd.to_datetime(df.first_release_date, unit='s')

# Convert some list strings in lists
df['alternative_names'] = df.alternative_names.apply(liststringToList)
df['franchises'] = df.franchises.apply(liststringToList)
df['genres'] = df.genres.apply(liststringToList)
df['involved_companies'] = df.involved_companies.apply(liststringToList)
df['keywords'] = df.keywords.apply(liststringToList)
df['platforms'] = df.platforms.apply(liststringToList)
df['release_dates'] = df.release_dates.apply(liststringToList)
df['similar_games'] = df.similar_games.apply(liststringToList)
df['themes'] = df.themes.apply(liststringToList)

# Drop some columns
df = df.drop(['bundles', 'dlcs', 'expansions', 'franchise', 'game_engines', 'popularity', 'rating', 'aggregated_rating', 'total_rating'], axis=1)

# dtypes are only needed, if pandas type inference is wrong and typing with pandas is too difficult!
df.to_sql(f'stage_{file_name}', engine, schema=file_dir, if_exists='replace', index=False, dtype={
    'first_release_date': sqlalchemy.types.TIMESTAMP,
    'parent_game': sqlalchemy.types.INT,
    'version_parent': sqlalchemy.types.INT,
    'alternative_names': postgresql.ARRAY(sqlalchemy.types.INT),
    'franchises': postgresql.ARRAY(sqlalchemy.types.INT),
    'genres': postgresql.ARRAY(sqlalchemy.types.INT),
    'involved_companies': postgresql.ARRAY(sqlalchemy.types.INT),
    'keywords': postgresql.ARRAY(sqlalchemy.types.INT),
    'platforms': postgresql.ARRAY(sqlalchemy.types.INT),
    'release_dates': postgresql.ARRAY(sqlalchemy.types.INT),
    'similar_games': postgresql.ARRAY(sqlalchemy.types.INT),
    'themes': postgresql.ARRAY(sqlalchemy.types.INT),
  })