import pandas as pd
import sqlalchemy
from utilities import engine
from queries import (
  select_igdb_users,
select_giantbomb_users,
select_metacritic_users
)
with engine.connect() as connection:
    i_users = select_igdb_users.select_igdb_users(connection).add_prefix('igdb_')
    g_users = select_giantbomb_users.select_giantbomb_users(connection).add_prefix('giantbomb_')
    m_users = select_metacritic_users.select_metacritic_users(connection).add_prefix('metacritic_')
    #print(i_users)
    #print(g_users)
    #print(m_users)
    combined_users=pd.concat([i_users, g_users, m_users], sort=False)
    #print(combined_users)

    combined_users.to_sql('users', engine, schema='lookup', if_exists='replace', index_label='id', dtype={
    'id': sqlalchemy.types.INT,
    'giantbomb_name': sqlalchemy.types.VARCHAR,
    'igdb_id': sqlalchemy.types.INT,
    'metacritic_name': sqlalchemy.types.VARCHAR,
    })

    # more elegant to edit current combined_users df, but more complicated
    i_users['igdb_id'] =  i_users['igdb_id'].astype(str) + '@igdb.user'
    g_users['giantbomb_name'] = g_users['giantbomb_name'].astype(str) + '@giantbomb.user'
    m_users['metacritic_name'] = m_users['metacritic_name'].astype(str) + '@metacritic.user'

    combined_users = pd.concat([i_users, g_users, m_users], sort=False)
    #print(combined_users)

    users = combined_users['igdb_id'].combine_first(combined_users['giantbomb_name']).combine_first(combined_users['metacritic_name']).to_frame().rename(columns={"igdb_id":"username"})
    users['password'] = 'VGRstandarduser'
    # hashed password for real users? Then this password should be stored in hashed form, too.
    #print(users)

    users.to_sql('users', engine, if_exists='replace', index_label='id')

