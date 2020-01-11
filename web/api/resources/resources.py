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


AUTH_PARSER = reqparse.RequestParser()
AUTH_PARSER.add_argument(
    'username', help='This field cannot be blank', required=True)
AUTH_PARSER.add_argument(
    'password', help='This field cannot be blank', required=True)


class Index(Resource):
    def get(self):
        return {
            'greeting': 'Hello Videogamer'
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
            access_token = create_access_token(identity=data['username'])
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
            access_token = create_access_token(identity=data['username'])
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
        access_token = create_access_token(identity=current_user)
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


class AllGames(Resource):
    def get(self):
        args = GAME_PARSER.parse_args()
        offset = 0 if args.offset is None else args.offset
        limit = 100 if args.limit is None else args.limit
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

    def initModel():
        print("Initializing Implicit model. This might take a while (approx. 1 minute)...")
        obj_ratings = Rating.query.all()
        game_ids = np.array(list(map(lambda r: r.game_id, obj_ratings)))
        user_ids = np.array(list(map(lambda r: r.user_id, obj_ratings)))
        values = np.asarray(list(map(lambda r: r.value, obj_ratings)))
        game_user_matrix = csr_matrix((values, (game_ids, user_ids)))
        global user_game_matrix
        user_game_matrix = game_user_matrix.T.tocsr()
        global model
        model = implicit.als.AlternatingLeastSquares(factors=50)
        model.fit(game_user_matrix)

    @jwt_required
    def get(self):
        user_email = get_jwt_identity()
        user_id = User.find_by_username(user_email).id

        recommendations = model.recommend(user_id, user_game_matrix, 100)
        print(type(recommendations))
        # return jsonify({'recommendations': recommendations}) #convert numpy int64 to normal python data type first
        return {'message': 'return is to be implemented'}

    @jwt_required
    def post(self):
        try:
            user_email = get_jwt_identity()
            user_id = User.find_by_username(user_email).id
            game_id = request.json['game_id']
            value = request.json['value']
            rating = Rating(
                game_id=game_id,
                user_id=user_id,
                value=value
            )
            rating.save()
            # TODO:
            # Implicit_instance.add(rating)
            # Imlicit_instance.recalculate()
        except:
            return {'message': 'Something went wrong'}, 500
        return {'message': 'Your rating was successfully saved'}, 201
