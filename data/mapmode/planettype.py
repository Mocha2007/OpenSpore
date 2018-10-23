import sys
sys.path.append('./data')
from color import Color
from constants import grey
from system import Planet
sys.path.append('./data/surface')
import continental


def main(*_) -> Color:
	return grey


def planet(p: Planet) -> Color:
	return continental.main(p).points[0][1]
