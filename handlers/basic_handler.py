import webapp2
import jinja2
import os
from general import *
from utility import *
import logging
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler) :
	def write(self, *a, **kw) :
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :
		self.write(self.render_str(template, **kw))
		
	def login(self, user) :
		self.response.set_cookie("user_id", make_secure_val(str(user.key())))
		self.redirect("/welcome")

	def logout(self) :
		self.response.delete_cookie("user_id")
		self.redirect("/login")

	def get_cookie_value(self, name) :
		cookie_value = self.request.cookies.get(name)
		return cookie_value

	# def read_secure_cookie(self, name):
	# 	# get the value of a cookie and see if it is correct
	# 	cookie_val = self.request.cookies.get(name)
 	#        return cookie_val and check_secure_val(cookie_val)

	def initialize(self, *a, **kw):
		""" 
		this is called everytime we make a request
		"""
		webapp2.RequestHandler.initialize(self, *a, **kw)
		user_cookie_value = self.get_cookie_value("user_id")
		# checking if is a valid user in the cookie
		if user_cookie_value :
			if check_secure_val(user_cookie_value) :
				# obtain data from cookie
				aux = user_cookie_value.split("|")
				key = aux[0]
				# getting username from cookie
				user = db.get(key)
				# saving user key
				self.user = user
			else :
				self.user = None
		else :
			self.user = None