from google.appengine.ext import db
from handlers.basic_handler import *
from category_model import *

class Blog(db.Model, Handler) :
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	category = db.ReferenceProperty(Category)
	# auto now is for overwriting a existed date if it exits
	last_modified = db.DateProperty(auto_now = True)
