from math import pi
import sys
sys.path.append('./data')
from points import Points
from constants import grey

p = []
# equator
lat = 0
for long in range(-180, 180):
	p.append(((lat*pi/180, long*pi/180), grey))
# meridians
for long in (-90, 0, 90, 180):
	for lat in range(-90, 90):
		p.append(((lat*pi/180, long*pi/180), grey))


def main(*_):
	return Points(p)
