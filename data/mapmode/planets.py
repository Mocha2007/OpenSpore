import sys
sys.path.append('./data')
from color import Color
from system import System


def main(system: System) -> Color:
	return Color(128, min(int(len(system.bodies)**2*3), 255), 128)


planet = main
