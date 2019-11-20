# Video Game Recommender

University project for a video game recommender system

## Project Setup

This project uses Docker. If you run the project for the first time, run `docker-compose build`. This will take some time. For the next time, just enter `docker-compose up` to start all services and `docker-compose down` to stop them. You need to run `docker-compose build` only again if you add changes for the container, e.g. install a new python library via pip in the container. The following services are started:

**Postgres Database**

To access the database, use the following credentials:

- Host: localhost
- Port: 5432
- Username: videogamer
- Password: pwned-by-headshot-1337
- Database: videogames

**ETL**

The ETL service runs all the python scripts. You can use the python installation with `docker exec etl <your command>`, for example `docker exec etl bash` to open the bash of the container or `docker exec etl python path/to/file.py` to execute a python script in the container. The working directory is the etl directory. Additional .sh files bundle multiple python commands for easier use.

In order to prepare the database (e.g. create schemas), run:

```
$ docker-compose exec etl sh scripts/setup.sh
```

To load all CSV files into the database, run:

```
$ docker-compose exec etl sh scripts/load_csv_files.sh
```

**Flask**

Flask listens on port 5000. You can access the web application on [localhost:5000](http://localhost:5000) by default.

## Datasets

### Metacritic

The dataset for Metacritic is [available online on Kaggle by Kaggle user dahlia25](https://www.kaggle.com/dahlia25/metacritic-video-game-comments). This dataset consists of data for ~3400 games and ~280k user comments from ~130k different users.

### GiantBomb

GiantBomb [offers a REST API](https://www.giantbomb.com/api/) for accessing resources. You need to register for an account to get an API key. We were able to extract ~30k user reviews and ~90k releases of ~70k games.

### IGDB

tbd
