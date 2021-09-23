
import nltk
from nltk import FreqDist
from collections import defaultdict

class BayesClassifier:

    def __init__(self, bag_of_words, labeled_reviews):
        '''
        bag_of_words = the distinct stems found in the data being classified
        labeled_reviews = the training data that the classifier will use
        '''
        self.bag_of_words = bag_of_words
        self.labeled_reviews = labeled_reviews

        # a mapping from stem -> int for positive reviews
        self.positive_stem_counts = {} 
        # a mapping from stem -> int for negative reviews
        self.negative_stem_counts = {}
        # maps label -> pr[label]
        self.label_frequency_distribution = {}
        # maps feature (stem) -> (pr[feature | pos], pr[feature | neg])
        self.feature_frequency_distribution = {}
        # self.distinct_stems = set()

    def train(self):
        '''
        this uses the provided training data to get all the info that we need
        to perform the naive bayes classification on future data
            - the count of each stem in positive reviews
            - the count of each stem in negative reviews
        it then determines the frequency distribution of features and labels,
        so that most valuable features can be determined
        '''
        label_frequencies = {'pos': 0, 'neg': 0}
        total_stems = 0
        for review in self.labeled_reviews:
            if review[1] == 'pos':
                label_frequencies['pos'] = label_frequencies.get('pos') + 1
                for stem in review[0]:
                    total_stems += 1
                    if stem in self.positive_stem_counts:
                        self.positive_stem_counts[stem] = self.positive_stem_counts.get(stem) + 1
                    else:
                        self.positive_stem_counts[stem] = 1
                        # self.distinct_stems.add(stem)
            else:
                label_frequencies['neg'] = label_frequencies.get('neg') + 1
                for stem in review[0]:
                    total_stems += 1
                    if stem in self.negative_stem_counts:
                        self.negative_stem_counts[stem] = self.negative_stem_counts.get(stem) + 1
                    else:
                        self.negative_stem_counts[stem] = 1
                        # self.distinct_stems.add(stem)
        total_labels = 0
        for _, frequency in label_frequencies.items():
            total_labels += frequency
        for label, frequency in label_frequencies.items():
            self.label_frequency_distribution[label] = frequency / total_labels
        for stem, count in self.positive_stem_counts.items():
            self.feature_frequency_distribution[stem] = {'pos': (count/total_stems)/self.label_frequency_distribution['pos'], 'neg': 0}
        for stem, count in self.negative_stem_counts.items():
            if stem in self.feature_frequency_distribution:
                self.feature_frequency_distribution[stem]['neg'] = (count/total_stems)/self.label_frequency_distribution['neg']
            else:
                self.feature_frequency_distribution[stem] = {'pos': 0, 'neg': (count/total_stems)/self.label_frequency_distribution['neg']}

    def report_useful_features(self, num_returned):

        pos_usefulness = []
        neg_usefulness = []
        for feature, distribution in self.feature_frequency_distribution.items():
            try:
                feature_pos_usefulness = distribution['pos'] / distribution['neg']
                pos_usefulness.append([feature_pos_usefulness, feature])
            except:
                pass
            try:
                feature_neg_usefulness = distribution['neg'] / distribution['pos']
                neg_usefulness.append([feature_neg_usefulness, feature])
            except:
                pass

        pos_usefulness.sort(reverse=True)
        neg_usefulness.sort(reverse=True)

        most_useful_pos = pos_usefulness[:num_returned]
        most_useful_neg = neg_usefulness[:num_returned]

        return most_useful_pos, most_useful_neg
        
    def classify(self):
        # TODO: apply the bayesian classification to the testing data
        pass
