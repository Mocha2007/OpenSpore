import sys
from random import seed, randint
sys.path.append('./data')
from color import Color
from system import System, Planet


def main(system: System) -> Color:
	seed(system.star.id)
	return Color(randint(0, 255), randint(0, 255), randint(0, 255))


def planet(p: Planet) -> Color:
	seed(p.orbit.primary.id + p.orbit.sma)
	return Color(randint(0, 255), randint(0, 255), randint(0, 255))
