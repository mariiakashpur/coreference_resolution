import re

class Token(object):
	def __init__(self, string, tag, parse, chain_number_column):
		if string == "I":
			string = "i"
		self.string = string
		self.tag = tag
		self.parse = parse
		if chain_number_column == "-" or "|" in chain_number_column:
			self.chain_number_column = ""
		else:
			self.chain_number_column = chain_number_column


	def is_definite_determiner(self):
		"""Look for 'the/those/this etc.'"""
		return re.match(r'^[Tt]h.+$', self.string) and self.tag == "DT"

	def is_personal_pronoun(self):
		"""Look for PRP"""
		return re.match(r'^PRP$', self.tag)
	
	def is_possesive_pronoun(self):
		"""Look for PRP$"""
		return re.match(r'^PRP\$+$', self.tag)

	def is_complete_np(self):
		"""Look for (NP*) in one line"""
		return re.match(r'^\(NP\*\)+$', self.parse)

	def count_np_open_brackets(self):
		"""Look for (NP in one line"""
		return len(re.findall(r'\(NP', self.parse))

	def count_open_brackets(self):
		"""Look for all ( in one line"""
		return len(re.findall(r'\(', self.parse))

	def count_closing_brackets(self):
		"""Look for all ) in one line"""
		return len(re.findall(r'\)', self.parse))

	def is_embedded_np(self):
		"""Look for (NP* which is embedded NP in current NP but not on the same line"""
		return re.match(r'^\(NP\*$', self.parse)

	def __repr__(self):
		"""To print the object"""
		return self.string 
		return self.string + " " + self.tag + " " + self.parse + " " + self.chain_number_column




