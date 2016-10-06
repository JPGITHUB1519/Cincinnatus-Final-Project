from basic_handler import *
from main_handler import *
import time

class PermalinkHandler(MainHandler):
    def get(self, post_id):
        if not self.user :
            self.redirect('/login')
        else :
            # if the user has not active his account
            if self.user.status == False :
                self.redirect("/verify")
            else :
            	update = self.request.get("p")
            	# if update is true query the cache and show the new post else load from cache
            	if update == "true" :
            		post = get_permalink(post_id, True)
            	else :
            		post = get_permalink(post_id)
            	key = str(db.Key.from_path('Blog', int(post_id), parent  = ancestor_key))
                query_time = time.time() - memcache.get(key)[1] 
                if not post:
                    self.write("ERRROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
                    return
                QUERIED =  "queried %s seconds ago" % int(query_time)
                self.render("permalink.html", p = post, QUERIED = QUERIED)