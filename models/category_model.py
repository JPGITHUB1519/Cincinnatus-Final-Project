from google.appengine.ext import db

class Category(db.Model):
	name = db.StringProperty()
	description = db.StringProperty()