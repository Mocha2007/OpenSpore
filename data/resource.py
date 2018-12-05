class Resource:
	def __init__(self, data: dict):
		self.data = data # expects dictionary
		self.name = data['name']
		self.value = data['value']

	def __ge__(self, other):
		return self.value >= other.value

	def __gt__(self, other):
		return self.value > other.value

	def __le__(self, other):
		return self.value <= other.value

	def __lt__(self, other):
		return self.value < other.value
