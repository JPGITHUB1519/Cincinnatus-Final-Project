from basic_handler import *
from utility import *
import json

class AdminHandler(Handler):
	def get(self):
		data = numpost_by_categories()
		data_numbers = []
		data_keys = []
		for key in data :
			data_numbers.append(data[key])
			data_keys.append(key)
		# to pass a list to javascript, we have to pass it as a json
		self.render("admin.html", data = data, data_numbers = data_numbers, data_json = json.dumps(data))

