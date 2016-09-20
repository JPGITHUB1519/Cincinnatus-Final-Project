from basic_handler import *
from utility import *

class MainHandler(Handler):
	def get(self):
		lista_post = get_posts()
		self.render("index.html", lista_post = lista_post)
