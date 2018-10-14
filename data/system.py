from random import random, randint
from constants import m2r, temp2


class Moon:
	def __init__(self, planet, system, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = 1e24
		while attempt > 1.4819e23:
			attempt = 3.7493e19 / random()
		self.mass = attempt
		self.radius = m2r(attempt, 4e3) # rocky density
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
		attempt = 1e29
		while attempt > 1.8982e27*13:
			attempt = 3.3011e23 / random()**3
		self.mass = attempt
		self.radius = m2r(attempt, 4e3) # rocky density
		self.name = planetnamegen()
		self.sma = sma
		self.temp = temp2(system.star, self)
		contents = []
		for i in range(randint(0, 1)):
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
		for i in range(randint(0, 9)):
			sma = 2**i * star.mass**2 / 3 # todo
			contents.append((i, Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
