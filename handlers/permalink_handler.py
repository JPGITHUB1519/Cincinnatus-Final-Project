from basic_handler import *
from main_handler import *
from models.comment_model import *
from utility import *
import time
import json

class PermalinkHandler(MainHandler):
    def get(self, post_id):
        if not self.user :
            self.redirect('/login')
        else :
            # if the user has not active his account
            if self.user.status == False :
                self.redirect("/verify")
            else :
                comments = Comment.get_comments_by_post(post_id)
                total_comments = Comment.count_comments_by_post(post_id)
                logging.error(total_comments)
            	update = self.request.get("p")
            	# if update is true query the cache and show the new post else load from cache
            	if update == "true" :
            		post = Blog.get_permalink(post_id, True)
            	else :
            		post = Blog.get_permalink(post_id)
            	key = str(db.Key.from_path('Blog', int(post_id), parent  = ancestor_key))
                query_time = time.time() - memcache.get(key)[1] 
                if not post:
                    self.write("ERRROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
                    return
                QUERIED =  "queried %s seconds ago" % int(query_time)
                self.render("permalink.html", p = post, QUERIED = QUERIED, comments = comments, total_comments = total_comments)

    def post(self, post_id):
        self.response.headers['Content-Type'] = "application/json"
        data = json.loads(self.request.body)
        subject = data["subject"]
        content = data["content"]
        action = data["action"]
        response = {"status" : "ok"}
        cond_error = False
        if action == "insert" :
            if not subject :
                response["status"] = "error"
                response["error_subject"] = "You must fill the subject"
                cond_error = True
            if not content :
                response["status"] = "error"
                response["error_content"] = "You must fill the Content"
                cond_error = True
            if not cond_error :
                post = Blog.post_by_id(post_id)
                comentario = Comment.insert_comment(subject, content, post.key(), self.user.key())
                # counting after 
                total_comments = Comment.count_comments_by_post(post_id)
                response["data"] = {"subject" : comentario.subject,
                                    "content" : comentario.content,
                                    "date" : str(comentario.date),
                                    "post_id" : int(post_id),
                                    "post_key" : str(post.key()),
                                    "user_key" : str(self.user.key()),
                                    "username" : comentario.user.username,
                                    "user_id" : int(self.user.key().id()),
                                    "total_comments" : total_comments}
                logging.error(total_comments)
        self.write(json.dumps(response))
