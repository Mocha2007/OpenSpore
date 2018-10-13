from sys import exit
from time import sleep
from importlib.machinery import SourceFileLoader
from math import log10, pi
import pygame

# constants
starRadius = 2 # px
darkColor = 8, 42, 54
lightColor = 40, 72, 95
lighterColor = 80, 144, 190
# may change later on as user does things
focus = 0, 0, 0
zoom = 15
focusNew = focus
currentmapmode = 0
currentprojmode = 0

# pygame setup
pygame.init()
size = 1280, 640
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
		d[ll[0]] = tuple(ll[1:])
	return d


cfg = cfg2dict('settings.cfg')

# load galaxy module
galaxy = SourceFileLoader('galaxy', 'data/'+cfg['galaxygen'][0]+'.py').load_module()

# load stargen module
stargen = SourceFileLoader('stargen', 'data/'+cfg['stargen'][0]+'.py').load_module()

# load starnamegen module
starnamegen = SourceFileLoader('starnamegen', 'data/name/'+cfg['starnamegen'][0]+'.py').load_module()

# load planetnamegen module
planetnamegen = SourceFileLoader('planetnamegen', 'data/name/'+cfg['planetnamegen'][0]+'.py').load_module()

# load moonnamegen module
moonnamegen = SourceFileLoader('moonnamegen', 'data/name/'+cfg['moonnamegen'][0]+'.py').load_module()

# load display module
display = SourceFileLoader('display', 'data/display/'+cfg['displaymode'][0]+'.py').load_module()

# load mapmode module
mapmode = SourceFileLoader('mapmode', 'data/mapmode/'+cfg['mapmode'][0]+'.py').load_module()

# load system module
systemclass = SourceFileLoader('systemclass', 'data/'+cfg['systemclass'][0]+'.py').load_module()

# load constants module
common = SourceFileLoader('common', 'data/constants.py').load_module()

# load resource module
resgen = SourceFileLoader('resgen', 'data/resources/'+cfg['resourcegen'][0]+'.py').load_module()


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
		tlabel = font.render(text[i], 1, (255, 255, 255))
		screen.blit(tlabel, (ul[0]+5, ul[1]+20*i))
		if i: # draw line above
			pygame.draw.line(screen, lightColor, (ul[0]+5, ul[1]+20*i), (ul[0]+width-5, ul[1]+20*i))
	# planet mapmode
	for i, planet in system.bodies:
		coords = ul[0]+35, ul[1]+20*(i+1)+10
		try:
			planetcolor = mapmode.planet(planet)
		except AttributeError:
			planetcolor = common.grey
		col = planetcolor.r, planetcolor.g, planetcolor.b
		pygame.draw.circle(screen, col, coords, 6)


def scale() -> float:
	if not display.showscale:
		return 1
	# get desired power of ten
	desired = 10**round(log10(100/zoom))
	pygame.draw.line(screen, lighterColor, (10, 10), (10 + zoom*desired, 10), 4)
	distlabel = font.render(str(desired)+' ly', 1, lighterColor)
	screen.blit(distlabel, (10, 10))
	return desired


def drawradius(desired: float):
	if not display.showscale:
		return 1
	# rect = (size[0]//2, size[1]//2) (for pygame.draw.circle)
	center = (size[0]//2, size[1]//2)
	dz = desired*zoom
	rect = center[0]-dz, center[1]-dz/3**.5, dz*2, dz*2/3**.5
	pygame.draw.ellipse(screen, lighterColor, rect, 4)
	distlabel = font.render(str(desired)+' ly', 1, lighterColor)
	screen.blit(distlabel, (center[0]-dz+5, center[1]-10))


def changemap(n: int):
	global currentmapmode
	global mapmode
	currentmapmode += n
	currentmapmode %= len(cfg['mapmode'])
	mapmode = SourceFileLoader('mapmode', 'data/mapmode/'+cfg['mapmode'][currentmapmode]+'.py').load_module()


def changeproj(n: int):
	global currentprojmode
	global display
	currentprojmode += n
	currentprojmode %= len(cfg['displaymode'])
	display = SourceFileLoader('display', 'data/display/'+cfg['displaymode'][currentprojmode]+'.py').load_module()


# main
g = galaxy.Galaxy(stargen.main, starnamegen.main, planetnamegen.main, moonnamegen.main, systemclass.System, resgen.main)
refresh()

mousePos = 0, 0
mousePosNew = 0, 0
delta = 0, 0
deltaNew = 0, 0
middleRadius = 1
while 1:
	screen.fill((0, 0, 0))
	# draw radii
	try:
		drawradius(middleRadius/10)
	except ValueError:
		pass
	drawradius(middleRadius)
	drawradius(middleRadius*10)
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
			shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
			direction = 1 if shift else -1
			if event.key == pygame.K_m: # mapmode
				changemap(direction)
			elif event.key == pygame.K_p: # projection
				changeproj(direction)
	# pressed keys
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_DOWN]:
		g.anyrotatey(-pi/45)
	if pressed[pygame.K_LEFT]:
		g.anyrotatez(pi/45)
	if pressed[pygame.K_RIGHT]:
		g.anyrotatez(-pi/45)
	if pressed[pygame.K_UP]:
		g.anyrotatey(pi/45)
	if pressed[pygame.K_KP4]:
		g.anyrotatex(pi/45)
	if pressed[pygame.K_KP6]:
		g.anyrotatex(-pi/45)
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
			starinfo(*star)
			break
	# scale
	middleRadius = scale()
	# mapmode/proj disp
	label = font.render('Mapmode: '+cfg['mapmode'][currentmapmode], 1, lighterColor)
	screen.blit(label, (0, size[1]-40))
	label = font.render('Projection: '+cfg['displaymode'][currentprojmode], 1, lighterColor)
	screen.blit(label, (0, size[1]-20))
	# finish
	refresh()
	sleep(1/30) # reduce cpu consumption
