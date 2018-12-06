from math import atan2, ceil, pi
from random import uniform
import pygame
import sys
from random import choice
sys.path.append('./data')
from chem import Chem
from color import Color

# characters
alphabet = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
greek = 'αβγδεζηθικλμνξοπρστυφχψω'
vowels = 'aeiou'


def rword(n: int) -> str:
	return ''.join([choice(alphabet) for _ in range(n)])


# astro
ld = 384399000
au = 149597870700
g = 6.67408e-11
hour = 60 * 60
day = 24 * hour
year = 365.2425 * day
planet_form_time = 1e6 * year # liberal estimate; prolly higher
universe_age = 13.799e9 * year
g_earth = 9.807
m_earth = 5.97237e24
# m_airless = 1.3e23 # must be less than titan
m_gg = m_earth * 10
m_ig = 3e26 # estimate; b/w nep and sat
m_j = 1.8982e27
m_rock = 1.8e-5 * m_j # smallest known exoplanet: http://exoplanets.org/detail/KOI_6705.01
m_browndwarf = 13 * m_j
m_sun = 1.9885e30
m_star = .075 * m_sun
p_earth = 101325
# https://www.physicsforums.com/threads/what-air-pressure-can-the-human-body-survive.333248/
# "72mm of Mercury as the minimal inspired partial pressure of Oxygen"
p_hab = 9630, 8*p_earth
p_troposphere = 18481.36 # tropopause
r_earth = 6.371e6
r_j = 6.9911e7
r_sun = 6.957e8
t_sun = 5772
t_earth = 288
soi_moon = 6.2e8 # just above venus; earth is 9.2e8 for comparison
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html
c_j = { # jovian atmospheric composition by volume
	'H2': (.8, .963), # neptune <> saturn
	'He': (.0325, .19), # saturn <> neptune
	'CH4': (3e-3, .023), # jupiter <> uranus
	'NH3': (1.25e-4, 2.6e-4), # saturn <> jupiter
	'HD': (2.8e-5, 1.9e-4), # jupiter <> neptune
	'C2H6': (1e-6, 7e-6), # neptune <> saturn
	'H2O': (4e-6, 4e-6)
}
# https://en.wikipedia.org/wiki/Atmosphere_of_Jupiter#Chemical_composition
j_H = .898
c_j['Ne'] = (j_H * 1.23e-4, j_H * 1.23e-4)
c_j['H2S'] = (j_H * 1.62e-5, j_H * 1.62e-5)
c_j['Ar'] = (j_H * 3.62e-6, j_H * 3.62e-6)
c_j['PH3'] = (j_H * 3.73e-7, j_H * 3.73e-7)
c_j['Kr'] = (j_H * 1.61e-9, j_H * 1.61e-9)
c_j['Xe'] = (j_H * 1.68e-10, j_H * 1.68e-10)

c_e = { # terran atmospheric composition by volume
	# sorted by molar mass
	'H2': (2.5, 3), # theoretical He-world
	'He': (5.24e-6, 1.5), # earth <> theoretical He-world
	'CH4': (1.79e-6, 1.79e-6),
	'H2O': (1e-5, .05), # earth <> earth
	'HF': (1e-9, 5e-9), # venus <> venus
	'Ne': (2.5e-6, 1.818e-5), # mars <> earth
	'CO': (1e-7, 5.57e-4), # earth <> mars
	'N2': (.0189, .78084), # mars <> earth
	'NO': (1e-6, 1e-4), # to fix errors <> mars
	'O2': (1.46e-3, .20946), # mars <> earth
	'HCl': (1e-7, 6e-7), # venus <> venus
	'Ar': (7e-5, .0193), # venus <> mars
	'CO2': (4e-3, .965), # earth <> venus
	'N2O': (5e-7, 5e-7),
	'NO2': (2e-8, 2e-8),
	'SO2': (1e-6, 1.5e-4), # earth <> venus
	'Kr': (3e-7, 1.14e-6), # mars <> earth
	'Xe': (8e-8, 9e-8), # mars <> earth
}

