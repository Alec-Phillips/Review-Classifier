
from math import log
import nltk
import string
import random

from importlib import reload

import naive_bayes_2
import logistic_regression
reload(naive_bayes_2)
reload(logistic_regression)
from naive_bayes_2 import BayesClassifier
from logistic_regression import LogisticRegressionClassifier


# get the reviews and label them positive or negative --------------------------
labeled_reviews = []

i = 1
    
while i <= 1000:
    negative_file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
    f = open(negative_file_name)
    text = f.read()
    text = ''.join([char for char in text if char not in string.punctuation])
    f.close()
    new_neg_data_point = (text.lower(), 'neg', i)
    labeled_reviews.append(new_neg_data_point)

    positive_file_name = 'Homework2-Data/pos/pos_' + str(i) + '.txt'
    f = open(positive_file_name)
    text = f.read()
    text = ''.join([char for char in text if char not in string.punctuation])
    f.close()
    new_pos_data_point = (text.lower(), 'pos', i)
    labeled_reviews.append(new_pos_data_point)

    i += 1
# ------------------------------------------------------------------------------

# tokenize the words -----------------------------------------------------------
nltk.download('punkt')
from nltk.tokenize import word_tokenize
tokens = set(word for words in labeled_reviews for word in word_tokenize(words[0]))
labeled_reviews = [(word_tokenize(review[0]), review[1], review[2]) for review in labeled_reviews]
# ------------------------------------------------------------------------------

# remove stopwords -------------------------------------------------------------
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
tokens = [word for word in tokens if word not in stopwords]
labeled_reviews = [([token for token in review[0] if token not in stopwords], review[1], review[2]) for review in labeled_reviews]
# ------------------------------------------------------------------------------

# stem -------------------------------------------------------------
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
stems = [stemmer.stem(word) for word in tokens]
labeled_reviews = [([stemmer.stem(token) for token in review[0]], review[1], review[2]) for review in labeled_reviews]
# ------------------------------------------------------------------------------

# train and test using the naive bayes -----------------------------------------
random.shuffle(labeled_reviews)
training = labeled_reviews[:len(labeled_reviews)//2]
testing = labeled_reviews[len(labeled_reviews)//2:]

bayes_classifier = BayesClassifier(stems, training)
bayes_classifier.train()
most_useful_pos, most_useful_neg = bayes_classifier.report_useful_features(10)
print('pos:')
for label in most_useful_pos:
    print('\t', label)
print('\nneg:')
for label in most_useful_neg:
    print('\t', label)

percent_correct, fake = bayes_classifier.test(testing)
fake = sorted(fake, key=lambda x: x[1])
# print(fake[:25])
print(len(fake))
print(f'Percent Correct: {percent_correct * 100}')
# ------------------------------------------------------------------------------


# train and test using logistic regression -------------------------------------
positive_stems = set()
negative_stems = set()
most_pos, most_neg = bayes_classifier.report_useful_features(100)
for item in most_pos:
    positive_stems.add(item[1])
for item in most_neg:
    negative_stems.add(item[1])

log_reg_classifier = LogisticRegressionClassifier()
weights = log_reg_classifier.train(training, positive_stems, negative_stems)
print('')
for i, weight in enumerate(weights):
    if i == len(weights) - 1:
        print(f'Bias: {weight}')
    else:
        print(f'Weight {i}: {weight}')



