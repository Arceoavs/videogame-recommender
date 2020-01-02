from utilities import engine
import pandas.io.sql as sqlio
import py_stringsimjoin as ssj
import py_stringmatching as sm


sql_gb_games = "select * from giantbomb.v_stage_games"
gb_games = sqlio.read_sql(sql_gb_games, engine)
sql_igdb_games = "select * from igdb.v_stage_games;"
igdb_games=sqlio.read_sql(sql_igdb_games, engine)
gram4=sm.QgramTokenizer(qval=4, return_set=True)
#TODO: Transformations in Pandas in order to avoid storing joined table in sql but instead directly store table games

igdb_giantbomb_distinct_jaccard_4gram_7 = ssj.jaccard_join(gb_games, igdb_games, 'id', 'id', 'distinct_clean_game_name', 'distinct_clean_name', gram4, 0.7, n_jobs=-1)
igdb_giantbomb_distinct_jaccard_4gram_7.to_sql('igdb_giantbomb_games_mapping', engine, schema='core', if_exists='replace', index=False)

with engine.connect() as connection:
  connection.execute("""
    DROP TABLE 
        IF EXISTS core.games CASCADE 
    """)
  connection.execute("""
    CREATE TABLE
        core.games AS
        (
                SELECT
                        j._id AS id,
                        i.name     ,
                        i.platforms
                                || ', '
                                || g.platform platforms                                                                             ,
                        CASE WHEN i.first_release_date<=g.first_release_date THEN i.first_release_date ELSE g.first_release_date END,
                        i.id        igdb_id                                                                                                ,
                        g.id        giantbomb_id                                                                                           ,
                        g.game_name giantbombName
                FROM
                        igdb.v_stage_games i
                INNER JOIN
                        joined.igdb_giantbomb_distinct_clean_jaccard_4gram_7 j
                ON
                        i.id=j.r_id
                INNER JOIN
                        giantbomb.v_stage_games g
                ON
                        g.id=j.l_id
                ORDER BY
                        j._id
        )  
  """)