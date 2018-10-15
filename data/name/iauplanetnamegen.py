import sys
sys.path.append('./data')
from constants import alphabet


def main(starname, position) -> str:
	if position > 25:
		return starname + ' ' + alphabet[position // len(alphabet)] + alphabet[position % len(alphabet)]
	return starname + ' ' + alphabet[position % len(alphabet)]
