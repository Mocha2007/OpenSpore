import sys
sys.path.append('./data')
from color import Color
from system import System, Planet

grey = Color(32, 32, 32)


def main(system: System) -> Color:
	for _, p in system.bodies:
		if p.civ:
			return p.civ.color
	return grey


def planet(p: Planet) -> Color:
	if p.civ:
		return p.civ.color
	return grey
