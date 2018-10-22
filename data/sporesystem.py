from random import random, randint, uniform
from system import Moon
from constants import m2r, temp2, m_gg, m_j, m_rock, r_j


class Planet:
	def __init__(self, system, sma: float, planetnamegen, moonnamegen, resourcegen):
		attempt = 1e29
		while attempt > m_j*13:
			attempt = m_rock / random()**3
		self.mass = attempt
		# radius
		if attempt > m_gg:
			self.radius = m2r(attempt, uniform(687, 1326)) # gassy density
		else:
			self.radius = m2r(attempt, uniform(3933.5, 5427)) # rocky density
		if r_j < self.radius:
			self.radius = r_j * uniform(.99, 1.01)
		# pressure
		if m_airless < attempt < m_gg:
			self.atm = attempt ** uniform(.11, .29) # min gas log ratio is mars, max venus
			# to calculate more, use log(P)/log(M) to get a ratio
		else:
			self.atm = None
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
		sma = star.mass**2 / 3
		for i in range(randint(1, 5)):
			sma *= uniform(1.38, 2.02)  # e/v u/s
			contents.append((i, Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)))
		self.bodies = contents
