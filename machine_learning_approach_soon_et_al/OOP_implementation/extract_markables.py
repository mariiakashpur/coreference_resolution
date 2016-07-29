import re
from collections import defaultdict

def extract_token_lines(filepath):
	"""Extract lines from corpus in a list of lists of lists structure: sentences->sentence->tokens"""
	with open(filepath) as f:
		# store all sentences in corpus
		all_lines = []
		# store all tokens of one sentence
		sentence = []
		for line in f:
			# check if we have a valid token line
			if line[0].isalpha():
				token_line = line.split()
				sentence.append(token_line)
			# check if line is empty - we reached end of current sentence
			elif not line.strip(): 
				all_lines.append(sentence)
				sentence = []
	return all_lines


def extract_nps(all_lines):
	"""Extract all NP's from syntactic parse annotation level together with coreference chain numbers, if applicable""" 
	# store all nps from corpus
	all_nps = []
	for j, sentence in enumerate(all_lines):
		# counter for opened/closed brackets around nps
		np_bracket_counter = 0
		embedded_counter = 0
		sentence_nps = []

		# ----------- 	REGEX COMPILATION -----------------------
		digit = re.compile(r'\d+')
		complete_np = re.compile(r'^\(NP\*\)+$')
		opening_bracket = re.compile(r'\(')
		closing_bracket = re.compile(r'\)')
		# -------------------------------------------------------

		for i, line in enumerate(sentence):
			# check for first line and lowercase the word
			# if i == 0:
			# 	line[3] = line[3].lower()
			if line[3] == "I":
				line[3] = "i"
			# look for possessive pronouns
			if re.match(r'^PRP\$+$', line[4]):
				sentence_nps.append(([(line[3], line[4])], re.findall(digit, line[-1])))
			else:
				# if we haven't seen open NP's yet
				if not np_bracket_counter:
					# look for (NP)
					if re.match(complete_np, line[5]):
						# line[3] contains word, line[4] its tag, line[-1] its coreference chain, if any
						sentence_nps.append(([(line[3], line[4])], re.findall(digit, line[-1])))
					else:
						# look for (NP
						np_bracket_counter = len(re.findall(r'\(NP', line[5]))
						# if several NP's start on same line - mistake in getting coreference chain numbers; here try to avoid that
						if np_bracket_counter == 1:
							# add coreference chain number
							current_np = ([(line[3], line[4])], re.findall(digit, line[-1]))
						else:
							# DON'T add coreference chain number
							current_np = ([(line[3], line[4])], [])
				else:
					if re.match(complete_np, line[5]):
						sentence_nps.append(([(line[3], line[4])], re.findall(digit, line[-1])))
					current_np[0].append((line[3], line[4]))
					# add all found opening brackets
					np_bracket_counter += len(re.findall(opening_bracket, line[5]))
					
					# ------ 	IF EMBEDDED NP'S INSIDE CURRENT NP BUT NOT ON SAME LINE ----------
					if not embedded_counter:
						if re.match(r'^\(NP\*$', line[5]):
							embedded_np = ([(line[3], line[4])], re.findall(digit, line[-1]))
							embedded_counter = 1
					else:
						embedded_np[0].append((line[3], line[4]))
						# add all found opening brackets
						embedded_counter += len(re.findall(opening_bracket, line[5]))

					# --------------------------------------------------------
				if np_bracket_counter:
					# substract all found closing brackets
					np_bracket_counter -= len(re.findall(closing_bracket, line[5]))
					if np_bracket_counter <= 0:
						np_bracket_counter = 0
						sentence_nps.append(current_np)
					if embedded_counter:
						embedded_counter -= len(re.findall(closing_bracket, line[5]))
						if embedded_counter <= 0:
							embedded_counter = 0
							sentence_nps.append(embedded_np)

		all_nps.append(sentence_nps)
	
		# if j == 5:
		# 	break
	return all_nps

#print extract_nps(extract_token_lines("data/ontonotes-train.conll"))


def generate_instances(all_nps):
	""" Return training instances extracted from list of all NP's.
	Instances stored in such a structure:
	{'61': [[['a', 'map', 1], [['a', 'wall', 'outside', 'the', 'headquarters', 1], ['the', 'headquarters', 1], ['we', 1]]], [['a', 'map', 1], []], [['This', 'map', 2], []]]}
	Where key is coref chain number, value is [[[pos instance 1 (last item - its sentence number)], [[its first incorrect np], [its second incorrect np]],
	                                           [[pos instance 2], [[its first incorrect np], [its second incorrect np]]]]"""
	instances = {}
	last_number = None
	for j, sent in enumerate(all_nps):
		for np, chain_number in sent:
			# add sent number for each NP - to later use in distance feature
			np.append(j)
			if chain_number:
				number = chain_number[0]
				if number in instances:
					# add new pos instance item, together with empty list for storing nps between this instance and next pos instance in coref chain
					instances[number].append([np, []])
					last_number = None
				else:
					instances[number] = [[np, []]]
					last_number = number
			else:
				if last_number:
					# add "incorrect" np 
					instances[last_number][-1][-1].append(np)
	return instances

# print generate_instances(extract_nps(extract_token_lines("data/ontonotes-train.conll")))

print extract_nps(extract_token_lines("data/dummy.txt"))
print generate_instances(extract_nps(extract_token_lines("data/dummy.txt")))

def generate_pos_pairs(instances):
	""" From all instances, extract positive pairs in a list of tuples structure. """
	pos_pairs = []
	for chain_number in instances:
		number_instances = len(instances[chain_number])
		if number_instances > 1:
			for k in range(number_instances - 1):
				pos_pairs.append((instances[chain_number][k][0], instances[chain_number][k + 1][0]))
	return pos_pairs


