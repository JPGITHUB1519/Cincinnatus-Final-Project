from basic_handler import *

class AdminReportsHandler(Handler):
	def get(self) :
		reports = get_reports()
		logging.error(reports)
		self.render("admin_reports.html", reports = reports)

