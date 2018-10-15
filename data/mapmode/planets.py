import sys
sys.path.append('./data')
from color import Color
from system import System


def main(system: System) -> Color:
	return Color(128, min(len(system.bodies)*255//9, 255), 128)


planet = main
