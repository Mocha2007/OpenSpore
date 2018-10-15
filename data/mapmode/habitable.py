import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import m_airless, m_gg, water

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	for _, p in system.bodies:
		if water.melt < p.temp < water.boil and m_airless < p.mass < m_gg:
			return colorMap[True]
	return colorMap[False]


def planet(p: Planet) -> Color:
	return colorMap[water.melt < p.temp < water.boil and m_airless < p.mass < m_gg]
