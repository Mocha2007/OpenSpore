import sys
from random import randint, seed
sys.path.append('./data')
from civ import Civ
from color import Color
from system import System, Planet

grey = Color(32, 32, 32)


def civcolor(civ: Civ) -> int:
	seed(civ.id)
	return Color(0, randint(64, 255), randint(64, 255))


def main(system: System) -> Color:
	for _, p in system.bodies:
		if p.civ:
			return civcolor(p.civ)
	return grey


def planet(p: Planet) -> Color:
	if p.civ:
		return civcolor(p.civ)
	return grey
