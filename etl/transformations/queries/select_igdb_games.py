import pandas as pd

def select_igdb_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT 
      g.id,
      title,
      year,
      string_agg(p.name, ', ') as platforms
    FROM (
      SELECT *, unnest(platforms) as platform
      FROM (
        SELECT 
          g.id,
          trim(unnest(array_append(a.alternative_names, g.name))) as title,
          EXTRACT('YEAR' FROM g.first_release_date) as year,
          g.platforms
        FROM igdb.stage_games g
        LEFT JOIN (
          SELECT game as game_id, array_agg(name) as alternative_names FROM igdb.stage_alternative_names GROUP BY 1
        ) a ON g.id = a.game_id
      ) g
    ) g
    LEFT JOIN lookup.platforms p on g.platform = p.igdb_id
    GROUP BY 1,2,3;
    ''',
    connection
  )