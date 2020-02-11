import pandas as pd
import sqlalchemy
from utilities import engine

# unhashed: leet1337
DEFAULT_PASSWORD = '$pbkdf2-sha256$29000$632vFeL8P0fIGUMIAYAQIg$X.IgODMuJGDYE.xpcWLjjnDJmU5BwQ3uyld5Ixgll6Y'

'''
Integrates the users of the data sources. 
Artificial domains are created for the different sources in order to differentiate these users and a standard password is set.
Therefore it is possible to log in into the frontend with the users from the sources and not only self-created users.
'''

with engine.connect() as connection:

    connection.execute('DELETE FROM users CASCADE')

    i_users = pd.read_sql_query('SELECT DISTINCT "user" AS username FROM igdb.stage_ratings', connection)
    i_users['username'] =  i_users['username'].astype(str) + '@igdb.user'
    i_users['password'] =  DEFAULT_PASSWORD
    i_users.to_sql('users', engine, if_exists='append', index=False)

    g_users = pd.read_sql_query('SELECT DISTINCT username FROM giantbomb.stage_user_reviews', connection)
    g_users['username'] =  g_users['username'].astype(str) + '@giantbomb.user'
    g_users['password'] =  DEFAULT_PASSWORD
    g_users.to_sql('users', engine, if_exists='append', index=False)

    m_users = pd.read_sql_query('SELECT DISTINCT username FROM metacritic.stage_user_comments', connection)
    m_users['username'] =  m_users['username'].astype(str) + '@metacritic.user'
    m_users['password'] =  DEFAULT_PASSWORD
    m_users.to_sql('users', engine, if_exists='append', index=False)

    connection.close()
