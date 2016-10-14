from google.appengine.ext import db

class Category(db.Model):
	name = db.StringProperty()
	date = db.DateProperty(auto_now_add=True)
