
import math

from feature_count_funcs import feature_count_funcs

class LogisticRegressionClassifier:

    def __init__(self):
        '''
        TODO: include params needed to perform gradient descent
        '''
        self.weights = []
        self.bias = 0

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



# log_reg = LogisticRegressionClassifier()
# print(log_reg.sigmoid_function(0))
# dist = log_reg.loss_function(1, 0)
# print(dist)
# print(log_reg.gradient_descent([[3, 2]], [1]))