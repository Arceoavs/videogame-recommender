import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd

from game_tokenizer import GameTokenizer
from queries import select_giantbomb_games, select_igdb_games, select_metacritic_games, select_i_g_lookup_games
from utilities import engine, numbers as nb


tokenizer_threshold = 0.5
max_year_diff = 3


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
  candidates = apply_last_number_filter(candidates, 'igdb', 'giantbomb')
  candidates = apply_platform_filter(candidates, 'igdb', 'giantbomb')

  i_best = candidates[['igdb_id', '_sim_score']].sort_values('_sim_score', ascending=False).groupby(candidates.igdb_id, as_index=False).first()
  g_best = candidates[['giantbomb_id', '_sim_score']].sort_values('_sim_score', ascending=False).groupby(candidates.giantbomb_id, as_index=False).first()

  candidates=pd.merge(pd.merge(candidates, i_best, on='igdb_id', suffixes=('_candidates', '_i')), g_best, on='giantbomb_id')
  print(f'Joining results in {len(candidates)} matches')
  candidates=candidates[(candidates._sim_score_candidates == candidates._sim_score_i) & (candidates._sim_score_candidates == candidates._sim_score)]
  print(f'After choosing top matches per id we have {len(candidates)} matches')

  print(candidates.head(20))
  candidates.to_sql('filtered_game_candidates', engine, schema='matching', if_exists='replace', index_label='key')

  n_G_IDs = candidates.groupby('igdb_id', as_index=False).agg({'giantbomb_id': pd.Series.nunique})
  n_I_IDs = candidates.groupby('giantbomb_id', as_index=False).agg({'igdb_id': pd.Series.nunique})

  mult_G_IDs = n_G_IDs[n_G_IDs['giantbomb_id'] > 1]
  mult_I_IDs = n_I_IDs[n_I_IDs['igdb_id'] > 1]

  candidates_1_to_1 = candidates[
    (~candidates.igdb_id.isin(mult_G_IDs.igdb_id)) & (~candidates.giantbomb_id.isin(mult_I_IDs.giantbomb_id))][
    ['igdb_id', 'giantbomb_id']].groupby('igdb_id', as_index=False).agg({'giantbomb_id': min})

  igdb_name_lookup = pd.read_sql_query('''select id, name from igdb.stage_games''', connection)
  giantbomb_name_lookup = pd.read_sql_query('''select id, game_name from giantbomb.stage_games''', connection)

  lookup_games=(candidates_1_to_1.merge(igdb_name_lookup, left_on='igdb_id', right_on='id', how='inner')
                .merge(giantbomb_name_lookup, left_on='giantbomb_id', right_on='id', how='inner')
                [['igdb_id', 'giantbomb_id', 'name', 'game_name']]
                .rename(columns={"name":"igdb_title", "game_name":"giantbomb_title"}))

  lookup_games.to_sql("games", engine, schema="lookup", if_exists="replace", index_label='id')

  metacritic_games = select_metacritic_games.select_metacritic_games(connection) #TODO why does this not work like above without xxx.xxx?


  i_g_lookup_games = select_i_g_lookup_games.select_i_g_lookup_games(connection)

  connection.close()