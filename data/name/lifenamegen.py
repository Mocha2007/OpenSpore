from random import randint
import sys
sys.path.append('./data')
from constants import rword


def main() -> str:
	return rword(randint(3, 10))
