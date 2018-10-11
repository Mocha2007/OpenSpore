import sys
sys.path.append('./data')
from galaxy import Galaxy
from constants import delta
showscale = False


def main(size: (int, int), galaxy: Galaxy, screendelta: (int, int), zoom: float) -> list:
	# main
	center = 0, 0, 0
	screendelta = tuple(map(lambda x: x*zoom, screendelta))
	starList = galaxy.stars
	screen_center = size[0]//2, size[1]//2

	# make list
	starList2 = []
	for star in starList:
		d = delta(center, star[0])
		d = tuple(map(lambda x: x*zoom, d))
		coords = tuple(map(sum, zip(screen_center, d, screendelta)))
		coords = tuple(map(int, coords))
		if not (0 <= coords[0] <= size[0] and 0 <= coords[1] <= size[1]):
			continue
		starList2.append(
			# coords, star
			(coords, star[1])
		)
	return starList2
