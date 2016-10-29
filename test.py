import operator

class a:
	def __init__(self):
		pass
	def b():
		pass

dic = {'5298615253729280': [4, a], 
'5439352742084608': [3, a], 
'6705990137282560': [3, a], 
'4514663463124992': [5, a], 
'5710932114145280': [6, a]}


dic = sorted(dic.items(), key=operator.itemgetter(1), reverse = True)
print dic
