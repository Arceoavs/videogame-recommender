"""This module initializes the whole application for use as an API server"""
import os

from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy_utils import create_database, database_exists

from api.config import config
from api.core import all_exception_handler
from api.resources import resources
from api.models import db

# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app(test_config=None):
    """The flask application factory."""
    app = Flask(__name__)
    api = Api(app)
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedToken.is_jti_blacklisted(jti)

    CORS(app)  # add CORS

    # register RESTful resources
    api.add_resource(resources.UserRegistration, '/registration')
    api.add_resource(resources.UserLogin, '/login')
    api.add_resource(resources.UserLogoutAccess, '/logout/access')
    api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/token/refresh')
    api.add_resource(resources.CurrentUser, '/user')
    api.add_resource(resources.Index, '/')

    api.add_resource(resources.GameDetail, '/games/<id>')
    api.add_resource(resources.AllGames, '/games')
    api.add_resource(resources.GameRecommendations, '/recommendations')
    api.add_resource(resources.GameRating, '/rate')
    api.add_resource(resources.AllGenres, '/genres')
    api.add_resource(resources.AllPlatforms, '/platforms')
    api.add_resource(resources.initializeModel, '/initModel')


    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    # for configuration options, look at api/config.py
    if test_config:
        # purposely done so we can inject test configurations
        # this may be used as well if you'd like to pass
        # in a separate configuration although I would recommend
        # adding/changing it in api/config.py instead
        # ignore environment variable config if config was given
        app.config.from_mapping(**test_config)
    else:
        # config dict is from api/config.py
        app.config.from_object(config[env])

    # decide whether to create database
    if env != "prod":
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_url):
            create_database(db_url)

    # register sqlalchemy to this app
    db.init_app(app)  # initialize Flask SQLALchemy with this flask app
    Migrate(app, db)

    # register error Handler
    app.register_error_handler(Exception, all_exception_handler)
    return app
