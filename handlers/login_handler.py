from basic_handler import *

class LoginHandler(Handler):
	def get(self):
		# if the user not logged
		if not self.user :
			self.render("login.html", user = self.user)
		else :
			self.redirect("/")
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		error_login = ""
		userobj = User.all().filter("username =", username).get()
		if userobj :
			if valid_password(username, password, userobj.password) :
				self.login(userobj)
			else :
				error_login = "Invalid Login"
				self.render("login.html", error_login = error_login)
		else :
			error_login = "Invalid Login"
			self.render("login.html", error_login = error_login)