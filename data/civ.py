from random import choice, randint, random, seed, shuffle, uniform
from constants import log_uniform, rbool
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
# constants for description generator
size_range = 1, 6.5 # dwarf <> elephant, in meters cf. chips, humans at 1.2 1.7
sleep_range = .08, .83 # horses, bats
textures = (
	# name, is plural?
	('fur', False),
	('feathers', True),
	('husk', False),
	('scales', True),
	('shell', False),
	('skin', False),
	('membrane', False),
)
values = (
	# min, max
	('independence', 'cooperation'),
	('simplicity', 'elegance'),
	('chaos', 'harmony'),
	('ignorance', 'knowledge'),
	('disloyalty', 'loyalty'),
	('chastity', 'romance'),
)
feels = (
	('soft', 'hard'),
	('sticky', 'oily'),
	('smooth', 'rough'),
	('dry', 'wet'),
)
colors = (
	'black',
	'blue',
	'brown',
	'cyan',
	'green',
	'grey',
	'orange',
	'pink',
	'purple',
	'red',
	'silver',
	'tan',
	'white',
	'yellow',
)
wing_adj = (
	'elegant',
	'flowing',
	'frightening',
	'graceful',
	'large',
)


def r_adj(adj_list, minimum: int, maximum: int) -> str:
	palette = list(adj_list)
	shuffle(palette)
	chosen = []
	limit = randint(minimum, maximum)
	for i in range(limit):
		if 1 < limit == i+1:
			if limit == 2:
				chosen[0] += ' and '+palette.pop()
			else:
				chosen.append('and '+palette.pop())
		else:
			chosen.append(palette.pop())
	return ', '.join(chosen)


def r_polar_adj(adj_list, minimum: int, maximum: int) -> str:
	palette = list(adj_list)
	shuffle(palette)
	chosen = []
	limit = randint(minimum, maximum)
	for i in range(limit):
		if 1 < limit == i+1:
			if limit == 2:
				chosen[0] += ' and '+choice(palette.pop())
			else:
				chosen.append('and '+choice(palette.pop()))
		else:
			chosen.append(choice(palette.pop()))
	return ', '.join(chosen)


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
		print(self.description())

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
		seed(self.id)
		# species size in m and kg
		size = log_uniform(*size_range)
		mass = uniform(18, 29) * size**3
		# sexual dimorphism?
		sexes = rbool()
		dimorphic = sexes and rbool()
		# Dinural? Nocturnal?
		activity = choice(['dinural', 'nocturnal', 'crepuscular'])
		sleep = uniform(*sleep_range)
		# appearance
		material_texture = r_polar_adj(feels, 1, 3)
		texture, texture_number = choice(textures)
		color = r_adj(colors, 1, 3)
		winged = rbool(.2)
		# todo Civ Philosophical Values
		pro, con = choice(values)[::choice([1, -1])]
		# compose
		describe = [self.name,
		'Their species has a size of {size} m and a mass of {mass} kg.'.format(mass=round(mass), size=round(size, 2))]
		if sexes:
			if dimorphic:
				describe.append('The species is sexually dimorphic.')
			else:
				describe.append('The species is divided into two virtually identical sexes.')
		else:
			describe.append('The species is asexual.')
		describe.append('Their sleep activity is '+activity+', and they sleep for '+str(round(sleep*100))+'% of the local day.')
		describe.append('Their '+material_texture+' '+texture+(' are ' if texture_number else ' is ')+color+'.')
		if winged:
			describe.append('Their wings are '+r_adj(wing_adj, 1, 3)+'.')
		# todo philo
		describe.append('They value '+pro+' above all else, and despise '+con+'.')
		return '\n\t'.join(describe)


def civgen(p):
	# p of type Planet
	if len(p.life) < 18:
		return None
	if True or .5 ** log(len(p.life), 6) < random():
		return Civ(True, p)
	return None
