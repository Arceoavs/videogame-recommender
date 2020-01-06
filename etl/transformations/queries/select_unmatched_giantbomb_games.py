import pandas as pd

def select_unmatched_giantbomb_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT id as giantbomb_id
    FROM giantbomb.stage_games
    LEFT JOIN (
      SELECT
        g.giantbomb_id
      FROM
        igdb.stage_games i
      FULL OUTER JOIN (
        SELECT igdb_id, giantbomb_id FROM matching.games_ig GROUP BY 1, 2
      ) g ON i.id = g.igdb_id
      FULL OUTER JOIN (
        SELECT igdb_id, metacritic_id FROM matching.games_im GROUP BY 1, 2
      ) m ON i.id = m.igdb_id
      GROUP BY 1
    ) igm ON igm.giantbomb_id = id
    WHERE giantbomb_id IS null;
    ''',
    connection
  )