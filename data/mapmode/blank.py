import sys
sys.path.append('./data')
from color import Color


def main(*unused) -> Color:
	return color.Color(128, 128, 128)
