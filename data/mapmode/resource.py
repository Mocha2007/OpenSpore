import sys
sys.path.append('./data')
from color import Color
from system import System


def main(system: System) -> Color:
	maxvalue = [0, Color(128, 128, 128)]
	if system.bodies:
		for _, planet in system.bodies:
			if planet.resources:
				for r in planet.resources:
					if r.value > maxvalue[0]:
						maxvalue[1] = r.data['color']
	return maxvalue[1]
