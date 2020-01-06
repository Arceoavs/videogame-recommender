import pandas as pd

def select_metacritic_games_with_integrated_metadata(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
      MIN(g.id) AS id,
      title, 
      MIN(year) AS year,
      string_agg(DISTINCT CAST(p.id AS varchar), ', ') AS platform_ids,
      string_agg(DISTINCT CAST(gn.id AS varchar), ', ') AS genre_ids
    FROM (
      SELECT
        id,
        title,
        year,
        platform,
        unnest(string_to_array(genres, ';')) as genre
      FROM metacritic.stage_games
    ) g
    LEFT JOIN lookup.genres gn ON gn.metacritic_name = g.genre
    LEFT JOIN lookup.platforms p ON p.metacritic_name = g.platform
    GROUP BY 2;
    ''',
    connection
  )