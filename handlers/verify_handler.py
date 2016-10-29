from basic_handler import *
from models.user_model import User

class VerifyHandler(Handler):
	def get(self):
		email = self.request.get("email")
		verify_hash = self.request.get("verify_hash")
		if not email and not verify_hash :
			self.render("verify.html")
		else :
			if self.user :
				# if the links is correct
				if self.user.email == email and self.user.verify_hash == verify_hash :
					user = User.get(self.user.key())
					user.status = True
					user.put()
					self.redirect('/')
				else :
					self.write("Error Verificando")


