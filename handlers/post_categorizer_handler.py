from basic_handler import *
import json

class PostCategorizerHandler(Handler):
	""" Post Categorize Service
		This Handler returns a json with the post clasified by category
	"""
	def get(self):
		self.write("hello")

	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(self.request.body)
		category = category_by_id(data["category_id"])
		post_list = post_by_category(category)
		logging.error(post_list)
		response = {"status" : "error", "data" : []}

		if post_list :
			for post in post_list :
				# converting model to json
				aux_dic = {}
				aux_dic["subject"] = post.subject
				aux_dic["content"] = post.content
				aux_dic["date"] = str(post.date)
				aux_dic["category"] = db.to_dict(post.category)   
				aux_dic["username"] = post.user.username
				aux_dic["last_modified"] = str(post.last_modified)
				aux_dic["status"] = post.status 
				response["data"].append(aux_dic)
				response["status"] = "ok"
		# sending data to client
		self.write(json.dumps(response))
