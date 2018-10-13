from math import atan2
import sys
sys.path.append('./data')
from color import Color

# characters
alphabet = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
greek = 'αβγδεζηθικλμνξοπρστυφχψω'

# astro
au = 149597870700
r_sun = 6.957e8
t_sun = 5772

# colors
grey = Color(128, 128, 128)


# functions
def delta(a: tuple, b: tuple) -> tuple:
	temporary = tuple(zip(a, b))
	temporary = tuple(map(lambda x: x[0]-x[1], temporary))
	return temporary


def dist(a: tuple, b: tuple) -> float:
	s = 0
	for i in range(len(a)):
		s += (a[i]-b[i])**2
	return s**.5


def spore_ishab(planet, star): # todo make actually spore
	inner, outer = star.mass*.95, star.mass*1.05
	return inner < planet.sma < outer


def temp(t: float, r: float, sma: float, a: float) -> float:
	'''Temperature of the star (K), Radius of the star (m), Semimajor axis (m), Albedo\n->
	Temperature of the body (K)\nFormula from https://en.wikipedia.org/wiki/Planetary_equilibrium_temperature#Theoretical_model'''
	return t*(1-a)**.25*(r/2/sma)**.5


def temp2(star, planet) -> float:
	return temp(star.temperature, star.radius, planet.sma*au, 0)


# from -pi to pi
def xyz2phitheta(xyz: (float, float, float)) -> (float, float):
	x, y, z = xyz
	phi = atan2(y, x)
	theta = atan2(z, (x ** 2 + y ** 2) ** .5)
	return phi, theta
