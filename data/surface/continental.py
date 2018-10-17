from math import cos, pi
from random import choice, randint, seed
import sys
sys.path.append('./data')
from points import Points
from system import Planet
from color import Color
from constants import m_airless, m_gg, m_ig, water

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
	),
	-3: ( # ice giants
		Color(64, 64, 160),
		Color(144, 192, 192)
	)
}

resolution = 30


def r(t: int) -> Color:
	c = choice([typecolor[t][0]]*(2*len(typecolor[t]))+list(typecolor[t][1:])) # land or sea?
	return c


def r2(t: int) -> Color:
	c = Color(0, 0, 0)
	if t == 2: # rock
		v = randint(64, 192)
		c.r, c.g, c.b = v, v, v
	else: # use typecolor
		c1, c2 = typecolor[t]
		c.r = randint(c1.r, c2.r)
		c.g = randint(c1.g, c2.g)
		c.b = randint(c1.b, c2.b)
	return c


def t2c(planet: Planet) -> Color:
	if planet.mass < m_airless:
		return r2(2)
	if planet.mass > m_gg:
		if planet.mass < m_ig:
			return r2(-3)
		return r2(-2)
	if planet.temp > water.melt:
		if planet.temp < water.boil:
			return r(0)
		return r(1)
	return r(-1)


def main(planet: Planet) -> list:
	seed(planet)
	p = []
	# equator
	for i in range(resolution):
		lat = i/resolution * pi - pi/2
		dots = int(cos(lat) * resolution) # reduce res around poles
		if dots < 1:
			continue
		for j in range(dots):
			long = j/dots * 2*pi
			p.append(((long, lat), t2c(planet)))
	return Points(p)
