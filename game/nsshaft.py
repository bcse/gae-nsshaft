# -*- coding: utf-8 -*-
from google.appengine.ext import db
import simplejson as json
import model

class Room(model.BaseRoom): # Global data in room
	#difficulty = db.StringProperty(choices=['easy', 'normal', 'hard'], default='normal', required=True) # Leave for future
	map_size = db.ListProperty(int, default=[20, 200], required=True)
	map = db.TextProperty(required=True) # Serialized dict of array of array

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'map_size': self.map_size,
            'map': json.loads(self.map)
        })
'''
class Player(model.BasePlayer):
    health = db.IntegerProperty(choices=range(0,10), default=10, required=True)
    position = db.ListProperty(int)

class NSShaft(BaseController):
    self.game = None
    
    def __init__(self):
        #create game
        #create map
        pass
    
    def set_difficulty(self, difficulty):
        pass
        
    def game_start(self):
        pass'''