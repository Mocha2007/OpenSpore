from constants import t_sun, r_sun, m_sun
from time import time


class Star:
	def __init__(self, mass: float, name: str):
		self.mass = mass
		if mass > .45:
			self.luminosity = 1.148*mass**3.4751
		else:
			self.luminosity = .2264*mass**2.52
		self.radius = r_sun*mass**0.96
		self.temperature = t_sun*mass**.54
		self.lifespan = 3.97310184e17*mass**-2.5162
		# class
		if mass < .45:
			self.type = 'M'
		elif mass < .8:
			self.type = 'K'
		elif mass < 1.04:
			self.type = 'G'
		elif mass < 1.4:
			self.type = 'F'
		elif mass < 2.1:
			self.type = 'A'
		elif mass < 16:
			self.type = 'B'
		else:
			self.type = 'O'
		self.name = name
		self.id = time()
		self.mass *= m_sun
