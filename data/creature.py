from random import choice, random, seed
from json import load

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
		self.name = name
		if 'plural' in kwargs:
			self.plural = kwargs['plural']
		else:
			self.plural = name+'s'
		# requirements
		if 'requires' in kwargs:
			self.requires = set(kwargs['requires'])
		else:
			self.requires = set()
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
		return 'Part("'+self.name+'", **'+str(self.kwargs)+')'

	def __str__(self) -> str:
		return self.__repr__()


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
			self.tags = set(kwargs['tags'])
		else:
			self.tags = set()

	def __repr__(self) -> str:
		return 'Creature("'+self.name+'", **'+str(self.kwargs)+')'

	def __str__(self) -> str:
		return self.__repr__()

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


parts = [Part(i[0], **i[1]) for i in parts_json.items()]
# [print(i) for i in parts] # debug

vital = {list(filter(lambda x: 'root' in x.tags, parts))[0]: 1}


def creature_gen(creature_id: float, **kwargs) -> Creature:
	seed(creature_id)
	name = str(creature_id)
	if 'tags' in kwargs:
		o = Creature(name, parts=vital, tags=kwargs['tags'])
	else:
		o = Creature(name, parts=vital)
	# add parts
	checked = set([i.name for i in vital])
	while checked != set([i.name for i in parts]):
		for part in parts:
			if part.name in checked: # no dupes!
				continue
			# check prereqs
			all_are_checked = True
			for prereq in part.requires: # if ANY prereq is unchecked
				if prereq not in checked:
					all_are_checked = False
					break
			if all_are_checked:
				checked.add(part.name)
			else:
				continue
			if not part.requires <= set([i.name for i in o.parts.keys()]):
				continue
			# check if rngesus loves you
			if random() < part.weight:
				o.parts[part] = choice(part.range)
	# check prereqs
	print(o.parts)
	for part in o.parts:
		# check prereqs
		if not part.requires < set([part.name for part in o.parts]):
			del o.parts[part]
	# todo add tags (feature not implemented yet)
	return o
