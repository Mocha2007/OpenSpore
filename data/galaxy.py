from random import random, choice
import sys
sys.path.append('./data')
from starcalc import Star
from system import System
from constants import dist

# constants
galaxyRadius = 50
minDistance = 3 # ly
maxDistance = 10 # ly
tries = 10
maxZ = 5


class Galaxy: # no type annotation since function can't be annotated
	def __init__(self, stargen, starnamegen, planetnamegen, moonnamegen, SystemClass):
		# generate home star
		home = (0, 0, 0), SystemClass(Star(1, 'Home'), planetnamegen, moonnamegen)
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
				(site, SystemClass(newStar, planetnamegen, moonnamegen))
			)
			failures = 0
		self.stars = starList
