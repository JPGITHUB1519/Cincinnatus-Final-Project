from basic_handler import *

class AdministrationHandler(Handler):
	def get(self):
		self.render("administration.html")