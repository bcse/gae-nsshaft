import simplejson as json
import model


def format_message(type='unknown', stat='fail', msg='Unknown request.'):
	return json.dumps({'response': type, 'stat': stat, 'msg': msg})


class Controller:
	@staticmethod
	def list_room(arg):
		return format_message('list_room', 'ok', 'Not Implemented.')


	@staticmethod
	def create_room(arg):
		return format_message('create_room', 'ok', 'Not Implemented.')


	@staticmethod
	def list_player(arg):
		return format_message('list_player', 'ok', 'Not Implemented.')


	@staticmethod
	def join_room(arg):
		return format_message('join_room', 'ok', 'Not Implemented.')


	@staticmethod
	def leave_room(arg):
		return format_message('leave_room', 'ok', 'Not Implemented.')


	@staticmethod
	def ready_game(arg):
		return format_message('ready_game', 'ok', 'Not Implemented.')


	@staticmethod
	def update_status(arg):
		return format_message('update_status', 'ok', 'Not Implemented.')


	@staticmethod
	def list_game(arg):
		return format_message('list_game', 'ok', {
			'games': [{'id': str(g.key()), 'name': g.title} for g in model.Game.all()]
			})


	@staticmethod
	def start_game(arg):
		return format_message('start_game', 'ok', 'Not Implemented.')


	@staticmethod
	def end_game(arg):
		return format_message('end_game', 'ok', 'Not Implemented.')
