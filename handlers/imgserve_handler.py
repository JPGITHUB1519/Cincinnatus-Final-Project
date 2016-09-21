from basic_handler import *
from google.appengine.ext import db
import mimetypes
from general import *
from utility import * 
class ImgServe(Handler):
	# i load the image from the user's data
	def get(self, user_id):
		# load image from database
		# user_key = db.Key.from_path('User', user_id)
		user = User.get_by_id(int(user_id))
		self.response.headers[b'Content-Type'] = mimetypes.guess_type(user.avatar_filename)[0]
		self.response.write(user.avatar)   