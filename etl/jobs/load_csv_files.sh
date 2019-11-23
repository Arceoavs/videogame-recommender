#!/bin/sh
python ./transformations/load_giantbomb_games.py
python ./transformations/load_giantbomb_releases.py
python ./transformations/load_giantbomb_user_reviews.py

python ./transformations/load_metacritic_games.py
python ./transformations/load_metacritic_user_comments.py