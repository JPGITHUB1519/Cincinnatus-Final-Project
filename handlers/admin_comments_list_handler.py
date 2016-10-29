from basic_handler import * 

class AdminCommentsListHandler(Handler) :
	def get(self, post_id) :
		comments = get_comments_by_post(post_id)
		total_comments = count_comments_by_post(post_id)
		post = get_permalink(post_id)
		logging.error(comments)
		self.render("admin_comment_list.html", p = post, list_comments = comments)