import py_stringsimjoin as ssj
import py_stringmatching as sm
import numpy as np
import pandas as pd
import sqlalchemy

from game_tokenizer import GameTokenizer, clean_string
from queries import select_giantbomb_games, select_igdb_games, select_metacritic_games, select_game_matches, select_unmatched_giantbomb_games, select_unmatched_metacritic_games
from utilities import engine, numbers as nb


tokenizer_threshold = 0.5
max_year_diff = 3


lev = sm.Levenshtein()


def apply_year_filter(df, left_prefix, right_prefix):
  new_df = df[
    abs(df[f'{left_prefix}_year']-df[f'{right_prefix}_year'])<=max_year_diff | 
    df[f'{left_prefix}_year'].isnull() |
    df[f'{right_prefix}_year'].isnull()
    ]
  print(f'[Year Filter] Before     {len(df)}')
  print(f'[Year Filter] Filtered   {len(df) - len(new_df)}')
  print(f'[Year Filter] After      {len(new_df)}')
  print(' ')
  return new_df


def apply_last_number_filter(df, left_prefix, right_prefix):
  print(f'[Last Number Filter] Before     {len(df)}')
  df = df[df.apply(lambda x: not(nb.is_number(x[f'{left_prefix}_title'].split(' ')[-1])
                                 and nb.is_number(x[f'{right_prefix}_title'].split(' ')[-1])
                                 and not nb.equal_numbers(x[f'{left_prefix}_title'].split(' ')[-1], x[f'{right_prefix}_title'].split(' ')[-1])),
                   axis=1)]
  print(f'[Last Number Filter] After      {len(df)}')
  print(' ')
  return df


def apply_platform_filter(df, left_prefix, right_prefix):
  print(f'[Platform Filter] Before     {len(df)}')
  new_df = df[df.apply(lambda x: not (
    set(x[f'{left_prefix}_platforms'].split(', ')).isdisjoint(set(x[f'{right_prefix}_platforms'].split(', ')))),
                       axis=1)]

  print(f'[Platform Filter] After      {len(new_df)}')
  print(' ')
  return (new_df)


def find_best_matches(candidates, left, right):
  new_candidates = candidates
  grouped = candidates.groupby(f'{right}_id').filter(lambda x: len(x) > 1).groupby(f'{right}_id')
  for name, group in grouped:
    highest_sim = 0.0
    sim_item = None
    for index, row in group.iterrows():
      current_item = row[f'{right}_id']
      sim = lev.get_sim_score(clean_string(row[f'{left}_title']), clean_string(row[f'{right}_title']))
      if sim > highest_sim:
        highest_sim = sim
        if sim_item is not None:
          new_candidates = new_candidates[(new_candidates[f'{right}_id'] != current_item) & (new_candidates[f'{left}_id'] != sim_item)]
        sim_item = row[f'{left}_id']
  return new_candidates


def process_candidates(candidates, left, right):
  print(f'[Match {left}-{right} games] {len(candidates)} potential matching candidates')

  candidates = apply_year_filter(candidates, left, right)
  candidates = apply_last_number_filter(candidates, left, right)
  candidates = apply_platform_filter(candidates, left, right)

  left_best = candidates[[f'{left}_id', '_sim_score']].sort_values('_sim_score', ascending=False).groupby(candidates[f'{left}_id'], as_index=False).first()
  right_best = candidates[[f'{right}_id', '_sim_score']].sort_values('_sim_score', ascending=False).groupby(candidates[f'{right}_id'], as_index=False).first()
  
  candidates=pd.merge(pd.merge(candidates, left_best, on=f'{left}_id', suffixes=(f'_candidates', f'_{left}')), right_best, on=f'{right}_id')
  print(f'[Match {left}-{right} games] {len(candidates)} matches after joining results')
  candidates=candidates[(candidates._sim_score_candidates == candidates[f'_sim_score_{left}']) & (candidates._sim_score_candidates == candidates._sim_score)]
  print(f'[Match {left}-{right} games] {len(candidates)} matches after choosing most similar matches')
 
  candidates = find_best_matches(candidates, left, right)
  print(f'[Match {left}-{right} games] {len(candidates)} matches after finding the best matches from the most similar matches')
 
  candidates.to_sql(f'{left}_{right}_game_candidates', engine, schema='matching', if_exists='replace', index_label='key')
  
  print(f'[Match {left}-{right} games] {len(candidates)} final matches')
  return candidates


