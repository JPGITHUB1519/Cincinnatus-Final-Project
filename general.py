from google.appengine.ext import db
import re
import logging
# validation variables
user_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_check = re.compile(r"^.{3,20}$")
email_check = re.compile(r"^[\S]+@[\S]+.[\S]+$")

email_account = "juanpedro1519@gmail.com"
ancestor_key = db.Key.from_path('User', 'some_id')