import sys
sys.path.append('./data')
from constants import alphabet


def main(starname, position) -> str:
	return starname + ' ' + alphabet[position % len(alphabet)]
