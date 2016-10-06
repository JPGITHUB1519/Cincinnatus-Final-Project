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
			email_subject = "Welcome to Ninja Blog"
			email_html = """
			<!doctype html>
			<html>
			<head>
			<meta name="viewport" content="width=device-width" />
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
			<title>Activation Account</title>
			<style>
			  /* -------------------------------------
			      GLOBAL RESETS
			  ------------------------------------- */
			  img {
			    border: none;
			    -ms-interpolation-mode: bicubic;
			    max-width: 100%%; }

			  body {
			    background-color: #f6f6f6;
			    font-family: sans-serif;
			    -webkit-font-smoothing: antialiased;
			    font-size: 14px;
			    line-height: 1.4;
			    margin: 0;
			    padding: 0; 
			    -ms-text-size-adjust: 100%%;
			    -webkit-text-size-adjust: 100%%; }
			    table {
			    border-collapse: separate;
			    mso-table-lspace: 0pt;
			    mso-table-rspace: 0pt;
			    width: 100%%; }
			    table td {
			      font-family: sans-serif;
			      font-size: 14px;
			      vertical-align: top; }

			  /* -------------------------------------
			      BODY & CONTAINER
			  ------------------------------------- */

			  .body {
			    background-color: #f6f6f6;
			    width: 100%%; }

			  .container {
			    display: block;
			    Margin: 0 auto !important;
			    /* makes it centered */
			    max-width: 580px;
			    padding: 10px;
			    width: auto !important;
			    width: 580px; }

			  .content {
			    box-sizing: border-box;
			    display: block;
			    Margin: 0 auto;
			    max-width: 580px;
			    padding: 10px; }

			    /* -------------------------------------
			      TYPOGRAPHY
			  ------------------------------------- */
			  h1,
			  h2,
			  h3,
			  h4 {
			    color: #000000;
			    font-family: sans-serif;
			    font-weight: 400;
			    line-height: 1.4;
			    margin: 0;
			    Margin-bottom: 30px; }

			  h1 {
			    font-size: 35px;
			    font-weight: 300;
			    text-align: center;
			    text-transform: capitalize; }

			  p,
			  ul,
			  ol {
			    font-family: sans-serif;
			    font-size: 14px;
			    font-weight: normal;
			    margin: 0;
			    Margin-bottom: 15px; }
			    p li,
			    ul li,
			    ol li {
			      list-style-position: inside;
			      margin-left: 5px; }

			  a {
			    color: #3498db;
			    text-decoration: underline; }
			   /* -------------------------------------
			      BUTTONS
			  ------------------------------------- */
			  .btn {
			    box-sizing: border-box;
			    width: 100%%; }
			    .btn > tbody > tr > td {
			      padding-bottom: 15px; }
			    .btn table {
			      width: auto; }
			    .btn table td {
			      background-color: #ffffff;
			      border-radius: 5px;
			      text-align: center; }
			    .btn a {
			      background-color: #ffffff;
			      border: solid 1px #3498db;
			      border-radius: 5px;
			      box-sizing: border-box;
			      color: #3498db;
			      cursor: pointer;
			      display: inline-block;
			      font-size: 14px;
			      font-weight: bold;
			      margin: 0;
			      padding: 12px 25px;
			      text-decoration: none;
			      text-transform: capitalize; }

			  .btn-primary table td {
			    background-color: #3498db; }

			  .btn-primary a {
			    background-color: #3498db;
			    border-color: #3498db;
			    color: #ffffff; }

			    /* -------------------------------------
			      OTHER STYLES THAT MIGHT BE USEFUL
			  ------------------------------------- */
			  .last {
			    margin-bottom: 0; }

			  .first {
			    margin-top: 0; }

			  .align-center {
			    text-align: center; }

			  .align-right {
			    text-align: right; }

			  .align-left {
			    text-align: left; }

			  .clear {
			    clear: both; }

			  .mt0 {
			    margin-top: 0; }

			  .mb0 {
			    margin-bottom: 0; }

			  .preheader {
			    color: transparent;
			    display: none;
			    height: 0;
			    max-height: 0;
			    max-width: 0;
			    opacity: 0;
			    overflow: hidden;
			    mso-hide: all;
			    visibility: hidden;
			    width: 0; }

			  .powered-by a {
			    text-decoration: none; }

			  hr {
			    border: 0;
			    border-bottom: 1px solid #f6f6f6;
			    Margin: 20px 0; }

			    /* -------------------------------------
			      RESPONSIVE AND MOBILE FRIENDLY STYLES
			  ------------------------------------- */
			  @media only screen and (max-width: 620px) {
			    table[class=body] h1 {
			      font-size: 28px !important;
			      margin-bottom: 10px !important; }
			    table[class=body] p,
			    table[class=body] ul,
			    table[class=body] ol,
			    table[class=body] td,
			    table[class=body] span,
			    table[class=body] a {
			      font-size: 16px !important; }
			    table[class=body] .wrapper,
			    table[class=body] .article {
			      padding: 10px !important; }
			    table[class=body] .content {
			      padding: 0 !important; }
			    table[class=body] .container {
			      padding: 0 !important;
			      width: 100%% !important; }
			    table[class=body] .main {
			      border-left-width: 0 !important;
			      border-radius: 0 !important;
			      border-right-width: 0 !important; }
			    table[class=body] .btn table {
			      width: 100%% !important; }
			    table[class=body] .btn a {
			      width: 100%% !important; }
			    table[class=body] .img-responsive {
			      height: auto !important;
			      max-width: 100%% !important;
			      width: auto !important; }}

			  /* -------------------------------------
			      PRESERVE THESE STYLES IN THE HEAD
			  ------------------------------------- */
			  @media all {
			    .ExternalClass {
			      width: 100%%; }
			    .ExternalClass,
			    .ExternalClass p,
			    .ExternalClass span,
			    .ExternalClass font,
			    .ExternalClass td,
			    .ExternalClass div {
			      line-height: 100%%; }
			    .apple-link a {
			      color: inherit !important;
			      font-family: inherit !important;
			      font-size: inherit !important;
			      font-weight: inherit !important;
			      line-height: inherit !important;
			      text-decoration: none !important; } 
			    .btn-primary table td:hover {
			      background-color: #34495e !important; }
			    .btn-primary a:hover {
			      background-color: #34495e !important;
			      border-color: #34495e !important; } }

			  /* own styles */
			  .text-center
			  {
			    text-align: center;
			  }

			</style>
			</head>
			<body class="">
			<table border="0" cellpadding="0" cellspacing="0" class="body">
			  <tr>
			    <td>&nbsp;</td>
			    <td class="container">
			      <div class="content">

			        <!-- START CENTERED WHITE CONTAINER -->
			        <span class="preheader">This is preheader text. Some clients will show this text as a preview.</span>
			        <table class="main">

			          <!-- START MAIN CONTENT AREA -->
			          <tr>
			            <td class="wrapper">
			              <table border="0" cellpadding="0" cellspacing="0">
			                <tr>
			                  <td>
			                    <h2 class="text-center">Hello %(username)s</h2>
			                    <p class="text-center">Thanks For Signup to <span style="font-weight: bold;">NINJAS BLOG!</span>. Please active your account by clicking the button below : </p>
			                    <table style="width : 0 !important; margin: 0 auto;" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
			                      <tbody>
			                        <tr>
			                          <td align="left">
			                            <table border="0" cellpadding="0" cellspacing="0">
			                              <tbody>
			                                <tr>
			                                  <td> <a href="%(link)s" target="_blank">Activate Your Account</a> </td>
			                                </tr>
			                              </tbody>
			                            </table>
			                          </td>
			                        </tr>
			                      </tbody>
			                    </table>
			                    <p class="text-center">Thanks and Happy Blogging</p>
			                    <p class="text-center" style="font-weight: bold; font-size: 1.3em;" >The Ninjas Team</p>
			                  </td>
			                </tr>
			              </table>
			            </td>
			          </tr>
			          <!-- END MAIN CONTENT AREA -->
			          </table>
			        
			<!-- END CENTERED WHITE CONTAINER --></div>
			    </td>
			    <td>&nbsp;</td>
			  </tr>
			</table>
			</body>
			</html>
			"""
			logging.error(user.email)
			email_html = email_html % {"username" : user.username , "link" : verify_link} 
			send_mailgun_complex_message(user.email, email_subject, email_html)
			# send_html_email(user.email, email_subject, email_html)
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
