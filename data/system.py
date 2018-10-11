from random import random, randint


class Moon:
	def __init__(self, system, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = 1e24
		while attempt > 1.4819e23:
			attempt = 3.7493e19 / random()
		self.mass = attempt
		self.name = moonnamegen()
		self.resources = []
		self.sma = 1 # todo
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)


class Planet:
	def __init__(self, system, planetnamegen, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = 1e28
		while attempt > 1.8982e27:
			attempt = 3.3011e23 / random()
		self.mass = attempt
		self.name = planetnamegen()
		contents = []
		for i in range(randint(0, 1)):
			contents.append((i, Moon(system, lambda: moonnamegen(self.name, i), resourcegen)))
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
		for i in range(randint(0, 9)):
			contents.append((i, Planet(self, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
