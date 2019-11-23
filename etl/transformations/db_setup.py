from engine import engine

with engine.connect() as connection:
  connection.execute("""CREATE SCHEMA IF NOT EXISTS igdb""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS giantbomb""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS metacritic""")

connection.close()
