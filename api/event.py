from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User, Event
from flask_restful import Resource
from mongoengine import Q


class EventsApi(Resource):
	@jwt_required
	def post(self):
		user_id = get_jwt_identity()
		body = request.get_json()
		proposer = User.objects.get(id=user_id)
		invited = User.objects.get(id=body['invited'])
		event = Event(**body, proposer=proposer, status="pending")
		event.invited = invited
		event.save()
		proposer.update(push__events=event)
		proposer.save()
		invited.update(push__events=event)
		invited.save()
		id = event.id
		return {'id': str(id)}, 200

	@jwt_required
	def get(self):
		user_id = get_jwt_identity()
		events = Event.objects.filter(
			Q(proposer=user_id) | Q(invited=user_id)).to_json()

		return {'events': events}, 200


class EventApi(Resource):
	@jwt_required
	def get(self, id):
		user_id = get_jwt_identity()
		event = Event.objects.get(Q(id=id) & Q(
			proposer=user_id, invited=user_id))
		return {'event': event}, 200

	@jwt_required
	def put(self, id):
		user_id = get_jwt_identity()
		body = request.get_json()
		Event.objects.get(Q(id=id) & (Q(proposer=user_id) | Q(invited=user_id))).update(location=body['location'], time=body['time'], length=body['length'], status='pending')
		event = Event.objects.get(id=id)
		invited = User.objects.get(id=body['invited'])
		proposer = User.objects.get(id=body['proposer'])
		event.invited = invited
		event.proposer = proposer
		event.save()
		return {'event': event.to_json()}, 200

class EventAcceptApi(Resource):
	@jwt_required
	def put(self, id):
		user_id = get_jwt_identity()
		event = Event.objects.get(id=id, invited=user_id)
		event.status = 'accepted'
		event.save()
		return {'event': event.to_json()}, 200

class EventDeclineApi(Resource):
	@jwt_required
	def delete(self, id):
		user_id = get_jwt_identity()
		event = Event.objects.get(Q(id=id) & (Q(invited=user_id) | Q(proposer=user_id)))
		event.delete()
		return '', 200