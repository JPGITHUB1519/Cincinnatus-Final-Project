from basic_handler import *

class LogoutHandler(Handler):
	def get(self):
		self.logout()