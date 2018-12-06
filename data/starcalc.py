from constants import t_sun, r_sun, m_sun, m_star, m_j
from time import time
from system import pradius


def getclass(mass: float) -> str:
	if mass < m_star/m_sun: # Brown Dwarfs
		if mass < 30 * m_j/m_sun: # forgot; but less than 2MASS 1237+6526
			return 'Y'
		if mass < 57 * m_j/m_sun:
			# between 62.1 m_j (LHS 6343 C) and 75 m_j (SDSS J1416+1348 A)
			# ... but based on a better database I found the limit appears to be around 57
			return 'T'
		return 'L'
	if mass < .45:
		return 'M'
	if mass < .8:
		return 'K'
	if mass < 1.04:
		return 'G'
	if mass < 1.4:
		return 'F'
	if mass < 2.1:
		return 'A'
	if mass < 16:
		return 'B'
	if mass < 100: # approximation - ~half of stars above this are WR
		return 'O'
	return 'WR'


class Star:
	def __init__(self, mass: float, namegen):
		# name is a function
		self.mass = mass
		if mass > .45:
			self.luminosity = 1.148*mass**3.4751
		else:
			self.luminosity = .2264*mass**2.52
		# class
		self.type = getclass(mass)
		if self.type in 'LTY':
			self.radius = pradius(mass*m_sun)
		else:
			self.radius = r_sun*mass**0.96
		self.temperature = t_sun*mass**.54
		self.lifespan = 3.97310184e17*mass**-2.5162
		self.id = time()
		self.mass *= m_sun
		self.name = namegen(self)
