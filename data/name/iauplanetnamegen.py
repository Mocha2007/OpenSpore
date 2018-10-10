alphabet = 'abcdefghijklmnopqrstuvwxyz'


def main(starname, position) -> str:
	return starname + ' ' + alphabet[position % len(alphabet)]
