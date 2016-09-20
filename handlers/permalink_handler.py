from basic_handler import *
from main_handler import *
import time

class PermalinkHandler(MainHandler):
    def get(self, post_id):
    	post = get_permalink(post_id)
    	key = str(db.Key.from_path('Blog', int(post_id), parent  = ancestor_key))
        query_time = time.time() - memcache.get(key)[1] 
        if not post:
            self.write("ERRROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
            return
        QUERIED =  "queried %s seconds ago" % int(query_time)
        self.render("permalink.html", p = post, QUERIED = QUERIED)