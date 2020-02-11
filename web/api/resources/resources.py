import datetime

from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from api.models import (
    Game,
    Genre,
    Platform,
    Rating,
    RevokedToken,
    User,
)
import implicit
from scipy.sparse import csr_matrix
import numpy as np
from sqlalchemy.sql import expression

AUTH_PARSER = reqparse.RequestParser()
AUTH_PARSER.add_argument(
    'username', help='This field cannot be blank', required=True)
AUTH_PARSER.add_argument(
    'password', help='This field cannot be blank', required=True)


class Index(Resource):
    def get(self):
        return {
            'greeting': 'Hello videogamer'
        }


class UserRegistration(Resource):
    def post(self):
        data = AUTH_PARSER.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 400

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password'])
        )

        try:
            new_user.save()
            expires = datetime.timedelta(days=31)
            access_token = create_access_token(
                identity=data['username'], expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = AUTH_PARSER.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 404

        if User.verify_hash(data['password'], current_user.password):
            expires = datetime.timedelta(days=31)
            access_token = create_access_token(
                identity=data['username'], expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 400


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        expires = datetime.timedelta(days=31)
        access_token = create_access_token(
            identity=current_user, expires_delta=expires)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


class CurrentUser(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return User.return_by_username(current_user)


GAME_PARSER = reqparse.RequestParser()
GAME_PARSER.add_argument('offset', type=int)
GAME_PARSER.add_argument('limit', type=int)
GAME_PARSER.add_argument('genres')
GAME_PARSER.add_argument('platforms')
GAME_PARSER.add_argument('search')


class AllGames(Resource):
    def get(self):
        args = GAME_PARSER.parse_args()
        offset = 0 if args.offset is None else args.offset
        limit = 100 if args.limit is None else args.limit
        genres = args.genres
        if args.search is not None:
            if args.genres is not None:
                if args.platforms is not None:
                    return Game.return_searchtitle_platform_genre(offset,limit,args.search,args.platforms.split(","), genres.split(","))
                else:
                    return Game.return_searchtitle_genre(offset,limit,args.search, genres.split(","))
            else:
                if args.platforms is not None:
                    return Game.return_searchtitle_platform(offset,limit,args.search,args.platforms.split(","))
                else:
                    return Game.return_searchtitle(offset, limit, args.search)
        if args.platforms is not None:
            if args.genres is not None:
                return Game.return_bygenres_platform(offset, limit, args.platforms.split(","), args.genres.split(","))
            else:
                return Game.return_byplatform(offset,limit,args.platforms.split(","))
        if args.genres is not None:
            return Game.return_bygenres(offset, limit, genres.split(",")) 
        return Game.return_all(offset, limit)


class GameDetail(Resource):
    def get(self, id):
        return Game.return_by_id(id)


class AllGenres(Resource):
    def get(self):
        return Genre.return_all()


class AllPlatforms(Resource):
    def get(self):
        return Platform.return_all()


class GameRating(Resource):

    @jwt_required
    def post(self):
        '''
        API route to provide and update game ratings. This route also enables to exclude games by giving them a negative rating.
        :return: Success message and response code
        '''
        user_email = get_jwt_identity()
        user = User.find_by_username(user_email)
        if not user:
            raise Exception(f'No user with email {user_email} found')
        user_id = user.id
        game_id = request.json['game_id']
        # games can be excluded if they are dismissed in the frontend, which is realized by storing a negative rating
        exclude = request.json['exclude'] if 'exclude' in request.json else False
        value = request.json['value'] if not exclude else -0.5
        if not exclude and (value < 0 or value > 5):
            raise Exception('Rating value should be between 0 and 5')
        value = value * 2
        rating = Rating.query.filter(Rating.game_id==game_id, Rating.user_id==user_id).first()
        # updates rating if one for specific user and specific game already exists
        if rating:
            rating.value = value
            rating.exclude_from_model = exclude
            rating.update()
            return {'message': 'Your rating was successfully updated'}, 200
        else:
            rating = Rating(
                game_id=game_id,
                user_id=user_id,
                value=value,
                exclude_from_model=exclude
            )
            rating.save()
            return {'message': 'Your rating was successfully saved'}, 201


class initializeModel(Resource):
    '''
    Class to call model training via API.
    '''
    def get(self):
        GameRecommendations.initializeImplicit()
        return {'message': 'The recommendation model was successfully (re)created.'}

class GameRecommendations(Resource):

    global is_trained
    is_trained=False

    def initializeImplicit():
        '''
        Initializes an implicit ALS (alternating least squares) model.
        In this model, user ratings are interpreted as confidences that the respective user liked the respecitve item.
        Therefore, a high user ratings leads to a high confidence and a low rating to a low confidence.
        For all unrated games there is no confidence at all.
        Please check the implicit documentation for more details about this model.
        '''

        print('[Implicit] Initializing Implicit model. This might take a while...')
        # retrieve all game ratings that are not to be excluded
        obj_ratings = Rating.query.filter(Rating.exclude_from_model == expression.false())
        games = Game.query.with_entities(Game.id).order_by(Game.id.asc())
        # create dictionaries to map game_ids to positions in matrix
        game_ids = [r.id for r in games]
        keys = list(range(0, Game.query.count()))
        global game_id_dict
        global index_dict
        game_id_dict = dict(zip(keys, game_ids))
        index_dict = dict(zip(game_ids, keys))
        # create utility matrix out of game ratings
        game_indices = np.array(
            [index_dict[r.game_id] for r in obj_ratings]) # operations take some while
        user_ids_minus1 = np.array(
            [r.user_id-1 for r in obj_ratings])
        values = np.asarray([r.value for r in obj_ratings])
        game_user_matrix = csr_matrix((values, (game_indices, user_ids_minus1)), shape=(
            Game.query.count(), user_ids_minus1.size))
        global user_game_matrix
        user_game_matrix = game_user_matrix.T.tocsr()
        global model
        # initialize and train the model
        model = implicit.als.AlternatingLeastSquares(factors=50)
        model.fit(game_user_matrix)
        global is_trained
        is_trained=True
        print('[Implicit] Initializing completed')

    @jwt_required
    def get(self):
        '''
        Gets recommendations from trained model for a specific user.
        Metadata about the games is added to the recommendations to properly display them in the frontend
        :return: ordered list of game recommendations with metadata
        '''
        if is_trained == False:
            return {'message': 'Model is not initialized. Please do so with /initModel'}, 503
        else:
            user_email = get_jwt_identity()
            user_id = User.find_by_username(user_email).id

            # create new user profile to also include ratings and predict for users not in model
            ratings = Rating.query.filter(Rating.user_id == user_id)

            game_ids_minus1 = np.array([index_dict[r.game_id] for r in ratings])
            user_ids_minus1 = np.array([0]*game_ids_minus1.size)
            values = np.asarray([r.value for r in ratings])

            user_profile = csr_matrix((values, (user_ids_minus1, game_ids_minus1)), shape=(
                1, user_game_matrix.shape[1]))
            # get recommendations from trained model
            rec = model.recommend(0, user_profile, 102, recalculate_user=True)
            rec_conv = [[int(rec[0]), float(rec[1])] for rec in rec]

            game_ids = [game_id_dict[r[0]] for r in rec_conv]
            # call function to add required metadata
            return Game.return_recommendations(game_ids)
