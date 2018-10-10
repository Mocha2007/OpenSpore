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

# load display module
display = SourceFileLoader('display', 'data/display/'+cfg['displaymode']+'.py').load_module()

# load mapmode module
mapmode = SourceFileLoader('mapmode', 'data/mapmode/'+cfg['mapmode']+'.py').load_module()


def starinfo(coords: (int, int), star):
	# draw main rectangle
	pygame.draw.rect(screen, (8, 42, 54), (coords[0]+20, coords[1]+25, 150, 50))
	# name
	label = font.render(star.name, 1, (255, 255, 255))
	screen.blit(label, (coords[0]+25, coords[1]+25))
	# find star
	site = focus
	for s in g.stars:
		if s[1].id == star.id:
			site = s[0]
			break
	# distance from home
	label = font.render('Distance: '+str(round(galaxy.dist(focus, site), 2))+' ly', 1, (255, 255, 255)) # todo replace 69 with
	screen.blit(label, (coords[0]+25, coords[1]+45))


# main
g = galaxy.Galaxy(stargen.main, starnamegen.main)
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
	sleep(1/20) # reduce cpu consumption
