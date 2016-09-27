from basic_handler import *
from utility import *
import json
import logging
class EnableDisableHandler(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		self.write(json.dumps({"data" : "number"}))
	def post(self):
		# self.response.headers['Content-Type'] = 'application/json'
		# self.write(json.dumps({"data" : "number post"}))
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(self.request.body);
		error = False
		if not data["post_id"] :
			error = True
		else :
			post_id = data["post_id"]
		if not error :
			response = {}
			post = post_by_id(post_id)
			if post : 
				response["post_id"] = post_id
				if post.status == True :
					post.status = False
					response["status"] = "false"
				else :
					post.status = True
					response["status"] = "true"
				# updating cache
				# this is a force change it!
				#memcache.flush_all()
				get_posts(True)
				post.put()
				self.write(json.dumps(response))
			else :
				response = {"error" : "This Post was not found in the database"}
				self.write(json.dumps(response))
		else :
			# if there was an error notify ut
			response = {"error" : "There was an error in your request, Please fill all the data"}
			self.write(json.dumps(response))


