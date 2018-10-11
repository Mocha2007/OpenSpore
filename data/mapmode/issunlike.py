import sys
sys.path.append('./data')
from color import Color
from system import System, Planet

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	return colorMap[.45 < system.star.mass < 1.4]


def planet(p: Planet) -> Color:
	return colorMap[273 < p.temp < 373]
