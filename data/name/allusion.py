from random import choice
from json import load
from iaustarnamegen import main as backup

names = load(open('data/name/allusion.json'))


def main(star) -> str:
	try:
		return choice(names[star.type])
	except KeyError:
		return backup()
