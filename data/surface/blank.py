from math import pi
import sys
sys.path.append('./data')
from points import Points
from constants import grey

resolution = 12

p = []
# equator
for lat in range(-90, 90, resolution):
	for long in range(-180, 180, resolution):
		p.append(((lat*pi/180, long*pi/180), grey))


def main(*_):
	return Points(p)
