from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from bson import json_util

class Dog(db.Document):
	breeds = (
		'Labrador',
		'Border Collie',
		'German Shepherd',
		'Dachshund',
		'Cocker Spaniel',
		'Other',
	)

	name = db.StringField(required=True, max_length=30)
	breed = db.StringField(required=True, choices=breeds)
	owner = db.ReferenceField('User', required=True)
	date_of_birth = db.DateTimeField()

	# def get_details(self):
	# 	return self.to_mongo()

class Event(db.Document):
	location = db.PointField(required=True)
	time = db.DateTimeField(required=True)
	proposer = db.ReferenceField('User', required=True)
	invited = db.ReferenceField('User', required=True)

	statuses = (
		'pending',
		'accepted'
	)
	status = db.StringField(required=True, choices=statuses)

	lengths = (
		'30 mins',
		'1 hour',
		'2 hours or more'
	)
	length = db.StringField(required=True, choices=lengths)

	def to_json(self):
		data = self.to_mongo()
		data["proposer"] = {"_id": self.proposer.id, "first_name": self.proposer.first_name, "last_name": self.proposer.last_name, "location": self.proposer.location, "dogs": [dog.to_mongo() for dog in self.proposer.dogs]}
		data["invited"] = {"_id": self.invited.id, "first_name": self.invited.first_name, "last_name": self.invited.last_name, "location": self.invited.location, "dogs": [dog.to_mongo() for dog in self.invited.dogs]}
		return json_util.dumps(data)

class User(db.Document):
	email = db.EmailField(required=True, unique=True)
	password = db.StringField(required=True, min_length=8)
	first_name = db.StringField(required=True, max_length=30)
	last_name = db.StringField(required=True, max_length=30)
	date_of_birth = db.DateTimeField(required=True)
	location = db.PointField(required=True)
	dogs = db.ListField(db.ReferenceField(Dog, reverse_delete_rule=db.PULL))
	events = db.ListField(db.ReferenceField(Event, reverse_delete_rule=db.PULL))

	def to_json(self):
		data = self.to_mongo()
		data["dogs"] = [dog.to_json() for dog in self.dogs]
		data["events"] = [event.to_json() for event in self.events]
		return json_util.dumps(data)
	
	def hash_password(self):
		self.password = generate_password_hash(self.password).decode('utf8')
	
	def check_password(self, password):
		return check_password_hash(self.password, password)

User.register_delete_rule(Dog, 'owner', db.CASCADE)
User.register_delete_rule(Event, 'proposer', db.CASCADE)
User.register_delete_rule(Event, 'invited', db.CASCADE)