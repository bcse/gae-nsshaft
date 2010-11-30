# -*- coding: utf-8 -*-
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import simplejson as json
from controller import Controller


class XMPPHandler(webapp.RequestHandler):
	def post(self):
		message = xmpp.Message(self.request.POST)
		result = self.dispatch(message)
		message.reply(result)


	def dispatch(self, message):
		try:
			request = json.loads(message.body)
			assert request.has_key('request')
			assert hasattr(Controller, request['request'])
			assert callable(getattr(Controller, request['request']))
			f = getattr(Controller, request['request'])
			if request.has_key('arg') and \
			   hasattr(request['arg'], '__setitem__'):
				request['arg']['sender'] = message.sender
				result = f(request['arg'])
			else:
				result = f({'sender': message.sender})
		except Exception, e:
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