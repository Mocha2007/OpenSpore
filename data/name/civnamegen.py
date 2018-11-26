from random import choice, randint, random
import sys
sys.path.append('./data')
from constants import rword


def forename(n: str):
	return lambda name: n + ' of ' + name


def hindname(n: str):
	return lambda name: name + ' ' + n


def bothname(n: str):
	return forename(n) if random() < .5 else hindname(n)


def neithername(n: str):
	return lambda name: name


def aroundname(n: (str, str)):
	return lambda name: n(0) + name + n(1)


# type, string
types = (
	(neithername, ''),
	(bothname, 'Commonwealth'),
	(bothname, 'Confederacy'),
	(bothname, 'Confederation'),
	(bothname, 'Empire'),
	(bothname, 'Federation'),
	(forename, 'Grand Duchy'),
	(bothname, 'Kingdom'),
	(bothname, 'Principality'),
	(bothname, 'Republic'),
	(bothname, 'State'),
	(bothname, 'Technate'),
	(aroundname, ('United', 'States')),
)


def main() -> str:
	f, t = choice(types)
	primary = rword(randint(4, 13)).title() # Liechtenstein = 13
	return f(t)(primary)
