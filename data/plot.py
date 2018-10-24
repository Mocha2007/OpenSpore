import sys
import pygame
from math import log10
from galaxy import Galaxy
from points import Points
from constants import density
sys.path.append('./data/mapmode')
from planettype import planet as planetcolor

radius = 5
size = 1024, 1024


# SAMPLE AXIS FUNCTIONS
def p_m(p) -> float:
	return p.mass


def p_r(p) -> float:
	return p.radius


def p_rho(p) -> float:
	return density(p.mass, p.radius)


def p_rgb(p) -> (int, int, int):
	return planetcolor(p).rgb()


# main
def locate(point: (float, float), minimum: (float, float), maximum: (float, float)) -> (int, int):
	xrange = maximum[0] - minimum[0]
	yrange = maximum[1] - minimum[1]
	point = list(point)
	point[0] -= minimum[0]
	point[1] -= minimum[1]
	point[0] /= xrange
	point[1] /= yrange
	# flip y axis
	point[1] = 1-point[1]
	# now convert from (0, 1) -> (0, size)
	point[0] *= size[0]
	point[1] *= size[1]
	return round(point[0]), round(point[1])


def planet(g: Galaxy, xaxis, yaxis, **options) -> Points:
	# options
	if 'xlog' not in options:
		options['xlog'] = False
	if 'ylog' not in options:
		options['ylog'] = False
	if 'point' not in options:
		options['point'] = '.'

	# pygame setup
	pygame.init()
	screen = pygame.display.set_mode(size)
	screen.fill((0, 0, 0))
	ptype = options['point']

	# set construction
	array = []
	for _, system in g.stars:
		for _, p in system.bodies:
			coords = [xaxis(p), yaxis(p)]
			# log plotting
			if options['xlog']:
				coords[0] = log10(coords[0])
			if options['ylog']:
				coords[1] = log10(coords[1])
			color = planetcolor(p)
			array.append((coords, color))
	# get minx, miny, maxx, maxy
	minx = min(array, key=lambda x: x[0][0])[0][0]
	miny = min(array, key=lambda x: x[0][1])[0][1]
	maxx = max(array, key=lambda x: x[0][0])[0][0]
	maxy = max(array, key=lambda x: x[0][1])[0][1]
	open('plot.txt', 'w+').write(str(((minx, maxx), (miny, maxy))))
	# display
	for coords, color in array:
		place = locate(coords, (minx, miny), (maxx, maxy))
		c = color.rgb()
		if ptype == '.':
			screen.set_at(place, c)
		elif ptype == '+':
			# horizontal
			pygame.draw.line(screen, c, (place[0]-radius, place[1]), (place[0]+radius, place[1]))
			# vertical
			pygame.draw.line(screen, c, (place[0], place[1]-radius), (place[0], place[1]+radius))
		elif ptype == 'o':
			pygame.draw.circle(screen, c, place, radius)
		elif ptype == 'x':
			pygame.draw.rect(screen, c, (place[0]-radius, place[1]-radius, radius*2, radius*2))
	# save graph
	pygame.display.flip()
	pygame.image.save(screen, 'plot.png')
