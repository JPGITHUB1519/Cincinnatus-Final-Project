from basic_handler import *
from utility import *

class MainHandler(Handler):
	def get(self):
		lista_post = get_posts()
		seconds_last = time.time() - memcache.get("time_last_query")
		QUERIED = "queried %s seconds ago" % int(seconds_last)
		self.render("index.html", lista_post = lista_post, QUERIED = QUERIED)
