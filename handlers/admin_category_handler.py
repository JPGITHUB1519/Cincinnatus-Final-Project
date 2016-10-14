from basic_handler import *
from models.category_model import *
import json
class AdminCategoryHandler(Handler):
	def get(self):
		category_list = get_category()
		self.render("admin_category.html", category_list = category_list)

	def post(self):
		# category_name = self.request.get("category_name")
		# cond_error = False
		# cond_exits = False
		# error_exits = "This Category Already Exits"
		# error = "You must fill all the Fields"
		# if category_name :
		# 	if(insert_category(category_name)) :
		# 		self.render("admin_category.html")
		# 	else :
		# 		self.render("admin_category.html", error_exits = error_exits)
		# else :
		# 	self.render("admin_category.html", error = error)
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(self.request.body);
		
		action = data["action"]
		response = {}
		if action == "insert" :
			category_name = data["category_name"]
			if category_name :
				category_entity = insert_category(category_name)
				if category_entity :
					response["status"] = "ok"
					response["category_entity"] = {
						"category_id" : int(category_entity.key().id()),
						"category_name" : category_entity.name,
						"category_key" : str(category_entity.key()),
						"category_date" : str(category_entity.date)
						}
				else :
					response["status"] = "error"
					response["error_exits"] = "This Category Already Exits"
			else :
				response["status"] = "error"
				response["error_empty"] = "You must fill all the Fields"

		if action == "delete" :
			category_key = data["category_key"]
			if category_key :
				db.delete(category_key)
				response["status"] = "ok"
				response["category_key"] = category_key
			else :
				response["error"] = "Empty Category Key"
		self.write(json.dumps(response))