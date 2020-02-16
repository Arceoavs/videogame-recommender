[![Netlify Status](https://api.netlify.com/api/v1/badges/9b4ce271-4d2e-43d0-b2b4-099d612d2479/deploy-status)](https://app.netlify.com/sites/videogames-muenster/deploys)
# Video Game Recommender

A recommender system for video games! The Video Game Recommender (VGR) project was created as an university project at the Westfälische Wilhelms-Universität Münster, as part of the Data Integartion Module in the Information Systems master programme.

You can access the video game recommender at http://vgr.best! Because we have a vision to create the best video game recommender there is!

## Project Structure
The VGR project is built as a web-application structured in independent services. The backend (see /web) is written in python, using the flask framework to provide an API which is consumed by the frontend. The frontend (see /client) is a Vue.js application written in Javascript and using the Pug/Jade templating engine. Furthermore the etl process also is written in python, using different libraries e.g. from the biggorilla library. Last but not least the postrgres database serves as the persistent data storage, accessed by the backend and the etl processes. 

All the independent services are containerized using docker. This makes development as well as deployment easier. For this purpose we defined Dockerfiles for production and for development. The differences between these are minimal and basically allow us to enable hot-reload web servers for development purposes, which are not needed in production. Docker-compose allows for easy orchestration of these services. 

Additionally, we introduced a NGINX reverse-proxy to encrypt the API requests for the user. This is only used in the production environment. You can find  about the reverse proxy in the chapter about deployment. 

## Development

This project uses Docker. In the following, the development method using the pre-defines Dockerfiles (dev.Dockerfilen in each directory) is described. The project of course also can be developed using e.g. the Vue-CLI and python virtualenv, but this makes setup more difficult. 

For orchestration the docker-compose.yml in the root directory can be used. 

### Setup
First, copy the `sample.env` file as a separate `.env` file in your local directory. Do not commit this file into version control! You can make changes to your local .env file as you please. 

If you run the project for the first time, run:

```
$ docker-compose build
```
To buld the image and install dependencies. This will take some time. For the next time, just enter

```
$ docker-compose up
```
to start all services and `docker-compose down` to stop them. You need to run `docker-compose build` only again if you add changes for the container, e.g. install a new python library via pip in the container. The following services are started. 

**Postgres Database**
To access the database, use the following default credentials defined in the `sample.env`:

- Host: localhost
- Port: 5432
- Username: videogamer
- Password: pwned-by-headshot-1337
- Database: videogames

You can define different access credentials in your local `.env` file. 

**ETL**

The ETL service runs all the python scripts. You can use the python installation with `docker-compose exec etl <your command>`, for example `docker-compose exec etl bash` to open the bash of the container or `docker-compose exec etl python path/to/file.py` to execute a python script in the container. The working directory is the etl directory. Additional .sh files bundle multiple python commands for easier use.

These commands are run automatically by the docker-compose.yml when you run `docker-compose up`, so no furher action is required necessarily. 

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
Flask listens on port 5000. You can access the web application on [localhost:5000](http://localhost:5000) by default. If you change this port, please also define the new port the frontend should access the API at. 

## Project Deployment
The fontend currently is deployed using the netlify service, accessable at https://www.vgr.best (see https://www.netlify.com/) for easy deployment of the Vue.js application. Additionally, the frontend is deployed separately on the university server, accessable under https://videogames.uni-muenster.de. 

The backend is deployed on the university server, accessable under https://videogames.uni-muenster.de/api. The frontend deployment on netlify as well as on the university server accesses this API. 

### HTTPS encryption
All traffic to the frontend is encrypted via HTTPS. For the deployment on netlify we use a LetsEncrypt certificate, the university server is certified by a certificate issued by the ZIV. The cert files are included in this project. 

For encrypting the API requests, we use a NGINX reverse proxy that establishes an encrypted connection to the end user via HTTPS, using said ZIV certificate. The request then is forewarded locally to the backend at the port specified in the docker-compose file. 

### ETL process
The ETL process in the production environment has to be started once the underlying data sources change. This is achieved by starting the ETL container as a one-off instance which executes its startup script and then is stopped to free up resources for the other containers. 

## New deployment
The project can be re-deployed using the provided docker-compose.prod.yml file. This automates orchestration and deployment. 

### Accessing the university server
To deploy the backend to the university server, first establish a SSH connection via the connection string `ssh videogames@videogames.uni-muenster.de -p 2222` using the password `#ioHom#qA!ZLmLo`. 
Please note, that connecting via SSH on port 2222 is only possible either from within the university network or a vpn connection to the university.

### Starting containers 
First, stop all running containers with `docker-compose stop` from within the `~/videogames` directory and pull the latest code from the master branch via `git pull`. It is not recommended to deploy from another branch than the master branch for production. 

By executing the command 
```
sudo docker-compose -f docker-compose.prod.yml up --build -d
```
You can start the pre-defined production orchestration. The --build flag will re-build the image every time. This might take quite some minutes, since all the ETL procersses will be executed automatically. 

The new backend will be re-deployed and available on http://videogames.uni-muenster.de on the standard http port 80.

### Initializing the recommender system
After every new deployment, the recommender system should be initialized once manually. This can be done by simly accessing the route `/initModel` via the browser or a REST client. The request might take some minutes, but not to worry, the timeout for the http servers is set high enough. 

## Error handling
Yout might want to execute sudo docker-compose `sudo docker-compose exec web python manage.py db init` and `sudo docker-compose exec web python manage.py db migrate` when running into database errors. 

If you have any problems, feel free to contact us at help@vgr.best

