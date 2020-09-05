from flask import Response, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.models import User
from flask_restful import Resource
import datetime

from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

from api.errors import SchemaValidationError, EmailAlreadyExistsError, InternalServerError, UnauthorizedError 

class SignupApi(Resource):
	def post(self):
		try:
			body = request.get_json()
			user = User(**body)
			user.hash_password()
			user.save()
			id = user.id
			return {'id': str(id)}, 200
		except FieldDoesNotExist:
			raise SchemaValidationError
		except NotUniqueError:
			raise EmailAlreadyExistsError
		except Exception as e:
			raise InternalServerError

class DeleteAccountApi(Resource):
	@jwt_required
	def delete(self):
		user_id = get_jwt_identity()
		user = User.objects.get(id=user_id)
		user.delete()
		return '', 200

class LoginApi(Resource):
	def post(self):
		try:
			body = request.get_json()
			user = User.objects.get(email=body.get('email'))
			authorized = user.check_password(body.get('password'))
			if not authorized:
				raise UnauthorizedError
			expires = datetime.timedelta(days=7)
			access_token = create_access_token(identity=str(user.id), expires_delta=expires)
			return {'token': access_token}, 200
		except DoesNotExist:
			raise UnauthorizedError
		except UnauthorizedError:
			raise UnauthorizedError
		except Exception as e:
			raise InternalServerError