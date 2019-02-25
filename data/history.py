from json import load
from random import choice, random, seed
from constants import earth_age # , format_year

events_json = load(open('data/history.json', encoding="utf-8"))


class Event:
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		# props; notes ignored
		self.name = kwargs['name']
		self.frequency = kwargs['frequency']
		# optional args
		self.desc = kwargs['desc'] if 'desc' in kwargs else ''
		self.requires = set(kwargs['requires']) if 'requires' in kwargs else set()
		self.types = kwargs['types'] if 'types' in kwargs else {}
		self.tags = set(kwargs['tags']) if 'tags' in kwargs else set()
		# detect limits
		self.limit = None
		for tag in self.tags:
			if tag[:5].lower() == 'limit':
				self.limit = int(tag.split()[1])
				break

	def __repr__(self) -> str:
		return 'Event(**'+str(self.kwargs)+')'

	def is_requirement(self) -> bool:
		for tag in self.tags:
			if tag[:12].lower() == 'required_for':
				return True
		return False


class EventInstance:
	def __init__(self, event: Event, event_type: str):
		self.event = event
		self.type = event_type


events = {i: [Event(**k) for k in j] for i, j in events_json.items()}
# print(events) # debug

# a history is a DICT of int(time) -> Event.
resolution = 10**13 # ~300 ky


def construct_types(types: dict) -> list:
	o = []
	for i, j in types.items():
		o += [i]*j
	return o


def frequency_to_probability(frequency: float) -> float:
	assert 0 <= frequency # so output always in (0, 1]
	return 1 - .5**(frequency * resolution / earth_age)


def history_gen(planet, **kwargs) -> dict:
	"""
	:param planet: Planet object
	:param kwargs: optional civ=Civ for filter
	:return: a "history" (dict mapping int to Event)
	"""
	seed(planet)
	if 'civ' in kwargs:
		requirements = {'required_for_civ', 'required_for_life'}
		if kwargs['civ'].creature.constants['sexes']:
			requirements.add('required_for_sex')
	elif planet.life: # if it has life
		requirements = {'required_for_life'}
	else:
		requirements = set()
	# check failures
	if 'fails' not in kwargs:
		kwargs['fails'] = 0
	bonus = 2**kwargs['fails']
	# now the bigboi
	history = {0: EventInstance(events['_'][1], '')}
	collected_tags = set()
	age = int(planet.orbit.primary.age)
	for sim_time in range(1, age, resolution):
		for category, cat_events in events.items():
			if category == '_':
				continue
			for event in cat_events:
				# limit tag? this tag will disable the event until the last event.limit*mtth of the planet's history
				if event.limit and event.limit * earth_age / event.frequency < age - sim_time:
					continue
				# one time only set?
				if 'one_time_event' in event.tags and event in map(lambda x: x.event, set(history.values())):
					continue
				# prereq set?
				if not event.requires <= set([i.event.name for i in history.values()]):
					continue
				# then check event
				this_bonus = bonus if event.is_requirement() else 1
				if random()/this_bonus < frequency_to_probability(event.frequency):
					# add event
					if event.types:
						event_type = choice(construct_types(event.types))
					else:
						event_type = ''
					history[sim_time] = EventInstance(event, event_type)
					collected_tags = collected_tags.union(event.tags)
	history[age] = EventInstance(events['_'][2], '')
	# all parameters satisfied?
	if requirements <= collected_tags:
		# print('succ')
		return history
	# else, restart
	# print('fail x'+str(kwargs['fails']), format_year(age), requirements-collected_tags) # debug
	kwargs['fails'] += 1
	return history_gen(planet, **kwargs)
