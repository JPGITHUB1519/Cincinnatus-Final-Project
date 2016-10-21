import operator
import time
from google.appengine.ext import db
from handlers.basic_handler import *
from category_model import *
from user_model import *

class Blog(db.Model) :
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	category = db.ReferenceProperty(Category)
	user = db.ReferenceProperty(User)
	# auto now is for overwriting a existed date if it exits
	last_modified = db.DateProperty(auto_now = True)
	status = db.BooleanProperty()
	likes = db.IntegerProperty(default = 0)
	users_liked = db.ListProperty(db.Key, default = [])
	dislikes = db.IntegerProperty(default = 0)
	users_disliked = db.ListProperty(db.Key, default = [])

	@staticmethod
	def get_posts(update = False) :
		""" 
			This obtain the post from the Cache. The Cache is always update
			and it get update when a user make a new Post. We only read in the
			Database when we write on it
		"""
		# using the global variable query time
		key = "post"
		posts = memcache.get(key)
		if posts is None or update :
			logging.error("DBQUERY")
			# getting post from the database
			# posts = db.GqlQuery("SELECT  * FROM Blog order by date desc limit 10")
			posts = Blog.all().filter("status =", True).order("-date").ancestor(ancestor_key)
			posts = list(posts)
			# saving the last time query to the database
			memcache.set("time_last_query", time.time()) 
			# updating cache
			memcache.set(key, posts)
		return posts

	@staticmethod
	def get_posts_whithout_status(update = False) :
		""" 
			The same that the before but without status filter
			This obtain the post from the Cache. The Cache is always update
			and it get update when a user make a new Post. We only read in the
			Database when we write on it
		"""
		# using the global variable query time
		key = "post_nostatus"
		posts = memcache.get(key)
		if posts is None or update :
			logging.error("DBQUERY")
			# getting post from the database
			# posts = db.GqlQuery("SELECT  * FROM Blog order by date desc limit 10")
			posts = Blog.all().order("-date").ancestor(ancestor_key)
			posts = list(posts)
			# saving the last time query to the database
			memcache.set("time_last_query", time.time()) 
			# updating cache
			memcache.set(key, posts)
		return posts

	@staticmethod
	def get_permalink(post_id, update = False) :
		#cache reference memcache[postid] = [post, time]
		# create key from id
		key = db.Key.from_path('Blog', int(post_id), parent = ancestor_key)
		cache_key = str(key)
		# look for the post in the cache
		post = memcache.get(cache_key)
		if not post or update :
		    logging.error("DBQUERY")
		    # obtain the model from the key
		    post = db.get(key)
		    query_time = time.time()
		    memcache.set(cache_key, [post, query_time])
		else :
		    # if exists the post in the cache take it
		    post = memcache.get(cache_key)[0]
		return post

	@staticmethod
	def hottest_posts(hootest_dic, num) :
		"""
			return dic["post_id" : num_comments]
			Returns the number of Comments  of The Hottets each Post 
		"""
		return dict(sorted(hootest_dic.iteritems(), key=operator.itemgetter(1), reverse=True)[:num])

	@staticmethod
	# post actions
	def post_by_category(category):
		"""
			returns posts filter by one categorie
		"""
		post = Blog.all().filter('category =', category.key()).ancestor(ancestor_key)
		return list(post)

	def post_by_user(user):
		post = Blog.all().filter('user =', user.key())
		return list(post)

	@staticmethod
	def post_by_user(user):
		post = Blog.all().filter('user =', user.key())
		return list(post)

	@staticmethod  
	# get post by id
	def post_by_id(id):
		post = Blog.get_by_id(int(id), parent = ancestor_key)
		return post

	@staticmethod
	# filter by user and category
	def post_by_category(category):
		"""
			returns posts filter by one categorie
		"""
		post = Blog.all().filter('category =', category.key()).ancestor(ancestor_key)
		return list(post)

	@staticmethod
	# filter by user and category
	def post_by_category_and_user(category, user):
		"""
			returns posts filter by one categorie
		"""
		post = Blog.all().filter('category =', category.key()).filter('user = ', user.key()).ancestor(ancestor_key)
		return list(post)

	@staticmethod
	# number of post by topic of all users
	def numpost_all():
	    """
	        it returns a dictionary with the topics and its numbers of pos
	    t"""
	    topics = Category.get_category()
	    data = {}
	    if topics :
	        for topic in topics :
	            post = Blog.post_by_category(topic)
	            data[topic.name] = len(post)
	        return data
	    else :
	        return None

	@staticmethod
	# number of post by topic and user
	def numpost_by_categories(user):
	    """
	        it returns a dictionary with the topics and its numbers of pos
	    t"""
	    topics = get_category()
	    data = {}
	    if topics :
	        for topic in topics :
	            post = post_by_category_and_user(topic, user)
	            data[topic.name] = len(post)
	        return data
	    else :
	        return None
