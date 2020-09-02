from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User, Event, Dog
from flask_restful import Resource
from mongoengine import Q


class UserApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.exclude('password').exclude('dogs').exclude('events').get(id=user_id)
        dogs = Dog.objects.exclude('owner').filter(owner=user_id)
        events = Event.objects.filter(Q(proposer=user_id) | Q(invited=user_id))
        eventsDetails = []
        for event in events:
            eventsDetails.append(event.to_json())
        return {'user': user.to_json(), 'dogs': dogs.to_json(), 'events': eventsDetails}, 200


class UserSearchApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        users = User.objects(location__geo_within_center=[user.location['coordinates'], 0.2], id__ne=user_id).exclude(
            'password').exclude('email').exclude('events').exclude('last_name')
        user_id_list = []
        for user in users:
            user_id_list.append(str(user.id))
        dogs = Dog.objects(owner__in=user_id_list)

        return {'users': users.to_json(), 'dogs': dogs.to_json()}, 200
