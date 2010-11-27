import simplejson as json

class Controller:
	@staticmethod
	def list_room(arg):
		return {
			'response': 'list_room',
			'msg': arg}


	@staticmethod
	def list_game(arg):
		return {
			'response': 'list_game',
			'msg': arg}


	@staticmethod
	def error_msg(msg):
		return {
			'response': 'error',
			'msg': msg}