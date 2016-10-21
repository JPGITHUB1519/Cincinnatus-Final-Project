import operator
from google.appengine.ext import db
from user_model import *
from blog_model import *

class Comment(db.Model) :
	user = db.ReferenceProperty(User)
	post = db.ReferenceProperty(Blog)
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	last_modified = db.DateProperty()
	status = db.BooleanProperty(default = True)

	@staticmethod
	def get_comments_by_post(post_id, update = False) :
		""" 
			Get All Comments of a specified Post
		"""
		# GETTING KEY BY
		post_key = key = db.Key.from_path('Blog', int(post_id), parent  = ancestor_key)
		# each comment has a different space in memcache
		key = "comments_by_post_" + str(post_key)
		comments = memcache.get(key)
		if comments is None or update :
			comments = Comment.all().order("-date").filter("post =", post_key).ancestor(ancestor_key)
			comments = list(comments)
			memcache.set(key, comments)
		return comments

	@staticmethod
	def num_comments_by_post(post_id) :
		post_key = key = db.Key.from_path('Blog', int(post_id), parent  = ancestor_key)
		num_comments = Comment.all().filter("post =", post_key).ancestor(ancestor_key).count()
		return num_comments

	@staticmethod
	def num_comments_all_post():
		"""
			return dic["post_id" : num_comments]
			Returns the number of Comments  of each Post 
		"""
		dic = {}
		posts = Blog.get_posts()
		for post in posts :
			dic[str(post.key().id())] = num_comments_by_post(post.key().id())
		return dic

	@staticmethod
	def numdata_comments_all_post():
		"""
			return dic["post_id" : [num_comments, data]]
			Returns the number of Comments  of each Post and the data
		"""
		dic = {}
		posts = Blog.get_posts()
		for post in posts :
			dic[str(post.key().id())] = []
			dic[str(post.key().id())].append(Comment.num_comments_by_post(post.key().id()))
			dic[str(post.key().id())].append(post)
		return dic

	@staticmethod
	def numcomments_all_category() :
		dic = {}
		category = Category.get_category()
		for cat in category :
			dic[cat.key().id()] = Comment.all().filter("post.category =", cat.key()).ancestor(ancestor_key).count()
		return dic

	@staticmethod
	# comments stuff
	def insert_comment(subject, content, post, user) :
	    comentario = Comment(user = user, post = post, subject = subject, content = content, parent = ancestor_key )
	    comentario.put()
	    Comment.get_comments_by_post(comentario.post.key().id(), True)
	    return comentario

	@staticmethod
	def count_comments_by_post(post_id) :
	    key = db.Key.from_path('Blog', int(post_id), parent  = ancestor_key)
	    return Comment.all().filter("post =", key).count()
