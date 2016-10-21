class P :
	def __init__(self, x):
		self.x  = x

	@property
	def x(self) :
		return self.__x


perro = P(1)

print P.x