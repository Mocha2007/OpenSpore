from random import random, choice
from math import atan2, cos, sin
import sys
sys.path.append('./data')
from starcalc import Star
from constants import dist

# constants
origin = 0, 0, 0
galaxyRadius = 100
minDistance = 3 # ly
maxDistance = 10 # ly
tries = 10
# maxZ = 30


class Galaxy: # no type annotation since function can't be annotated
	def __init__(self, stargen, starnamegen, planetnamegen, moonnamegen, SystemClass, resourcegen):
		# generate home star
		home = origin, SystemClass(Star(1, lambda x: 'Home'), planetnamegen, moonnamegen, resourcegen)
		starList = [home]
		# generate stars until ten failed placements in a row
		failures = 0
		while (failures < tries or len(starList) < 100) and len(starList) < 1000:
			failures += 1 # if successful, this'll get reset at the end
			# choose random star
			head = choice(starList)
			# choose random delta xyz
			delta = random()*2*maxDistance-maxDistance, random()*2*maxDistance-maxDistance, random()*2*maxDistance-maxDistance
			# calculate proposed site
			site = tuple(map(sum, zip(head[0], delta)))
			# verify the site is not too far from the origin
			if dist(origin, site) > galaxyRadius:
				continue
			# make sure z isn't too high or low
			# if abs(site[2]) > maxZ:
			# 	continue
			# verify the site is not too close to another star
			# for star in starList:
			# 	if dist(star[0], site) < minDistance:
			# 		continue
			newStar = Star(stargen(), starnamegen)
			starList.append(
				(site, SystemClass(newStar, planetnamegen, moonnamegen, resourcegen))
			)
			failures = 0
		self.stars = starList

	def rotate(self, times: int):
		assert isinstance(times, int)
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
		assert isinstance(times, int)
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

	def anyrotatez(self, theta: float):
		"""Rotate an image theta radians"""
		# rotate
		starList = []
		for star in self.stars:
			x, y, z = star[0]
			r, t = (x**2+y**2)**.5, atan2(y, x)
			t += theta
			site = cos(t)*r, sin(t)*r, z
			starList.append(
				(site, star[1])
			)
		self.stars = starList
		return self

	def anyrotatex(self, theta: float):
		"""Rotate an image theta radians"""
		# rotate
		starList = []
		for star in self.stars:
			x, y, z = star[0]
			r, t = (y**2+z**2)**.5, atan2(z, y)
			t += theta
			site = x, cos(t)*r, sin(t)*r
			starList.append(
				(site, star[1])
			)
		self.stars = starList
		return self

	def anyrotatey(self, theta: float):
		"""Rotate an image theta radians"""
		# rotate
		starList = []
		for star in self.stars:
			x, y, z = star[0]
			r, t = (z**2+x**2)**.5, atan2(x, z)
			t += theta
			site = sin(t)*r, y, cos(t)*r
			starList.append(
				(site, star[1])
			)
		self.stars = starList
		return self
