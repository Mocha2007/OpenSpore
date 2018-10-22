import sys
sys.path.append('./data')
from color import Color
from system import System, Planet


def main(system: System) -> Color:
	maxvalue = [0, Color(128, 128, 128)]
	if system.bodies:
		for _, p in system.bodies:
			# go through planet
			if p.resources:
				for r in p.resources:
					if r.value > maxvalue[0]:
						maxvalue[0] = r.value
						maxvalue[1] = r.data['color']
			# go through moons
			# if p.bodies:
			# 	for _, m in p.bodies:
			# 		if m.resources:
			# 			for r in m.resources:
			# 				if r.value > maxvalue[0]:
			# 					maxvalue[0] = r.value
			# 					maxvalue[1] = r.data['color']
	return maxvalue[1]


def planet(p: Planet) -> Color:
	maxvalue = [0, Color(128, 128, 128)]
	if p.resources:
		for r in p.resources:
			if r.value > maxvalue[0]:
				maxvalue[0] = r.value
				maxvalue[1] = r.data['color']
	# go through moons
	if p.bodies:
		for _, m in p.bodies:
			if m.resources:
				for r in m.resources:
					if r.value > maxvalue[0]:
						maxvalue[0] = r.value
						maxvalue[1] = r.data['color']
	return maxvalue[1]
