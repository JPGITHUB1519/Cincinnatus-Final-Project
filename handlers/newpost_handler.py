from basic_handler import *
from models.blog_model import *

class NewpostHandler(Handler) :
	def get(self) :
		self.render("newpost.html")

	def post(self) :
		subject = self.request.get("subject")
		content = self.request.get("content")
		error = ""
		if subject and content :
			post = Blog(subject = subject, content = content)
			post.put()
			# Updating the Cache when writing
			get_posts(True)
			# redirecting with the key of the new post
			self.redirect('/%s' % str(post.key().id()))
		else :
			error= "YOU MUST FILL ALL THE FIELDS" 
			self.render("newpost.html", error = error, 
										subject = subject,
										content  = content)