from math import cos, pi, sin
import sys
sys.path.append('./data')
from constants import grey
from system import System
from starcalc import Star
from resource import Resource

resolution = 400

borderResource = Resource({
	'name': 'Border',
	'color': grey,
	'value': 0
})


# map tools
def border(*_, **__):
	return 'Border'


def borderresourcegen(*_, **__):
	return [borderResource]


greystar = Star(1, border)
greystar.type = border()
greysys = System(greystar, border, border, borderresourcegen)
greysys.bodies = []
starmapborder = []
# equator
for i in range(resolution):
	site = sin(i/resolution * 2*pi), cos(i/resolution * 2*pi), 0
	starmapborder.append(
		(site, greysys)
	)
# meridians
for i in range(resolution):
	site = sin(i/resolution * 2*pi), 0, cos(i/resolution * 2*pi)
	starmapborder.append(
		(site, greysys)
	)
# halfway meridians
for i in range(resolution):
	site = 0, sin(i/resolution * 2*pi), cos(i/resolution * 2*pi)
	starmapborder.append(
		(site, greysys)
	)
# left meridian???
for i in range(resolution//2, resolution):
	site = sin(i/resolution * 2*pi)*(resolution-1)/resolution, sin(i/resolution * 2*pi)/resolution, cos(i/resolution * 2*pi)
	starmapborder.append(
		(site, greysys)
	)
