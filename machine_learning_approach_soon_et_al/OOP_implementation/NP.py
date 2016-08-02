import re

class NP(object):
	def __init__(self, token, sentence_number, line_number, chain_number=""):
		self.tokens = [token]
		self.sentence_number = sentence_number
		self.chain_number = chain_number
		self.line_number = line_number
		
	def add_token(self, token):
		self.tokens.append(token)

	def has_cap(self):
		"""Used for generating features. Any word in NP begins with capital letter"""
		upper = False
		for token in self.tokens:
			if token.string.isupper():
				upper = True
				break
		return upper

	def is_pronoun(self):
		is_pronoun = False
		if len(self.tokens) == 1:
			for token in self.tokens:
				if token.is_possesive_pronoun() or token.is_personal_pronoun():
					is_pronoun = True
		return is_pronoun

	def is_definite(self):
		return self.tokens[0].is_definite_determiner()


	def __repr__(self):
		return "".join(str(self.tokens))