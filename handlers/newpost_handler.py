from basic_handler import *
from utility import *
from models.blog_model import *
from models.category_model import *
from general import *


class NewpostHandler(Handler) :
	def get(self) :
		# a = Category(name = "Tec", description = "Tecnology")
		# a.put()
		category_list = get_category()
		self.render("newpost.html", category_list = category_list)

	def post(self) :
		subject = self.request.get("subject")
		content = self.request.get("content")
		category = self.request.get("category")
		new_category = self.request.get("new_category")
		error = ""
		if subject and content :
			# if select a category already made
			if not new_category :
				# category_key = db.Key.from_path("Category", int(category), parent = ancestor_key)
				category_entity = Category.get_by_id(int(category))
				post = Blog(subject = subject, content = content, category = category_entity.key(), user = self.user.key(), parent = ancestor_key)
			else :
				cat = Category(name = new_category, parent = ancestor_key)
				cat.put()
				post = Blog(subject = subject, content = content, category = cat.key(), user = self.user.key(), parent = ancestor_key)

			# if category == "other" :
				
			# 	post = Blog(subject = subject, content = content, category = new_category, parent = ancestor_key)
			post.put()
			# Updating the Cache when writing
			get_posts(True)
			# redirecting with the key of the new post
			self.redirect('/%s' % str(post.key().id()))
		else :
			error= "YOU MUST FILL ALL THE FIELDS" 
			self.render("newpost.html", error = error, 
										subject = subject,
										content  = content,
										category_list = category_list)