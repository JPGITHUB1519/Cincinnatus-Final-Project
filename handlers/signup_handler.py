import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utility import *
from basic_handler import *
from models.user_model import User
from general import * 
from google.appengine.ext import db
# image api
from google.appengine.api import images


class SignupHandler(Handler):
	def get(self):
		# if the user not logged
		if not self.user :
			self.render("signup.html")
		else :
			self.redirect("/")

	def post(self):
		# getting data from form
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email") 
		# avatar = images.resize(avatar, 32, 32)
		# error variables
		error_username = ""
		error_password = ""
		error_verify = ""
		error_email = ""
		error_exits = ""
		# flag for errors
		cond_error = False
		# getting user from database. get for take the first colunn
		user = User.all().filter("username =", username).get()
		# checking if the user exits in the database
		if user :
			error_exits = "This User Already Exits in the Database"
			cond_error = True
		else :
			if not self.validate_user(username) :
				error_username = "That's not a Valid User"
				cond_error = True
			if not self.validate_password(password):
				error_password = "That's not a Valid Password"
				cond_error = True
			else :
				if password != verify :
					error_verify = "Your passwords didn't match."
					cond_error = True
			if email :
				if not self.validate_email(email) :
					error_email = "That's not a Valid Email"
					cond_error = True
		if cond_error == False :
			# generating password hash
			password = make_password_hash(username, password)
			# creating a new instance of the object
			user = User(username=username, password = password, email = email)
			# saving data in the database
			user.put()
			send_mailgun_simple_message(user.email, "hola")
			self.login(user)
		else :
			self.render("signup.html",
							error_username= error_username, 
							error_password = error_password,
							error_verify = error_verify,
							error_email = error_email, 
							username = username, 
							email = email,
							error_exits = error_exits,
							)

	# validates functions
	def validate_user(self, usuario) :
		return user_check.match(usuario)

	def validate_password(self, password) :
		return password_check.match(password)

	def validate_email(self, email) :
		return email_check.match(email)

	def validate_group(self, group) :
		if group == 0 or group == 1 or group == 2 or group == 3 :
			return True
		return False
