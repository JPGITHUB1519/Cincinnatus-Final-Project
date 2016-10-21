from basic_handler import *
from utility import *
import json

class mainJsonHandler(Handler):
	def get(self):
		lista_post = Blog.get_posts()
		#lista_post = Blog.all.order('-created'.fetch(limit = 10))
		dicc = []
		# makin the dictionaries lst
		for p in lista_post :
			aux_dic = {}
			aux_dic["content"] = p.content
			aux_dic["created"] = date_to_string(p.date)
			aux_dic["last_modified"] = date_to_string(p.last_modified)
			aux_dic["subject"] = p.subject
			dicc.append(aux_dic)
			aux_dic = {}
		#output dictionary
		self.response.headers['Content-Type'] = 'application/json'
		result_json = json.dumps(dicc)
		self.response.out.write(result_json)