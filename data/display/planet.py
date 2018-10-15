from math import cos, sin
import sys
sys.path.append('./data')
from points import Points

# equirectangular projection, with the origin as the source
showscale = False


def main(radius: int, pointmap: Points, center: (int, int)) -> list:
	# main
	starList = pointmap.points
	starList.sort(key=lambda w: cos(w[0][0])*cos(w[0][1]))

	# make list
	starList2 = []
	for star in starList:
		# plane angles
		phi, theta = star[0]
		if cos(phi)*cos(theta) < 0:
			continue
		# orthographic transform
		x = cos(theta)*sin(phi)
		y = sin(theta)
		# convert from -1:1 to screen size
		x *= radius
		y *= radius
		# center
		x += center[0]
		y += center[1]
		# finalize
		coords = int(x), int(y)
		starList2.append(
			# coords, star
			(coords, star[1])
		)
	return starList2
