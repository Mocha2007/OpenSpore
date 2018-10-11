import sys
sys.path.append('./data')
from color import Color
from system import System, Planet

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	for _, p in system.bodies:
		if 273 < p.temp < 373:
			return colorMap[True]
	return colorMap[False]


def planet(p: Planet) -> Color:
	return colorMap[273 < p.temp < 373]
