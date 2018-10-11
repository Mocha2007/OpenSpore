import sys
sys.path.append('./data')
from color import Color
from system import System, Planet

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	hasmoon = False
	for _, p in system.bodies:
		if p.bodies:
			hasmoon = True
			break
	return colorMap[hasmoon]


def planet(p: Planet) -> Color:
	hasmoon = False
	if p.bodies:
		hasmoon = True
	return colorMap[hasmoon]