molmass = {
	'H2': 2, # NOT DEUTERIUM!
	'HD': 3,
	'He': 4.002602,
	'CH4': 16.04,
	'NH3': 17.031,
	'H2O': 18.015,
	'HF': 20.01,
	'Ne': 20.1797,
	'CO': 28.01,
	'N2': 28.014,
	'NO': 30.01,
	'C2H6': 30.06,
	'O2': 31.998,
	'PH3': 33.998,
	'H2S': 34.08,
	'HCl': 36.46,
	'Ar': 39.948,
	'CO2': 44.009,
	'N2O': 44.0128,
	'NO2': 46.0055,
	'SO2': 64.066,
	'Kr': 83.798,
	'Xe': 131.293,
}

# other
grey = Color(128, 128, 128)
statemap = {
	'solid': 0,
	'liquid': 1,
	'gas': 2,
	'supercritical fluid': 3
}
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
	},
	'ammonia': {
		'name': 'Ammonia',
		'melt': 195.42,
		'boil': 239.81,
		'triple': (195.4, 6.06e3),
		'critical': (405.5, 1.128e7)
	}
}
water = Chem(**chemprop['water'])
methane = Chem(**chemprop['methane'])
ammonia = Chem(**chemprop['ammonia'])
lifechems = (
	water,
	methane,
	ammonia
)

planet_types = {
	2: 'Rocky',
	1: 'Hell',
	0.5: 'Desert',
	0.1: 'Toxic',
	0: 'Terra',
	-1: 'Snowball',
	-2: 'Gas Giant',
	-3: 'Ice Giant'
}


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
	return temp(star.temperature, star.radius, planet.orbit.sma, a)


def m2r(mass: float, rho: float) -> float:
	return (mass*3/4/pi/rho)**(1/3)


def grav(mass: float, radius: float) -> float:
	return g*mass/radius**2


def density(mass: float, radius: float) -> float:
	return mass/(4/3 * pi * radius**3)


def density_to_radius(mass: float, density: float) -> float:
	return (mass/density/(4/3*pi))**(1/3)


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


def chemstate(c: Chem, p) -> str:
	if p.atm is None:
		return c.state2((p.temp, 1))
	return c.state2((p.temp, p.atm))


def v_e(m: float, r: float) -> float:
	return (2*g*m/r)**.5


def v_e2(p) -> float:
	return v_e(p.mass, p.radius)


def getv_eslope(molarmass: float) -> float:
	"""Get the v_e calc slope in km/s per kelvin"""
	# https://upload.wikimedia.org/wikipedia/commons/4/4a/Solar_system_escape_velocity_vs_surface_temperature.svg
	return 50 / molarmass**.5


def atmchems(p) -> list:
	"""List of ALL compounds which can be retained by the planet"""
	compoundlist = []
	for compound in molmass:
		if v_e2(p) > p.temp * getv_eslope(molmass[compound]):
			compoundlist.append(compound)
	return compoundlist


def ishab(p) -> bool:
	if p.atm and 'O2' in p.atmosphere and p_hab[0] < p.atmosphere['O2']*p.atm:
		return chemstate(water, p) == 'liquid' and p_hab[0] < p.atm < p_hab[1]
	return False


# source for the formula: http://phl.upr.edu/projects/earth-similarity-index-esi
def esi(r: float, m: float, t: float) -> float:
	# Radius, Density, Escape Velocity, Temperature
	esi1 = 1-abs((r-r_earth)/(r+r_earth))
	esi22 = 1-abs((density(m, r)-density(m_earth, r_earth))/(density(m, r)+density(m_earth, r_earth)))
	esi3 = 1-abs((v_e(m, r)-v_e(m_earth, r_earth))/(v_e(m, r)+v_e(m_earth, r_earth)))
	esi4 = 1-abs((t-255)/(t+255))
	return esi1**(.57/4)*esi22**(1.07/4)*esi3**(.7/4)*esi4**(5.58/4)


def esi2(p) -> float:
	return esi(p.radius, p.mass, p.temp)


def soi(p) -> float:
	return p.orbit.sma * (p.mass / p.orbit.primary.mass)**.4


def getmb(a: (float, float), b: (float, float)) -> (float, float):
	rise = b[1] - a[1]
	run = b[0] - a[0]
	m = rise/run
	b = a[1] - m*a[0]
	return m, b


def temprange(p) -> (float, float):
	if p.atm is None:
		return p.temp, p.temp
	ratios = .63, 1/(5*p.atm+2)+1 # based on Earth and Mars
	return ratios[0]*p.temp, ratios[1]*p.temp


