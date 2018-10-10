import sys
sys.path.append('./data')
from galaxy import Galaxy
from constants import delta

# |+Z /+Y
# |  /
# | /
# |/
#  \
#   \
#    \+X


def main(size: (int, int), galaxy: Galaxy, center: (float, float, float), zoom: float) -> list:
	# main
	starList = galaxy.stars
	screen_center = size[0]//2, size[1]//2

	# make list
	starList2 = []
	for star in starList:
		d = delta(center, star[0])
		d = tuple(map(lambda x: x*zoom, d)) # absolute pixel difference... now, to convert it to rotation...
		sx, sy = screen_center
		# todo factor in dx
		sx += d[0] * 3**-.5
		sy -= d[0] / 2
		# todo factor in dy
		sx += d[1] * 3**-.5
		sy += d[1] / 2
		# todo factor in dz
		sy += d[2] * 3**-.5
		# finalize
		coords = int(sx), int(sy)
		if not (0 <= coords[0] <= size[0] and 0 <= coords[1] <= size[1]):
			continue
		starList2.append(
			# coords, star
			(coords, star[1])
		)
	return starList2
