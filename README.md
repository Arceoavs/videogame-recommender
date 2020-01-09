[![Netlify Status](https://api.netlify.com/api/v1/badges/9b4ce271-4d2e-43d0-b2b4-099d612d2479/deploy-status)](https://app.netlify.com/sites/videogames-muenster/deploys)
# Video Game Recommender

A recommender system for video games! The Video Game Recommender (VGR) project was created as an university project at the Westfälische Wilhelms-Universität Münster, as part of the Data Integartion Module in the Information Systems master programme.

You can access the video game recommender at http://vgr.best! Because we have a vision to create the best video game recommender there is!

## Project Setup

This project uses Docker. If you run the project for the first time, run :

```
$ docker-compose build
```

This will take some time. For the next time, just enter

```
$ docker-compose up
```
to start all services and `docker-compose down` to stop them. You need to run `docker-compose build` only again if you add changes for the container, e.g. install a new python library via pip in the container. The following services are started.

**Postgres Database**

To access the database, use the following credentials:

- Host: localhost
- Port: 5432
- Username: videogamer
- Password: pwned-by-headshot-1337
- Database: videogames

**ETL**

The ETL service runs all the python scripts. You can use the python installation with `docker-compose exec etl <your command>`, for example `docker-compose exec etl bash` to open the bash of the container or `docker-compose exec etl python path/to/file.py` to execute a python script in the container. The working directory is the etl directory. Additional .sh files bundle multiple python commands for easier use.

In order to prepare the database (e.g. create schemas), run:

```
$ docker-compose exec etl sh jobs/setup.sh
```

To load all CSV files into the database, run:

```
$ docker-compose exec etl sh jobs/load_csv_files.sh
```

If you want to run only a python script, just use:

```
$ docker-compose exec etl python transformations/load_metacritic_games.py
```
**Flask Web API**

Flask listens on port 5000. You can access the web application on [localhost:5000](http://localhost:5000) by default.

## Project Deployment
To deploy the backend to the university server, first establish a SSH connection via the connection string `ssh videogames@videogames.uni-muenster.de -p 2222` using the password `#ioHom#qA!ZLmLo`. 
Please note, that connecting via SSH on port 2222 is only possible either from within the university network or a vpn connection to the university.

Next, stop all running containers with `docker-compose stop` from within the `~/videogames` directory and pull the latest code from the master branch via `git pull`. 

By executing the command 
```
sudo docker-compose -f docker-compose.prod.yml up --build -d
```
The new backend will be re-deployed and available on http://videogames.uni-muenster.de on the standard http port 80.

## Datasets

### Metacritic

The dataset for Metacritic is [available online on Kaggle by Kaggle user dahlia25](https://www.kaggle.com/dahlia25/metacritic-video-game-comments). This dataset consists of data for ~3400 games and ~280k user comments from ~130k different users.

### GiantBomb

GiantBomb [offers a REST API](https://www.giantbomb.com/api/) for accessing resources. You need to register for an account to get an API key. We were able to extract ~30k user reviews and ~90k releases of ~70k games.

### IGDB

tbd
