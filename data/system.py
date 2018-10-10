from random import random, randint


class Moon:
	def __init__(self, moonnamegen): # no type annotation since function can't be annotated
		attempt = 1e24
		while attempt > 1.4819e23:
			attempt = 3.7493e19 / random()
		self.mass = attempt
		self.name = moonnamegen()


class Planet:
	def __init__(self, planetnamegen, moonnamegen): # no type annotation since function can't be annotated
		attempt = 1e28
		while attempt > 1.8982e27:
			attempt = 3.3011e23 / random()
		self.mass = attempt
		self.name = planetnamegen()
		contents = []
		for i in range(randint(0, 1)):
			contents.append((i, Moon(lambda: moonnamegen(self.name, i))))
		self.bodies = contents


class System:
	def __init__(self, star, planetnamegen, moonnamegen): # no type annotation since function can't be annotated
		self.name = star.name
		contents = []
		for i in range(randint(0, 9)):
			contents.append((i, Planet(lambda: planetnamegen(star.name, i), moonnamegen)))
		self.bodies = contents
		self.star = star