def generate_neg_pairs(instances):
	""" From all instances, extract negative pairs in a list of tuples structure. To create pairs, combine non-related NP's in between an instance 
	of coref chain and next instance of this chain. """
	neg_pairs = []
	for chain_number in instances:
		number_instances = len(instances[chain_number])
		if number_instances > 1:
			for k in range(number_instances - 1):
				for np in instances[chain_number][k][1]:
					neg_pairs.append((np, instances[chain_number][k + 1][0]))
	return neg_pairs

print generate_pos_pairs(generate_instances(extract_nps(extract_token_lines("data/dummy.txt"))))
print generate_neg_pairs(generate_instances(extract_nps(extract_token_lines("data/dummy.txt"))))

def generate_features(pairs):
	pairs_features = []
	for i, (pair1, pair2) in enumerate(pairs):
		pairs_features.append([(pair1[:-1], pair2[:-1]), "DISTANCE=" + str(pair2[-1] - pair1[-1])])

		# ------- Either word in both NP's begins with a cap ------------
		first_upper = False
		for word, tag in pair1[:-1]:
			if word[0].isupper():
				first_upper = True
				break
		second_upper = False
		for word, tag in pair2[:-1]:
			if word[0].isupper():
				second_upper = True
				break		
		if first_upper and second_upper:
			pairs_features[i].append("BOTHPROPER=yes")
		else:
			pairs_features[i].append("BOTHPROPER=no")
		#------------------------------------------------------------
	return pairs_features

print generate_features(generate_pos_pairs(generate_instances(extract_nps(extract_token_lines("data/dummy.txt")))))

# [([('a', 'DT'), ('map', 'NN'), 1], [('a', 'DT'), ('map', 'NN'), 1]), ([('a', 'DT'), ('map', 'NN'), 1], [('This', 'DT'), ('map', 'NN'), 2])]
# [([('a', 'DT'), ('wall', 'NN'), ('outside', 'IN'), ('the', 'DT'), ('headquarters', 'NN'), 1], [('a', 'DT'), ('map', 'NN'), 1]), ([('the', 'DT'), 
# 	('headquarters', 'NN'), 1], [('a', 'DT'), ('map', 'NN'), 1]), ([('we', 'PRP'), 1], [('a', 'DT'), ('map', 'NN'), 1])]

# [(['a', 'map', 1], ['a', 'map', 1]), (['a', 'map', 1], ['This', 'map', 2])]
# [(['a', 'wall', 'outside', 'the', 'headquarters', 1], ['a', 'map', 1]), (['the', 'headquarters', 1], ['a', 'map', 1]), (['we', 1], ['a', 'map', 1])]

# [[(['a', 'map'], ['a', 'map']), 'DISTANCE=0', 'BOTHPROPER=no'], [(['a', 'map'], ['This', 'map']), 'DISTANCE=1', 'BOTHPROPER=no']]





# def extract_all_nps(all_lines):
# 	"""Extract all NP's from syntactic parse annotation level"""
# 	# store all nps from corpus
# 	all_nps = []
# 	for j, sentence in enumerate(all_lines):
# 		# counter for opened/closed brackets around nps
# 		bracket_counter = 0
# 		sentence_nps = []
# 		for i, line in enumerate(sentence):
# 			if not bracket_counter:
# 				embedded_counter = []
# 				bracket_counter = len(re.findall(r'\(NP', line[5]))

# 				if bracket_counter:
# 					after_np =  re.findall(r'\(NP((?:(?!\(NP).)+)', line[5])
# 					nonp_bracket_counter  = 0
# 					for node in after_np:
# 						nonp_bracket_counter += len(re.findall(r'\(', node))
# 						nonp_bracket_counter -= len(re.findall(r'\)', node))
					
# 					if bracket_counter > 1:
# 						current_np = []
# 						for counter in range(bracket_counter):
# 							# embedded_counter.append(1 + nonp_bracket_counter)
# 							embedded_counter.append(1)
# 							current_np.append([line[3]])
# 					else:
# 						current_np = [line[3]]
# 			else:
# 				if embedded_counter:
# 					for np in current_np:
# 						np.append(line[3])
# 					for counter in embedded_counter:
# 						counter += len(re.findall(r'\(', line[5]))
# 				else:
# 					# print line[3]
# 					current_np.append(line[3])
# 				bracket_counter += len(re.findall(r'\(', line[5]))
# 			if bracket_counter:
# 				bracket_counter += nonp_bracket_counter
# 				if embedded_counter:
# 					for k, counter in enumerate(embedded_counter):
# 						counter  += nonp_bracket_counter
# 						counter -= len(re.findall(r'\)', line[5]))
# 						if counter <= 0:
# 							# remove subcounter from embedded counter
# 							embedded_counter.pop(k)
# 							sentence_nps.append(" ".join(current_np[k]))
# 							# remove sub-np from current_np - we have reached its end
# 							current_np.pop(k)
# 					bracket_counter -= len(re.findall(r'\)', line[5]))
# 					if bracket_counter <= 0:
# 						bracket_counter = 0
# 				else:
# 					bracket_counter -= len(re.findall(r'\)', line[5]))
# 					if bracket_counter <= 0:
# 						bracket_counter = 0
# 						# sentence_nps.append(" ".join(current_np))
# 		if j == 5:
# 			break
# 		all_nps.append(sentence_nps)
# 	return all_nps





















