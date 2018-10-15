import sys
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import m_airless, m_gg

colorMap = {
	True: Color(0, 192, 0),
	False: Color(192, 0, 0)
}


def main(system: System) -> Color:
	for _, p in system.bodies:
		if 273 < p.temp < 373 and m_airless < p.mass < m_gg:
			return colorMap[True]
	return colorMap[False]


def planet(p: Planet) -> Color:
	return colorMap[273 < p.temp < 373 and m_airless < p.mass < m_gg]
