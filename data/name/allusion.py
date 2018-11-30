from random import choice
from json import load

names = load(open('data/name/allusion.json'))


def main(star) -> str:
	sources = names['Any']
	if star.type in names:
		sources += names[star.type]
	return choice(sources)
