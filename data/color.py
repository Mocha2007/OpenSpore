def d2h(x: int) -> str:
	if x < 16:
		return '0' + hex(x)[2:]
	return hex(x)[2:]


# https://docs.python.org/3.5/reference/datamodel.html
class Color:
	"""For fucking with color in python"""
	def __init__(self, r: int, g: int, b: int):
		assert isinstance(r+g+b, int)
		assert max(r, g, b) <= 255 and min(r, g, b) >= 0
		self.r = r
		self.g = g
		self.b = b

	def __str__(self) -> str:
		return '#' + d2h(self.r) + d2h(self.g) + d2h(self.b)

	def __repr__(self) -> str:
		return 'Color(' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b) + ')'

	def __add__(self, other):
		r = min(self.r + other.r, 255)
		g = min(self.g + other.g, 255)
		b = min(self.b + other.b, 255)
		return Color(r, g, b)

	def __sub__(self, other):
		r = abs(self.r - other.r)
		g = abs(self.g - other.g)
		b = abs(self.b - other.b)
		return Color(r, g, b)

	def __mul__(self, other):
		return Color((self.r*other.r)//255, (self.g*other.g)//255, (self.b*other.b)//255)

	def __matmul__(self, other):
		return Color((self.r+other.r)//2, (self.g+other.g)//2, (self.b+other.b)//2)

	def __truediv__(self, other):
		r = min((self.r*255)//other.r, 255) if other.r else 255
		g = min((self.g*255)//other.g, 255) if other.g else 255
		b = min((self.b*255)//other.b, 255) if other.b else 255
		return Color(r, g, b)

	def __and__(self, other):
		return Color(self.r & other.r, self.g & other.g, self.b & other.b)

	def __xor__(self, other):
		return Color(self.r ^ other.r, self.g ^ other.g, self.b ^ other.b)

	def __or__(self, other):
		return Color(self.r | other.r, self.g | other.g, self.b | other.b)

	def __neg__(self):
		return Color(255-self.r, 255-self.g, 255-self.b)

	def __pos__(self):
		return self

	def __invert__(self):
		return self.__neg__()

	def __int__(self):
		return self.r*256**2 + self.g*256 + self.b

	def __le__(self, other):
		return self.r <= other.r and self.g <= other.g and self.b <= other.b

	def __lt__(self, other):
		return (self.r < other.r or self.g < other.g or self.b < other.b) and self.__le__(other)

	def __ge__(self, other):
		return self.r >= other.r and self.g >= other.g and self.b >= other.b

	def __gt__(self, other):
		return (self.r > other.r or self.g > other.g or self.b > other.b) and self.__ge__(other)

	def complement(self):
		return self.__neg__()

	def rgb(self):
		return self.r, self.g, self.b

	def triad(self):
		return Color(self.g, self.b, self.r), Color(self.b, self.r, self.g)

	def value(self):
		return self.r + self.g + self.b

	# color blends
	def blend(self, other):
		return self @ other

	def cool(self): # shade
		return self @ Color(0, 0, 255)

	def dark(self): # shade
		return self @ Color(0, 0, 0)

	def light(self): # tint
		return self @ Color(255, 255, 255)

	def fade(self): # tone
		return self @ Color(128, 128, 128)

	def warm(self): # shade
		return self @ Color(255, 0, 0)

	# mul by scalar
	def scalar(self, other):
		assert other >= 0
		return Color(int(min(self.r*other, 255)), int(min(self.g*other, 255)), int(min(self.b*other, 255)))

	# blends
	def burn(self, other):
		return ~((~other)/self)

	def darken(self, other):
		return Color(min(self.r, other.r), min(self.g, other.g), min(self.b, other.b))

	def dodge(self, other):
		return other/(~self)

	def lighten(self, other):
		return Color(max(self.r, other.r), max(self.g, other.g), max(self.b, other.b))

	def overlay(self, other): # I AM NOT SURE IF THIS WORKS FINE
		if self.r < 128:
			r = 2*self.r*other.r//255**2
		else:
			r = int((1-2*(1-self.r/255)*(1-other.r/255))*255)
		if self.g < 128:
			g = 2*self.g*other.g//255**2
		else:
			g = int((1-2*(1-self.g/255)*(1-other.g/255))*255)
		if self.b < 128:
			b = 2*self.b*other.b//255**2
		else:
			b = int((1-2*(1-self.b/255)*(1-other.b/255))*255)
		return Color(r, g, b)

	def screen(self, other):
		return ~((~self)*(~other))

	def soft_light(self, other):
		r = int(((1-2*other.r/255)*(self.r/255)**2 + 2*self.r*other.r/255**2)*255)
		g = int(((1-2*other.g/255)*(self.g/255)**2 + 2*self.g*other.g/255**2)*255)
		b = int(((1-2*other.b/255)*(self.b/255)**2 + 2*self.b*other.b/255**2)*255)
		return Color(r, g, b)
