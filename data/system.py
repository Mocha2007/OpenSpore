from random import random, randint, uniform
from math import e, exp, log, log10
from constants import au, m2r, temp2, m_earth, m_browndwarf, m_gg, m_j, m_rock, r_j, r_sun, t_sun, soi, soi_moon, m_sun
from constants import atmchems, c_e, c_j # for atm
from constants import getmb # for pradius
from orbit import rporbit
from life import lifegen
from civ import civgen


def chemrange(minimum: float, maximum: float) -> float:
	"""uniform but weighted logarithmically"""
	return e**uniform(log(minimum), log(maximum))


def atm(p) -> dict:
	chems = atmchems(p)
	a = {}
	totalfraction = 0
	for chem in chems:
		if p.mass > m_gg:
			if chem in c_j:
				fraction = chemrange(*c_j[chem])
				a[chem] = fraction
				totalfraction += fraction
		elif chem in c_e: # must be terran
			fraction = chemrange(*c_e[chem])
			a[chem] = fraction
			totalfraction += fraction
	# normalize based on totalfraction
	for chem in a:
		a[chem] /= totalfraction
	return a


def mmass() -> float:
	moon = 3.7493e19, 1.4819e23 # mimas, ganymede
	return exp(log(moon[1]/moon[0])*random()) * moon[0]


def pmass() -> float:
	return exp(log(m_browndwarf/m_rock)*random()) * m_rock


def pradius(m: float) -> float:
	absmin = 100 # probably
	absmax = 23000 # https://en.wikipedia.org/wiki/PSR_J1719-1438_b
	if m < 3e21: # based on ss data; smaller mesoplanets
		rhomin = 820 # (55637) 2002 UX25
		rhomax = 2170 # Ceres
	else:
		if m < 3e23: # based on ss data; larger mesoplanets
			mmin, bmin = getmb((log10(3.014E+21), log10(1630)), (log10(1.08E+23), log10(1834.4))) # Oberon -> Callisto
			mmax, bmax = getmb((log10(4.01E+21), log10(2550)), (log10(8.93E+22), log10(3528))) # Haumea -> Io
		elif m < 1e25: # based on ss data; terrestrials
			# rhomin = 2682 # Kepler-138 b; cf. Mars = 3933.5
			# rhomax = 5514 # Earth
			mmin, bmin = getmb((log10(3.98622E+23), log10(2682.517339)), (log10(4.8675E+24), log10(5243))) # kepler-138b -> venus
			mmax, bmax = getmb((log10(4.01E+21), log10(2550)), (log10(3.3011E+23), log10(5427))) # Haumea -> mercury
			# i'd do mercury -> earth but this causes fewer issues
		else: # superearths + gas giants
			if m < 7e26: # based on exoplanetary data; rough estimate
				mmin, bmin = getmb((25, 3), (27, 2))
				mmax, bmax = getmb((25, 4.5), (27, 2.5))
			else:
				mmin, bmin = getmb((27, 2), (28.5, 4))
				mmax, bmax = getmb((27, 3), (28, 4))
		rhomin = 10 ** (mmin*log10(m) + bmin)
		rhomax = 10 ** (mmax*log10(m) + bmax)
		rhomin = max(absmin, rhomin)
		rhomax = min(absmax, rhomax)
	# if m > m_gg:
	# 	rho = uniform(687, 1326) # gassy density
	# else:
	# 	rho = uniform(3933.5, 5427) # rocky density
	r = m2r(m, uniform(rhomin, rhomax))
	# critical radius
	if r_j < r:
		r = r_j * uniform(.99, 1.01)
	return r


class Moon:
	def __init__(self, planet, system, moonnamegen, resourcegen): # no type annotation since function can't be annotated
		attempt = planet.mass
		while attempt >= planet.mass:
			attempt = mmass()
		self.mass = attempt
		self.radius = pradius(attempt)
		self.name = moonnamegen()
		self.resources = []
		self.sma = rporbit(planet, planet.radius*2) # todo
		self.temp = planet.temp
		self.atm = None # todo
		self.atmosphere = [] # todo
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)


class Planet: # no type annotation since function can't be annotated
	def __init__(self, system, sma: float, planetnamegen, moonnamegen, resourcegen):
		self.mass = pmass()
		# radius
		self.radius = pradius(self.mass)
		# pressure
		self.orbit = rporbit(system.star, sma)
		self.temp = temp2(system.star, self)
		self.atmosphere = atm(self)
		if self.atmosphere and self.mass < m_gg:
			self.atm = self.mass ** uniform(.11, .29) # min gas log ratio is mars, max venus
			# to calculate more, use log(P)/log(M) to get a ratio
		else:
			self.atm = None
		self.name = planetnamegen()
		contents = []
		# GRAVITATIONALLY ROUNDED MOONS ONLY!!!!!
		soi_ = soi(self)
		if soi_moon < soi_:
			maxmoons = round(3.3e-5 * soi_**.5) # not perfect, but certainly more realistic than before!
			for i in range(0, randint(1, maxmoons)):
				contents.append((i, Moon(self, system, lambda: moonnamegen(self.name, i), resourcegen)))
		self.bodies = contents
		data = {
			'system': system,
			'body': self
		}
		self.resources = resourcegen(**data)
		self.life = lifegen(self)
		self.civ = civgen(self)


class System: # no type annotation since function can't be annotated
	def __init__(self, star, planetnamegen, moonnamegen, resourcegen):
		self.name = star.name
		self.star = star
		contents = []
		sma = au * (star.temperature/t_sun)**2 * star.radius/r_sun / 5 # 3 too low
		for i in range(randint(1, 9)):
			while 1:
				sma *= uniform(1.38, 2.02)  # e/v u/s
				attempt = Planet(self, sma, lambda: planetnamegen(star.name, i), moonnamegen, resourcegen)
				limit = star.radius * 4.5 # WD 1202-024 B (est.)
				if limit < attempt.orbit.sma:
					contents.append((i, attempt))
					break
				else:
					sma = limit
		self.bodies = contents
