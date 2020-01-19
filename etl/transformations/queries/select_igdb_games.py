import pandas as pd


def select_igdb_games(connection):
    return pd.read_sql_query(
        ''' 
        SELECT
          game.id,
          trim(unnest(array_append(a.alternative_names, game.name))) as title,
          EXTRACT('YEAR' FROM min(first_release_date)) as year,
          STRING_AGG(DISTINCT p.platform_name, ', ') as platforms
        FROM igdb.stage_games game 
        -- alternative names
        LEFT JOIN (
          SELECT game as game_id, array_agg(name) as alternative_names FROM igdb.stage_alternative_names GROUP BY 1
        ) a ON game.id = a.game_id
        -- platforms
        LEFT JOIN (
          SELECT game_id, name as platform_name FROM (
          SELECT id AS game_id, unnest(platforms) AS platform_id FROM igdb.stage_games
          ) op
          LEFT JOIN lookup.platforms lp ON lp.igdb_id = op.platform_id
        ) p on p.game_id = game.id
        GROUP BY 1,2;
        ''',
        connection
    )
