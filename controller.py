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
	assert arg.has_key('name'), 'Required argument is missing: "name".'
	assert arg.has_key('capacity'), 'Required argument is missing: "capacity".'
	assert arg.has_key('game'), 'Required argument is missing: "game".'
	assert arg['game'].has_key('id'), 'Required argument is missing: "game.id".'
	game_info = Game.get(arg['game']['id'])
	assert game_info is not None, 'Specified game is not exists.'

	# Create the room and join current player
	game = _import_game(game_info.module_name)
	msg = game.create_room(arg)

	return _format_message('create_room', 'ok', msg)


def list_player(arg):
	player = arg['sender']
	if 'room' in arg:
		room = Room.get(arg['room'])
 	elif player.room:
		room = player.room
	else:
		raise AssertionError('Required argument is missing: "room".')

	return _format_message('list_player', 'ok', {
		'players': [{
			'id': p.account.address,
			'is_ready': int(p.is_ready)
			} for p in room.players]
		})


def join_room(arg):
	assert arg.has_key('room'), 'Required argument is missing: "room".'
	room = Room.get(arg['room'])
	assert room is not None, 'Specified room is not exists.'
	assert room.capacity - room.players.count() > 0, 'Sorry, specified room is fulled. %s' % (room.capacity - room.players.count())
	player = arg['sender']
	player.room = room
	player.put()
	
	return _format_message('join_room', 'ok', {'room': str(player.room.key())})


def leave_room(arg):
	player = arg['sender']
	room_id = str(player.room.key())
	player.is_ready = False
	player.room = None
	player.put()

	return _format_message('leave_room', 'ok', {
		'player': player.account.address,
		'room': room_id
		})


def ready_game(arg):
	assert arg.has_key('is_ready'), 'Required argument is missing: "is_ready".'
	player = arg['sender']
	assert player.room is not None, 'You are not in any room yet.'
	player.is_ready = bool(arg['is_ready'])
	player.put()

	if arg.get('broadcast', 0):
		pass

	return _format_message('ready_game', 'ok', {
		'player': player.account.address,
		'is_ready': int(arg['is_ready'])
		})


def update_status(arg):
	player = arg['sender']
	assert player.room is not None, 'You are not in any room yet.'
	assert player.room.players.filter('is_ready =', False).count() == 0, 'Please do not cheating.'
	assert hasattr(player.room, 'player_status'), 'Are you cheating?'

	game = _import_game(player.room.game.module_name)
	msg = game.update_status(arg)

	return _format_message('update_status', 'ok', msg)


def list_game(arg):
	return _format_message('list_game', 'ok', {
		'games': [{'id': str(g.key()), 'name': g.title} for g in Game.all()]
		})


def init_game(arg):
	player = arg['sender']
	assert player.room is not None, 'You are not in any room yet.'
	unready_players = player.room.players.filter('is_ready =', False).count()
	assert unready_players == 0, 'You can not start game now. There are %s players not ready yet.' % unready_players

	# Initialize game data (map, player_status)
	game = _import_game(player.room.game.module_name)
	msg = game.init_game(arg)

	return _format_message('init_game', 'ok', msg)


def end_game(arg):
	return _format_message('end_game', 'ok', 'Not Implemented.')
