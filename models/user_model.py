from google.appengine.ext import db
import utility
class User(db.Model) :
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	email = db.StringProperty()
	date = db.DateProperty(auto_now_add=True)
	# User Group
	group = db.IntegerProperty(required = True)
	avatar = db.BlobProperty()
	avatar_filename = db.StringProperty()
	status = db.BooleanProperty(default=False)
	verify_hash = db.StringProperty()
	# group 
	# 0 -> reading
	# 1 -> writing
	# 2 -> reading / writing
	# 3 -> Full

	@staticmethod
	# get all emails
	def get_users_by_emails(email):
	    data = User.all().filter('email =', email).ancestor(ancestor_key)
	    return data