from basic_handler import * 

class TestHandler(Handler) :
	def get(self) :
		self.render("base.html")