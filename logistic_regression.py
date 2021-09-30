
import math

from feature_count_funcs import feature_count_funcs

class LogisticRegressionClassifier:

    def __init__(self, labeled_reviews):
        '''
        TODO: include params needed to perform gradient descent
        '''
        self.weights = []
        self.bias = 0
        self.labeled_reviews = labeled_reviews
        self.positive_bigram_counts = {}
        self.negative_bigram_counts = {}
        self.bigram_frequency_distribution = {}
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0
        self.precision = 0
        self.recall = 0
        self.f_measure = 0

    def gradient_descent(self, x_list, y):
        '''
        param x: the list of vectors of feature results for each review
        param y: the vector of correct labels for each review
        also utilizes:
            our loss_function
            our sigmoid function and dot product
        '''
        learning_rate = .1
        w = [0] * (len(x_list[0]) + 1)
        for review_counter, x in enumerate(x_list):
            current_vector = [0] * (len(x) + 1)
            for i in range(len(x)):
                current_term = (self.sigmoid_function(self.get_y_hat(w[:-1], x, w[-1])) - y[review_counter]) * x[i]
                current_vector[i] = current_term
            final_term = (self.sigmoid_function(self.get_y_hat(w[:-1], x, w[-1])) - y[review_counter])
            current_vector[-1] = final_term
            for i in range(len(current_vector)):
                current_vector[i] *= learning_rate
            for i in range(len(w)):
                w[i] -= current_vector[i]
        self.weights = w[:-1]
        self.bias = w[-1]
        return w

    def loss_function(self, y, y_hat):
        '''
        param y: the correct classification
        param y_hat: the estimated classification
        return: the 'distance' between y and y_hat
        implements the Cross Entropy Loss function based on the textbook
        '''
        return -1 * ( (y * math.log(y_hat)) + ((1 - y) * math.log(1 - y_hat)) )


    def sigmoid_function(self, z):
        '''
        determines the liklihood of positive based on our z value
        z value calculated using (dot product of weights and features) + bias
        '''
        return 1/(1+(math.e**(-1*z)))

    def get_y_hat(self, w, x, b):
        '''
        returns the dot product of w and x and sums that result with b
        '''
        dot = 0
        for i, weight in enumerate(w):
            dot += (weight * x[i])
        return dot + b

    def train(self, training_data, pos_word_set, neg_word_set):
        '''
        determines the feature counts for each review
        and uses gradient descent to optimize weights
        for each feature
        returns: the vector of optimized weights
        '''
        feature_counts = []
        labels = []
        for review in training_data:
            if review[1] == 'pos':
                labels.append(1)
            else:
                labels.append(0)
            curr_feature_counts = []
            # for func in feature_count_funcs:
            count1 = feature_count_funcs[0](pos_word_set, review[0])
            curr_feature_counts.append(count1)
            count2 = feature_count_funcs[1](neg_word_set, review[0])
            curr_feature_counts.append(count2)
            feature_counts.append(curr_feature_counts)
        weights = self.gradient_descent(feature_counts, labels)
        return weights

    def classify(self, feature_results):
        '''
        classifies a single review based on its feature results and
        the computed weights
        '''
        dot_product = self.get_y_hat(self.weights, feature_results, self.bias)
        prediction = self.sigmoid_function(dot_product)
        return 1 if prediction >= .5 else 0

    def count_bigrams(self):
        '''
        gets the:
            most useful positive bigrams
            most useful negative bigrams
        '''
        label_frequencies = {'pos': 0, 'neg': 0}
        total_stems = 0
        for review in self.labeled_reviews:
            if review[1] == 'pos':
                label_frequencies['pos'] = label_frequencies.get('pos') + 1
                for i in range(len(review[0]) - 1):
                    total_stems += 1
                    bigram = review[0][i] + ' ' + review[0][i + 1]
                    # self.total_positive += 1
                    if bigram in self.positive_bigram_counts:
                        self.positive_bigram_counts[bigram] = self.positive_bigram_counts.get(bigram) + 1
                    else:
                        self.positive_bigram_counts[bigram] = 1
                        # self.distinct_stems.add(stem)
            else:
                label_frequencies['neg'] = label_frequencies.get('neg') + 1
                for i in range(len(review[0]) - 1):
                    total_stems += 1
                    bigram = review[0][i] + ' ' + review[0][i + 1]
                    # self.total_negative += 1
                    if bigram in self.negative_bigram_counts:
                        self.negative_bigram_counts[bigram] = self.negative_bigram_counts.get(bigram) + 1
                    else:
                        self.negative_bigram_counts[bigram] = 1
                        # self.distinct_stems.add(stem)
        total_labels = 0
        for _, frequency in label_frequencies.items():
            total_labels += frequency
        for label, frequency in label_frequencies.items():
            self.bigram_frequency_distribution[label] = frequency / total_labels
        for stem, count in self.positive_bigram_counts.items():
            self.bigram_frequency_distribution[stem] = {'pos': (count/total_stems)/self.bigram_frequency_distribution['pos'], 'neg': 0}
        for stem, count in self.negative_bigram_counts.items():
            if stem in self.bigram_frequency_distribution:
                self.bigram_frequency_distribution[stem]['neg'] = (count/total_stems)/self.bigram_frequency_distribution['neg']
            else:
                self.bigram_frequency_distribution[stem] = {'pos': 0, 'neg': (count/total_stems)/self.bigram_frequency_distribution['neg']}

    def most_useful_bigrams(self, num_returned):
        pos_usefulness = []
        neg_usefulness = []
        for feature, distribution in self.bigram_frequency_distribution.items():
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

    def test(self, testing_data, feature_count_vectors):
        incorrect = 0
        for i, tup in enumerate(testing_data):
            review = tup[0]
            label = 1 if tup[1] == 'pos' else 0
            current_feature_counts = feature_count_vectors[i]
            z = self.get_y_hat(self.weights, current_feature_counts, self.bias)
            prob_pos = self.sigmoid_function(z)
            # print(prob_pos, label)
            prediction = 1 if prob_pos > .5 else 0
            if prediction != label:
                incorrect += 1
            if prediction == 1 and label == 1:
                self.true_positive += 1
            if prediction == 0 and label == 0:
                self.true_negative += 1
            if prediction == 1 and label == 0:
                self.false_positive += 1
            if prediction == 0 and label == 1:
                self.false_negative += 1
        return incorrect

    def get_precision(self):
        self.precision = self.true_positive / (self.true_positive + self.false_positive)
        return self.precision

    def get_recall(self):
        self.recall = self.true_positive / (self.true_positive + self.false_negative)
        return self.recall

    def get_fmeasure(self):
        self.f_measure = (2 * self.precision * self.recall) / (self.precision + self.recall)
        return self.f_measure
