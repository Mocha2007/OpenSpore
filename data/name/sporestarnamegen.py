from random import choice
import sys
sys.path.append('./data')
from constants import alphabet, digits


def main(*_) -> str:
	name = ''
	for _ in range(3):
		name += choice(alphabet)
	name = name.upper() + '-'
	for _ in range(5):
		name += choice(digits)
	return name + choice(alphabet)
