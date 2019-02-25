from math import log10

stp = 273.15, 1e5


class Chem:
	def __init__(self, **data):
		self.name = data['name']
		try:
			self.triple = data['triple']
			assert isinstance(self.triple, tuple)
			self.critical = data['critical']
			assert isinstance(self.critical, tuple)
		except IndexError:
			pass
		self.melt = data['melt']
		assert isinstance(self.melt, float)
		self.freeze = self.melt
		self.boil = data['boil']
		assert isinstance(self.boil, float)

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
		if stp[0] < t: # upper part of the liq-gas boundary
			slope = log10(self.critical[1] - stp[1]) / (self.critical[0] - self.boil)
		else: # lower part of the liq-gas boundary
			slope = log10(stp[1] - self.triple[1]) / (self.boil - self.triple[0])
		yintercept = log10(stp[1]) - slope * self.boil
		f = lambda x: slope * x + yintercept
		# upper right
		if f(t) < log10(p):
			return 'liquid'
		# lower right
		return 'gas'
