from os import path

import requests
import csv
from utilities import engine
import pandas as pd

BASE_URL = "https://api.rawg.io/api/games"

connection = engine.connect()

csv_name='../datasets/giantbomb/images.csv'

if path.exists(csv_name):
    data = pd.read_csv(csv_name, delimiter=';')
    try:
        maxid=max(data['giantbomb_id'])
    except ValueError as err:
        maxid=-2

else:
    maxid=-1

with open(csv_name, 'a', newline='', encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if(maxid)==-1:
        spamwriter.writerow(["giantbomb_id", "image_link"])

    giantbomb_games = pd.read_sql_query(
        '''
        SELECT id,
               game_name
        FROM   giantbomb.stage_games
        WHERE  id IN (SELECT giantbomb_id
                      FROM   lookup.games
                      WHERE  id IN (SELECT DISTINCT( game_id )
                                    FROM   ratings))
                                    and id>'''+str(maxid)+'''
        ORDER BY id ASC
        ''',
        connection
    )
    for index, row in giantbomb_games.iterrows():
        response = requests.get(
            BASE_URL,
            params={'search':row['game_name']}
        )
        id = row['id']
        try:
            image_url = response.json()['results'][0]['background_image']
        except Exception as err:
            print(response.json())
            print(id)
            print(f'Following error occurred: {err}. Skipping current id')
            continue

        spamwriter.writerow([id, image_url])
        if index%50==0:
            print(f'{index} images saved.')




