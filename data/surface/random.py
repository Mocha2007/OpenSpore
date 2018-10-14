from math import pi
from random import randint, seed
import sys
sys.path.append('./data')
from points import Points
from color import Color

resolution = 12

rr = lambda: randint(0, 128)
rg = lambda: randint(128, 192)
rb = lambda: randint(128, 192)


def main(planet):
	seed(planet)
	p = []
	# equator
	for lat in range(-90, 90, resolution):
		for long in range(-180, 180, resolution):
			p.append(((lat*pi/180, long*pi/180), Color(rr(), rg(), rb())))
	return Points(p)
