from constants import ishab
from toxic import istox
from random import random, randint


class Life:
	def __init__(self, **kwargs):
		self.name = kwargs['name']


def rlife() -> Life:
	return Life(name='dingus')


def lifegen(p) -> list:
	"""p of type Planet"""
	if not ishab(p) or istox(p):
		# see https://en.wikipedia.org/wiki/Drake_equation#Fraction_of_the_above_that_actually_go_on_to_develop_life,_fl
		return []
	# only 50/50 for when it is hab
	# t1
	i = 0
	while 1:
		if random() < .5:
			return [rlife() for _ in range(randint(6*i+1, 6*i+6))]
		i += 1 # this represents "Tier n-1" sporelike worlds
