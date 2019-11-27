import os
import pandas as pd
from utilities import engine

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/giantbomb/user_reviews.csv'))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';', quotechar='|')

# Remove all reviews which have no game anymore
df = df[df.release_name.notnull()]

# Extract game id from review_url
# e.g.16179 from https://www.giantbomb.com/skies-of-arcadia-legends/3030-16179/user-reviews/2200-1812/
df['game_id'] = df.review_url.apply(lambda url: int(url.split('/')[4].split('-')[1]))

# Drop guid, review_url, created and updated column
df = df.drop(['guid', 'review_url', 'created', 'updated'], axis=1)

print(df.dtypes)

df.to_sql('stage_user_reviews', engine, schema='giantbomb', if_exists='replace', index=False)