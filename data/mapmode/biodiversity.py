import sys
sys.path.append('./data')
from color import Color
from system import System
from math import log


def viridity(p: Planet) -> int:
	if p.life:
		return min(len(p.life), 255)
	return 0


def v2c(vir: int) -> Color:
	if vir == 0:
		return Color(64, 64, 64)
	if vir <= 13:
		return Color(0, 59 + vir**2, 0)
	light = min(round(log(vir)**2), 255)
	return Color(light, 255, light)


def main(system: System) -> Color:
	maxvir = 0
	for _, p in system.bodies:
		thisvir = viridity(p)
		if maxvir < thisvir:
			maxvir = thisvir
	return v2c(maxvir)


def planet(p: Planet) -> Color:
	return v2c(viridity(p))
