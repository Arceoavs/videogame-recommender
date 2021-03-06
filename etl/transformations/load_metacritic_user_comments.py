import os
import pandas as pd
from utilities import engine

'''
Loads metacritic user comments from csv file into stage_user_comments table of schema metacritic.
'''

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../datasets/metacritic/user_comments.csv"))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=',', quotechar='"')

# Remove all records with no username or seemingly deleted accounts
df = df[df.username.notnull() & (df.username != 'AnonymousMC') & (df.username != '[Anonymous]')]

print(df.dtypes)

df.to_sql('stage_user_comments', engine, schema='metacritic', if_exists='replace', index=False)