import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd

from game_tokenizer import GameTokenizer
from queries import select_giantbomb_games, select_igdb_games
from utilities import engine


tokenizer_threshold = 0.5
max_year_diff = 3


def apply_year_filter(df, left_suffix, right_suffix):
  new_df = df[
    abs(df[f'{left_suffix}_year']-df[f'{right_suffix}_year'])<=max_year_diff | 
    df[f'{left_suffix}_year'].isnull() |
    df[f'{right_suffix}_year'].isnull()
    ]
  print(f'[Year Filter] Before     {len(df)}')
  print(f'[Year Filter] Filtered   {len(df) - len(new_df)}')
  print(f'[Year Filter] After      {len(new_df)}')
  print(' ')
  return new_df


with engine.connect() as connection:
  igdb_games = select_igdb_games(connection)
  giantbomb_games = select_giantbomb_games(connection)
  
  igdb_games['key'] = range(0, len(igdb_games))
  giantbomb_games['key'] = range(0, len(giantbomb_games))

  print('[Data Profiling]')
  print(ssj.profile_table_for_join(igdb_games))
  print(ssj.profile_table_for_join(giantbomb_games))
  print(' ')

  gt = GameTokenizer()

  candidates = ssj.jaccard_join(
    igdb_games, giantbomb_games, 
    'key', 'key', 
    'title', 'title', 
    gt, tokenizer_threshold, 
    l_out_attrs=['id', 'title', 'year', 'platforms'], r_out_attrs=['id', 'title', 'year', 'platforms'],
    l_out_prefix='igdb_', r_out_prefix='giantbomb_'
  )
  print(f'[Match games] {len(candidates)} potential matching candidates')

  candidates = apply_year_filter(candidates, 'igdb', 'giantbomb')

  i_best = candidates[['igdb_id', '_sim_score']].sort_values('_sim_score', ascending=False).groupby(candidates.igdb_id, as_index=False).first()
  g_best = candidates[['giantbomb_id', '_sim_score']].sort_values('_sim_score', ascending=False).groupby(candidates.giantbomb_id, as_index=False).first()

  candidates=pd.merge(pd.merge(candidates, i_best, on='igdb_id', suffixes=('_candidates', '_i')), g_best, on='giantbomb_id')
  print(f'Joining results in {len(candidates)} matches')
  candidates=candidates[(candidates._sim_score_candidates == candidates._sim_score_i) & (candidates._sim_score_candidates == candidates._sim_score)]
  print(f'After choosing top matches per id we have {len(candidates)} matches')

  print(candidates.head(20))
  candidates.to_sql('filtered_game_candidates', engine, schema='matching', if_exists='replace', index_label='key')

  connection.close()