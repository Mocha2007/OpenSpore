import sys
sys.path.append('./data')
from color import Color
from constants import grey
from system import Planet
sys.path.append('./data/surface')
from continental import gettype, typecolor


def main(*_) -> Color:
	return grey


def planet(p: Planet) -> Color:
	c1, c2 = typecolor[gettype(p)]
	return c1.blend(c2)
