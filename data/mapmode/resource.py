import sys
sys.path.append('./data')
from color import Color
from system import System, Planet


def main(system: System) -> Color:
	maxvalue = [0, Color(128, 128, 128)]
	if system.bodies:
		for _, p in system.bodies:
			if p.resources:
				for r in p.resources:
					if r.value > maxvalue[0]:
						maxvalue[1] = r.data['color']
	return maxvalue[1]


def planet(p: Planet) -> Color:
	maxvalue = [0, Color(128, 128, 128)]
	if p.resources:
		for r in p.resources:
			if r.value > maxvalue[0]:
				maxvalue[1] = r.data['color']
	return maxvalue[1]
