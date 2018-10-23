import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import esi2


def colormap(esi: float) -> Color:
	assert 0 <= esi <= 1
	if esi < .5:
		return Color(0, int(255-255*2*esi), 255)
	return Color(int(255*2*esi-255), 0, 255)


def main(system: System) -> Color:
	maxesi = 0
	for _, p in system.bodies[:4]: # never beyond p3; reduces lag tremendously
		maxesi = max(esi2(p), maxesi)
	return colormap(maxesi)


def planet(p: Planet) -> Color:
	return colormap(esi2(p))
