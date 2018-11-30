from random import choice, randint, random, seed
from math import log
from resource import Resource
from color import Color
import sys
sys.path.append('./data/name')
from civnamegen import main as name
# Empire Class
# 	-> npc: bool
# 	-> cash: int
# 	-> inv: list of tuples of (item: Resource, count: int)
#
# Empires will have a 50% chance of generating on world with biodiversity 6
goal_list = (
	'$',
	'colony',
	'resource',
	'war'
)


def r_goal() -> str:
	return choice(goal_list)


class Civ:
	def __init__(self, npc: bool, planet):
		self.npc = npc
		self.cash = 1e5
		self.cash_hist = []
		self.inv = {} # Resource -> count (int)
		self.inv_hist = [] # list of invs
		self.id = planet.orbit.primary.id
		self.home = planet # original homeworld
		self.name = name()
		seed(self.id)
		self.color = Color(0, randint(64, 255), randint(64, 255))
		self.goal = r_goal() # AI's current project
		self.diplo = {} # civ.id (float) -> state (str)

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

	def delta(self, resource: Resource, indices_ago: int) -> float:
		try:
			now = self.inv[resource]
		except KeyError:
			now = 0
		try:
			then = self.inv_hist[-indices_ago][resource]
		except KeyError:
			then = 0
		return now - then

	def cashflow(self, indices_ago: int) -> float:
		now = self.cash
		try:
			then = self.cash_hist[-indices_ago]
		except KeyError:
			then = 0
		return now - then

	def value(self) -> float:
		return sum([resource.value*quantity for resource, quantity in self.inv.items()])

	def refresh_goal(self):
		self.goal = r_goal()
		return self

	def update_hist(self):
		self.cash_hist.append(self.cash)
		self.inv_hist.append(self.inv)
		# trim histories for mem
		self.cash_hist = self.cash_hist[-100:]
		self.inv_hist = self.inv_hist[-100:]
		return self


def civgen(p):
	# p of type Planet
	if len(p.life) < 18:
		return None
	if True or .5 ** log(len(p.life), 6) < random():
		return Civ(True, p)
	return None
