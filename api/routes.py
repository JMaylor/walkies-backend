# flask packages
from flask_restful import Api

# project resources
from .dog import DogsApi, DogApi
from .event import EventsApi, EventApi, EventAcceptApi, EventDeclineApi
from .auth import SignupApi, LoginApi, DeleteAccountApi #, LogoutApi
from .user import UserApi, UserSearchApi
# from .reset_password import ForgotPassword, ResetPassword


def create_routes(api: Api):
	api.add_resource(DogsApi, '/api/dogs')
	api.add_resource(DogApi, '/api/dogs/<id>')
	api.add_resource(SignupApi, '/api/auth/signup')
	api.add_resource(DeleteAccountApi, '/api/auth/delete')
	api.add_resource(LoginApi, '/api/auth/login')
	# api.add_resource(ForgotPassword, '/api/auth/forgot')
	# api.add_resource(ResetPassword, '/api/auth/reset')
	api.add_resource(EventsApi, '/api/events')
	api.add_resource(EventApi, '/api/events/<id>')
	api.add_resource(EventAcceptApi, '/api/events/accept/<id>')
	api.add_resource(EventDeclineApi, '/api/events/decline/<id>')
	api.add_resource(UserApi, '/api/user')
	api.add_resource(UserSearchApi, '/api/user/search')
	# api.add_resource(LogoutApi, '/api/auth/logout')