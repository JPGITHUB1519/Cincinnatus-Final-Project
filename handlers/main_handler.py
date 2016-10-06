from basic_handler import *
from utility import *

class MainHandler(Handler):
	def get(self):
		# if the user is not logged, sent to login
		if not self.user :
			self.redirect('/login')
		else :
			# if the user has not active his account
			if self.user.status == False :
				self.redirect("/verify")
			else :
				# if the user has reading permmisions
				if self.user.group == 0 or self.user.group == 2 or self.user.group == 3 :
					lista_post = get_posts()
					list_categories = get_category()
					seconds_last = time.time() - memcache.get("time_last_query")
					QUERIED = "queried %s seconds ago" % int(seconds_last)
					self.render("index.html", 
								lista_post = lista_post, 
								QUERIED = QUERIED, 
								username = self.user.username,
								list_categories = list_categories)
				else :
					self.write("You have not Permission to access this page because you are a only Writer User")
