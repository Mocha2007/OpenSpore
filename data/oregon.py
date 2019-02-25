# PROJECT OREGON
# HUMOROUS SPACE-THEMED OREGON TRAIL CLONE
# LOADING SCREEN MINIGAME
from json import load
from random import choice

data = load(open('oregon.json', 'r'))
parts = data['parts']
qualities = data['qualities']

# the game is a TRAIL divided into a number of ZONES.
# each ZONE contains unique EVENTS which may or may not happen.
# the player will need to manage RESOURCES and make tough DECISIONS to make it to their new home alive.
# in the beginning, players will select from a pool of PARTS of varying QUALITIES.
# once they get all their PARTS, they begin their journey.


def generate_random_part() -> (int, int):
	return choice(range(len(parts))), choice(range(len(qualities)))


def generate_auction() -> set:
	rounds = len(parts)
	parts_per_round = 3
	return {{generate_random_part() for _ in range(parts_per_round)} for _ in range(rounds)}


def game_tick(**kwargs) -> dict:
	if kwargs['gamestate'] == 'start':
		kwargs['ship'] = [-1] * len(parts)
		kwargs['gamestate'] = 'auction'
		kwargs['auction'] = generate_auction()
		kwargs['auction_round'] = 0
		return kwargs
	if kwargs['gamestate'] == 'auction':
		pass
	return kwargs
