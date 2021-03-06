from basic_handler import *
from utility import *
import json

class AdminHandler(Handler):
	def get(self):
		if not self.user :
			self.redirect('/login')
		else :
			# if the user has not active his account
			if self.user.status == False :
				self.redirect("/verify")
			else :
				# dictionary getting post data by categories
				dic_posts = numpost_by_categories(self.user)
				list_posts = post_by_user_quit_html(self.user)
				self.render("admin.html", username = self.user.username, data_json = json.dumps(dic_posts), dic_posts = dic_posts, list_posts = list_posts, user_key = self.user.key().id())
