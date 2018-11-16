from random import random
from math import log
# Empire Class
# 	-> npc: bool
# 	-> cash: int
# 	-> inv: list of tuples of (item: Resource, count: int)
#
# Empires will have a 50% chance of generating on world with biodiversity 6


class Civ:
	def __init__(self, npc: bool):
		self.npc = npc
		self.cash = 1e5
		self.inv = [] # (Resource, count)

	def toggle_control(self):
		self.npc = not self.npc


def civgen(p):
	# p of type Planet
	if len(p.life) < 18:
		return None
	if True or .5 ** log(len(p.life), 6) < random():
		return Civ(True)
	return None
