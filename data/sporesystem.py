from random import random, randint, uniform
from system import Moon, atm, pmass, pradius
from constants import au, m2r, temp2, m_gg, m_j, m_rock, r_j, t_sun, r_sun, planet_form_time
from orbit import rporbit
from life import lifegen
from civ import civgen


class Planet:
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
		self.period = (sma**3/system.star.mass)**.5
		contents = []
		hasmoon = False
		if self.mass > m_gg: # gas giant; 60% chance of moon
			if random() < .6:
				hasmoon = True
		elif random() < .01: # 1% chance terrestrial has moon
				hasmoon = True
		if hasmoon:
			contents.append((1, Moon(self, system, lambda: moonnamegen(self.name, 1), resourcegen)))
		self.bodies = contents
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)
		self.life = lifegen(self)
		self.civ = civgen(self)


class System:
	def __init__(self, star, planetnamegen, moonnamegen, resourcegen):
		self.name = star.name
		self.star = star
		# too young to form planets?
		if star.lifespan < planet_form_time:
			self.bodies = []
		else:
			contents = []
			sma = au * (star.temperature/t_sun)**2 * star.radius/r_sun / 5 # 3 too low
			limit = star.radius * 4.5 # WD 1202-024 B (est.)
			while sma < limit:
				sma *= 2
			for i in range(randint(1, 5)):
				attempt = Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)
				contents.append((i, attempt))
				sma *= uniform(1.38, 2.02)  # e/v u/s
			self.bodies = contents
