import sys
from math import log
sys.path.append('./data')
from color import Color
from system import System, Planet
from constants import grey, m_browndwarf, m_rock


def m2u(mass: float) -> float:
	mrange = log(m_browndwarf) - log(m_rock)
	return (log(mass)-log(m_rock))/mrange


def m2c(minimum: float, maximum: float) -> Color:
	r = 255 - round(m2u(minimum) * 255)
	b = round(m2u(maximum) * 255)
	return Color(r, 128, b)


def main(system: System) -> Color:
	if not system.bodies:
		return grey
	maximum = 0
	minimum = m_browndwarf
	for _, p in system.bodies:
		if p.mass > maximum:
			maximum = p.mass
		if p.mass < minimum:
			minimum = p.mass
	return m2c(minimum, maximum)


def planet(p: Planet) -> Color:
	return m2c(p.mass, p.mass)
