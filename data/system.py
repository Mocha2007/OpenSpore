from random import random, randint, uniform
from math import e, exp, log
from constants import au, m2r, temp2, m_earth, m_browndwarf, m_gg, m_j, m_rock, r_j, r_sun, t_sun, soi, soi_moon
from constants import atmchems, c_e, c_j # for atm
from orbit import rporbit


def chemrange(minimum: float, maximum: float) -> float:
	"""uniform but weighted logarithmically"""
	return e**uniform(log(minimum), log(maximum))


def atm(p) -> dict:
	chems = atmchems(p)
	a = {}
	totalfraction = 0
	for chem in chems:
		if p.mass > m_gg:
			if chem in c_j:
				fraction = chemrange(*c_j[chem])
				a[chem] = fraction
				totalfraction += fraction
		elif chem in c_e: # must be terran
			fraction = chemrange(*c_e[chem])
			a[chem] = fraction
			totalfraction += fraction
	# normalize based on totalfraction
	for chem in a:
		a[chem] /= totalfraction
	return a


def pmass() -> float:
	return exp(log(m_browndwarf/m_rock)*random()) * m_rock


def pradius(m: float) -> float:
	if m > m_gg:
		rho = uniform(687, 1326) # gassy density
	else:
		rho = uniform(3933.5, 5427) # rocky density
	r = m2r(m, rho)
	if r_j < r:
		r = r_j * uniform(.99, 1.01)
	return r


class Moon:
	def __init__(self, planet, system, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = 1e24
		while attempt > 1.4819e23:
			attempt = 3.7493e19 / random()
		self.mass = attempt
		self.radius = m2r(attempt, 3.5e3) # rocky density
		self.name = moonnamegen()
		self.resources = []
		self.sma = rporbit(planet, planet.radius*2) # todo
		self.temp = planet.temp
		self.atm = None # todo
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)


class Planet: # no type annotation since function can't be annotated
	def __init__(self, system, sma: float, planetnamegen, moonnamegen, resourcegen):
		self.mass = pmass()
		# radius
		self.radius = pradius(self.mass)
		# pressure
		self.orbit = rporbit(system.star, sma)
		self.temp = temp2(system.star, self)
		self.atmosphere = atm(self)
		if self.atmosphere and self.mass < m_gg:
			self.atm = self.mass ** uniform(.11, .29) # min gas log ratio is mars, max venus
			# to calculate more, use log(P)/log(M) to get a ratio
		else:
			self.atm = None
		self.name = planetnamegen()
		contents = []
		# GRAVITATIONALLY ROUNDED MOONS ONLY!!!!!
		soi_ = soi(self)
		if soi_moon < soi_:
			maxmoons = round(3.3e-5 * soi_**.5) # not perfect, but certainly more realistic than before!
			for i in range(0, randint(1, maxmoons)):
				contents.append((i, Moon(self, system, lambda: moonnamegen(self.name, i), resourcegen)))
		self.bodies = contents
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)


class System: # no type annotation since function can't be annotated
	def __init__(self, star, planetnamegen, moonnamegen, resourcegen):
		self.name = star.name
		self.star = star
		contents = []
		sma = au * (star.temperature/t_sun)**2 * star.radius/r_sun / 5 # 3 too low
		for i in range(randint(1, 9)):
			sma *= uniform(1.38, 2.02)  # e/v u/s
			contents.append((i, Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
