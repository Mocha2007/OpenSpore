from random import choice, randint, random
import sys
sys.path.append('./data')
from constants import rword

types = (
	'Confederation',
	'Empire',
	'Federation',
	'Kingdom',
	'Principality',
	'Republic',
	'Technate',
)


def main() -> str:
	t = choice(types)
	primary = rword(randint(4, 13)) # Liechtenstein = 13
	if random() < .5:
		return primary.title() + ' ' + t
	return t + ' of ' + primary.title()
