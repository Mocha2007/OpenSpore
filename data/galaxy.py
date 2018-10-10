from random import random, choice
import sys
sys.path.append('./data')
from starcalc import Star

# constants
galaxyRadius = 25 # fixme works for now, until 100 works
minDistance = 3 # ly
maxDistance = 10 # ly
tries = 10
maxZ = 5


def dist(a: tuple, b: tuple) -> float:
	s = 0
	for i in range(len(a)):
		s += (a[i]-b[i])**2
	return s**.5


class Galaxy:
	def __init__(self, stargen, starnamegen): # no type annotation since function can't be annotated
		# generate home star
		home = Star(1, 'Home')
		starList = [((0, 0, 0), home)]
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
			starList.append(
				(site, Star(stargen(), starnamegen()))
			)
			failures = 0
		self.stars = starList
