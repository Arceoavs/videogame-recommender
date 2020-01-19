import statistics
import math
import numpy as np
import pandas as pd
from queries import (
  select_giantbomb_games_with_integrated_metadata, 
  select_igdb_games_with_integrated_metadata, 
  select_metacritic_games_with_integrated_metadata,
  select_igdb_images,
  select_giantbomb_images,
  select_metacritic_images
)
from utilities import engine

debug = False # set this to True to see all steps

# determines value by priority
def determine_value(s1, s2, s3):
  if s1 is np.NaN:
    if s2 is np.NaN:
      if s3 is np.NaN:
        return ''
      return s3
    return s2
  return s1

def determine_mean(s1, s2, s3):
  nmbrs = []
  if not math.isnan(s1):
    nmbrs.append(s1)
  if not math.isnan(s2):
    nmbrs.append(s2)
  if not math.isnan(s3):
    nmbrs.append(s3)
  result = 'undefined'
  if len(nmbrs) > 0:
    return statistics.median(nmbrs)
  else:
    return np.NaN


def union_lists(s1, s2, s3):
  union = set()
  if s1 is not np.NaN and s1 is not None:
    s1 = s1.split(', ')
    union |= set(s1)
  if s2 is not np.NaN and s2 is not None:
    s2 = s2.split(', ')
    union |= set(s2)
  if s3 is not np.NaN and s3 is not None:
    s3 = s3.split(', ')
    union |= set(s3)
  return list(union)

with engine.connect() as connection:

  check_genres = pd.read_sql_query('SELECT * FROM genres', connection)
  if len(check_genres) == 0:
    print('[Integrate Games] Error: Please integrate genres first')
    exit()
  check_platforms = pd.read_sql_query('SELECT * FROM platforms', connection)
  if len(check_platforms) == 0:
    print('[Integrate Games] Error: Please integrate platforms first')
    exit()


  print('[Integrate Games] Select games')
  games = pd.read_sql_query('SELECT * FROM lookup.games', connection)

  g_games = select_giantbomb_games_with_integrated_metadata(connection).add_prefix('giantbomb_')
  i_games = select_igdb_games_with_integrated_metadata(connection).add_prefix('igdb_')
  m_games = select_metacritic_games_with_integrated_metadata(connection).add_prefix('metacritic_')
  print(f'[Integrate Games] {len(games)} games selected')

  print('[Integrate Games] Joining all game tables')
  games = games.merge(
    i_games, on='igdb_id', how='left'
  ).merge(
    g_games, on='giantbomb_id', how='left'
  ).merge(
    m_games, on='metacritic_id', how='left'
  )

  print('[Integrate Games] Merging all columns')
  games['title'] = games.apply(lambda row: determine_value(row.igdb_title, row.giantbomb_title, row.metacritic_title), axis=1)
  games['description'] = games.apply(lambda row: determine_value(row.igdb_description, row.giantbomb_description, np.NaN), axis=1)
  games['year'] = games.apply(lambda row: determine_mean(row.igdb_year, row.giantbomb_year, row.metacritic_year), axis=1)
  games['genre_ids'] = games.apply(lambda row: ', '.join(union_lists(row.igdb_genre_ids, row.metacritic_genre_ids, np.NaN)), axis=1)
  games['platform_ids'] = games.apply(lambda row: ', '.join(union_lists(row.igdb_platform_ids, row.giantbomb_platform_ids, row.metacritic_platform_ids)), axis=1)

  if debug:
    games.to_sql('debug_games_joined', engine, schema='lookup', if_exists='replace', index=False)
  
  games.drop(games.columns.difference(['id','title', 'description','year','genre_ids', 'platform_ids']), 1, inplace=True)

  if debug:
    games.to_sql('debug_games_joined_subset', engine, schema='lookup', if_exists='replace', index=False)


  print('[Integrate Games] Group similar entries')
  grouped = games.groupby('id', as_index=False).agg(lambda x: list(x))
  grouped['title'] = grouped['title'].apply(lambda t: t[0])
  grouped['description'] = grouped['description'].apply(lambda d: d[0] if len(d) > 0 else np.NaN)
  grouped['year'] = grouped['year'].apply(lambda t: t[0] if len(t) > 0 else np.NaN)
  grouped['genre_ids'] = grouped['genre_ids'].apply(lambda g: ', '.join(list(set(g))))
  grouped['platform_ids'] = grouped['platform_ids'].apply(lambda p: ', '.join(list(set(p))))

  print('[Integrate Games] Adding image URLs')
  igdb_images = select_igdb_images(connection)
  giantbomb_images = select_giantbomb_images(connection)
  metacritic_images = select_metacritic_images(connection)
  unioned_images = pd.concat([pd.concat([igdb_images, giantbomb_images], ignore_index=True), metacritic_images],
                             ignore_index=True)
  unique_images = unioned_images.groupby('id').first().reset_index()

  grouped = grouped.merge(unique_images, how='left', left_on='id', right_on='id')
  
  if debug:
    grouped.to_sql('debug_games_joined_and_grouped', engine, schema='lookup', if_exists='replace', index=False)


  # Create the dataframe for final games table
  integrated_games = grouped[['id', 'title', 'description', 'year', 'image_url']]

  # Create the dataframe for final games-genre-association table
  # We use a column exploding technique, see also:
  # https://medium.com/@sureshssarda/pandas-splitting-exploding-a-column-into-multiple-rows-b1b1d59ea12e
  game_genres = grouped[['id', 'genre_ids']]
  game_genres.columns = ['game_id', 'genre_ids']
  integrated_game_genres = pd.DataFrame(game_genres.genre_ids.str.split(', ').tolist(), index=game_genres.game_id).stack()
  integrated_game_genres = integrated_game_genres.reset_index([0, 'game_id'])
  integrated_game_genres.columns = ['game_id', 'genre_id']
  integrated_game_genres = integrated_game_genres.drop_duplicates()
  integrated_game_genres['genre_id'].replace('', np.nan, inplace=True)
  integrated_game_genres = integrated_game_genres.dropna(subset=['genre_id'])

  # Create the dataframe for final games-platform-association table
  game_platforms = grouped[['id', 'platform_ids']]
  game_platforms.columns = ['game_id', 'platform_ids']
  integrated_game_platforms = pd.DataFrame(game_platforms.platform_ids.str.split(', ').tolist(), index=game_platforms.game_id).stack()
  integrated_game_platforms = integrated_game_platforms.reset_index([0, 'game_id'])
  integrated_game_platforms.columns = ['game_id', 'platform_id']
  integrated_game_platforms = integrated_game_platforms.drop_duplicates()
  integrated_game_platforms['platform_id'].replace('', np.nan, inplace=True)
  integrated_game_platforms = integrated_game_platforms.dropna(subset=['platform_id'])

  print('[Integrate Games] Delete Flask table content')
  connection.execute('DELETE FROM game_genres')
  connection.execute('DELETE FROM game_platforms')
  connection.execute('DELETE FROM ratings')
  connection.execute('DELETE FROM games')

  print('[Integrate Games] Load integrated data to database')
  integrated_games.to_sql('games', engine, if_exists='append', index=False)
  print(f'[Integrate Games] {len(integrated_games)} games loaded into database')
  integrated_game_genres.to_sql('game_genres', engine, if_exists='append', index=False)
  print(f'[Integrate Games] {len(integrated_game_genres)} game-genre-associations loaded into database')
  integrated_game_platforms.to_sql('game_platforms', engine, if_exists='append', index=False)
  print(f'[Integrate Games] {len(integrated_game_platforms)} game-platform-associations loaded into database')

  connection.close()