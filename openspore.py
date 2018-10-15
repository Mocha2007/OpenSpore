from sys import exit
from time import sleep
from importlib.machinery import SourceFileLoader
from math import log10, pi
from time import time
import pygame

# constants
starRadius = 2 # px
darkColor = 8, 42, 54
lightColor = 40, 72, 95
lighterColor = 80, 144, 190
planetkeys = (
	pygame.K_1,
	pygame.K_2,
	pygame.K_3,
	pygame.K_4,
	pygame.K_5,
	pygame.K_6,
	pygame.K_7,
	pygame.K_8,
	pygame.K_9,
	pygame.K_0
)
globeperiod = 15 # s
maxmoonlist = 8
# may change later on as user does things
focus = 0, 0, 0
zoom = 15
currentmapmode = 0
currentprojmode = 0
moonskip = 0


# setup
def cfg2dict(loc: str) -> dict:
	f = open(loc, 'r').read()
	d = {}
	for line in f.split('\n'):
		ll = line.split(' ')
		d[ll[0]] = tuple(ll[1:])
	return d


cfg = cfg2dict('settings.cfg')

# pygame setup
pygame.init()
# size = 1280, 640
size = int(cfg['size'][0]), int(cfg['size'][1])
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip
# font = pygame.font.SysFont("trebuchetms", 15)
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('OpenSpore')

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

# load planetmap module
planetmap = SourceFileLoader('planetmap', 'data/display/planet.py').load_module()

# load surface module
surface = SourceFileLoader('surface', 'data/surface/'+cfg['surface'][0]+'.py').load_module()

# load mapmode module
mapmode = SourceFileLoader('mapmode', 'data/mapmode/'+cfg['mapmode'][0]+'.py').load_module()

# load system module
systemclass = SourceFileLoader('systemclass', 'data/'+cfg['systemclass'][0]+'.py').load_module()

# load constants module
common = SourceFileLoader('common', 'data/constants.py').load_module()
font = common.font

# load resource module
resgen = SourceFileLoader('resgen', 'data/resources/'+cfg['resourcegen'][0]+'.py').load_module()


def starinfo(coords: (int, int), system):
	width = 175
	sysstar = system.star
	# upper left of box
	ul = coords[0]+20, coords[1]+25
	# name
	text = sysstar.name
	# find star
	site = focus
	for ss in g.stars:
		if ss[1].star.id == sysstar.id:
			site = ss[0]
			break
	# list planets
	for _, planet in system.bodies:
		text += '\n\t\t'+planet.name
	# distance from home
	text += '\nDistance: '+str(round(common.dist(focus, site), 2))+' ly'
	# draw highlight circle
	pygame.draw.circle(screen, lightColor, (ul[0]-20, ul[1]-25), 8, 1)
	# print text
	common.text(text, screen, (ul[0], ul[1], ul[0]+width, ul[1]+175), darkColor, lightColor)
	# planet mapmode
	for i, planet in system.bodies:
		coords = ul[0]+35, ul[1]+20*(i+1)+10
		try:
			planetcolor = mapmode.planet(planet)
		except AttributeError:
			planetcolor = common.grey
		col = planetcolor.r, planetcolor.g, planetcolor.b
		pygame.draw.circle(screen, col, coords, 6)


