# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class AdminHandler(webapp.RequestHandler):
	def get(self, target, action):
		try:
			method = '%s_%s' % (target, action)
			assert hasattr(self, method)
			f = getattr(self, method)
			assert callable(f)
			f()
		except Exception:
			self.response.out.write(u'Hello, hello, baby; You called, I can’t hear a thing')

	def game_new(self):
		#game = model.Game(module_name='nsshaft', title=u'小朋友下樓梯')
		#game.put()
		#self.response.out.write(u'Game added!')
		pass


def main():
	application = webapp.WSGIApplication([('/admin/(.*)/(.*)', AdminHandler)],
										 debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