def atmos_water(p) -> bool:
	return ('H2O' in p.atmosphere) and (water.melt < temprange(p)[1])


def possible_koppen(p) -> set:
	t_min, t_max = temprange(p)
	haswater = atmos_water(p)
	climates = set()
	# A
	if 291 < t_max:
		climates = climates.union({'Am', 'As'})
		if haswater:
			climates.add('Af')
	# B
	if 291 < t_max:
		climates.add('BWh')
		if haswater:
			climates.add('BSh')
	if 283 < t_max and t_min < 291: # need max otherwise it'll include snowballs
		climates.add('BWk')
		if haswater:
			climates.add('BSk')
	# C
	if 283 < t_max and t_min < 291:
		if 295 < t_max:
			climates.add('Cfa')
			if haswater:
				climates.union({'Cwa', 'Csa'})
		climates = climates.union({'Cfb', 'Cfc'})
		if haswater:
			climates.union({'Cwb', 'Cwc', 'Csb', 'Csc'})
	# D
	if 283 < t_max and t_min < 273:
		if 295 < t_max:
			climates.add('Dfa')
			if haswater:
				climates.union({'Dwa', 'Dsa'})
		climates = climates.union({'Dfb', 'Dfc'})
		if haswater:
			climates.union({'Dwb', 'Dwc', 'Dsb', 'Dsc'})
		if t_min < 235:
			climates.add('Dfd')
			if haswater:
				climates.union({'Dwd', 'Dsd'})
	# ET
	if 273 < t_max and t_min < 283:
		climates.add('ET')
	# EF
	if t_min < 273:
		climates.add('EF')
	return climates


def cansnow(p) -> bool:
	t_min, t_max = temprange(p)
	return t_min < 273 < t_max and atmos_water(p)


def temp2function(temperature: float):
	# albedo, stellar radius, stellar temp -> semimajor axis
	return lambda a, r, t: t**2 * (1-a)**.5 * r/2/temperature**2


def print_orbit(system, **kwargs):
	sys.path.append('./data/surface')
	from planettype import planet as planet_color
	from starclass import main as star_color
	# set up size
	size = 1024
	if 'size' in kwargs:
		assert type(kwargs['size']) == int
		size = kwargs['size']
	center = size//2, size//2
	orbit_map = pygame.display.set_mode((size, size))
	orbit_map.fill((0, 0, 0))
	# star name and type
	color_for_star = star_color(system).rgb()
	name = font.render(system.star.name+' - '+system.star.type, 1, color_for_star)
	orbit_map.blit(name, (0, 0))
	if system.bodies:
		scale = system.bodies[-1][1].orbit.sma # pixels per au
		scale = .5 * size/scale # only 50% filled cause radius
		# hab zone iff has planets (otherwise the program will hang)
		# hab = scale * au * system.star.luminosity**.5
		fargs = .3, system.star.radius, system.star.temperature
		inner, outer = temp2function(299)(*fargs), temp2function(229)(*fargs)
		radius = round(scale * (outer+inner)/2)
		width = round(scale * (outer-inner)/2)
		pygame.draw.circle(orbit_map, (0, 32, 0), center, radius, width)
	else:
		scale = system.star.radius
		scale = .5 * size/scale # only 50% filled cause radius
	# star
	radius = round(scale * system.star.radius)
	pygame.draw.circle(orbit_map, color_for_star, center, radius)
	# planets
	for _, planet in system.bodies:
		radius = round(scale * planet.orbit.sma)
		p_color = planet_color(planet).rgb()
		pygame.draw.circle(orbit_map, p_color, center, radius, 1)
		name = font.render(planet.name, 1, p_color)
		name_pos = center[0]-int(radius*.7), center[1]-int(radius*.7)
		orbit_map.blit(name, name_pos)
	pygame.image.save(orbit_map, 'orbit_map.png')


def mapping_prettify(mapping: dict, reverse: bool) -> (tuple, tuple):
	return zip(*sorted(mapping.items(), key=lambda x: x[0], reverse=reverse))


