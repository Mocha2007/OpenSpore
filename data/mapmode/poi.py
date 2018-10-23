import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import grey, atmchems, m_earth, m_gg, m_ig, ishab, t_earth

# WARNING this module is super laggy; I get 14 fps from this!!!

poicolors = {
	'Carbon Planet': Color(64, 64, 64),
	'Helium Giant': Color(0, 255, 255),
	'Hot Jupiter': Color(255, 0, 0),
	'Hot Neptune': Color(128, 0, 0),
	'Superhabitable': Color(255, 128, 0)
}


def poi(p: Planet) -> str:
	"""See if planet contains an oddity!"""
	# Superhabitable https://en.wikipedia.org/wiki/Superhabitable_planet
	# "... superhabitable worlds would likely be larger, warmer,
	# and older than Earth, and orbiting K-type main-sequence stars."
	if p.mass > m_earth and p.temp > t_earth and ishab(p):
		return 'Superhabitable'
	# Hot Jupiter/Neptune
	if p.mass > m_gg and p.temp > t_earth:
		if p.mass > m_ig:
			return 'Hot Jupiter'
		return 'Hot Neptune'
	# Carbon Planet
	if p.mass < m_gg:
		carbon = sum(map(lambda x: x[1], filter(lambda x: 'C' in x[0], p.atmosphere.items())))
		oxygen = sum(map(lambda x: x[1], filter(lambda x: 'O' in x[0], p.atmosphere.items())))
		if carbon > oxygen:
				return 'Carbon Planet'
	# Helium Giant
	atm = atmchems(p)
	if 'He' in atm:
		if max(p.atmosphere.items(), key=lambda x: x[1]) == 'He':
			return 'Helium Giant'
	return ''


def main(system: System) -> Color:
	for _, p in system.bodies:
		pp = poi(p)
		if pp:
			return poicolors[pp]
	return grey


def planet(p: Planet) -> Color:
	p = poi(p)
	return poicolors[p] if p else grey
