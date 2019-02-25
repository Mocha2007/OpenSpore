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
		# article
		if 'article' in kwargs:
			self.article = kwargs['article']
		else:
			self.article = 'a' if self.word[0] in 'aeiou' else 'an'
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

	def number(self) -> bool:
		if self.always_singular or not self.is_plural:
			return False
		else:
			return True

	def read(self) -> str:
		return self.plural if self.number() else self.word

	def get_be(self):
		return 'are' if self.number() else 'is'

	def get_existential(self, **kwargs):
		n = kwargs['n'] if 'n' in kwargs else 1
		proper = kwargs['proper'] if 'proper' in kwargs else False
		be = 'is' if n == 1 else 'are'
		fstring = 'there '+be+' {0} {1}'
		if proper:
			fstring = fstring[0].upper()+fstring[1:]+'.'
		word = self.word if n == 1 else self.plural
		return fstring.format(n, word)


class Description:
	def __init__(self, objects: dict, relationships: set):
		"""
		:param objects: a dict mapping Parts to ints (how many)
		:param relationships: a set of tuple(tuple, str), first tuple is which parts, str is the relationship
		"""
		self.objects = objects
		self.relationships = relationships

	def read(self) -> str:
		o = []
		# list the characters
		for object_, count in self.objects.items():
			assert isinstance(object_, Noun)
			o.append(object_.get_existential(n=count, proper=True))
		# list the relations
		for relation in self.relationships:
			parts_tuple, relation_str = relation
			special = {}
			for i, part in enumerate(parts_tuple):
				assert isinstance(part, Noun)
				# a/an?
				special[str(i)+'_article'] = part.article
				# is/are?
				special[str(i)+'_be'] = part.get_be()
			s = relation_str.format(*[i.read() for i in parts_tuple], **special)
			o.append(s+'.')
		return ' '.join(o)
