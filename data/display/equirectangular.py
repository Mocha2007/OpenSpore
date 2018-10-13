from math import pi
import sys
sys.path.append('./data')
from galaxy import Galaxy
from border import starmapborder
from constants import xyz2phitheta
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
		# plane angles
		phi, theta = xyz2phitheta(star[0])
		# convert from -pi:pi to screen size
		phi *= size[0]/2/pi * zoom/defaultzoom
		theta *= size[1]/pi * zoom/defaultzoom
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
