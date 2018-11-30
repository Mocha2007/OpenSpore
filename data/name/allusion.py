from random import choice
from json import load

# Generates ~1000 stars so need at least that many names
names = load(open('data/name/allusion.json', encoding="utf-8"))
sets = {}
for _, name_list in names.items():
	for name, types in name_list.items():
		for char in types:
			if char in sets:
				sets[char].add(name)
			else:
				sets[char] = {name}


def main(star) -> str:
	sources = set(sets['.']) # gotta make it a new set
	if star.type in sets:
		sources = sources.union(sets[star.type])
	return choice(list(sources))
