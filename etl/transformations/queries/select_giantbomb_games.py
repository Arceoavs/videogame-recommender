import pandas as pd

def select_giantbomb_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT id, title, year, string_agg(distinct platform, ', ') as platforms FROM (
      SELECT g.id, title, year, p.name as platform FROM (
        SELECT
          id,
          title,
          year,
          trim(unnest(string_to_array(platforms, ','))) as platform
        FROM (
          SELECT * FROM (
            SELECT 
              id, 
              trim(unnest(array_append(string_to_array(aliases, ','), g.game_name))) as title, 
              year,
              g.platform as platforms 
            FROM giantbomb.stage_games g
            LEFT JOIN (SELECT game_id, EXTRACT('YEAR' FROM min(release_date)) as year from giantbomb.stage_releases GROUP BY 1) r
            ON g.id = r.game_id
          ) g WHERE title IS NOT null AND title <> '' AND (platforms IS NOT null OR year IS NOT null)
        ) g
      ) g
      LEFT JOIN giantbomb.stage_platforms gbp ON g.platform = gbp.name
      LEFT JOIN lookup.platforms p ON gbp.id = p.giantbomb_id
    ) g
    GROUP BY 1,2,3;
    ''',
    connection
  )