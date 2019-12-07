from utilities import engine

with engine.connect() as connection:
  connection.execute("""
    CREATE OR REPLACE VIEW
          igdb.v_stage_games AS
          (
                  SELECT *
                  FROM
                          (
                                  -- this query groups games by name and first_release_date (assumption that this correctly identifies unique games)
                                  -- the lowest id is kept in the id column, all other ids are added in an extra column alternative_ids
                                  SELECT
                                          MIN(id)                                      AS id                                              ,
                                          MIN(NAME)                                    AS name                                            ,
                                          String_agg(DISTINCT alternative_names, ', ')    alternative_names                               ,
                                          String_agg(DISTINCT platforms, ', ')         AS platforms                                       ,
                                          String_agg(DISTINCT summary, '\n')              summary                                         ,
                                          first_release_date                                                                              ,
                                          substring(string_agg(CAST(id AS VARCHAR) , ', ' ORDER BY id) FROM '[^,]*,(.+)$') alternative_ids,
                                          MIN(NAME)
                                                  || ' '
                                                  || DATE(first_release_date)                                                                        distinct_name,
                                          substring(string_agg(name , '| ' ORDER BY name) FROM '[^|]*\|(.+)$')                                       other_names  ,
                                          trim(both FROM lower(regexp_replace(regexp_replace(name, '[^A-Za-z0-9 ]+', ' ', 'g'), ' +', ' ', 'g'))) AS clean_name   ,
                                          trim(both FROM lower(regexp_replace(regexp_replace(name, '[^A-Za-z0-9 ]+', ' ', 'g'), ' +', ' ', 'g')))
                                                  || ' '
                                                  || TO_CHAR(first_release_date, 'YYYYMMDD') distinct_clean_name
                                  FROM
                                          (
                                                  -- this query selects columns of the games table and replaces the arrays of platform and alternative_name ids with their actual name
                                                  -- the query only keeps entries that have no parent game, have the cateogry main_game
                                                  SELECT
                                                          g.id                                                  ,
                                                          MIN(g.NAME)                       AS name             ,
                                                          string_agg(DISTINCT n.NAME, ', ')    alternative_names,
                                                          string_agg(DISTINCT p.NAME, ', ')    platforms        ,
                                                          MIN(g.summary)                       summary          ,
                                                          MIN(g.first_release_date)            first_release_date
                                                  FROM
                                                          igdb.stage_games g
                                                  LEFT JOIN
                                                          igdb.stage_alternative_names n
                                                  ON
                                                          n.id = ANY(g.alternative_names)
                                                  LEFT JOIN
                                                          igdb.stage_platforms p
                                                  ON
                                                          p.id = ANY(g.platforms)
                                                  WHERE
                                                          g.parent_game IS NULL
                                                  AND     g.category          = 'main_game'
                                                  GROUP BY
                                                          g.id
                                                  ORDER BY
                                                          g.id ASC) t
                                  GROUP BY
                                          lower(regexp_replace(regexp_replace(name, '[^A-Za-z0-9 ]+', ' ', 'g'), ' +', ' ', 'g')),
                                          first_release_date) t2
                  WHERE
                          platforms IS NOT NULL
                  AND     LENGTH(clean_name)  >3
          )
  """)

connection.close()
