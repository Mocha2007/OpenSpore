from math import pi
from constants import g
from random import uniform


class Orbit:
	def __init__(self, primary, sma: float, ecc: float, inc: float, aop: float, lan: float, man: float):
		self.primary = primary
		assert 0 < sma
		self.sma = sma
		assert 0 <= ecc < 1
		self.ecc = ecc
		assert 0 <= inc <= pi
		self.inc = inc
		assert 0 <= aop < 2*pi
		self.aop = aop
		assert 0 <= lan < 2*pi
		self.lan = lan
		assert 0 <= man < 2*pi
		self.man = man

	def period(self) -> float:
		return 2*pi*(self.sma**3/self.primary.mass/g)**.5

	def periapsis(self) -> float:
		return (1-self.ecc)*self.sma

	def apoapsis(self) -> float:
		return (1+self.ecc)*self.sma


def rporbit(primary, sma: float) -> Orbit:
	# max ecc = mercury; max inc = mercury
	return Orbit(primary, sma, uniform(0, .21), uniform(0, .1223), uniform(0, 2*pi), uniform(0, 2*pi), uniform(0, 2*pi))
