class Noun:
	def __init__(self, word: str, **kwargs):
		self.word = word
		self.kwargs = kwargs
		# countable?
		if 'countable' in kwargs:
			self.countable = kwargs['countable']
		else:
			self.countable = True
		# always singular?
		if 'always_singular' in kwargs:
			self.always_singular = kwargs['always_singular']
		else:
			self.always_singular = False
		# always plural?
		if 'always_plural' in kwargs:
			self.always_plural = kwargs['always_plural']
		else:
			self.always_plural = False
		# plural form
		if self.always_singular or self.always_plural:
			self.plural = word
		elif 'plural' in kwargs:
			self.plural = kwargs['plural']
		else:
			self.plural = word+'s'
		# is it plural right now?
		if self.always_singular:
			self.is_plural = False
		elif self.always_plural:
			self.is_plural = True
		elif 'is_plural' in kwargs:
			self.is_plural = kwargs['is_plural']
		else:
			self.is_plural = False

	def __repr__(self) -> str:
		return 'Noun("'+self.word+'", **'+str(self.kwargs)+')'

	def read(self) -> str:
		if self.always_singular or not self.is_plural:
			return self.word
		else:
			return self.plural
