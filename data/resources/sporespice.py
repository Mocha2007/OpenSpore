from random import choice
import sys
sys.path.append('./data')
from resource import Resource
from constants import m_gg, water
from color import Color

redspice = Resource({
	'name': 'Red Spice',
	'color': Color(255, 0, 0),
	'value': 281
})
yellowspice = Resource({
	'name': 'Yellow Spice',
	'color': Color(255, 255, 0),
	'value': 375
})
bluespice = Resource({
	'name': 'Blue Spice',
	'color': Color(0, 0, 255),
	'value': 436
})
greenspice = Resource({
	'name': 'Green Spice',
	'color': Color(0, 255, 0),
	'value': 843
})
pinkspice = Resource({
	'name': 'Pink Spice',
	'color': Color(255, 128, 128),
	'value': 936
})
purplespice = Resource({
	'name': 'Purple Spice',
	'color': Color(128, 0, 128),
	'value': 1218
})


def main(**data):
	if data['body'].mass > m_gg:
		return []
	t = data['system'].star.type
	# h = spore_ishab(data['body'], data['system'].star)
	h = water.melt < data['body'].temp < water.boil
	if t in ('WR', 'O', 'B', 'A'):
		if h:
			return [bluespice]
		return [choice([bluespice]*20 + [greenspice]*30 + [pinkspice]*35 + [purplespice]*15)]
	if t in 'KGF':
		if h:
			return [choice([yellowspice]*94 + [greenspice]*2 + [pinkspice]*2 + [purplespice]*2)]
		return [choice([yellowspice]*74 + [greenspice]*22 + [pinkspice]*2 + [purplespice]*2)]
	# else M-
	if h:
		return [choice([redspice]*96 + [bluespice]*2 + [pinkspice]*2)]
	return [choice([redspice]*50 + [yellowspice]*44 + [greenspice]*2 + [pinkspice]*2 + [purplespice]*2)]
