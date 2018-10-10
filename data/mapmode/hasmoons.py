import sys
sys.path.append('./data')
from color import Color
from system import System

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	hasmoon = False
	for _, planet in system.bodies:
		if planet.bodies:
			hasmoon = True
			break
	return colorMap[hasmoon]
