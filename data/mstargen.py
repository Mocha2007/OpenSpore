from random import random


def main() -> float:
	# https://www.nasa.gov/vision/universe/starsgalaxies/brown_dwarf_detectives.html
	# "There are probably around the same number of brown dwarfs as stars within the immediate solar neighborhood."
	if random() > .5:
		# star will fall approximately within normal distribution
		n = 13
	else:
		# star will have an ~80% chance of being a brown dwarf
		n = 80
	return 1/(n*random()**1.1)
