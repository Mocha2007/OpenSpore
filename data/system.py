from random import random, randint, uniform
from math import exp, log
from constants import m2r, temp2, m_earth, m_browndwarf, m_gg, m_j, m_rock, r_j, r_sun, t_sun
from constants import atmchems, c_e, c_j # for atm


def atm(p) -> dict:
	chems = atmchems(p)
	a = {}
	totalfraction = 0
	for chem in chems:
		if p.mass > m_gg:
			if chem in c_j:
				a[chem] = c_j[chem]
				totalfraction += c_j[chem]
		elif chem in c_e: # must be terran
			a[chem] = c_e[chem]
			totalfraction += c_e[chem]
	# normalize based on totalfraction
	for chem in a:
		a[chem] /= totalfraction
	return a


def pmass() -> float:
	return exp(log(m_browndwarf/m_rock)*random()) * m_rock


class Moon:
	def __init__(self, planet, system, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = 1e24
		while attempt > 1.4819e23:
			attempt = 3.7493e19 / random()
		self.mass = attempt
		self.radius = m2r(attempt, 3.5e3) # rocky density
		self.name = moonnamegen()
		self.resources = []
		self.sma = 1 # todo
		self.temp = planet.temp
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)


class Planet: # no type annotation since function can't be annotated
	def __init__(self, system, sma: float, planetnamegen, moonnamegen, resourcegen):
		self.mass = pmass()
		# radius
		if self.mass > m_gg:
			self.radius = m2r(self.mass, uniform(687, 1326)) # gassy density
		else:
			self.radius = m2r(self.mass, uniform(3933.5, 5427)) # rocky density
		if r_j < self.radius:
			self.radius = r_j * uniform(.99, 1.01)
		# pressure
		self.sma = sma
		self.temp = temp2(system.star, self)
		self.atmosphere = atm(self)
		if self.atmosphere and self.mass < m_gg:
			self.atm = self.mass ** uniform(.11, .29) # min gas log ratio is mars, max venus
			# to calculate more, use log(P)/log(M) to get a ratio
		else:
			self.atm = None
		self.name = planetnamegen()
		self.period = (sma**3/system.star.mass)**.5
		contents = []
		maxmoons = max(0, int((self.mass/m_earth)**.7)) # not perfect, but certainly more realistic than before!
		for i in range(randint(maxmoons//2, maxmoons)):
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
		sma = (star.temperature/t_sun)**2 * star.radius/r_sun / 5 # 3 too low
		for i in range(randint(1, 9)):
			sma *= uniform(1.38, 2.02)  # e/v u/s
			contents.append((i, Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