with engine.connect() as connection:
  igdb_games = select_igdb_games(connection)
  igdb_games['key'] = range(0, len(igdb_games))
  
  giantbomb_games = select_giantbomb_games(connection)
  giantbomb_games['key'] = range(0, len(giantbomb_games))

  metacritic_games = select_metacritic_games(connection)
  metacritic_games['key'] = range(0, len(metacritic_games))

  print('[Data Profiling]')
  print(ssj.profile_table_for_join(igdb_games))
  print(ssj.profile_table_for_join(giantbomb_games))
  print(ssj.profile_table_for_join(metacritic_games))
  print(' ')

  gt = GameTokenizer()

  #############################
  ### CREATE MATCHING TABLE ###
  #############################

  ig_candidates = ssj.jaccard_join(
    igdb_games, giantbomb_games, 
    'key', 'key', 
    'title', 'title', 
    gt, tokenizer_threshold, 
    l_out_attrs=['id', 'title', 'year', 'platforms'], r_out_attrs=['id', 'title', 'year', 'platforms'],
    l_out_prefix='igdb_', r_out_prefix='giantbomb_'
  )
  ig_candidates = process_candidates(ig_candidates, 'igdb', 'giantbomb')
  ig_candidates.to_sql('games_ig', engine, schema='matching', if_exists='replace', index_label='key')


  im_candidates = ssj.jaccard_join(
    igdb_games, metacritic_games, 
    'key', 'key', 
    'title', 'title', 
    gt, tokenizer_threshold, 
    l_out_attrs=['id', 'title', 'year', 'platforms'], r_out_attrs=['id', 'title', 'year', 'platforms'],
    l_out_prefix='igdb_', r_out_prefix='metacritic_'
  )
  im_candidates = process_candidates(im_candidates, 'igdb', 'metacritic')
  im_candidates.to_sql('games_im', engine, schema='matching', if_exists='replace', index_label='key')


  gm_candidates = ssj.jaccard_join(
    giantbomb_games, metacritic_games, 
    'key', 'key', 
    'title', 'title', 
    gt, tokenizer_threshold, 
    l_out_attrs=['id', 'title', 'year', 'platforms'], r_out_attrs=['id', 'title', 'year', 'platforms'],
    l_out_prefix='giantbomb_', r_out_prefix='metacritic_'
  )
  gm_candidates = process_candidates(gm_candidates, 'giantbomb', 'metacritic')
  gm_candidates.to_sql('games_gm', engine, schema='matching', if_exists='replace', index_label='key')

  ###########################
  ### CREATE LOOKUP TABLE ###
  ###########################

  matches = select_game_matches(connection)
  unmatched_giantbomb = select_unmatched_giantbomb_games(connection)
  unmatched_giantbomb['igdb_id'] = np.NaN
  unmatched_giantbomb['metacritic_id'] = np.NaN
  unmatched_metacritic = select_unmatched_metacritic_games(connection)
  unmatched_metacritic['igdb_id'] = np.NaN
  unmatched_metacritic['giantbomb_id'] = np.NaN
  
  matches = matches.append(unmatched_giantbomb, ignore_index=True).append(unmatched_metacritic, ignore_index=True)
  matches['id'] = np.NaN # default value


  generated_id = 1

  # Addign ids for all common IGDB games
  grouped = matches.groupby('igdb_id').filter(lambda x: len(x) > 1).groupby('igdb_id')
  for name, group in grouped:
    for index, row in group.iterrows():
      matches.loc[index, 'id'] = generated_id
    generated_id += 1

  # Assign ids for all common GiantBomb games
  grouped = matches[matches['id'].isnull()].groupby('giantbomb_id').filter(lambda x: len(x) > 1).groupby('giantbomb_id')
  for name, group in grouped:
    for index, row in group.iterrows():
      matches.loc[index, 'id'] = generated_id
    generated_id += 1

  # Assign ids for all common Metacritic games
  grouped = matches[matches['id'].isnull()].groupby('metacritic_id').filter(lambda x: len(x) > 1).groupby('metacritic_id')
  for name, group in grouped:
    for index, row in group.iterrows():
      matches.loc[index, 'id'] = generated_id
    generated_id += 1

  # Assign unique ids for all remaining games
  for index, row in matches[matches['id'].isnull()].iterrows():
     matches.loc[index, 'id'] = generated_id
     generated_id += 1

  matches.to_sql('games', engine, schema='lookup', if_exists='replace', index=False, dtype={
    'id': sqlalchemy.types.INT,
    'igdb_id': sqlalchemy.types.INT,
    'giantbomb_id': sqlalchemy.types.INT,
    'metacritic_id': sqlalchemy.types.INT,
  })

  connection.close()