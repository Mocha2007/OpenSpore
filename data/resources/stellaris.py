from random import choice, random
import sys
sys.path.append('./data')
from resource import Resource
from constants import chemstate, m_gg, water
from color import Color
from toxic import istox

frequency = .01

aldar = Resource({
	'name': 'Aldar Crystals',
	'color': Color(156, 34, 198),
	'value': 1
})
engos = Resource({
	'name': 'Engos Vapor',
	'color': Color(2, 122, 46),
	'value': 1
})
lythuric = Resource({
	'name': 'Lythuric Gases',
	'color': Color(108, 124, 169),
	'value': 1
})
pitharian = Resource({
	'name': 'Pitharian Dust',
	'color': Color(216, 85, 3),
	'value': 1
})
satramene = Resource({
	'name': 'Satramene Gas',
	'color': Color(156, 37, 117),
	'value': 1
})
teldar = Resource({
	'name': 'Teldar Crystals',
	'color': Color(179, 101, 40),
	'value': 1
})
terraformingg = Resource({
	'name': 'Terraforming Gases',
	'color': Color(43, 172, 149),
	'value': 1
})
terraformingl = Resource({
	'name': 'Terraforming Liquids',
	'color': Color(40, 148, 108),
	'value': 1
})
yurantic = Resource({
	'name': 'Yurantic Crystals',
	'color': Color(32, 161, 219),
	'value': 1
})
zro = Resource({
	'name': 'Zro Dust',
	'color': Color(16, 83, 164),
	'value': 1
})


def main(**data) -> list:
	if data['body'].mass > m_gg:
		if random() < frequency:
			return [choice([engos, lythuric, satramene, terraformingg])]
	elif istox(data['body']):
		if random() < frequency:
			return [choice([pitharian, zro])]
	elif chemstate(water, data['body']) == 'solid':
		if random() < frequency:
			return [choice([aldar, teldar, terraformingl, yurantic])]
	return []
