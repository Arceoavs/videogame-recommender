import statistics
import numpy as np
import pandas as pd
from queries import (
  select_giantbomb_games_with_integrated_metadata, 
  select_igdb_games_with_integrated_metadata, 
  select_metacritic_games_with_integrated_metadata
)
from utilities import engine

def determine_value(s1, s2, s3):
  if s1 is np.NaN:
    if s2 is np.NaN:
      if s3 is np.NaN:
        return ''
      return s3
    return s2
  return s1

def determine_mean(s1, s2, s3):
  if s1 is np.NaN:
    if s2 is np.NaN:
      if s3 is np.NaN:
        return s3
      return s3
    return statistics.median([s2, s3])
  return statistics.median([s1, s2, s3])

def union_lists(s1, s2, s3):
  union = set()
  if s1 is not np.NaN:
    s1 = s1.split(', ')
    union |= set(s1)
  if s2 is not np.NaN:
    s2 = s2.split(', ')
    union |= set(s2)
  if s3 is not np.NaN:
    s3 = s3.split(', ')
    union |= set(s3)
  return union

with engine.connect() as connection:
  # TODO: REMOVE THIS LIMIT CONSTRAIN
  games = pd.read_sql_query('SELECT * FROM lookup.games LIMIT 5000', connection)

  g_games = select_giantbomb_games_with_integrated_metadata(connection).add_prefix('giantbomb_')
  i_games = select_igdb_games_with_integrated_metadata(connection).add_prefix('igdb_')
  m_games = select_metacritic_games_with_integrated_metadata(connection).add_prefix('metacritic_')

  ###################
  ### JOIN TABLES ###
  ###################

  games = games.merge(
    i_games, on='igdb_id', how='left'
  ).merge(
    g_games, on='giantbomb_id', how='left'
  ).merge(
    m_games, on='metacritic_id', how='left'
  )

  # DEBUG
  # games.to_sql('games_joined', engine, schema='lookup', if_exists='replace')

  ####################
  ### CREATE GAMES ###
  ####################

  integrated_games = pd.DataFrame([], columns = ['id' , 'title', 'description' , 'year'])
  integrated_game_genres = pd.DataFrame([], columns = ['game_id' , 'genre_id'])
  integrated_game_platforms = pd.DataFrame([], columns = ['game_id' , 'platform_id'])

  for index, row in games.iterrows():
    if not (integrated_games['id'] == row['id']).any():
      integrated_games = integrated_games.append({
        'id' : row.id, 
        'title' : determine_value(row.igdb_title, row.giantbomb_title, row.metacritic_title),
        'description': determine_value(row.igdb_description, row.giantbomb_description, np.NaN),
        'year': determine_mean(row.igdb_year, row.giantbomb_year, row.metacritic_year)
        } , ignore_index=True)
      genre_ids = union_lists(row.igdb_genre_ids, row.metacritic_genre_ids, np.NaN)
      for genre_id in genre_ids:
        integrated_game_genres = integrated_game_genres.append({
        'game_id' : row.id, 
        'genre_id' : genre_id,
        } , ignore_index=True)
      platform_ids = union_lists(row.igdb_platform_ids, row.giantbomb_platform_ids, row.metacritic_platform_ids)
      for platform_id in platform_ids:
        integrated_game_platforms = integrated_game_platforms.append({
        'game_id' : row.id, 
        'platform_id' : platform_id,
        } , ignore_index=True)
    else:
      genre_ids = union_lists(row.igdb_genre_ids, row.metacritic_genre_ids, np.NaN)
      for genre_id in genre_ids:
        if not ((integrated_game_genres['game_id'] == row['id']) & (integrated_game_genres['genre_id'] == genre_id)).any():
          integrated_game_genres = integrated_game_genres.append({
          'game_id' : row.id, 
          'genre_id' : genre_id,
          } , ignore_index=True)
      platform_ids = union_lists(row.igdb_platform_ids, row.giantbomb_platform_ids, row.metacritic_platform_ids)
      for platform_id in platform_ids:
        if not ((integrated_game_platforms['game_id'] == row['id']) & (integrated_game_platforms['platform_id'] == platform_id)).any():
          integrated_game_platforms = integrated_game_platforms.append({
          'game_id' : row.id, 
          'platform_id' : platform_id,
          } , ignore_index=True)

  connection.execute('DELETE FROM game_genres')
  connection.execute('DELETE FROM game_platforms')
  connection.execute('DELETE FROM games')
  integrated_games.to_sql('games', engine, if_exists='append', index=False)
  integrated_game_genres.to_sql('game_genres', engine, if_exists='append', index=False)
  integrated_game_platforms.to_sql('game_platforms', engine, if_exists='append', index=False)

  connection.close()