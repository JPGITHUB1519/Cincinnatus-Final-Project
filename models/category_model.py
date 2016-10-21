from google.appengine.ext import db
from google.appengine.api import memcache
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from general import *
class Category(db.Model):
	name = db.StringProperty()
	date = db.DateProperty(auto_now_add=True)

	@staticmethod
	def check_exits_category(category_name):
		""""
			Check if exits a category
		"""
		category_entity = Category.get_category_by_name(category_name)
		logging.error(category_entity)
		if category_entity :
			return True
		return False

	@staticmethod
	def insert_category(category_name) :
		if not Category.check_exits_category(category_name) :
			category_entity = Category(name = category_name, parent = ancestor_key)
			category_entity.put()
			return category_entity
		else :
			return None

	@staticmethod        
	def get_category(update = False):
		"""
			return all categories
		"""
		key = "post"
		categories_list = memcache.get(key)
		if categories_list is None or update :
			logging.info("DBQUERY")
			categories_list = list(Category.all())
			memcache.set(key, categories_list)
		return list(Category.all())

	@staticmethod
	def get_category_by_key(category_key):
		return db.get(category_key)

	@staticmethod
	def get_category_by_name(category_name):
		category_entity = Category.all().filter("name =", category_name).ancestor(ancestor_key)
		return list(category_entity)
	@staticmethod
	def category_by_id(category_id):
		category_entity = Category.get_by_id(int(category_id), parent = ancestor_key)
		return category_entity
