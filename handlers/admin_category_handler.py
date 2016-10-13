from basic_handler import *

class AdminCategoryHandler(Handler):
	def get(self):
		self.render("admin_category.html")

	def post(self):
		category_name = self.request.get("category_name")
		cond_error = False
		cond_exits = False
		error_exits = "This Category Already Exits"
		error = "You must fill all the Fields"
		if category_name :
			if(insert_category(category_name)) :
				self.render("admin_category.html")
			else :
				self.render("admin_category.html", error_exits = error_exits)
		else :
			self.render("admin_category.html", error = error)