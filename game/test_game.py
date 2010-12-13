# -*- coding: utf-8 -*-
from google.appengine.ext import db
from model import Game
from model import Room


def create_room(arg):
	game_info = Game.get(arg['game']['id'])
	room = Room(name=arg['name'], capacity=arg['capacity'], game=game_info,
				difficulty=arg['game']['difficulty'])
	room.put()
	return room