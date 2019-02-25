from random import choice, randint, random, seed, uniform
from json import load
from constants import log_uniform, r_adj, r_polar_adj, rbool
from word import Noun, Description

parts_json = load(open('data/parts.json', encoding="utf-8"))
"""
stomach [hydra+]
	<- brain [acoelomorpha+]
		<- kidney [nematode+]
			<-? adrenal gland
			<- bladder [crustacea, some chordates+]
			<-? gizzard [some chordates+]
			<- liver [vertebrata+]
				<-? heart [amniote+]
				<- gallbladder [most vertebrates+]
			<- lung [vertebrata+]
			<- pancreas [vertebrates+]
			<- spleen [vertebrates excluding lamprey and hagfishes+]
			<- thyroid [vertebrates+]
				<- parathyroid [tetrapods+]
	<-? intestine
		<- appendix [most Euarchontoglires subset of Mammalia]
"""


class Part:
	def __init__(self, name: str, **kwargs):
		self.kwargs = kwargs
		if 'plural' in kwargs:
			plural = kwargs['plural']
		else:
			plural = name+'s'
		self.noun = Noun(name, plural=plural)
		# requirements
		if 'requires' in kwargs:
			self.requires = set(kwargs['requires'])
		else:
			self.requires = set()
		# exclusions
		if 'exclude' in kwargs:
			self.exclude = set(kwargs['exclude'])
		else:
			self.exclude = set()
		# connected to (if different from requirements)
		if 'connect' in kwargs:
			self.connect = kwargs['connect']
		elif 'requires' in kwargs:
			self.connect = kwargs['requires'][0]
		else:
			self.connect = None
		# plurality
		if 'range' in kwargs:
			range_range = list(kwargs['range'])
			range_range[1] += 1
			r = range_range
		else:
			r = 1, 2
		self.range = range(*r)
		# tags
		if 'tags' in kwargs:
			self.tags = set(kwargs['tags'])
		else:
			self.tags = set()
		# rng weighting
		if 'weight' in kwargs:
			self.weight = kwargs['weight']
		else:
			self.weight = .5

	def __repr__(self) -> str:
		return 'Part("'+self.noun.read()+'", **'+str(self.kwargs)+')'


# constants for description generator
size_range = 1, 6.5 # dwarf <> elephant, in meters cf. chips, humans at 1.2 1.7
sleep_range = .08, .83 # horses, bats
textures = {
	Noun('chitin', countable=False),
	Noun('fur', countable=False),
	Noun('feather', is_plural=True),
	Noun('husk'),
	Noun('membrane'),
	Noun('photophore', is_plural=True),
	Noun('scale', is_plural=True),
	Noun('skin', countable=False),
}
feels = {
	('soft', 'hard'),
	('sticky', 'oily'),
	('smooth', 'rough'),
	('dry', 'wet'),
}
colors = {
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
}


class Material:
	def __init__(self, material_type: Noun, material_textures: set, material_colors: set):
		self.type = material_type
		self.textures = material_textures
		self.colors = material_colors

	def __repr__(self):
		return 'Material('+', '.join(map(str, [self.type, self.textures, self.colors]))+')'

	def add_color(self, color: str):
		self.colors.add(color)
		return self

	def add_texture(self, texture: str):
		self.textures.add(texture)
		return self


class Skin:
	def __init__(self, materials: set):
		self.types = materials

	def __add__(self, other):
		self.types.add(other)
		return self

	def __repr__(self):
		return 'Skin('+str(self.types)+')'


