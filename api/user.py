from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User, Event, Dog
from flask_restful import Resource
from mongoengine import Q


class UserApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.exclude('password').get(id=user_id)
        return {'user': user.to_json()}, 200


class UserSearchApi(Resource):
    @jwt_required
    def get(self):
        # get user id
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        # retrieve the distance sent in the request
        body = request.get_json()
        distance = body['distance']

        # distance is going to be sent in miles - need to convert to radius
        distance_in_radians = distance / 3963.2

        users = User.objects(location__geo_within_sphere=[user.location['coordinates'], distance_in_radians], id__ne=user_id).exclude(
            'password').exclude('email').exclude('events').exclude('last_name')
        users = [user.to_json() for user in users]

        return {'users': users}, 200
