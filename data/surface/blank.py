from math import cos, pi
import sys
sys.path.append('./data')
from points import Points
from constants import grey

resolution = 30

p = []
# equator
for i in range(resolution):
	lat = i / resolution * pi - pi / 2
	dots = int(cos(lat) * resolution)  # reduce res around poles
	if dots < 1:
		continue
	for j in range(dots):
		long = j / dots * 2 * pi
		p.append(((long, lat), grey))


def main(*_):
	return Points(p)
