# Coreference Resolution program based on the Soon et al. (2001) machine learning approach
Author: Mariia Kashpur

To start the program, please run the "main.py" script. Please provide path to the training corpus and path to the test corpus (in CoNLL format) as arguments. This will create the training and test instances files ("training_file_mallet.txt" and "test_file_mallet.txt") in the current folder. The number of training and test instances will be printed on the screen.

Then you have to run the Mallet classifier. The classifier has to be installed on the machine. After that, you need to convert the created "training_file_mallet.txt" file to the mallet format by going to the Mallet folder and executing the command bin/mallet import-file --input training_file_mallet.txt --output training_file_mallet.mallet

After that, a classifier can be trained by executing bin/mallet train-classifier --input training_file_mallet.mallet --output-classifier my.classifier \
  --trainer DecisionTree

To classify the instances from the test file, run bin/mallet classify-file --input test_file_mallet.txt --output - --classifier my.classifier > classification_results.txt

This way, you will create the "classification_results.txt" file with the results of labelling. Then run the "eval.py" script and pass the path to this file and the path to the test file as arguments. You will see the accuracy of the classifier. 