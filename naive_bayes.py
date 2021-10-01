

class BayesClassifier:

    def __init__(self, distinct_words, labeled_reviews):
        '''
        bag_of_words = the distinct stems found in the data being classified
        labeled_reviews = the training data that the classifier will use
        '''
        self.distinct_words = distinct_words
        self.labeled_reviews = labeled_reviews

        # a mapping from stem -> int for positive reviews
        self.positive_stem_counts = {} 
        # a mapping from stem -> int for negative reviews
        self.negative_stem_counts = {}
        self.total_negative = 0
        self.total_positive = 0
        # maps label -> pr[label]
        self.label_frequency_distribution = {}
        # maps feature (stem) -> (pr[feature | pos], pr[feature | neg])
        self.feature_frequency_distribution = {}
        # self.distinct_stems = set()
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0
        self.precision = 0
        self.recall = 0
        self.f_measure = 0

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
                    self.total_positive += 1
                    if stem in self.positive_stem_counts:
                        self.positive_stem_counts[stem] = self.positive_stem_counts.get(stem) + 1
                    else:
                        self.positive_stem_counts[stem] = 1
                        # self.distinct_stems.add(stem)
            else:
                label_frequencies['neg'] = label_frequencies.get('neg') + 1
                for stem in review[0]:
                    total_stems += 1
                    self.total_negative += 1
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
        '''
        does a basic analysis of stem usefulness
        determines the 'num_returned' most useful positive stems as well as the
        'num_returned' most useful negative stems
        '''
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
        
    def classify(self, stems):
        '''
        classifies a single review as positive or negative
        returns 1 if classified as positive, 0 if classified as negative
        '''
        prob_by_word = {}
        prob_negative = self.label_frequency_distribution['neg']
        prob_positive = self.label_frequency_distribution['pos']
        for stem in stems:
            if stem in self.negative_stem_counts:
                numerator = self.negative_stem_counts.get(stem) + 1
            else:
                numerator = 1
            denominator = self.total_negative + len(self.distinct_words)
            prob_by_word[stem] = numerator / denominator

        for stem in prob_by_word:
            prob_negative *= prob_by_word.get(stem)

        prob_by_word = {}
        for stem in stems:
            if stem in self.positive_stem_counts:
                numerator = self.positive_stem_counts.get(stem) + 1
            else:
                numerator = 1
            denominator = self.total_positive + len(self.distinct_words)
            prob_by_word[stem] = numerator / denominator

        for stem in prob_by_word:
            prob_positive *= prob_by_word.get(stem)
        
        return 1 if prob_positive > prob_negative else 0

    def test(self, testing_data):
        '''
        apply the classifier to the testing data set
        returns the percent correct and the list of potentially fake reviews
        '''
        correct = 0
        incorrect = 0

        fake = []
        for review in testing_data:
            stems = review[0]
            c = 1 if review[1] == 'pos' else 0
            classification = self.classify(stems)
            if classification == c:
                correct += 1
            else:
                incorrect += 1
                fake.append((c, review[2]))
            if classification == 1 and c == 1:
                self.true_positive += 1
            if classification == 0 and c == 0:
                self.true_negative += 1
            if classification == 1 and c == 0:
                self.false_positive += 1
            if classification == 0 and c == 1:
                self.false_negative += 1
        
        return correct / (correct + incorrect), fake

    def get_precision(self):
        self.precision = self.true_positive / (self.true_positive + self.false_positive)
        return self.precision

    def get_recall(self):
        self.recall = self.true_positive / (self.true_positive + self.false_negative)
        return self.recall

    def get_fmeasure(self):
        self.f_measure = (2 * self.precision * self.recall) / (self.precision + self.recall)
        return self.f_measure

