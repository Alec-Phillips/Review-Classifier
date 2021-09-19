# first file: Naive Bayes Classifier

from parser import get_words
from parser import WordCounts


class BayesClassifier:

    def __init__(self, new_text):
        self.words = get_words(new_text)
        self.bag_of_words = set(self.words)
        self.word_data = WordCounts()
        self.pos_prob = 0.5
        self.neg_prob = 0.5
        self.result = self.get_probabilities()

    def get_probabilities(self):
        prob_by_word = {}
        for word in self.bag_of_words:
            if word in self.word_data.word_count_neg:
                numerator = self.word_data.word_count_neg.get(word) + 1
            else:
                numerator = 1
            denominator = self.word_data.total_negative + len(self.word_data.distinct_words)
            prob_by_word[word] = numerator / denominator

        for word in prob_by_word:
            self.neg_prob *= prob_by_word.get(word)

        prob_by_word = {}
        for word in self.bag_of_words:
            if word in self.word_data.word_count_pos:
                numerator = self.word_data.word_count_pos.get(word) + 1
            else:
                numerator = 1
            denominator = self.word_data.total_positive + len(self.word_data.distinct_words)
            prob_by_word[word] = numerator / denominator

        for word in prob_by_word:
            self.pos_prob *= prob_by_word.get(word)
        
        return 1 if self.pos_prob > self.neg_prob else 0


def test():
    classifier = BayesClassifier('rainbows')
    print(classifier.result)


test()

