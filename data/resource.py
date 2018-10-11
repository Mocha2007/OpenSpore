class Resource:
	def __init__(self, data: dict):
		self.data = data # expects dictionary
		self.name = data['name']
