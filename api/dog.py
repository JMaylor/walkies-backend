from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Dog, User
from flask_restful import Resource

# from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

# from resources.errors import SchemaValidationError, MovieAlreadyExistsError, InternalServerError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError


class DogsApi(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        user = User.objects.get(id=user_id)
        dog = Dog(**body, owner=user)
        dog.save()
        user.update(push__dogs=dog)
        user.save()
        id = dog.id
        return {'id': str(id)}, 200

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        dogs = Dog.objects.filter(owner=user_id).to_json()
        return {'dogs': dogs}, 200


class DogApi(Resource):
    @jwt_required
    def put(self, id):
        user_id = get_jwt_identity()
        dog = Dog.objects.get(id=id, owner=user_id)
        body = request.get_json()
        dog.update(**body)
        return {'dog': dog.to_json()}, 200

    @jwt_required
    def delete(self, id):
        user_id = get_jwt_identity()
        dog = Dog.objects.get(id=id, owner=user_id)
        dog.delete()
        return '', 200

    @jwt_required
    def get(self, id):
        dogs = Dog.objects.get(id=id).to_json()
        return Response(dogs, mimetype="application/json", status=200)
