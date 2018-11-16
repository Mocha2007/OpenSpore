from random import random
from math import log
from resource import Resource
sys.path.append('./name')
from benis import main as name
# Empire Class
# 	-> npc: bool
# 	-> cash: int
# 	-> inv: list of tuples of (item: Resource, count: int)
#
# Empires will have a 50% chance of generating on world with biodiversity 6


class Civ:
	def __init__(self, npc: bool, planet):
		self.npc = npc
		self.cash = 1e5
		self.inv = {} # (Resource, count)
		self.id = planet.orbit.primary.id
		self.name = name()

	def __add__(self, other):
		assert type(other) in (float, int, Resource)
		if type(other) == Resource:
			if other in self.inv:
				self.inv[other] += 1
			else:
				self.inv[other] = 1
		else:
			self.cash -= other
		return self

	def __sub__(self, other):
		assert type(other) in (float, int, Resource)
		if type(other) == Resource:
			self.inv[other] -= 1
		else:
			assert other <= self.cash
			self.cash -= other
		return self

	def toggle_control(self):
		self.npc = not self.npc
		return self


def civgen(p):
	# p of type Planet
	if len(p.life) < 18:
		return None
	if True or .5 ** log(len(p.life), 6) < random():
		return Civ(True, p)
	return None
