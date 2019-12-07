from utilities import engine

with engine.connect() as connection:
  connection.execute("""
    CREATE OR REPLACE VIEW
        giantbomb.v_stage_games AS
        (
                SELECT *
                FROM
                        (
                                -- this query groups games by game_name and first_release_date (assumption that this correctly identifies unique games)
                                -- the lowest id is kept in the id column, all other ids are added in an extra column alternative_ids
                                SELECT
                                        MIN(id) AS id                                                                                    ,
                                        game_NAME                                                                                        ,
                                        String_agg(DISTINCT aliases, ', ')     aliases                                                   ,
                                        String_agg(DISTINCT platform, ', ')    AS platform                                               ,
                                        String_agg(DISTINCT description, '\n')    description                                            ,
                                        first_release_date                                                                               ,
                                        substring(string_agg(CAST(id AS VARCHAR) , ', ' ORDER BY id) FROM E'[^,]*,(.+)$') alternative_ids,
                                        game_name
                                                || ' '
                                                || DATE(first_release_date)                                                                             distinct_game_name,
                                        trim(both FROM lower(regexp_replace(regexp_replace(game_name, '[^A-Za-z0-9 ]+', ' ', 'g'), ' +', ' ', 'g'))) AS clean_game_name   ,
                                        trim(both FROM lower(regexp_replace(regexp_replace(game_name, '[^A-Za-z0-9 ]+', ' ', 'g'), ' +', ' ', 'g')))
                                                || ' '
                                                || TO_CHAR(first_release_date, 'YYYYMMDD') distinct_clean_game_name
                                FROM
                                        (
                                                --this query selects columns of the games table and adds the first_release_date of the release table
                                                SELECT
                                                        g.id         ,
                                                        g.game_name  ,
                                                        g.aliases    ,
                                                        g.description,
                                                        g.platform   ,
                                                        MIN(r.release_date) AS first_release_date
                                                FROM
                                                        giantbomb.stage_games g
                                                LEFT JOIN
                                                        giantbomb.stage_releases r
                                                ON
                                                        g.id = r.game_id
                                                GROUP BY
                                                        g.id)t
                                WHERE
                                        first_release_date IS NOT NULL
                                GROUP BY
                                        game_name, --LOWER(game-name) and matching on clean string not necessary as it doesn't lead to fewer matches
                                        first_release_date) t2
                WHERE
                        platform     IS NOT NULL
                AND     LENGTH(clean_game_name)>3
        )
  """)

connection.close()
