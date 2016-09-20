from basic_handler import *

class FlushcacheHandler(Handler) :
	def get(self) :
		# Empty Cache
		memcache.flush_all()
		self.redirect("/")