class Creature:
	def __init__(self, name: str, **kwargs):
		self.kwargs = kwargs
		self.name = name
		if 'plural' in kwargs:
			self.plural = kwargs['plural']
		else:
			self.plural = name+'s'
		# parts
		if 'parts' in kwargs:
			self.parts = kwargs['parts']
		else:
			self.parts = {}
		# tags
		if 'tags' in kwargs:
			self.tags = kwargs['tags']
		else:
			self.tags = set()
		# constants
		if 'constants' in kwargs:
			self.constants = kwargs['constants']
		else:
			self.constants = {}
		# skin
		if 'skin' in kwargs:
			self.skin = kwargs['skin']
		else:
			self.skin = Skin(set())

	def __repr__(self) -> str:
		return 'Creature("'+self.name+'", **'+str(self.kwargs)+')'

	def __add__(self, other: Part):
		if other in self.parts:
			self.parts[other] += 1
		else:
			self.parts[other] = 1
		return self

	def list_tags(self) -> set:
		tags = set()
		for part in self.parts:
			if 'root' not in part.tags:
				tags = tags.union(part.tags)
		return tags

	def is_winged(self) -> bool:
		return 'wing' in [part.noun.read() for part in self.parts]

	def description(self) -> str:
		# compile part -> int dict
		part_dict = {i.noun: j for i, j in self.parts.items()}
		# compile set of tuple(tuple, str)
		part_set = set()
		for part, _ in self.parts.items():
			# connections
			if part.connect is not None:
				part_tuple = part.noun, get_part_from_name(part.connect).noun
				part_string = 'The {0} {0_be} connected to the {1}'
				part_set.add((part_tuple, part_string))
			# functions
			if part.tags:
				for tag in part.tags:
					part_tuple = part.noun, Noun(tag)
					part_string = 'The {0} {0_be} involved with {1}'
					part_set.add((part_tuple, part_string))
		return Description(part_dict, part_set)


parts = [Part(i[0], **i[1]) for i in parts_json.items()]
# [print(i) for i in parts] # debug

vital = {list(filter(lambda x: 'root' in x.tags, parts))[0]: 1}


def get_part_from_name(name: str) -> Part:
	for part in parts:
		if part.noun.read() == name:
			return part
	raise KeyError(name)


def creature_gen(creature_id: float, **kwargs) -> Creature:
	seed(creature_id)
	name = str(creature_id)
	if 'tags' in kwargs:
		o = Creature(name, parts=vital, tags=kwargs['tags'])
	else:
		o = Creature(name, parts=vital)
	# add parts
	checked = set([i.noun.read() for i in vital])
	while checked != set([i.noun.read() for i in parts]):
		for part in parts:
			if part.noun.read() in checked: # no dupes!
				continue
			# check prereqs
			all_are_checked = True
			for prereq in part.requires: # if ANY prereq is unchecked
				if prereq not in checked:
					all_are_checked = False
					break
			if all_are_checked:
				checked.add(part.noun.read())
			else:
				continue
			# if prereqs not satisfied
			if not part.requires <= set([i.noun.read() for i in o.parts.keys()]):
				continue
			# if exclusions broken
			if part.exclude and part.exclude <= set([i.noun.read() for i in o.parts.keys()]):
				continue
			# check if rngesus loves you
			if random() < part.weight:
				primary_prereq_count = o.parts[get_part_from_name(part.connect)]
				o.parts[part] = choice(part.range) * primary_prereq_count
	# check prereqs
	for part in o.parts:
		# check prereqs
		if not part.requires <= set([i.noun.read() for i in o.parts.keys()]):
			del o.parts[part]
	# add skin
	for _ in range(randint(1, 2)):
		material_texture = r_polar_adj(feels, 1, 3)
		color = r_adj(colors, 1, 3)
		o.skin += Material(choice(list(textures)), material_texture, color)
	# todo add tags (feature not implemented yet)
	# species size in m and kg
	size = log_uniform(*size_range)
	mass = uniform(18, 29) * size**3
	# sexual dimorphism?
	sexes = rbool(.2)
	dimorphic = sexes and rbool()
	# Dinural? Nocturnal?
	activity = choice(['dinural', 'nocturnal', 'crepuscular'])
	sleep = uniform(*sleep_range)

	o.constants = {
		'size': size,
		'mass': mass,
		'sexes': sexes,
		'dimorphic': dimorphic,
		'activity': activity,
		'sleep': sleep,
	}
	return o
