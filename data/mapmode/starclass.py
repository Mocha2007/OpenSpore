import sys
sys.path.append('./data')
from color import Color
from system import System

colorMap = {
	'O': Color(0, 128, 255),
	'B': Color(128, 192, 255),
	'A': Color(255, 255, 255),
	'F': Color(255, 255, 128),
	'G': Color(255, 255, 0),
	'K': Color(255, 128, 0),
	'M': Color(255, 0, 0)
}
planetMap = (
	Color(255, 0, 0),
	Color(0, 255, 0),
	Color(0, 0, 255)
)


def main(system: System) -> Color:
	return colorMap[system.star.type]


def planet(p: Planet) -> Color:
	if 273 < p.temp:
		if p.temp < 373:
			return planetMap[1]
		return planetMap[0]
	return planetMap[2]
