from random import choice, randint, random, seed
from math import log
from resource import Resource
from color import Color
from creature import creature_gen
from history import history_gen
from constants import format_year
import sys
sys.path.append('./data/name')
from civnamegen import main as name
# Empire Class
# 	-> npc: bool
# 	-> cash: int
# 	-> inv: list of tuples of (item: Resource, count: int)
#
# Empires will have a 50% chance of generating on world with biodiversity 6
goal_list = {
	'$',
	'colony',
	'resource',
	'war'
}
values = {
	# min, max
	('independence', 'cooperation'),
	('simplicity', 'elegance'),
	('chaos', 'harmony'),
	('ignorance', 'knowledge'),
	('disloyalty', 'loyalty'),
	('chastity', 'romance'),
}


def r_goal() -> str:
	return choice(list(goal_list))


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
		self.creature = creature_gen(self.id)
		print(self.description())
		print(self.read_history())

	def __add__(self, other):
		assert type(other) in (float, int, Resource)
		if isinstance(other, Resource):
			if other in self.inv:
				self.inv[other] += 1
			else:
				self.inv[other] = 1
		else:
			self.cash -= other
		return self

	def __sub__(self, other):
		assert type(other) in (float, int, Resource)
		if isinstance(other, Resource):
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
		except IndexError:
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

	def description(self) -> str:
		species = self.creature
		# todo Civ Philosophical Values
		pro, con = choice(list(values))[::choice([1, -1])]
		# compose
		describe = [self.name,
		'Their species has a size of {size} m and a mass of {mass} kg.'.format(
			mass=round(species.constants['mass']), size=round(species.constants['size'], 2))]
		if species.constants['sexes']:
			if species.constants['dimorphic']:
				describe.append('The species is sexually dimorphic.')
			else:
				describe.append('The species is divided into two virtually identical sexes.')
		else:
			describe.append('The species is asexual.')
		describe.append('Their sleep activity is '+species.constants['activity']+', and they sleep for ' +
						str(round(species.constants['sleep']*100))+'% of the local day.')
		# describe.append('Their '+material_texture+' '+texture+(' are ' if texture_number else ' is ')+color+'.')
		if self.creature.is_winged():
			describe.append('They are winged.')
		# todo philo
		describe.append('They value '+pro+' above all else, and despise '+con+'.')
		describe.append('Body Parts: ' +
						', '.join(sorted(list([part.noun.read()+' x'+str(count) for part, count in self.creature.parts.items()]))))
		describe.append('Skin: '+str(self.creature.skin))
		describe.append('Tags: '+str(self.creature.list_tags()))
		describe.append('Description: '+self.creature.description().read())
		return '\n\t'.join(describe)

	def history(self) -> dict:
		return history_gen(self.home, civ=self)

	def read_history(self) -> str:
		o = []
		for date, eventinstance in sorted(self.history().items(), key=lambda x: x[0]):
			event = eventinstance.event
			eventtype = eventinstance.type
			o.append(format_year(date)+': '+event.name)
			if eventtype:
				o.append('\t-> '+eventtype)
		return '\n'.join(o)


def civgen(p):
	# p of type Planet
	if len(p.life) < 18:
		return None
	if True or .5 ** log(len(p.life), 6) < random():
		return Civ(True, p)
	return None
