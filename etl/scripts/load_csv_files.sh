#!/bin/sh
python ./staging/load_giantbomb_games.py
python ./staging/load_giantbomb_releases.py
python ./staging/load_giantbomb_user_reviews.py

python ./staging/load_metacritic_games.py
python ./staging/load_metacritic_user_comments.py