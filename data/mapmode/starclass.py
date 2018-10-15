import sys
sys.path.append('./data')
from color import Color
from system import System
from constants import water

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
	try:
		return colorMap[system.star.type]
	except KeyError:
		return Color(128, 128, 128)


def planet(p: Planet) -> Color:
	if water.melt < p.temp:
		if p.temp < water.boil:
			return planetMap[1]
		return planetMap[0]
	return planetMap[2]
