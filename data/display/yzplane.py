import sys
sys.path.append('./data')
from galaxy import Galaxy
from constants import delta


def main(size: (int, int), galaxy: Galaxy, center: (float, float, float), zoom: float) -> list:
	# main
	starList = galaxy.stars
	screen_center = size[0]//2, size[1]//2

	# make list
	starList2 = []
	for star in starList:
		d = delta(center, star[0])
		d = tuple(map(lambda x: x*zoom, d))[1:]
		coords = tuple(map(sum, zip(screen_center, d)))
		coords = tuple(map(int, coords))
		if not (0 <= coords[0] <= size[0] and 0 <= coords[1] <= size[1]):
			continue
		starList2.append(
			# coords, star
			(coords, star[1])
		)
	return starList2
