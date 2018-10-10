from sys import exit
from time import sleep
from importlib.machinery import SourceFileLoader
import pygame

# constants
starRadius = 2 # px
focus = 0, 0, 0 # may change later on as user does things
focusNew = focus

# pygame setup
pygame.init()
size = 1280, 720
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip
font = pygame.font.SysFont("trebuchetms", 15)


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

# load benis module (for test names)
benis = SourceFileLoader('benis', 'data/name/benis.py').load_module()


def starinfo(coords: (int, int), system):
	width = 175
	star = system.star
	# upper left of box
	ul = coords[0]+20, coords[1]+25
	# name
	text = [star.name]
	# find star
	site = focus
	for s in g.stars:
		if s[1].star.id == star.id:
			site = s[0]
			break
	# list planets
	for _, planet in system.bodies:
		text.append(' '*8+planet.name)
	# distance from home
	text.append('Distance: '+str(round(galaxy.dist(focus, site), 2))+' ly')
	# draw main rectangle
	pygame.draw.rect(screen, (8, 42, 54), (ul[0], ul[1], width, 20 * len(text)))
	# display label
	for i in range(len(text)):
		label = font.render(text[i], 1, (255, 255, 255))
		screen.blit(label, (ul[0]+5, ul[1]+20*i))
		if i: # draw line above
			pygame.draw.line(screen, (40, 72, 95), (ul[0]+5, ul[1]+20*i), (ul[0]+width-5, ul[1]+20*i))


# main
g = galaxy.Galaxy(stargen.main, starnamegen.main, planetnamegen.main, moonnamegen.main) # todo replace namegens
refresh()

# todo add click + drag
mousePos = 0, 0
mousePosNew = 0, 0
while 1:
	screen.fill((0, 0, 0))
	# stars
	displaylist = display.main(size, g, focusNew)
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
	# mousedown?
	if pygame.mouse.get_pressed()[0]: # left click enabled
		mousePosNew = pygame.mouse.get_pos()
		focusNew = tuple(map(lambda x: (x[1]-x[0])/display.zoom, zip(mousePos, mousePosNew)))
		# shift focus
		focusDelta = focusNew[0], focusNew[1], 0
		focusNew = tuple(map(sum, zip(focus, focusDelta)))
	else:
		# reset
		mousePosNew = pygame.mouse.get_pos()
		mousePos = pygame.mouse.get_pos()
		focus = focusNew
	for star in displaylist:
		if galaxy.dist(pygame.mouse.get_pos(), star[0]) < starRadius*4:
			starinfo(star[0], star[1])
			break
	refresh()
	sleep(1/30) # reduce cpu consumption
