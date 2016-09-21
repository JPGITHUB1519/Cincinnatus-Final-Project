from google.appengine.ext import db
class User(db.Model) :
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	email = db.StringProperty()
	date = db.DateProperty(auto_now_add=True)
	# User Group
	group = db.IntegerProperty(required = True)
	avatar = db.BlobProperty()
	avatar_filename = db.StringProperty()
	# group 
	# 0 -> reading
	# 1 -> writing
	# 2 -> reading / writing
	# 3 -> Full


