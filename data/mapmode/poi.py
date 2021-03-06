import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import grey, m_earth, m_gg, m_ig, m_j, ishab, t_earth
from toxic import istox
sys.path.append('./data/surface')
from continental import typecolor

# WARNING this module is super laggy; I get 14 fps from this!!!

poicolors = {
	'Carbon Planet': Color(64, 32, 64),
	'Helium Planet': Color(0, 255, 255),
	'Hot Jupiter': Color(255, 0, 0),
	'Hot Neptune': Color(128, 0, 0),
	'Mesoplanet': Color(255, 192, 192),
	'Mini-Neptune': Color(192, 128, 255),
	'Superhabitable': Color(255, 128, 0),
	'Super-Jupiter': Color(255, 224, 192),
	'Toxic': typecolor[.1][0].blend(typecolor[.1][1])
}


def poi(p: Planet) -> str:
	"""See if planet contains an oddity!"""
	# Gas giants
	if m_gg < p.mass:
		# Hot Jupiter/Neptune
		if t_earth < p.temp:
			if p.mass > m_ig:
				return 'Hot Jupiter'
			return 'Hot Neptune'
		# Mini-Neptune
		if p.mass < 8.681e25:
			return 'Mini-Neptune'
		# Super-Jupiter
		if m_j < p.mass:
			return 'Super-Jupiter'
		return ''
	# otherwise, MUST be terrestrial
	# Helium Planet
	atm = p.atmosphere
	if 'He' in atm and m_earth < p.mass:
		if max(p.atmosphere.items(), key=lambda x: x[1])[0] == 'He':
			return 'Helium Planet'
	# "Habitables"
	if ishab(p):
		# Superhabitable https://en.wikipedia.org/wiki/Superhabitable_planet
		# "... superhabitable worlds would likely be larger, warmer,
		# and older than Earth, and orbiting K-type main-sequence stars."
		if p.mass > m_earth and p.temp > t_earth:
			return 'Superhabitable'
		# Toxics
		if istox(p):
			return 'Toxic'
	# Mesoplanet
	if p.mass < 3.3011e23:
		return 'Mesoplanet'
	return ''
	# the following are currently impossible and thus temporarily blocked for performance
	# Carbon Planet
	# if p.mass < m_gg:
	# 	carbon = sum(map(lambda x: x[1], filter(lambda x: 'C' in x[0], p.atmosphere.items())))
	# 	oxygen = sum(map(lambda x: x[1], filter(lambda x: 'O' in x[0], p.atmosphere.items())))
	# 	if carbon > oxygen:
	# 			return 'Carbon Planet'
	# return ''


def main(system: System) -> Color:
	for _, p in system.bodies:
		pp = poi(p)
		if pp:
			return poicolors[pp]
	return grey


def planet(p: Planet) -> Color:
	p = poi(p)
	return poicolors[p] if p else grey
