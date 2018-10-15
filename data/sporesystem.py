from random import random, randint, uniform
from system import Moon
from constants import m2r, temp2, m_gg


class Planet:
	def __init__(self, system, sma: float, planetnamegen, moonnamegen, resourcegen):
		attempt = 1e29
		while attempt > 1.8982e27*13:
			attempt = 3.3011e23 / random()**3
		self.mass = attempt
		if attempt > m_gg:
			self.radius = m2r(attempt, uniform(687, 1326)) # gassy density
		else:
			self.radius = m2r(attempt, uniform(3933.5, 5427)) # rocky density
		self.name = planetnamegen()
		self.sma = sma
		self.temp = temp2(system.star, self)
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


class System:
	def __init__(self, star, planetnamegen, moonnamegen, resourcegen):
		self.name = star.name
		self.star = star
		contents = []
		for i in range(randint(1, 5)):
			sma = 2**i * star.mass**2 / 3 # todo
			contents.append((i, Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
