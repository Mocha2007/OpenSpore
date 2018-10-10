from random import choice


def main() -> float:
	# spore approximate weights:
	# 60% M 0.4 solar masses
	# 25% G 1 solar mass
	# 15% O 2.5 solar masses
	return choice([2.5]*3 + [1]*5 + [.4]*12)
