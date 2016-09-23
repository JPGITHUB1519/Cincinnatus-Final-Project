from basic_handler import *

class AdminHandler(Handler):
	def get(self):
		self.render("admin.html")
