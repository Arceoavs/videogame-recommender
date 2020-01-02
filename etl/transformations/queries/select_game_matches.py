import pandas as pd

def select_game_matches(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
      i.id as igdb_id,
      g.giantbomb_id,
      m.metacritic_id
    FROM
      igdb.stage_games i
    FULL OUTER JOIN (
      SELECT igdb_id, giantbomb_id FROM matching.games_ig GROUP BY 1, 2
    ) g ON i.id = g.igdb_id
    FULL OUTER JOIN (
      SELECT igdb_id, metacritic_id FROM matching.games_im GROUP BY 1, 2
    ) m ON i.id = m.igdb_id;
    ''',
    connection
  )