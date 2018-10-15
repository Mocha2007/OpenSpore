from math import atan2, ceil, pi
import pygame
import sys
sys.path.append('./data')
from color import Color

# characters
alphabet = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
greek = 'αβγδεζηθικλμνξοπρστυφχψω'
vowels = 'aeiou'

# astro
au = 149597870700
g = 6.67408e-11
g_earth = 9.807
m_earth = 5.97237e24
m_airless = m_earth / 9 # must be greater than mars... but likely not by a whole lot
m_gg = m_earth * 10
m_ig = 3e26 # estimate; b/w nep and sat
m_j = 1.8982e27
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
	"""Temperature of the star (K), Radius of the star (m), Semimajor axis (m), Albedo\n->
	Temperature of the body (K)\nFormula from https://en.wikipedia.org/wiki/Planetary_equilibrium_temperature#Theoretical_model"""
	return t*(1-a)**.25*(r/2/sma)**.5


def temp2(star, planet) -> float:
	return temp(star.temperature, star.radius, planet.sma*au, 0)


def m2r(mass: float, density: float) -> float:
	return (mass*3/4/pi/density)**(1/3)


def grav(mass: float, radius: float) -> float:
	return g*mass/radius**2


def density(mass: float, radius: float) -> float:
	return mass/(4/3 * pi * radius**3)


# from -pi to pi
def xyz2phitheta(xyz: (float, float, float)) -> (float, float):
	x, y, z = xyz
	phi = atan2(y, x)
	theta = atan2(z, (x ** 2 + y ** 2) ** .5)
	return phi, theta


font = pygame.font.SysFont("trebuchetms", 15)


def text(t: str, screen: pygame.Surface, rect: (int, int, int, int), backcolor: (int, int, int), forecolor: (int, int, int)):
	t = t.replace('\t', ' '*4)
	coords = rect[:2]
	width = rect[2]-rect[0]
	rectborder = coords[0], coords[1], width, 20 * (t.count('\n')+1)
	pygame.draw.rect(screen, backcolor, rectborder)
	pygame.draw.rect(screen, forecolor, rectborder, 1)
	t = t.split('\n')
	for i in range(len(t)):
		tlabel = font.render(t[i], 1, (255, 255, 255))
		screen.blit(tlabel, (coords[0]+10, coords[1]+i*20))
		if i: # draw line above
			pygame.draw.line(screen, forecolor, (coords[0]+10, coords[1]+20*i), (coords[0]+width-10, coords[1]+20*i))


def bestresource(b): # Planet/Moon -> Resource
	maxvalue = [0, None]
	if b.resources:
		for r in b.resources:
			if r.value > maxvalue[0]:
				maxvalue[0] = r.value
				maxvalue[1] = r
	return maxvalue[1]


def bestmoonresource(p): # Planet -> Resource
	maxvalue = [0, None]
	# go through moons
	if p.bodies:
		for _, m in p.bodies:
			br = bestresource(m)
			if br.value > maxvalue[0]:
				maxvalue[0] = br.value
				maxvalue[1] = br
	return maxvalue[1]


def limittext(s: str, l: int) -> str:
	if l < 1:
		return ''
	if len(s) <= l:
		return s
	# slowly remove vowels
	s = list(s)
	for i in range(len(s)-1, -1, -1):
		if s[i] in vowels:
			del s[i]
			if len(s) <= l:
				break
	s = ''.join(s)
	# figure out how many consonants to skip
	skip = ceil(len(s)/l)
	return s[::skip]
