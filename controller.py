import simplejson as json

class Controller:
	@staticmethod
	def list_room(arg):
		return {
			'response': 'list_room',
			'msg': 'Not Implemented.'}


	@staticmethod
	def create_room(arg):
		return {
			'response': 'list_room',
			'msg': 'Not Implemented.'}


	@staticmethod
	def list_player(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def join_room(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def leave_room(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def ready_game(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def update_status(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def list_game(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def start_game(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def end_game(arg):
		return {
			'response': 'list_game',
			'msg': 'Not Implemented.'}


	@staticmethod
	def error_msg(msg):
		return {
			'response': 'error',
			'msg': msg}