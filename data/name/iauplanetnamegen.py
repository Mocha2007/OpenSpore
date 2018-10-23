import sys
sys.path.append('./data')
from constants import alphabet


def main(starname, position) -> str:
	if position > len(alphabet) - 1:
		try:
			return starname + ' ' + alphabet[position // len(alphabet) - 1] + alphabet[position % len(alphabet)]
		except IndexError:
			return 'OwO What\'s this???'
	return starname + ' ' + alphabet[position % len(alphabet)]
