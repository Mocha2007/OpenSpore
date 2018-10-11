import sys
sys.path.append('./data')
from color import Color
from system import System


def main(system: System) -> Color:
	return Color(128, int(len(system.bodies)*255/9), 128)


planet = main

