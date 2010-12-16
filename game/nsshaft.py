# -*- coding: utf-8 -*-
from google.appengine.ext import db
import simplejson as json
from model import Game
from model import Room


def _create_map(width, height):
	map = {'plain': [], 'thorn': [], 'flip': []}
	return json.dumps(map)


def create_room(arg):
	assert arg['game'].has_key('map_size'), 'Required argument is missing: "game.map_size".'
	player = arg['sender']
	game_info = Game.get(arg['game']['id'])
	room = Room(name=arg['name'], capacity=arg['capacity'], game=game_info,
				map_size=arg['game']['map_size'])
	room.put()
	player.room = room
	player.is_ready = True
	player.put()

	return {'room': str(player.room.key())}


def init_game(arg):
	player = arg['sender']
	# Generate map if not exists
	if not hasattr(player.room, 'map'):
		player.room.map = db.Text(_create_map(*player.room.map_size))
	# Initialize player status
	player_status = {}
	for p in player.room.players:
		player_status[p.account.address] = {
			'position': [0, 0],
			'health': 10
			}
	player.room.player_status = db.Text(json.dumps(player_status))
	player.room.put()

	return {
		'map': json.loads(player.room.map),
		'map_size': player.room.map_size
		}


def update_status(arg):
	assert arg.has_key('position'), 'Required argument is missing: "position".'
	assert arg.has_key('health'), 'Required argument is missing: "health".'
	player = arg['sender']
	player_status = json.loads(player.room.player_status)
	player_status[player.account.address] = {
		'position': arg['position'],
		'health': arg['health']
		}
	player.room.player_status = json.dumps(player_status)
	player.put()

	return {
		'players': [{
			'id': p.account.address,
			'position': player_status[p.account.address]['position'],
			'health': player_status[p.account.address]['health']
			} for p in player.room.players]
		}