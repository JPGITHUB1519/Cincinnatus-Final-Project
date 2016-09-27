from basic_handler import *
from utility import *
import json

class AdminHandler(Handler):
	def get(self):
		# dictionary getting post data by categories
		dic_posts = numpost_by_categories(self.user)
		list_posts = post_by_user(self.user)
		self.render("admin.html", data_json = json.dumps(dic_posts), dic_posts = dic_posts, list_posts = list_posts)