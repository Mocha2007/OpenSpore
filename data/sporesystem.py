from random import random, randint
from system import Moon


class Planet:
	def __init__(self, planetnamegen, moonnamegen): # no type annotation since function can't be annotated
		attempt = 1e28
		while attempt > 1.8982e27:
			attempt = 3.3011e23 / random()
		self.mass = attempt
		self.name = planetnamegen()
		contents = []
		if self.mass > 6e25: # gas giant; 60% chance of moon
			if random() < .6:
				contents.append((1, Moon(lambda: moonnamegen(self.name, 1))))
		elif random() < .01: # 1% chance terrestrial has moon
				contents.append((1, Moon(lambda: moonnamegen(self.name, 1))))
		self.bodies = contents


class System:
	def __init__(self, star, planetnamegen, moonnamegen): # no type annotation since function can't be annotated
		self.name = star.name
		contents = []
		for i in range(randint(1, 5)):
			contents.append((i, Planet(lambda: planetnamegen(star.name, i), moonnamegen)))
		self.bodies = contents
		self.star = star
