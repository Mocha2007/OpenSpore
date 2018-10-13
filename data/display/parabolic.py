from math import atan2, cos, pi
import sys
sys.path.append('./data')
from galaxy import Galaxy
from border import starmapborder
# equirectangular projection, with the origin as the source

showscale = False
defaultzoom = 15 # fixme from openspore.py


def main(size: (int, int), galaxy: Galaxy, screendelta: (int, int), zoom: float) -> list:
	# main
	screendelta = tuple(map(lambda w: int(w*zoom), screendelta))
	starList = galaxy.stars + starmapborder
	screen_center = size[0]//2, size[1]//2

	# make list
	starList2 = []
	for star in starList:
		x, y, z = star[0]
		# plane angles
		phi = atan2(y, x)/pi # from -1 to 1
		theta = atan2(z, (x**2+y**2)**.5)/pi # from -1 to 1
		# sinusoidal conversion for x
		phi *= .25-theta**2
		# convert from -1:1 to screen size
		phi *= size[0]*2 * zoom/defaultzoom
		theta *= size[1] * zoom/defaultzoom
		# center
		phi += screen_center[0]
		theta += screen_center[1]
		# finalize
		coords = int(phi) + screendelta[0], int(theta) + screendelta[1]
		if not (0 <= coords[0] <= size[0] and 0 <= coords[1] <= size[1]):
			continue
		starList2.append(
			# coords, star
			(coords, star[1])
		)
	return starList2
