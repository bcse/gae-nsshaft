# -*- coding: utf-8 -*-
from google.appengine.api import xmpp
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import simplejson as json
import controller
from model import Player


class XMPPHandler(webapp.RequestHandler):
	def post(self):
		message = xmpp.Message(self.request.POST)
		result = self.dispatch(message)
		message.reply(result)


	def dispatch(self, message):
		try:
			request = json.loads(message.body)
			assert request.has_key('request') # Any request must have this item
			f = getattr(controller, request['request'])
			assert callable(f) # Make sure the attribute is a method but not a property

			# Get Player record from server.
			sender = db.IM('xmpp', message.sender.split('/')[0])
			player = Player.all().filter('account =', sender).fetch(limit=1)
			if len(player) == 0: # Create a new record for new Player.
				player = Player(account=sender)
				player.put()
			else:
				player = player[0]

			# Take action
			arg = request['arg'] if request.has_key('arg') else {}
			assert hasattr(arg, '__setitem__') # arg should be a dict()
			arg['sender'] = player # append sender to arguments
			result = f(arg)
		except:
			import sys, traceback
			tb = traceback.format_exception(*sys.exc_info())
			result = json.dumps({
				'response': 'unknown',
				'stat': 'fail',
				'msg': {
					'raw_request': message.body,
					'traceback': ''.join(tb)}})
		finally:
			return result


application = webapp.WSGIApplication(
	[('/_ah/xmpp/message/chat/', XMPPHandler)],
	debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()