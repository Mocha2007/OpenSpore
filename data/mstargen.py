from random import random


def main() -> float:
	# https://www.nasa.gov/vision/universe/starsgalaxies/brown_dwarf_detectives.html
	# "There are probably around the same number of brown dwarfs as stars within the immediate solar neighborhood."
	# ie. 50%
	# https://www.centauri-dreams.org/2017/07/07/how-many-brown-dwarfs-in-the-milky-way/
	# "For every ten stars there are five brown dwarfs"
	# ie. 33%
	if .4 < random(): # the float is the chance of becoming a brown dwarf (kinda)
		# star will fall approximately within normal distribution
		n = 13
	else:
		# star will have an ~80% chance of being a brown dwarf
		n = 80
	return 1/(n*random()**1.1)
