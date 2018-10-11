from random import random, randint
from system import Moon
from constants import temp2


class Planet:
	def __init__(self, system, planetnamegen, moonnamegen, resourcegen):
		attempt = 1e28
		while attempt > 1.8982e27:
			attempt = 3.3011e23 / random()
		self.mass = attempt
		self.name = planetnamegen()
		self.sma = 1 # todo
		self.temp = temp2(system.star, self)
		contents = []
		hasmoon = False
		if self.mass > 6e25: # gas giant; 60% chance of moon
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
			contents.append((i, Planet(self, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
