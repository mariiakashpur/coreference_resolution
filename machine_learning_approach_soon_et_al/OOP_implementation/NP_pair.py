class NP_pair(object):
	def __init__(self, np1, np2, is_coreferent):
		self.pair = [np1, np2]
		self.np1 = np1
		self.np2 = np2
		self.is_coreferent = is_coreferent

		
	def add_np(self, np):
		self.pair.append(np)

	def get_label(self):
		if self.is_coreferent:
			label = "coref"
		else:
			label = "non-coref"
		return label

	def last_word_match(self):
		return self.np1.tokens[-1].string == self.np2.tokens[-1].string


	def generate_features(self):
		self.features = []

		# ------- Distance between NP's -----------
		self.features.append("DISTANCE:" + str(self.np2.sentence_number - self.np1.sentence_number))

		# ------- Either word in both NP's begins with a cap ------------	
		if self.np1.has_cap() and self.np2.has_cap():
			self.features.append("BOTHPROPER:yes")
		else:
			self.features.append("BOTHPROPER:no")

		#--------- Antecedent is a pronoun -------------------
		if self.np1.is_pronoun():
			self.features.append("ANTECEDENT_PRONOUN:yes")
		else:
			self.features.append("ANTECEDENT_PRONOUN:no")

		# -------- Anaphor is a pronoun -----------------------
		if self.np2.is_pronoun():
			self.features.append("ANAPHOR_PRONOUN:yes")
		else:
			self.features.append("ANAPHOR_PRONOUN:no")

		# --------- Anaphor is definite NP ------------
		if self.np2.is_definite():
			self.features.append("ANAPHOR_DEFINITE:yes")
		else:
			self.features.append("ANAPHOR_DEFINITE:no")

		# --------- Last words in NP's match --------------
		if self.last_word_match():
			self.features.append("LAST_MATCH:yes")
		else:
			self.features.append("LAST_MATCH:no")

		return self.features
			
	def __repr__(self):
		return "".join(str(self.pair))




