from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Game(db.Model): # List games on the server
	module_name = db.StringProperty(required=True)
	title = db.StringProperty(required=True)
	pass

class Room(db.Expando): # List rooms on the server
	name = db.StringProperty(required=True)
	capacity = db.IntegerProperty(required=True)
	game = db.ReferenceProperty(Game, collection_name='rooms') # game:room = 1:*
	#player_status # memcached; auto-volatile (position, health)
	pass

class Player(db.Model): # List players on the server
	account = db.IMProperty(required=True)
	is_ready = db.BooleanProperty(default=False, required=True)
	room = db.ReferenceProperty(Room, collection_name='players') # room:player = 1:*
	#name # Leave for future
	pass