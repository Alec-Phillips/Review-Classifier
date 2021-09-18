# first file: Naive Bayes Classifier

from parser import get_words


class BayesClassifier:

    def __init__(self, new_text):
        self.words = get_words(new_text)
        # print(self.words)
    






def test():
    classifier = BayesClassifier('this is a test review')
    print(classifier.words)



test()

