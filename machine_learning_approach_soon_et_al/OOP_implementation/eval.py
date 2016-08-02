from __future__ import division
import sys

def compare_results(results_file, test_file):
	"""Compute the accuracy of predictions"""
	t = tuple(open(test_file, 'r'))
	pairs_counter = 0
	with open(results_file) as r:
		incorrectly_predicted = []
		for line in r:
			pairs_counter += 1
			results_line = line.split()
			if float(results_line[2]) > float(results_line[4]):
				predicted_coreferent = "coref"
			else:
				predicted_coreferent = "non-coref"
			np_pair = results_line[0].split(">")
			np1_line = np_pair[0].split("|")[0]
			np1_tokens = np_pair[0].split("|")[1:]
			np1_len = len(np1_tokens)
			
			np2_line = np_pair[1].split("|")[0]
			np2_tokens = np_pair[1].split("|")[1:]
			np2_len = len(np2_tokens)

			t_line1 = t[int(np1_line)].split()
			t_line2 = t[int(np2_line)].split()

			chain_number1 = t_line1[-1].strip(")").strip("(")
			chain_number2 = t_line2[-1].strip(")").strip("(")
			if chain_number1 == chain_number2:
				really_coreferent = "coref"
			else:
				really_coreferent = "non-coref"
			if predicted_coreferent != really_coreferent:
				incorrectly_predicted.append(line)

		return len(incorrectly_predicted) / pairs_counter


def main():

	if len(sys.argv) != 3:
		print "Please provide paths to classification results file and the test corpus!"
	else:
		print "The accuracy of the classifier is " + str(compare_results(sys.argv[1], sys.argv[2])) + "."



if __name__ == '__main__':
    main()



