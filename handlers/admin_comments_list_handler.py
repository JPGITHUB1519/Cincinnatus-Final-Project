from basic_handler import *
import json 

class AdminCommentsListHandler(Handler) :
	def get(self, post_id) :
		comments = get_comments_by_post(post_id)
		total_comments = count_comments_by_post(post_id)
		post = get_permalink(post_id)
		logging.error(comments)
		self.render("admin_comment_list.html", p = post, list_comments = comments)

	def post(self, post_id) :
		self.response.headers['Content-Type'] = 'application/json'
		data = json.loads(self.request.body);
		action = data["action"]
		comment_id = data["comment_id"]
		response = {}
		response["status"] = "ok"
		response["comment_id"] = comment_id
		response["action"] = action
		cond_error = False
		error_subject = "You Must Fill the Subject"
		error_content = "You Must Fill the Content"

		if action == "delete_comment" :
			comment_entity = comment_by_id(comment_id)
			if comment_entity :
				comment_entity.delete()
				get_comments_by_post(post_id, True)

		if action == "update_comment" :
			subject = data["subject"]
			content = data["content"]
			if subject == "" :
				cond_error = True
				response["error_subject"] = error_subject
			if content == "" :
				cond_error = True
				response["error_content"] = error_content
			if not cond_error : 
				comment_entity = comment_by_id(comment_id)
				if comment_entity :
					comment_entity.subject = subject
					comment_entity.content = content
					comment_entity.put()
					get_comments_by_post(post_id, True)
		self.write(json.dumps(response))