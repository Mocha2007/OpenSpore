from random import choice, randint
import sys
sys.path.append('./data')
from constants import rword

types = (
	('', ''),
)


def main() -> str:
	pre, post = choice(types)
	primary = rword(randint(4, 13)) # Liechtenstein = 13
	name = ' '.join([pre, primary.title(), post])
	return name
