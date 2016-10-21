from basic_handler import *
from models.blog_model import *
import json
import logging

class PostSensationHandler(Handler):
	"""
	 	This handler is for like/ dislike and other sensations of a post
	"""
	def post(self):
		self.response.headers["Content-Type"] = "application/json"
		data = json.loads(self.request.body)
		response = {"status" : "error"}
		post_id = int(data["post_id"])
		action_type = data["action_type"]
		post = Blog.post_by_id(post_id)
		response["post_id"] = post_id
		if post :
			# if client call like
			if action_type == "like" :
				# if the user has not clicked like before like it!
				if self.user.key() not in post.users_liked :
					post.users_liked.append(self.user.key())
					post.likes = post.likes + 1
					response["likes"] = post.likes
					post.put()
					Blog.get_posts(True)
					response["status"] = "ok"

				else :
					response["status"] = "already"
					response["likes"] = post.likes
			if action_type == "dislike" :
				if self.user.key() not in post.users_disliked :
					post.users_disliked.append(self.user.key())
					post.dislikes = post.dislikes + 1
					response["dislikes"] = post.dislikes
					post.put()
					Blog.get_posts(True)
					response["status"] = "ok"
				else:
					response["status"] = "already"
					response["dislikes"] = post.dislikes



		self.write(json.dumps(response))