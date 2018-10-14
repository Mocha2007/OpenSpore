from math import cos, pi
from random import randint, seed
import sys
sys.path.append('./data')
from points import Points
from color import Color

resolution = 30

rr = lambda: randint(0, 128)
rg = lambda: randint(128, 192)
rb = lambda: randint(128, 192)


def main(planet):
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
			p.append(((long, lat), Color(rr(), rg(), rb())))
	return Points(p)
