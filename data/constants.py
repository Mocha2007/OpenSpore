from math import atan2, ceil, log10, pi
from random import uniform
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
m_airless = 1.3e23 # must be less than titan
m_gg = m_earth * 10
m_ig = 3e26 # estimate; b/w nep and sat
m_j = 1.8982e27
p_earth = 101325
# https://www.physicsforums.com/threads/what-air-pressure-can-the-human-body-survive.333248/
# https://en.wikipedia.org/wiki/Hypoxia_(medical)#Cause
p_hab = 5300, 8*p_earth
p_troposphere = 18481.36 # tropopause
r_j = 6.9911e7
r_sun = 6.957e8
t_sun = 5772
t_earth = 288

# colors
grey = Color(128, 128, 128)


class Chem:
	def __init__(self, **data):
		self.name = data['name']
		try:
			self.triple = data['triple']
			assert type(self.triple) == tuple
			self.critical = data['critical']
			assert type(self.critical) == tuple
		except IndexError:
			pass
		self.melt = data['melt']
		assert type(self.melt) == float
		self.freeze = self.melt
		self.boil = data['boil']
		assert type(self.boil) == float

	# get current state
	def state(self, t: float) -> str:
		if t < self.melt:
			return 'solid'
		if t < self.boil:
			return 'liquid'
		return 'gas'

	# use crit/trip instead - fairly accurate, but not perfect
	def state2(self, tp: (float, float)) -> str:
		t, p = tp
		# supercritical?
		if self.critical[0] < t and self.critical[1] < p:
			return 'supercritical fluid'
		# normal
		if t < self.triple[0]:
			# sol? gas?
			# upper left
			# if p > self.triple[1]:
			return 'solid' # more accurate than previous solution
			# lower left
			# f = lambda x: log10(self.triple[1]) / self.triple[0] * x
			# if f(t) < log10(p):
			# 	return 'solid'
			# return 'gas'
		# now... liq? gas?
		f = lambda x: log10(self.triple[1]) / self.triple[0] * x
		# upper right
		if f(t) < log10(p):
			return 'liquid'
		# lower right
		return 'gas'


chemprop = {
	'water': {
		'name': 'Water',
		'melt': 273.15,
		'boil': 373.13,
		'triple': (273.16, 611.657),
		'critical': (647.096, 2.2064e7)
	},
	'methane': {
		'name': 'Methane',
		'melt': 90.7,
		'boil': 111.65,
		'triple': (90.68, 1.17e4),
		'critical': (190.4, 4.6e6)
	}
}
water = Chem(**chemprop['water'])
methane = Chem(**chemprop['methane'])
stp = 273.15, 1e5
ntp = 293.15, 1.01325e5


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
	Temperature of the body (K)\n
	Formula from https://en.wikipedia.org/wiki/Planetary_equilibrium_temperature#Theoretical_model"""
	return t*(1-a)**.25*(r/2/sma)**.5


def temp2(star, planet) -> float:
	# gg
	if planet.mass < m_gg:
		a = uniform(.142, .689)
	elif planet.mass < m_ig:
		a = uniform(.442, .488)
	else:
		a = uniform(.499, .538)
	return temp(star.temperature, star.radius, planet.sma*au, a)


def m2r(mass: float, rho: float) -> float:
	return (mass*3/4/pi/rho)**(1/3)


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


def gettype(p) -> str: # Planet ->
	words = []
	# temp
	if p.temp < water.melt:
		words.append('Frozen')
	elif p.temp < (water.melt + t_earth)/2:
		words.append('Cold')
	elif p.temp < (water.melt + t_earth*3)/4:
		words.append('Cool')
	elif p.temp < (water.boil + t_earth)/2:
		words.append('Temperate')
	elif p.temp < (water.boil + t_earth*3)/4:
		words.append('Warm')
	elif p.temp < water.boil:
		words.append('Hot')
	else:
		words.append('Boiling')
	# size
	if p.mass < m_gg:
		words.append('Rock')
	elif p.mass < m_ig:
		words.append('Ice Giant')
	else:
		words.append('Gas Giant')
	return ' '.join(words)


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