def advplt(galaxy):
	import matplotlib.pyplot as plt
	sys.path.append('./surface/data')
	from continental import gettype
	type_to_count = {}
	type_to_count2 = {}
	type_to_count3 = {}
	type_to_count4 = {}
	moons_vs_mass = {}
	mass_vs_density = []
	bwplt = {}
	for _, system in galaxy.stars:
		typeof = system.star.type
		if typeof in type_to_count:
			type_to_count[typeof] += 1
			type_to_count4[typeof].append(system.star.age)
		else:
			type_to_count[typeof] = 1
			type_to_count4[typeof] = [system.star.age]
		if len(typeof) == 1:
			mass_vs_density.append((system.star.mass, density(system.star.mass, system.star.radius)))
		for _, planet in system.bodies:
			typeof = planet_types[gettype(planet)]
			if typeof in bwplt:
				bwplt[typeof].append(esi2(planet))
			else:
				bwplt[typeof] = [esi2(planet)]
			if typeof in type_to_count2:
				type_to_count2[typeof] += 1
			else:
				type_to_count2[typeof] = 1
			if planet.resources:
				resource = planet.resources[0]
				if resource in type_to_count3:
					type_to_count3[resource] += 1
				else:
					type_to_count3[resource] = 1
			mass_vs_density.append((planet.mass, density(planet.mass, planet.radius)))
			# t vs moons
			mooncount = len(planet.bodies)
			mooncount = mooncount if mooncount < 10 else '10+'
			if mooncount in moons_vs_mass:
				moons_vs_mass[mooncount].append(planet.mass)
			else:
				moons_vs_mass[mooncount] = [planet.mass]

	plt.subplot(2, 5, 1)
	labels, types = mapping_prettify(type_to_count, True)
	plt.pie(types, labels=labels, autopct='%1.1f%%') # , startangle=90
	plt.title('Stellar Classes')

	plt.subplot(2, 5, 2)
	type_to_countb = dict(type_to_count)
	for i in ('WR', 'L', 'T', 'Y', 'WD', 'NS', 'BH'):
		try:
			del type_to_countb[i]
		except KeyError:
			pass
	labels, types = mapping_prettify(type_to_countb, True)
	plt.pie(types, labels=labels, autopct='%1.1f%%') # , startangle=90
	plt.title('Main Sequence Stars')

	plt.subplot(2, 5, 3)
	type_to_countc = {'Main Sequence': 0, 'Brown Dwarf': 0, 'Other': 0}
	for i, j in type_to_count.items():
		if i in 'LTY':
			type_to_countc['Brown Dwarf'] += j
		elif i in 'OBAFGKM':
			type_to_countc['Main Sequence'] += j
		else:
			type_to_countc['Other'] += j
	labels, types = mapping_prettify(type_to_countc, True)
	plt.pie(types, labels=labels, autopct='%1.1f%%') # , startangle=90
	plt.title('Star Superclass')

	plt.subplot(2, 5, 4)
	labels, types = mapping_prettify(type_to_count2, True)
	plt.pie(types, labels=labels, autopct='%1.1f%%')
	plt.title('Planet Class')

	plt.subplot(2, 5, 5)
	labels, types = mapping_prettify(type_to_count3, True)
	plt.pie(types, labels=list(map(lambda r: r.name if r else 'None', labels)), autopct='%1.1f%%')
	plt.title('Resources (Excludes None)')

	plt.subplot(2, 5, 6)
	labels, types = mapping_prettify(type_to_count4, False)
	plt.boxplot(types, labels=labels)
	plt.yscale('log')
	plt.xlabel('Type')
	plt.ylabel('Age (s)')
	plt.title('Age by Type')

	plt.subplot(2, 5, 8)
	labels, types = zip(*sorted(moons_vs_mass.items(), key=lambda x: int(str(x[0])[:2])))
	plt.boxplot(types, labels=labels)
	plt.yscale('log')
	plt.xlabel('Moons')
	plt.ylabel('Mass (kg)')
	plt.title('Moon Count')

	plt.subplot(2, 5, 9)
	plt.scatter(*zip(*mass_vs_density))
	plt.xscale('log')
	plt.yscale('log')
	plt.xlabel('Mass (kg)')
	plt.ylabel('Density (kg/m^3)')
	plt.title('Body Mass vs. Density')

	plt.subplot(2, 5, 10)
	labels, types = mapping_prettify(bwplt, False)
	plt.boxplot(types, labels=labels)
	plt.xlabel('Type')
	plt.ylabel('ESI')
	plt.title('Planet ESI')

	plt.show()
