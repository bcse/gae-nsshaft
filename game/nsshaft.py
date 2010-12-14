# -*- coding: utf-8 -*-
from google.appengine.ext import db
import simplejson as json
from model import Game
from model import Room


def create_room(arg):
	game_info = Game.get(arg['game']['id'])
	map = _create_map(*arg['game']['map_size'])
	room = Room(name=arg['name'], capacity=arg['capacity'], game=game_info,
				map_size=arg['game']['map_size'], map=map)
	room.put()
	return room


def _create_map(width, height):
	map = {'plain': [], 'thorn': [], 'flip': []}
	return json.dumps(map)