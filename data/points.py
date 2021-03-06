from math import cos


class Points: # no type annotation since function can't be annotated
	def __init__(self, points: tuple):
		self.points = points

	def rot(self, theta: float):
		"""Rotate an image theta radians"""
		# rotate
		starList = []
		for star in self.points:
			r, t = star[0]
			r += theta
			site = r, t
			starList.append(
				(site, star[1])
			)
		self.points = starList
		return self

	def shade(self, theta: float):
		"""Darken rim"""
		starList = []
		for coords, color in self.points:
			lat, long = coords[0], coords[1]
			if cos(lat) * cos(long) < 0:
				continue
			dark = max(cos(lat+theta) * cos(long), 0)
			starList.append(
				(coords, color.scalar(dark))
			)
		self.points = starList
		return self
