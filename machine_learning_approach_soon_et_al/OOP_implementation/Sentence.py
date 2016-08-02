from NP import NP

class Sentence(object):
	def __init__(self, sentence_number):
		self.sentence_number = sentence_number
		self.tokens = []

	def add_token(self, token):
		self.tokens.append(token)

	def extract_nps(self):
		"""Extract all NP's from syntactic parse annotation level together with coreference chain numbers, if applicable""" 
		self.nps = []
		# counter for opened/closed brackets around nps
		np_bracket_counter = 0
		embedded_counter = 0

		sentence_number = self.sentence_number

		for token in self.tokens:
			# look for possessive pronouns - in Token class
			if token.is_possesive_pronoun():
				# add NP 
				self.nps.append(NP(token, sentence_number, token.line_number, token.chain_number_column))
			else:
				# if we haven't seen open NP's yet
				if not np_bracket_counter:
					# look for (NP)
					if token.is_complete_np():
						self.nps.append(NP(token, sentence_number, token.line_number, token.chain_number_column))
					else:
						np_bracket_counter = token.count_np_open_brackets()
						# if several NP's start on same line - mistake in getting coreference chain numbers; here try to avoid that
						if np_bracket_counter == 1:
							# add coreference chain number
							current_np = NP(token, sentence_number, token.line_number, token.chain_number_column)
						else:
							# DON'T add coreference chain number
							current_np = NP(token, sentence_number, token.line_number)

				else:
					if token.is_complete_np():
						self.nps.append(NP(token, sentence_number, token.line_number, token.chain_number_column))
					current_np.add_token(token)
					# add all found opening brackets
					np_bracket_counter += token.count_open_brackets()
					
					# ------ 	IF EMBEDDED NP'S INSIDE CURRENT NP BUT NOT ON SAME LINE ----------
					if not embedded_counter:
						if token.is_embedded_np():
							embedded_np = NP(token, sentence_number, token.line_number, token.chain_number_column)
							embedded_counter = 1
					else:
						embedded_np.add_token(token)
						# add all found opening brackets
						embedded_counter += token.count_open_brackets()

					# --------------------------------------------------------
				if np_bracket_counter:
					# substract all found closing brackets
					np_bracket_counter -= token.count_closing_brackets()
					if np_bracket_counter <= 0:
						np_bracket_counter = 0
						self.nps.append(current_np)
					if embedded_counter:
						embedded_counter -= token.count_closing_brackets()
						if embedded_counter <= 0:
							embedded_counter = 0
							self.nps.append(embedded_np)
		

		return self.nps


