from main_handler import * 
import json

class PermalinkJsonHandler(Handler):
	def get(self, post_id) :
		# create key from id
		key = db.Key.from_path('Blog', int(post_id))
		# obtain the model from the key
		post = db.get(key)
		if not post:
		    self.write("ERRROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
		    return
		dicc = {}
		dicc["content"] = post.content
		dicc["created"] = date_to_string(post.date)
		dicc["last_modified"] = date_to_string(post.last_modified)
		dicc["subject"] = post.subject
		# creating json
		result_json = json.dumps(dicc)
		# printing json
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(result_json)


