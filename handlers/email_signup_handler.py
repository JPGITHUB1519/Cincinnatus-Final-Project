import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utility import *
from basic_handler import *
from models.user_model import User
from general import * 
from google.appengine.ext import db
# image api
from google.appengine.api import images
import logging


class EmailSignupHandler(Handler):
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
		group = int(self.request.get("group")) 
		avatar = self.request.POST.get("pic", None)
		avatar_filename = avatar.filename
		avatar_route = self.request.get("image_route")
		# avatar = images.resize(avatar, 32, 32)
		# error variables
		error_username = ""
		error_password = ""
		error_verify = ""
		error_email = ""
		error_exits = ""
		error_group = ""
		emails = get_users_by_emails(email)
		verify_hash = random_hash()
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
			if not self.validate_group(group) :
				error_group = "That's not a Valid Group"
			if not self.validate_password(password):
				error_password = "That's not a Valid Password"
				cond_error = True
			else :
				if password != verify :
					error_verify = "Your passwords didn't match."
					cond_error = True
			# if emails : 
			# 	error_email = "This Email already Exits in the database"
			# 	cond_error = True
			# else :
			# 	if not self.validate_email(email) :
			# 		error_email = "That's not a Valid Email"
			# 		cond_error = True
					
		if cond_error == False :
			# generating password hash
			password = make_password_hash(username, password)
			# creating a new instance of the object
			user = User(username=username, password = password, email = email, group = group, avatar = avatar.file.read(), avatar_filename = avatar_filename, verify_hash = verify_hash)
			# saving data in the database
			user.put()
			verify_link = "http://localhost:10080/verify?email=%s&verify_hash=%s" %(user.email, user.verify_hash)
			email_text = "Verification Email"
			email_html = """
			<!DOCTYPE html>
			<html>
			<head>
			<style type="text/css">
				body
				{
					background-color: #ECEBE7;
				}
				.container
				{
					width: 960px;
					margin : 0 auto;
					background-color: white;
				}
				.text-center
				{
					text-align: center;
				}
				.link
				{
					width: 200px;
					height: 200px;
					border: 1px solid;
				}
				.btn-custom {
					background-color: hsl(195, 60%, 35%) !important;
					background-repeat: repeat-x;
					filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#2d95b7", endColorstr="#23748e");
					background-image: -khtml-gradient(linear, left top, left bottom, from(#2d95b7), to(#23748e));
					background-image: -moz-linear-gradient(top, #2d95b7, #23748e);
					background-image: -ms-linear-gradient(top, #2d95b7, #23748e);
					background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #2d95b7), color-stop(100%, #23748e));
					background-image: -webkit-linear-gradient(top, #2d95b7, #23748e);
					background-image: -o-linear-gradient(top, #2d95b7, #23748e);
					background-image: linear-gradient(#2d95b7, #23748e);
					border-color: #23748e #23748e hsl(195, 60%, 32.5%);
					color: #fff !important;
					text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.16);
					-webkit-font-smoothing: antialiased;
					padding: 1em;
					display: block;
					margin: 0 auto;
					width: 200px;
					height: 20px;
					text-decoration: none;

				}
				.btn-custom:hover
				{
					background-color: hsl(0, 69%, 22%) !important;
					background-repeat: repeat-x;
					filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#b42121", endColorstr="#5e1111");
					background-image: -khtml-gradient(linear, left top, left bottom, from(#b42121), to(#5e1111));
					background-image: -moz-linear-gradient(top, #b42121, #5e1111);
					background-image: -ms-linear-gradient(top, #b42121, #5e1111);
					background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #b42121), color-stop(100%, #5e1111));
					background-image: -webkit-linear-gradient(top, #b42121, #5e1111);
					background-image: -o-linear-gradient(top, #b42121, #5e1111);
					background-image: linear-gradient(#b42121, #5e1111);
					border-color: #5e1111 #5e1111 hsl(0, 69%, 17%);
					color: #fff !important;
					text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.33);
					-webkit-font-smoothing: antialiased;
				}
			</style>
			<title></title>
			</head>
			<body>
			<div class="container">
				<h2 class="text-center">%(username)s</h2>
				<p class="text-center">Thanks For SignUp to NINJAS BLOG!. Please active your accouunt by clicking the button below : </p>
				<a href="%(link)s" class="btn-custom text-center">Activate Your Account</a>
				<p class="text-center">Thanks and Happy Blogging</p>
				<p class="text-center">The Ninjas Team</p>
			</div>
			</body>
			</html>""" % {"name" : user.username, "link" : verify_link}
			send_complex_message(user.email, email_text, email_html)
			self.login(user)
			self.redirect('/verify')
		else :
			self.render("signup.html",
							error_username= error_username, 
							error_password = error_password,
							error_verify = error_verify,
							error_email = error_email, 
							username = username, 
							email = email,
							error_exits = error_exits,
							error_group = error_group,
							avatar_route = avatar_route
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
