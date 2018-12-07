from random import random


def main() -> float:
	# https://www.nasa.gov/vision/universe/starsgalaxies/brown_dwarf_detectives.html
	# "There are probably around the same number of brown dwarfs as stars within the immediate solar neighborhood."
	# ie. 50%
	# https://www.centauri-dreams.org/2017/07/07/how-many-brown-dwarfs-in-the-milky-way/
	# "For every ten stars there are five brown dwarfs"
	# ie. 33%
	if .3 < random(): # the float is the chance of becoming a brown dwarf (kinda)
		# star will fall approximately within normal distribution
		n = 9
		# 13 -> .777 .818 .784
		# 12 -> .783 .778 .789
		# 11 -> .744 .779 .800 .774 .783
		# 10 -> .755 .733 .767 .747 .731
	else:
		# star will have an ~80% chance of being a brown dwarf
		n = 80
	return 1/(n*random()**1.1)
