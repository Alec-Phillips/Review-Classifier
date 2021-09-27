
import math

class LogisticRegressionClassifier:

    def __init__(self):
        '''
        TODO: include params needed to perform gradient descent
        '''
        pass

    def gradient_descent(self):
        '''
        TODO: implement gradient descent based on pseudocode from textbook
        '''

    def loss_function(self):
        '''
        TODO: implement loss functions based on algorithm in textbook
        '''

    def sigmoid_function(self, z):
        '''
        determines the liklihood of positive based on our z value
        z value calculated using (dot product of weights and features) + bias
        '''
        return 1/(1+(math.e**(-1*z)))