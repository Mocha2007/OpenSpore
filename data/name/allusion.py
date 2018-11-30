from random import choice
from json import load

names = load(open('data/name/allusion.json', encoding="utf-8"))
universal = list(filter(lambda x: x[0] != '_', names['Any']))


def main(star) -> str:
	sources = universal[:]
	if star.type in names:
		sources += names[star.type]
	sources = list(set(sources))
	return choice(sources)
