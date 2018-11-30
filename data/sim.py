from galaxy import Galaxy
from system import System


def civ_from_system(s: System):
	for _, p in s.bodies:
		if p.civ:
			return p.civ
	return None


def get_civs(g: Galaxy) -> set:
	civ_set = set([civ_from_system(system) for (_, system) in g.stars])
	civ_set.remove(None)
	return civ_set


def main(g: Galaxy) -> Galaxy:
	civ_list = get_civs(g)
	for civ in civ_list:
		if civ.goal == '$':
			if 0 < civ.cashflow(1):
				civ.goal = civ.refresh_goal()
			else:
				pass # todo DO THINGS TO HELP MOOLAH
		# todo: elifs for colony, resource, war
		# now, add to histories
		civ = civ.update_hist()
		# now, refresh money
		pass # nothing to do for now
	return g
