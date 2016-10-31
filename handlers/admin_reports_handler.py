from basic_handler import *

class AdminReportsHandler(Handler):
	def get(self):
		reports_list = get_reports()
		self.render("administration_reports.html", reports_list = reports_list)
