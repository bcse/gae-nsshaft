import simplejson as json
from model import Room
from model import Game
from model import Player


def _format_message(type='unknown', stat='fail', msg='Unknown request.'):
	return json.dumps({'response': type, 'stat': stat, 'msg': msg})


def _import_game(module_name):
	return __import__('game.%s' % str(module_name), fromlist=['game'])


def list_room(arg):
	return _format_message('list_room', 'ok', {
		'rooms': [{
			'id': str(r.key()),
			'name': r.name,
			'game': r.game.title,
			'remain_capacity': r.capacity - r.players.count()
			} for r in Room.all() if r.players.count() > 0]
		})


def create_room(arg):
	player = arg['sender']
	game_info = Game.get(arg['game']['id'])
	assert isinstance(game_info, Game), 'Specified game is not exists.'

	# Create the room and join current player
	game = _import_game(game_info.module_name)
	room = game.create_room(arg)
	player.room = room
	player.put()

	return _format_message('create_room', 'ok', {
		'room': str(room.key())
		})


def list_player(arg):
	player = arg['sender']
	if 'room' in arg:
		room = Room.get(arg['room'])
 	elif player.room:
		room = player.room
	else:
		return _format_message('list_player', 'fail', 'Required field "room" is missing.')

	return _format_message('list_player', 'ok', {
		'players': [{
			'id': p.account.address,
			'is_ready': int(p.is_ready)
			} for p in room.players]
		})


def join_room(arg):
	return _format_message('join_room', 'ok', 'Not Implemented.')


def leave_room(arg):
	return _format_message('leave_room', 'ok', 'Not Implemented.')


def ready_game(arg):
	return _format_message('ready_game', 'ok', 'Not Implemented.')


def update_status(arg):
	return _format_message('update_status', 'ok', 'Not Implemented.')


def list_game(arg):
	return _format_message('list_game', 'ok', {
		'games': [{'id': str(g.key()), 'name': g.title} for g in Game.all()]
		})


def start_game(arg):
	return _format_message('start_game', 'ok', 'Not Implemented.')


def end_game(arg):
	return _format_message('end_game', 'ok', 'Not Implemented.')
