import sys
sys.path.append('./data')
from starcalc import Star

# constants
galaxyWidth = 15


class Galaxy: # no type annotation since function can't be annotated
	def __init__(self, stargen, starnamegen, planetnamegen, moonnamegen, SystemClass):
		# generate home star
		home = (0, 0, 0), SystemClass(Star(1, 'Home'), planetnamegen, moonnamegen)
		starList = [home]
		# generate stars until ten failed placements in a row
		for x in range(galaxyWidth):
			for y in range(galaxyWidth):
				for z in range(galaxyWidth):
					if (x, y, z) != (0, 0, 0):
						# conditionals
						if x <= galaxyWidth/2 and z > x:
							continue
						if x > galaxyWidth/2 and z > galaxyWidth - x:
							continue
						if y <= galaxyWidth/2 and z > y:
							continue
						if y > galaxyWidth/2 and z > galaxyWidth - y:
							continue
						# main
						newStar = Star(stargen(), starnamegen())
						starList.append(
							((x, y, z), SystemClass(newStar, planetnamegen, moonnamegen))
						)
		self.stars = starList
