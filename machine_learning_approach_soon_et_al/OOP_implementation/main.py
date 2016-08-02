from Corpus import Corpus
from NP_pair import NP_pair
import sys


def main():

	if len(sys.argv) != 3:
		print "Please provide paths to train and test corpora!"
	else:

		training_corpus = Corpus(sys.argv[1])
		test_corpus = Corpus(sys.argv[2])
		len_pos_train = len(training_corpus.generate_pos_pairs())
		len_neg_train = len(training_corpus.generate_neg_pairs())
		training_corpus.create_mallet_file("training_file_mallet.txt")

		len_test = len(test_corpus.generate_pos_pairs()) + len(test_corpus.generate_neg_pairs())
		test_corpus.create_test_file("test_file_mallet.txt")


		print "There are " + str(len_pos_train) + " positive training instances and " + str(len_neg_train) + " negative training instances."
		print "There are " + str(len_test) + " test instances."



if __name__ == '__main__':
    main()



