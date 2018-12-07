from random import random
from constants import m_star, m_sun


def main() -> float:
	# https://www.nasa.gov/vision/universe/starsgalaxies/brown_dwarf_detectives.html
	# "There are probably around the same number of brown dwarfs as stars within the immediate solar neighborhood."
	# ie. 50%
	# https://www.centauri-dreams.org/2017/07/07/how-many-brown-dwarfs-in-the-milky-way/
	# "For every ten stars there are five brown dwarfs"
	# ie. 33%
	n = m_sun/m_star # min size ~ .075 solar masses
	bd_chance = .25 # star will have an ~25% chance of being a brown dwarf
	if bd_chance < random(): # main sequence
		# star will fall approximately within normal distribution
		e = 1.5
	else: # brown dwarfs
		e = -.2
	return 1/(n*random()**e)
