from random import random, choice
import sys
sys.path.append('./data')
from starcalc import Star
from constants import dist

# constants
galaxyRadius = 30
minDistance = 3 # ly
maxDistance = 10 # ly
tries = 10
maxZ = 5


class Galaxy: # no type annotation since function can't be annotated
	def __init__(self, stargen, starnamegen, planetnamegen, moonnamegen, SystemClass, resourcegen):
		# generate home star
		home = (0, 0, 0), SystemClass(Star(1, 'Home'), planetnamegen, moonnamegen, resourcegen)
		starList = [home]
		# generate stars until ten failed placements in a row
		failures = 0
		while failures < tries:
			failures += 1 # if successful, this'll get reset at the end
			# choose random star
			head = choice(starList)
			# choose random delta xyz
			delta = random()*2*maxDistance-maxDistance, random()*2*maxDistance-maxDistance, random()*2*maxDistance-maxDistance
			# calculate proposed site
			site = tuple(map(sum, zip(head[0], delta)))
			# verify the site is not too far from the origin
			if dist((0, 0, 0), site) > galaxyRadius:
				continue
			# make sure z isn't too high or low
			if abs(site[2]) > maxZ:
				continue
			# verify the site is not too close to another star
			for star in starList:
				if dist(star[0], site) < minDistance:
					continue
			newStar = Star(stargen(), starnamegen())
			starList.append(
				(site, SystemClass(newStar, planetnamegen, moonnamegen, resourcegen))
			)
			failures = 0
		self.stars = starList

	def rotate(self, times: int):
		if type(times) != int:
			return ValueError
		times %= 4
		if times == 0:
			return self
		# rotate once and decrement times
		starList = []
		for star in self.stars:
			site = -star[0][1], star[0][0], star[0][2]
			starList.append(
				(site, star[1])
			)
		self.stars = starList
		return self.rotate(times-1)

	def vrotate(self, times: int):
		if type(times) != int:
			return ValueError
		times %= 4
		if times == 0:
			return self
		# rotate once and decrement times
		starList = []
		for star in self.stars:
			site = -star[0][2], star[0][1], star[0][0]
			starList.append(
				(site, star[1])
			)
		self.stars = starList
		return self.rotate(times-1)
