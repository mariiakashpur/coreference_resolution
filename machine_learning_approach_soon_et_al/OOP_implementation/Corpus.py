from Token import Token
from Sentence import Sentence
from NP_pair import NP_pair
import copy

class Corpus(object):
	def __init__(self, filepath):
		self.filepath = filepath
		# all sents in corpus
		self.sents = []
		sentence_number = 0 
		sentence = Sentence(sentence_number)
		self.instances = {}

		with open(filepath) as f:
			for line in f:
				# check if we have a valid token line
				if line[0].isalpha():
					token_line = line.split()
					# create new Token object
					token = Token(token_line[3], token_line[4], token_line[5], token_line[-1].strip(")").strip("(")) 
					sentence.add_token(token)
				# check if line is empty - we reached end of current sentence
				elif not line.strip(): 
					self.sents.append(sentence)
					sentence_number += 1
					sentence = Sentence(sentence_number)



	def generate_instances(self):
		""" Return training instances extracted from list of all NP's.
		Instances stored in such a structure: {chain_num: [[np, its incorrect np], 
		                                                   [np, its incorrect np1, its incorrect np2]]}"""
		# last_number = None
		# for sent in self.sents:
		# 	for np in sent.extract_nps():
				# if np.chain_number:
				# 	number = np.chain_number
				# 	if number in self.instances:
				# 		self.instances[number].append([np])
				# 		last_number = None
				# 	else:
				# 		self.instances[number] = [[np]]
				# 		last_number = number
				# else:
				# 	if last_number:
				# 		# add "incorrect" np 
				# 		self.instances[last_number][-1].append(np)
		last_number = []
		tmp_instances = {}
		for sent in self.sents:
			for np in sent.extract_nps():
				if(np.chain_number) :
					if np.chain_number in last_number:
						last_number.remove(np.chain_number)
						self.instances[np.chain_number][-1] += tmp_instances[np.chain_number]
						self.instances[np.chain_number].append([np])
					else:
						last_number.append(np.chain_number)
						if np.chain_number in self.instances:
							self.instances[np.chain_number].append([np])
						else:
							self.instances[np.chain_number] = [[np]]
					tmp_instances[np.chain_number] = []
				for i in last_number:
					if i != np.chain_number:
						tmp_instances[i].append(np)
		


	def generate_pos_pairs(self):
		""" From all instances, extract positive pairs in a list of NP_pair objects. """
		self.pos_pairs = []
		# check if self.instances is empty - then call generate_instances
		if not self.instances:
			self.generate_instances()
		for chain_number in self.instances:
			number_instances = len(self.instances[chain_number])
			if number_instances > 1:
				for k in range(number_instances - 1):
					self.pos_pairs.append(NP_pair(self.instances[chain_number][k][0], self.instances[chain_number][k + 1][0], True))
		return self.pos_pairs


	def generate_neg_pairs(self):
		""" From all instances, extract negative pairs in a list of NP_pair objects. To create pairs, combine non-related NP's in between an instance 
		of coref chain and next instance of this chain. """
		self.neg_pairs = []
		if not self.instances:
			self.generate_instances()
		# print self.instances
		for chain_number in self.instances:
			number_instances = len(self.instances[chain_number])
			if number_instances > 1:
				for k in range(number_instances - 1):
					for np in self.instances[chain_number][k][1:]:
						self.neg_pairs.append(NP_pair(np, self.instances[chain_number][k + 1][0], False))
		return self.neg_pairs


	def create_mallet_file(self, filepath):
		all_pairs = self.pos_pairs + self.neg_pairs
		with open(filepath, 'w') as f:
			for j, pair in enumerate(all_pairs):
				two_nps = []
				for np in pair.pair:
					tokens = []
					for token in np.tokens:
						tokens.append(token.string)
					two_nps.append("|".join(tokens))
				concat = ">".join(two_nps)
				f.write(str(j) + concat + " " + pair.get_label() + " " + " ".join(pair.generate_features()) + "\n") 


	def create_test_file(self, filepath):
		all_pairs = self.pos_pairs + self.neg_pairs
		with open(filepath, 'w') as f:
			for j, pair in enumerate(all_pairs):
				two_nps = []
				for np in pair.pair:
					tokens = []
					for token in np.tokens:
						tokens.append(token.string)
					two_nps.append("|".join(tokens))
				concat = ">".join(two_nps)
				f.write(str(j) + concat + " " + " ".join(pair.generate_features()) + "\n") 



# a=[[1,2],[3,4]]


# [x for b in a for x in b]
# [b for b in a]











