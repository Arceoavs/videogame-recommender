import pandas as pd
import sqlalchemy
from utilities import engine
from queries import (
  select_igdb_ratings,
select_giantbomb_ratings,
select_metacritic_ratings
)
with engine.connect() as connection:
    # queries could also be done with pandas, but SQL should be fine as they are understandable and not too long
    i_ratings = select_igdb_ratings.select_igdb_ratings(connection)
    g_ratings = select_giantbomb_ratings.select_giantbomb_ratings(connection)
    m_ratings = select_metacritic_ratings.select_metacritic_ratings(connection)
    #print(i_ratings)
    #print(g_ratings)
    #print(m_ratings)

    combined_ratings=pd.concat([i_ratings, g_ratings, m_ratings])
    #print(combined_ratings)
    lookup_ratings=combined_ratings[['igdb_user_id', 'igdb_game_id', 'giantbomb_user_name', 'giantbomb_game_id', 'metacritic_user_name', 'metacritic_game_id', 'rating']]
    #print(lookup_ratings)

    lookup_ratings.to_sql('ratings', engine, schema='lookup', if_exists='replace', index_label='id', dtype={
        'id': sqlalchemy.types.INT,
        'igdb_user_id': sqlalchemy.types.INT,
        'igdb_game_id': sqlalchemy.types.INT,
        'giantbomb_user_name': sqlalchemy.types.VARCHAR,
        'giantbomb_game_id': sqlalchemy.types.INT,
        'metacritic_user_name': sqlalchemy.types.VARCHAR,
        'metacritic_game_id': sqlalchemy.types.INT,
        'rating': sqlalchemy.types.INT,
    })

    final_ratings=combined_ratings[['user_id', 'game_id', 'rating']]
    #print(final_ratings)

    #TODO: Create rating schema in Flask
    final_ratings.to_sql('ratings', engine, if_exists='replace', index_label='id', dtype={
        'id': sqlalchemy.types.INT,
        'user_id': sqlalchemy.types.INT,
        'game_id': sqlalchemy.types.INT,
        'rating': sqlalchemy.types.INT,
    })

