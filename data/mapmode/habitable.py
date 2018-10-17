import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import m_gg, p_hab, water

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def p2b(p: Planet) -> bool:
	return water.melt < p.temp < water.boil and p.mass < m_gg and p_hab[0] < p.atm < p_hab[1]


def main(system: System) -> Color:
	for _, p in system.bodies:
		if p2b(p):
			return colorMap[True]
	return colorMap[False]


def planet(p: Planet) -> Color:
	return colorMap[p2b(p)]
