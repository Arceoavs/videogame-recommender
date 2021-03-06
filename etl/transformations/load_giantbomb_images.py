import os
import pandas as pd
from utilities import engine

'''
Loads images from giantbomb games from csv file into stage_images table of schema giantbomb.
Images are retrieved from RAWG-API (https://rawg.io/apidocs) based on the game names.
'''

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../datasets/giantbomb/images.csv"))

print(f'Loading file {file_path} into database...')

df = pd.read_csv(file_path, sep=';')

# Remove all records with no username or seemingly deleted accounts
df = df[df.image_link.notnull()]

print(df.dtypes)

df.to_sql('stage_images', engine, schema='giantbomb', if_exists='replace', index=False)