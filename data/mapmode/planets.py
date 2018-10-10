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


def main(system: System) -> Color:
	return Color(128, int(len(system.bodies)*255/9), 128)
