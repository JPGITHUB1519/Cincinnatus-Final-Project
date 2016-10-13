from basic_handler import *
import json

class AdministrationHandler(Handler):
	def get(self):
		if not self.user :
			self.redirect('/login')
		else :
			# if the user has not active his account
			if self.user.status == False :
				self.redirect("/verify")
			else :
				# dictionary getting post data by categories
				dic_posts = numpost_all()
				list_posts = get_posts_whithout_status()
				self.render("administration.html", username = self.user.username, data_json = json.dumps(dic_posts), dic_posts = dic_posts, list_posts = list_posts)