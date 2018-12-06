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
# print(len(sets['.']), 'neutral starnames')


def main(star) -> str:
	sources = set(sets['.']) # gotta make it a new set
	star_type = star.type if len(star.type) == 1 else 'X'
	if star_type in sets:
		sources = sources.union(sets[star_type])
	return choice(list(sources))
