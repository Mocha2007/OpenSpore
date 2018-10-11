import sys
sys.path.append('./data')
from color import Color
from system import System


def main(system: System) -> Color:
	if system.bodies:
		for _, planet in system.bodies:
			if planet.resources:
				return planet.resources[0].data['color']
	return Color(128, 128, 128)
