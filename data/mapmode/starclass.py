import sys
sys.path.append('./data')
from color import Color
from system import System
from constants import chemstate, water

colorMap = {
	'O': Color(0, 128, 255),
	'B': Color(128, 192, 255),
	'A': Color(255, 255, 255),
	'F': Color(255, 255, 128),
	'G': Color(255, 255, 0),
	'K': Color(255, 128, 0),
	'M': Color(255, 0, 0)
}
planetMap = {
	'supercritical fluid': Color(255, 0, 255),
	'gas': Color(255, 0, 0),
	'liquid': Color(0, 255, 0),
	'solid': Color(0, 0, 255)
}


def main(system: System) -> Color:
	try:
		return colorMap[system.star.type]
	except KeyError:
		return Color(128, 128, 128)


def planet(p: Planet) -> Color:
	return planetMap[chemstate(water, p)]
