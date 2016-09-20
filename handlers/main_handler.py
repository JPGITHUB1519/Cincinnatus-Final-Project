from basic_handler import *

class MainHandler(Handler):
	def get(self):
		self.render("index.html")