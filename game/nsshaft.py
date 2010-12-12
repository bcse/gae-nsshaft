# -*- coding: utf-8 -*-
from google.appengine.ext import db
import simplejson as json
from model import Game
from model import BaseRoom

class Room(BaseRoom): # Global data in room
	#difficulty = db.StringProperty(choices=['easy', 'normal', 'hard'], default='normal', required=True) # Leave for future
	map_size = db.ListProperty(int, default=[20, 200], required=True)
	map = db.TextProperty(required=True) # Serialized dict of array of array

	def to_json(self):
		return json.dumps({
			'name': self.name,
			'map_size': self.map_size,
			'map': json.loads(self.map)
		})


def create_room(arg):
	game_info = Game.get(arg['game']['id'])
	map = create_map(*arg['game']['map_size'])
	room = Room(name=arg['name'], capacity=arg['capacity'], game=game_info,
				map_size=arg['game']['map_size'], map=map)
	room.put()
	return room


def create_map(width, height):
	map = {'plain': [], 'thorn': [], 'flip': []}
	return json.dumps(map)