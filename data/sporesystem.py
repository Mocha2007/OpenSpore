from random import random, randint
from system import Moon


class Planet:
	def __init__(self, system, planetnamegen, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = 1e28
		while attempt > 1.8982e27:
			attempt = 3.3011e23 / random()
		self.mass = attempt
		self.name = planetnamegen()
		contents = []
		if self.mass > 6e25: # gas giant; 60% chance of moon
			if random() < .6:
				contents.append((1, Moon(system, lambda: moonnamegen(self.name, 1), resourcegen)))
		elif random() < .01: # 1% chance terrestrial has moon
				contents.append((1, Moon(system, lambda: moonnamegen(self.name, 1), resourcegen)))
		self.bodies = contents
		self.sma = 1 # todo
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)


class System:
	def __init__(self, star, planetnamegen, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		self.name = star.name
		self.star = star
		contents = []
		for i in range(randint(1, 5)):
			contents.append((i, Planet(self, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
