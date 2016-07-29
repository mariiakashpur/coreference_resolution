from Corpus import Corpus
from NP_pair import NP_pair

# dummy_corpus = Corpus("../data/dummy.txt")
training_corpus = Corpus("../data/ontonotes-train.conll")
# test_corpus = Corpus("../data/ontonotes-test.conll")
# lala_corpus = Corpus("../data/lala.txt")

# dummy_corpus.create_mallet_file("dummy-mallet.txt")


pos = training_corpus.generate_pos_pairs()
neg = training_corpus.generate_neg_pairs()
# print len(pos)
# print len(neg)
training_corpus.create_mallet_file("training-mallet.txt")



# test_corpus.create_test_file("test-mallet.txt")





