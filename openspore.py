from sys import exit
from time import sleep
from importlib.machinery import SourceFileLoader
import pygame

# constants
starRadius = 2 # px
focus = 0, 0, 0 # may change later on as user does things
zoom = 15
focusNew = focus
darkColor = 8, 42, 54
lightColor = 40, 72, 95

# pygame setup
pygame.init()
size = 1280, 720
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip
font = pygame.font.SysFont("trebuchetms", 15)
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('OpenSpore')


# setup
def cfg2dict(loc: str) -> dict:
	f = open(loc, 'r').read()
	d = {}
	for line in f.split('\n'):
		ll = line.split(' ')
		d[ll[0]] = ll[1]
	return d


cfg = cfg2dict('settings.cfg')

# load galaxy module
galaxy = SourceFileLoader('galaxy', 'data/'+cfg['galaxygen']+'.py').load_module()

# load stargen module
stargen = SourceFileLoader('stargen', 'data/'+cfg['stargen']+'.py').load_module()

# load starnamegen module
starnamegen = SourceFileLoader('starnamegen', 'data/name/'+cfg['starnamegen']+'.py').load_module()

# load planetnamegen module
planetnamegen = SourceFileLoader('planetnamegen', 'data/name/'+cfg['planetnamegen']+'.py').load_module()

# load moonnamegen module
moonnamegen = SourceFileLoader('moonnamegen', 'data/name/'+cfg['moonnamegen']+'.py').load_module()

# load display module
display = SourceFileLoader('display', 'data/display/'+cfg['displaymode']+'.py').load_module()

# load mapmode module
mapmode = SourceFileLoader('mapmode', 'data/mapmode/'+cfg['mapmode']+'.py').load_module()

# load system module
systemclass = SourceFileLoader('systemclass', 'data/'+cfg['systemclass']+'.py').load_module()

# load constants module
common = SourceFileLoader('common', 'data/constants.py').load_module()


def starinfo(coords: (int, int), system):
	width = 175
	sysstar = system.star
	# upper left of box
	ul = coords[0]+20, coords[1]+25
	# name
	text = [sysstar.name]
	# find star
	site = focus
	for s in g.stars:
		if s[1].star.id == sysstar.id:
			site = s[0]
			break
	# list planets
	for _, planet in system.bodies:
		text.append(' '*8+planet.name)
	# distance from home
	text.append('Distance: '+str(round(common.dist(focus, site), 2))+' ly')
	# draw highlight circle
	pygame.draw.circle(screen, lightColor, (ul[0]-20, ul[1]-25), 8, 1)
	# draw main rectangle
	pygame.draw.rect(screen, darkColor, (ul[0], ul[1], width, 20 * len(text)))
	# display label
	for i in range(len(text)):
		label = font.render(text[i], 1, (255, 255, 255))
		screen.blit(label, (ul[0]+5, ul[1]+20*i))
		if i: # draw line above
			pygame.draw.line(screen, lightColor, (ul[0]+5, ul[1]+20*i), (ul[0]+width-5, ul[1]+20*i))


def scale():
	pygame.draw.line(screen, lightColor, (10, 10), (110, 10), 2)
	label = font.render(str(100/zoom)+' ly', 1, lightColor)
	screen.blit(label, (10, 10))


# main
g = galaxy.Galaxy(stargen.main, starnamegen.main, planetnamegen.main, moonnamegen.main, systemclass.System)
refresh()

mousePos = 0, 0
mousePosNew = 0, 0
delta = 0, 0
deltaNew = 0, 0
while 1:
	screen.fill((0, 0, 0))
	# stars
	displaylist = display.main(size, g, tuple(map(sum, zip(delta, deltaNew))), zoom)
	for element in displaylist:
		colorOfStar = mapmode.main(element[1])
		c = colorOfStar.r, colorOfStar.g, colorOfStar.b
		pygame.draw.circle(screen, c, element[0], starRadius)
	# window
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				zoom *= 2
			elif event.button == 5:
				zoom /= 2
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				g = g.rotate(1)
			elif event.key == pygame.K_RIGHT:
				g = g.rotate(-1)
			elif event.key == pygame.K_UP:
				g = g.vrotate(1)
			elif event.key == pygame.K_DOWN: # fixme - code runs as if -1 were 2... no idea why
				pass # g = g.vrotate(-1)
	# mousedown?
	if pygame.mouse.get_pressed()[0]: # left click enabled
		mousePosNew = pygame.mouse.get_pos()
		deltaNew = tuple(map(lambda x: (x[1]-x[0])/zoom, zip(mousePos, mousePosNew)))
	else:
		# reset
		mousePos = pygame.mouse.get_pos()
		delta = tuple(map(sum, zip(delta, deltaNew)))
		# reset
		mousePosNew = pygame.mouse.get_pos()
		deltaNew = 0, 0
	# infobox
	for star in displaylist:
		if common.dist(pygame.mouse.get_pos(), star[0]) < starRadius*4:
			starinfo(star[0], star[1])
			break
	# scale
	scale()
	# finish
	refresh()
	sleep(1/30) # reduce cpu consumption
