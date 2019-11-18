import os
import pandas as pd
import psycopg2
from engine import engine

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../datasets/metacritic/user_comments.csv"))

df = pd.read_csv(file_path, sep=',', quotechar='"')

# Remove all records with no username or seemingly deleted accounts
df = df[df.username.notnull() & (df.username != 'AnonymousMC') & (df.username != '[Anonymous]')]

print(df.dtypes)

df.to_sql('stage_user_comments', engine, schema='metacritic', if_exists='replace', index=False)