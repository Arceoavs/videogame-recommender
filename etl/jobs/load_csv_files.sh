#!/bin/sh
python ./transformations/load_giantbomb_games.py
python ./transformations/load_giantbomb_releases.py
python ./transformations/load_giantbomb_user_reviews.py

python ./transformations/load_igdb_alternative_names.py
python ./transformations/load_igdb_companies.py
python ./transformations/load_igdb_franchises.py
python ./transformations/load_igdb_games.py
python ./transformations/load_igdb_genres.py
python ./transformations/load_igdb_keywords.py
python ./transformations/load_igdb_platforms.py
python ./transformations/load_igdb_ratings.py
python ./transformations/load_igdb_reviews.py
python ./transformations/load_igdb_themes.py

python ./transformations/load_metacritic_games.py
python ./transformations/load_metacritic_user_comments.py

python ./transformations/create_giantbomb_games_view.py
python ./transformations/create_igdb_games_view.py
python ./transformations/create_core_games.py
python ./transformations/create_core_users.py
python ./transformations/create_core_reviews.py
