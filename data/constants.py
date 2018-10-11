# characters
alphabet = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
greek = 'αβγδεζηθικλμνξοπρστυφχψω'

# sun
r_sun = 6.957e8
t_sun = 5772


# functions
def delta(a: tuple, b: tuple) -> tuple:
	temp = tuple(zip(a, b))
	temp = tuple(map(lambda x: x[0]-x[1], temp))
	return temp


def dist(a: tuple, b: tuple) -> float:
	s = 0
	for i in range(len(a)):
		s += (a[i]-b[i])**2
	return s**.5


def spore_ishab(planet, star): # todo make actually spore
	inner, outer = star.mass*.95, star.mass*1.05
	return inner < planet.sma < outer
