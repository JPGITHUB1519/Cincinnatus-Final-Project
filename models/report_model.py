from google.appengine.ext import db
from user_model import *
from comment_model import *

class Report(db.Model) :
	user_reporter = db.ReferenceProperty(User)
	comment = db.ReferenceProperty(Comment)
	reason = db.StringProperty(required = True)
	date = db.DateProperty(auto_now_add = True)