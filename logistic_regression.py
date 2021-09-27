
import math

class LogisticRegressionClassifier:

    def __init__(self):
        '''
        TODO: include params needed to perform gradient descent
        '''
        pass

    def gradient_descent(self, x, y):
        '''
        param x: the vector of feature results
        param y: the vector of correct labels
        param w: the vector of the weights and also the bias
        also utilizes:
            our loss_function
            our sigmoid function and dot product
        TODO: implement gradient descent based on pseudocode from textbook
        '''
        w = [0 * (len(x) + 1)]
        # for i in range(len(x)):


    def loss_function(self, y, y_hat):
        '''
        param y: the correct classification
        param y_hat: the estimated classification
        return: the 'distance' between y and y_hat
        TODO: implement loss functions based on algorithm in textbook
        implements the Cross Entropy Loss function based on the textbook
        '''
        return -1 * ( (y * math.log(y_hat)) + ((1 - y) * math.log(1 - y_hat)) )


    def sigmoid_function(self, z):
        '''
        determines the liklihood of positive based on our z value
        z value calculated using (dot product of weights and features) + bias
        '''
        return 1/(1+(math.e**(-1*z)))


log_reg = LogisticRegressionClassifier()
dist = log_reg.loss_function(1, 0)
print(dist)