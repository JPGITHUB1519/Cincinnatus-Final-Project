from basic_handler import *
import json

class AdministrationHandler(Handler):
	def get(self):
		if not self.user :
			self.redirect('/login')
		else :
			# if the user has not active his account
			if self.user.status == False :
				self.redirect("/verify")
			else :
				# dictionary getting post data by categories
				dic_posts = numpost_all()
				list_posts = get_posts_whithout_status()
				self.render("administration.html", username = self.user.username, data_json = json.dumps(dic_posts), dic_posts = dic_posts, list_posts = list_posts)
	
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(self.request.body)
		response = {}
		action = data["action"]
		post_id = data["post_id"] 
		response["status"] = "ok"
		if action == "delete_post" :
			# rembember delete the post in cascada(with comments)
			post = post_by_id(post_id)
			if post :
				post_key = post.key()
				logging.error(post_key)
				# deleting post in cascade
				post.delete()
				delete_comments_cascade_bypost(post)
				get_posts_whithout_status(True)
				get_comments_by_post(post_id, True)
			else :
				response["status"] = "error"
		self.write(json.dumps(data))