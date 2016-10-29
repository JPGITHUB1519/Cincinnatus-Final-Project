from google.appengine.ext import db
from user_model import *
from blog_model import *

class Comment(db.Model) :
	user = db.ReferenceProperty(User)
	post = db.ReferenceProperty(Blog)
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	last_modified = db.DateProperty()
	status = db.BooleanProperty(default = True)
