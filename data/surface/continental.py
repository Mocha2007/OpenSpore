from math import cos, pi
from random import choice, randint, seed
import sys
sys.path.append('./data')
from points import Points
from system import Planet
from color import Color
from constants import m_gg, m_ig, statemap, chemstate, water, ishab
from toxic import istox

typecolor = {
	2: ( # RESERVED - used by other modules
		Color(64, 64, 64),
		Color(192, 192, 192)
	),
	1: ( # hells
		Color(128, 0, 0),
		Color(255, 32, 32)
	),
	0.5: ( # deserts
		Color(123, 94, 77),
		Color(252, 123, 93)
	),
	0.1: ( # toxics
		Color(80, 96, 64),
		Color(160, 176, 80)
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


def gettype(p: Planet) -> float:
	if not p.atmosphere:
		return 2
	if p.mass > m_gg:
		if p.mass < m_ig:
			return -3
		return -2
	state = statemap[chemstate(water, p)]
	if ishab(p):
		return .1 if istox(p) else 0
	if state == 1:
		return .5
	if state == 0:
		return -1
	return 1


def r(t: float, ratio: (int, int)) -> Color:
	c = choice([typecolor[t][0]]*(ratio[0]*len(typecolor[t])) +
				list(typecolor[t][1:])*(ratio[1]*len(typecolor[t]))) # sea, land
	return c


def r2(t: float) -> Color:
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


def t2c(planet: Planet, ratio: (int, int)) -> Color:
	t = gettype(planet)
	if t not in (0,):
		return r2(t)
	return r(t, ratio)


def main(planet: Planet) -> list:
	seed(planet)
	p = []
	# equator
	ratio = randint(1, 5), randint(1, 5) # water % must be >20% for water cycle
	for i in range(resolution):
		lat = i/resolution * pi - pi/2
		dots = int(cos(lat) * resolution) # reduce res around poles
		if dots < 1:
			continue
		for j in range(dots):
			long = j/dots * 2*pi
			p.append(((long, lat), t2c(planet, ratio)))
	return Points(p)
