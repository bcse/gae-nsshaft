from google.appengine.ext import db
import simplejson as json
from model import Game
from model import Player


def format_message(type='unknown', stat='fail', msg='Unknown request.'):
	return json.dumps({'response': type, 'stat': stat, 'msg': msg})


def import_game(module_name):
	return __import__('game.%s' % str(module_name), fromlist=['game'])


def list_room(arg):
	rooms = db.GqlQuery('SELECT * FROM BaseRoom') # Workaround for Issue 2053
	return format_message('list_room', 'ok', {
		'rooms': [{
			'id': str(r.key()),
			'name': r.name,
			'game': r.game.title,
			'remain_capacity': r.capacity - r.players.count()
			} for r in rooms if r.players.count() > 0]
		})


def create_room(arg):
	game_info = Game.get(arg['game']['id'])
	player = arg['sender']
	assert isinstance(game_info, Game)
	assert isinstance(player, Player)

	# Create the room and join current player
	game = import_game(game_info.module_name)
	room = game.create_room(arg)
	player.room = room
	player.put()

	return format_message('create_room', 'ok', {
		'room': str(room.key())
		})


def list_player(arg):
	return format_message('list_player', 'ok', 'Not Implemented.')


def join_room(arg):
	return format_message('join_room', 'ok', 'Not Implemented.')


def leave_room(arg):
	return format_message('leave_room', 'ok', 'Not Implemented.')


def ready_game(arg):
	return format_message('ready_game', 'ok', 'Not Implemented.')


def update_status(arg):
	return format_message('update_status', 'ok', 'Not Implemented.')


def list_game(arg):
	return format_message('list_game', 'ok', {
		'games': [{'id': str(g.key()), 'name': g.title} for g in Game.all()]
		})


def start_game(arg):
	return format_message('start_game', 'ok', 'Not Implemented.')


def end_game(arg):
	return format_message('end_game', 'ok', 'Not Implemented.')
