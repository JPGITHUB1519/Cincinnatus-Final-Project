from basic_handler import * 
from utility import *

HTML = """
<html>
	<body>
		<h1>Welcome To OUR PAGE</h1>
	</body>
</html>
"""

TEXT = "Email Testing"
class TestHandler(Handler) :
	def get(self) :
		try:
			response = send_complex_message("juanpedrotramposo@gmail.com", TEXT, HTML)
			self.write("Enviado")
		except Exception as e:
			self.write("Error %s" % e.message)
		finally:
			pass
		