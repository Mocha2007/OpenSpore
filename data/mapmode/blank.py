import sys
sys.path.append('./data')
from color import Color


def main(*_) -> Color:
	return color.Color(128, 128, 128)
