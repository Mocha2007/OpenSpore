from sys import exit
from importlib.machinery import SourceFileLoader
from math import ceil, log10, pi
from time import time
import pygame

# logging
open('openspore.log', 'a+').write('\nSTART '+str(time()))

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
maxmoonlist = 6
# may change later on as user does things
focus = 0, 0, 0
zoom = 15
currentmapmode = 0
currentprojmode = 0
moonskip = 0
currentchem = 0


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

# load constants module
common = SourceFileLoader('common', 'data/constants.py').load_module()
font = common.font

# loading
screen.fill((0, 0, 0))
loading = font.render('Loading...', 1, lighterColor)
screen.blit(loading, (size[0]//2, size[1]//2))
refresh()

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

# load resource module
resgen = SourceFileLoader('resgen', 'data/resources/'+cfg['resourcegen'][0]+'.py').load_module()

# load plotting module
plot = SourceFileLoader('plot', 'data/plot.py').load_module()

# load sim module
sim = SourceFileLoader('sim', 'data/sim.py').load_module()


def shift() -> bool:
	return pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]


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
		warnings = []
		cstate = common.chemstate(common.lifechems[currentchem], planet)
		csint = common.statemap[cstate]
		if csint > 1:
			tlabel = font.render('!', 1, (255, 192, 128))
			haswarning = True
			warnings.append('Boiling')
		elif csint == 0:
			tlabel = font.render('!', 1, (128, 192, 255))
			haswarning = True
			warnings.append('Freezing')
		if haswarning:
			screen.blit(tlabel, warningcoords)
		if not (planet.atm and common.p_hab[0] < planet.atm < common.p_hab[1]):
			tlabel = font.render('!', 1, (128, 128, 128))
			haswarning = True
			if planet.atm:
				warnings.append('Thin' if planet.atm < common.p_hab[0] else 'Thick')
			else:
				warnings.append('Thin' if planet.mass < common.m_earth else 'Thick')
			screen.blit(tlabel, (warningcoords[0]-5, warningcoords[1]))
		# habitability info if mouse over
		mousepos = pygame.mouse.get_pos()
		warningcoords = warningcoords[0], warningcoords[1] + 10
		if common.dist(mousepos, warningcoords) <= 8 and haswarning:
			# hover info
			warnname = ', '.join(warnings)
			common.text(warnname, screen, (warningcoords[0], warningcoords[1]-20, warningcoords[0]+125, 0), darkColor, lightColor)
		# planet info if mouse over
		elif common.dist(mousepos, coords) <= radius:
			# hover info
			t = planet.name
			sma = planet.orbit.sma
			if common.au/10 < sma:
				t += '\n'+str(round(planet.orbit.sma/common.au, 3))+' au'
			else:
				t += '\n'+str(round(planet.orbit.sma/common.ld, 3))+' LD'
			period = planet.orbit.period()
			if common.year < period:
				t += '\n'+str(round(period/common.year, 3))+' y'
			elif common.day < period:
				t += '\n'+str(round(period/common.day, 3))+' d'
			else:
				t += '\n'+str(round(period/common.hour, 3))+' h'
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
			t = '\t'+common.gettype(planet)+'\n'
			if planet.mass < common.m_earth*100:
				t += 'Mass: '+str(round(planet.mass/common.m_earth, 3))+' M_E'
			else: # bigger than saturn
				t += 'Mass: '+str(round(planet.mass/common.m_j, 3))+' M_J'
			t += '\nRadius: '+str(round(planet.radius/1000))+' km'
			t += '\nTemperature: '+str(round(planet.temp))+' K'
			if shift():
				t += '\nDensity: '+str(round(common.density(planet.mass, planet.radius)))+' kg/m^3'
				t += '\nESI: '+str(round(common.esi2(planet), 3))
				t += '\nGravity: '+str(round(common.grav(planet.mass, planet.radius)/common.g_earth, 3))+' g'
				t += '\nV_e: '+str(round(common.v_e2(planet)))+' m/s'
				if planet.atm:
					if planet.atm < common.p_earth:
						t += '\nPressure: '+str(round(planet.atm))+' Pa'
					else:
						t += '\nPressure: '+str(round(planet.atm/common.p_earth, 3))+' atm'
			else:
				t += '\n(Shift) Advanced...'
			# states
			t += '\n(c) '+common.lifechems[currentchem].name+': '+cstate.title()
			# atmosphere
			t += '\n(a) Show Atmosphere'
			if pygame.key.get_pressed()[pygame.K_a]:
				t_a = ['Atmosphere']
				for j, k in sorted(planet.atmosphere.items(), key=lambda x: x[1], reverse=True):
					quantity = round(k, 4)
					if quantity:
						t_a.append(j + '\t' + str(quantity))
				if shift():
					debug = lambda x: str(round(planet.temp * common.getv_eslope(common.molmass[x])))
					for j in ('H2', 'He', 'N2', 'Xe'):
						t_a.append(j+' > '+debug(j)+' m/s')
				common.text('\n'.join(t_a), screen, (ful[0] - 150, ful[1] + 310, ful[0]+1, 0), darkColor, lightColor)
			# resources
			if planet.resources:
				t += '\nResources:'
				for resource in planet.resources:
					t += '\n\t'+resource.name
					t += '\n\t\t$'+str(resource.value)+'/u'
			# life!
			t += '\n(l) Biodiversity: '+str(len(planet.life))+('+' if planet.civ else '')
			if planet.civ:
				t += '\n> ' + planet.civ.name
			# life info
			if planet.life and pygame.key.get_pressed()[pygame.K_l]:
				t_a = ['\tLifeforms']
				for species in sorted(planet.life, key=lambda x: x.name):
					t_a.append(species.name.title())
				common.text('\n'.join(t_a), screen, (ful[0] - 150, ful[1] + 310, ful[0]+1, 0), darkColor, lightColor)
			# moons
			try:
				bmrv = common.bestmoonresource(planet).value
			except AttributeError:
				bmrv = 0
			if planet.bodies:
				t += '\n(+ -) Moons ('+str(len(planet.bodies))+'):'
				for j in range(len(planet.bodies)):
					n, moon = planet.bodies[(j + moonskip) % len(planet.bodies)]
					if j > maxmoonlist:
						t += '\n... and '+str(len(planet.bodies)-maxmoonlist)+' more'
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
			# atm label
			if shift() and planet.atm:
				# atm layer info
				atmcoords = size[0]-157, 310
				if planet.atm > common.p_earth:
					atminfo = "Superterran"
					atmcolor = 128, 255, 128
				elif planet.atm > common.p_troposphere:
					atminfo = "Tropospheric"
					atmcolor = 0, 255, 0
				else:
					atminfo = "Stratospheric"
					atmcolor = 0, 128, 0
				templabel = font.render('!', 1, atmcolor)
				screen.blit(templabel, atmcoords)
				if common.dist(mousepos, (atmcoords[0], atmcoords[1]+5)) <= 8:
					# hover info
					common.text(atminfo, screen, (atmcoords[0]-120, atmcoords[1], atmcoords[0]-10, 0), darkColor, lightColor)
			# spinny globe
			globe = surface.main(planet)
			rotation = (time() % globeperiod)/globeperiod*2*pi
			globe.rot(rotation)
			globe.shade(pi/4)
			borders = planetmap.main(50, globe, fcenter)
			for coords, col in borders:
				pygame.draw.circle(screen, col.rgb(), coords, ceil(150/surface.resolution))


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


# loading
screen.fill((0, 0, 0))
loading = font.render('Generating...', 1, lighterColor)
screen.blit(loading, (size[0]//2, size[1]//2))
refresh()
open('openspore.log', 'a+').write('\nGENERATION START '+str(time()))
g = galaxy.Galaxy(stargen.main, starnamegen.main, planetnamegen.main, moonnamegen.main, systemclass.System, resgen.main)
open('openspore.log', 'a+').write('\nGENERATION END '+str(time()))
# plotting + reset
# plot.body(g, plot.mass, plot.rho, xlog=True, ylog=True, point='.')
# screen = pygame.display.set_mode(size)

# main

delta = 0, 0
deltaNew = 0, 0
middleRadius = 1
focusSystem = g.stars[0][1]
focusPlanet = 0
frames = [0, 1]
while 1:
	# blank
	screen.fill((0, 0, 0))
	# framerate
	frames[1] = time()
	fps = str(round(1/(frames[1] - frames[0])))+' fps'
	fpslabel = font.render(fps, 1, lighterColor)
	screen.blit(fpslabel, (0, 0))
	frames[0] = frames[1]
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
			direction = -1 if shift() else 1
			if event.key == pygame.K_m: # mapmode
				changemap(direction)
			elif event.key == pygame.K_p: # projection
				changeproj(direction)
			elif event.key == pygame.K_c: # chemstate
				currentchem += 1
				currentchem %= len(common.lifechems)
			elif event.key in planetkeys: # planet foci
				focusPlanet = planetkeys.index(event.key)
			elif event.key == pygame.K_KP_PLUS: # zoom
				zoom *= 2
			elif event.key == pygame.K_KP_MINUS: # zoom
				zoom /= 2
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
	if pressed[pygame.K_PERIOD]:
		# galaxy change!
		g = sim.main(g)
		if int(time()) % 2 == 0:
			common.text('>>> x1 >>>', screen, (-1, 20, 0, 0), darkColor, lightColor)
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