def showsystem():
	global focusPlanet
	global moonskip
	ss = focusSystem
	# display size
	w = size[0]//4
	h = w//2
	ul = size[0]-w, size[1]-h # aligned to bottom right
	centerh = h//2 + ul[1]
	# name, for upper left corner
	# text = s.name
	# evenly space planets
	space = w//(len(ss.bodies)+1)
	# draw rect
	pygame.draw.rect(screen, darkColor, (ul[0], ul[1], w, h))
	# draw rect border
	pygame.draw.rect(screen, lightColor, (ul[0], ul[1], w, h), 1)
	# label
	common.text(ss.star.name+' System', screen, (ul[0], ul[1]+5, ul[0]+1, 0), darkColor, lightColor)
	# place sun
	# try:
	# 	starcolor = mapmode.main(ss)
	# except AttributeError:
	# 	starcolor = common.grey
	# col = starcolor.r, starcolor.g, starcolor.b
	# pygame.draw.circle(screen, col, (ul[0]+space, centerh), 18)
	# planet mapmode
	for i, planet in ss.bodies:
		coords = ul[0] + (i+1)*space, centerh
		try:
			planetcolor = mapmode.planet(planet)
		except AttributeError:
			planetcolor = common.grey
		radius = round(planet.mass**(1/6) / 2e3)
		col = planetcolor.r, planetcolor.g, planetcolor.b
		pygame.draw.circle(screen, col, coords, radius)
		# label
		textcolor = (255, 0, 0) if i == focusPlanet else (255, 255, 255)
		tlabel = font.render(str(i+1), 1, textcolor)
		screen.blit(tlabel, (coords[0]-4, size[1]-20))
		# hot? cold? small?
		warningcoords = coords[0]-2, size[1]-40
		haswarning = False
		if 373 < planet.temp:
			tlabel = font.render('!', 1, (255, 192, 128))
			haswarning, warnname = True, 'Boiling'
		elif planet.temp < 273:
			tlabel = font.render('!', 1, (128, 192, 255))
			haswarning, warnname = True, 'Freezing'
		elif not common.m_airless < planet.mass < common.m_gg:
			tlabel = font.render('!', 1, (128, 128, 128))
			haswarning = True
			warnname = 'Airless' if planet.mass < common.m_airless else 'Giant'
		if haswarning:
			screen.blit(tlabel, warningcoords)
		# habitability info if mouse over
		mousePos = pygame.mouse.get_pos()
		warningcoords = warningcoords[0], warningcoords[1] + 10
		if common.dist(mousePos, warningcoords) <= 5 and haswarning:
			# hover info
			common.text(warnname, screen, (warningcoords[0], warningcoords[1]-20, warningcoords[0]+75, 0), darkColor, lightColor)
		# planet info if mouse over
		elif common.dist(mousePos, coords) <= radius:
			# hover info
			t = planet.name
			t += '\n'+str(round(planet.mass/common.m_earth, 3))+' Earth masses'
			t += '\n'+str(round(planet.radius/1000))+' km radius'
			common.text(t, screen, (coords[0], coords[1]+10, coords[0]+150, 0), darkColor, lightColor)
			# switch focus if LMB is held down
			if pygame.mouse.get_pressed()[0]:
				focusPlanet = i
				moonskip = 0
		# infobox
		if i == focusPlanet:
			# display size
			fw = w//2
			ful = size[0]-fw, 0 # aligned to top right above system
			fcenter = size[0]-fw//2, h//2 + ful[1]
			# draw rect
			rectbounds = ful[0], ful[1], fw, size[1]-h+1
			pygame.draw.rect(screen, darkColor, rectbounds)
			# draw rect border
			pygame.draw.rect(screen, lightColor, rectbounds, 1)
			# label
			common.text(planet.name, screen, (ful[0], ful[1]+5, ful[0]+1, 0), darkColor, lightColor)
			# circle
			# try:
			# 	planetcolor = mapmode.planet(planet)
			# except AttributeError:
			# 	planetcolor = common.grey
			# col = planetcolor.r, planetcolor.g, planetcolor.b
			# pygame.draw.circle(screen, col, fcenter, 40)
			# info text
			if planet.mass < common.m_earth*100:
				t = 'Mass: '+str(round(planet.mass/common.m_earth, 3))+' M_E'
			else: # bigger than saturn
				t = 'Mass: '+str(round(planet.mass/common.m_j, 3))+' M_J'
			t += '\nRadius: '+str(round(planet.radius/1000))+' km'
			t += '\nDensity: '+str(round(common.density(planet.mass, planet.radius)))+' kg/m^3'
			t += '\nGravity: '+str(round(common.grav(planet.mass, planet.radius)/common.g_earth, 3))+' g'
			t += '\nTemperature: '+str(round(planet.temp))+' K'
			# resources
			if planet.resources:
				t += '\nResources:'
				for resource in planet.resources:
					t += '\n\t'+resource.name
					t += '\n\t\t$'+str(resource.value)+'/u'
			# moons
			try:
				bmrv = common.bestmoonresource(planet).value
			except AttributeError:
				bmrv = 0
			if planet.bodies:
				t += '\nMoons ('+str(len(planet.bodies))+'):'
				for j in range(len(planet.bodies)):
					n, moon = planet.bodies[(j + moonskip) % len(planet.bodies)]
					if j > maxmoonlist:
						t += '\n... and '+str(len(planet.bodies)-maxmoonlist)+' more (+ -)'
						break
					# resource value
					try:
						brv = common.bestresource(moon).value
						n = (3*brv)//bmrv
						kaching = '$'*n + ' '*(4-n)
					except (AttributeError, ZeroDivisionError):
						kaching = '\t'
					t += '\n'+kaching+' '+moon.name
			common.text(t, screen, (ful[0], ful[1]+150, size[0], 0), darkColor, lightColor)
			# spinny globe
			globe = surface.main(planet)
			rotation = (time() % globeperiod)/globeperiod*2*pi
			globe.rot(rotation)
			globe.shade()
			borders = planetmap.main(50, globe, fcenter)
			for b in borders:
				pygame.draw.circle(screen, b[1].rgb, b[0], 5)


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

# mousePos = 0, 0
# mousePosNew = 0, 0
delta = 0, 0
deltaNew = 0, 0
middleRadius = 1
focusSystem = g.stars[0][1]
focusPlanet = 0
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
			if event.button == 1:
				for star in displaylist:
					if common.dist(pygame.mouse.get_pos(), star[0]) < starRadius * 4:
						starid = star[1].star.id
						for s in g.stars:
							if s[1].star.id == starid:
								focus, focusSystem = s
								focusPlanet = 0
								break
						break
			elif event.button == 4:
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
			elif event.key in planetkeys: # planet foci
				focusPlanet = planetkeys.index(event.key)
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
	if pressed[pygame.K_KP_MINUS]:
		moonskip -= 1
	if pressed[pygame.K_KP_PLUS]:
		moonskip += 1
	# mousedown?
	# if pygame.mouse.get_pressed()[0]: # left click enabled
		# 	mousePosNew = pygame.mouse.get_pos()
	# 	deltaNew = tuple(map(lambda x: (x[1]-x[0])/zoom, zip(mousePos, mousePosNew)))
		# else:
		# 	# reset
		# 	mousePos = pygame.mouse.get_pos()
		# 	delta = tuple(map(sum, zip(delta, deltaNew)))
		# 	# reset
		# 	mousePosNew = pygame.mouse.get_pos()
	# 	deltaNew = 0, 0
	# focusSystem is of type System
	showsystem()
	# infobox
	for star in displaylist:
		if common.dist(pygame.mouse.get_pos(), star[0]) < starRadius*4:
			starinfo(*star)
			break
	# display system info
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
