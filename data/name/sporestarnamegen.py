from random import choice
import sys
sys.path.append('./data')
from starcalc import Star

alphabet = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'


def main() -> str:
	name = ''
	for i in range(3):
		name += choice(alphabet)
	name = name.upper() + '-'
	for i in range(5):
		name += choice(digits)
	return name + choice(alphabet)
