from google.appengine.ext import db
from handlers.basic_handler import *
from category_model import *
from user_model import *

class Blog(db.Model) :
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	category = db.ReferenceProperty(Category)
	user = db.ReferenceProperty(User)
	# auto now is for overwriting a existed date if it exits
	last_modified = db.DateProperty(auto_now = True)
	status = db.BooleanProperty()
	likes = db.IntegerProperty(default = 0)
	users_liked = db.ListProperty(db.Key, default = [])
	dislikes = db.IntegerProperty(default = 0)
	users_disliked = db.ListProperty(db.Key, default = [])