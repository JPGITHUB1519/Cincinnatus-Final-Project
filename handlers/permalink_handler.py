from basic_handler import *
from main_handler import *
from models.comment_model import *
from models.user_model import *
from models.report_model import *
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
                comments = get_comments_by_post(post_id)
                total_comments = count_comments_by_post(post_id)
            	update = self.request.get("p")
            	# if update is true query the cache and show the new post else load from cache
            	if update == "true" :
            		post = get_permalink(post_id, True)
            	else :
            		post = get_permalink(post_id)
            	key = str(db.Key.from_path('Blog', int(post_id), parent  = ancestor_key))
                query_time = time.time() - memcache.get(key)[1] 
                if not post:
                    self.write("ERROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
                    return
                QUERIED =  "queried %s seconds ago" % int(query_time)
                self.render("permalink.html", p = post, 
                                              QUERIED = QUERIED, 
                                              comments = comments, 
                                              total_comments = total_comments, 
                                              user_key = self.user.key().id(),
                                              username = self.user.username)

    def post(self, post_id):
        self.response.headers['Content-Type'] = "application/json"
        data = json.loads(self.request.body)
        action = data["action"]
        response = {"status" : "ok"}
        cond_error = False
        if action == "insert" :
            subject = data["subject"]
            content = data["content"]
            action = data["action"]
            if not subject :
                response["status"] = "error"
                response["error_subject"] = "You must fill the subject"
                cond_error = True
            if not content :
                response["status"] = "error"
                response["error_content"] = "You must fill the Content"
                cond_error = True
            if not cond_error :
                post = post_by_id(post_id)
                comentario = insert_comment(subject, content, post.key(), self.user.key())
                # counting after 
                total_comments = count_comments_by_post(post_id)
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
        if action == "report" :
            comment_key = db.Key.from_path('Comment', data["comment_id"], parent = ancestor_key)
            user_reporter_key = db.Key.from_path('User', data["user_id"], parent = ancestor_key)
            reason = data["reason"]
            if not reason :
                response["error_comment"] = "You Must Fill The Reason"
                cond_error = True
            if not comment_key and not user_reporter_key :
                response["error"] = "An Unexpected Error Ocurred"
            if not cond_error :
                # report comment!
                reporte = Report(user_reporter = user_reporter_key, 
                                comment = comment_key, 
                                reason = reason, parent = ancestor_key)
                reporte.put()
        self.write(json.dumps(response))
