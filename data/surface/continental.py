from math import pi
from random import choice, random, seed
import sys
sys.path.append('./data')
from points import Points
from system import Planet
from color import Color
from constants import m_gg

typecolor = {
	1: ( # hells
		Color(255, 0, 0),
		Color(128, 32, 32)
	),
	0: ( # terras
		Color(0, 128, 255),
		Color(0, 192, 0)
	),
	-1: ( # snowballs
		Color(160, 192, 255),
		Color(255, 255, 255)
	),
	-2: ( # gas giants
		Color(192, 160, 128),
		Color(224, 192, 128)
	)
}

resolution = 12


def r(t: int) -> Color:
	c = choice([typecolor[t][0]]*2+[typecolor[t][1]]) # land or sea?
	# c.r *= random()
	# c.g *= random()
	# c.b *= random()
	return c


def t2c(planet: Planet) -> Color:
	if planet.mass > m_gg:
		return r(-2)
	if planet.temp > 273:
		if planet.temp < 373:
			return r(0)
		return r(1)
	return r(-1)


def main(planet: Planet) -> list:
	seed(planet)
	p = []
	# equator
	for lat in range(-90, 90, resolution):
		for long in range(-180, 180, resolution):
			p.append(((lat*pi/180, long*pi/180), t2c(planet)))
	return Points(p)
