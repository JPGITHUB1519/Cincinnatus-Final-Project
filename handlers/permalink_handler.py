from basic_handler import *
from main_handler import *

class PermalinkHandler(MainHandler):
    def get(self, post_id):
    	post = get_permalink(post_id)
    	# key = str(db.Key.from_path('Blog', int(post_id)))
        if not post:
            self.write("ERRROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
            return
        self.render("permalink.html", p = post)