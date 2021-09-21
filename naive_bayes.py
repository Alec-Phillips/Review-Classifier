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

    def update_text(self, new_text):
        self.words = get_words(new_text)
        self.bag_of_words = set(self.words)
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
    classifier = BayesClassifier('great food, love the atmosphere')
    print(classifier.result)


# test()

def apply_classifier():

    fake_reviews = []
    classifier = BayesClassifier('')

    i = 1

    while i <= 1000:
        negative_file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
        f = open(negative_file_name)
        text = f.read()
        classifier.update_text(text)
        result = classifier.result
        if result == 1:
            fake_reviews.append(negative_file_name)
        f.close()

        positive_file_name = 'Homework2-Data/pos/pos_' + str(i) + '.txt'
        f = open(positive_file_name)
        text = f.read()
        classifier.update_text(text)
        result = classifier.result
        if result == 0:
            fake_reviews.append(positive_file_name)
        f.close()

        i += 1
        # print(i)
    
    for review in fake_reviews:
        print(review)
    print(len(fake_reviews))


apply_classifier()