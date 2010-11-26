# -*- coding: utf-8 -*-
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import simplejson as json

class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        try:
            result = json.loads(message.body)
        except:
            message.reply(json.dumps({'error': 'JSON parse error.'}))
        else:
            message.reply(json.dumps(result))

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()