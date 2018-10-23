import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import ishab, m_gg, p_hab, water

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	for _, p in system.bodies:
		if ishab(p):
			return colorMap[True]
	return colorMap[False]


def planet(p: Planet) -> Color:
	return colorMap[ishab(p)]
