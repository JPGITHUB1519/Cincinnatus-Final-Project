from basic_handler import *
from utility import *
from models.blog_model import *
from models.category_model import *
from general import *
import logging


class NewpostHandler(Handler) :
	def get(self) :
		if not self.user :
			self.redirect('/login')
		else :
			# if the user has not active his account
			if self.user.status == False :
				self.redirect("/verify")
			else :
				if self.user.group > 0 : 
					# a = Category(name = "Tec", description = "Tecnology")
					# a.put()
					category_list = get_category()
					edit_post_id = self.request.get("p") 
					# if send id in the url, edit it!
					if edit_post_id :
						post = post_by_id(edit_post_id)
						self.render("newpost.html",
									category_list = category_list, 
									subject = post.subject, 
									content = post.content,
									category = post.category,
									username = self.user.username,
									user_key = self.user.key().id())
					else :
						self.render("newpost.html", 
									category_list = category_list,
									subject = "",
									content = "",
									category = "", 
									username = self.user.username,
									user_key = self.user.key().id())
				else :
					self.write("You have not Permission to access this page because you are a only reader User")

	def post(self) :
		subject = self.request.get("subject")
		content = self.request.get("content")
		category = self.request.get("category")
		new_category = self.request.get("new_category")
		error = ""
		edit_post_id = self.request.get("p") 
		category_list = get_category()
		if subject and content :
			# if select a category already made
			if edit_post_id :
				post = post_by_id(edit_post_id)
				post.subject = subject
				post.content = content
				post.category = self.check_get_category(category, new_category)
				post.put()
				# Updating the Cache when writing
				get_posts(True)
				get_posts_whithout_status(True)
				# redirecting with the key of the new post
				self.redirect('/%s' % str(post.key().id()) + "?p=true")
			else :
				category_entity = self.check_get_category(category, new_category)
				post = Blog(subject = subject, content = content, category = category_entity.key(), user = self.user.key(), status = True, parent = ancestor_key)
				post.put()
				# Updating the Cache when writing
				get_posts(True)
				get_posts_whithout_status(True)
				# redirecting with the key of the new post
				self.redirect('/%s' % str(post.key().id()))
		else :
			error= "YOU MUST FILL ALL THE FIELDS" 
			self.render("newpost.html", error = error, 
										subject = subject,
										content  = content,
										category = category,
										category_list = category_list,
										username = self.user,
										user_key = self.user.key().id())

	def check_get_category(self, category, new_category):
		""""
			return the post category
			if the category exits look for it in the db and return it
			else create a new one category and return it!
		"""
		if category != "other" and not new_category :
			# category_key = db.Key.from_path("Category", int(category), parent = ancestor_key)
			category_entity = category_by_id(category)
			# cr = Category(name = "Math")
			# cr.put()
			# error on take category
			return category_entity
		else :
			category_entity  = Category(name = new_category, parent = ancestor_key)
			category_entity.put()
			return category_entity
