
import nltk
import string
import random


# this import just reloads the local imports incase we edited them
from importlib import reload
# my python environment gets mad without it

import naive_bayes
import logistic_regression
reload(naive_bayes)
reload(logistic_regression)
from naive_bayes import BayesClassifier
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

percent_correct, possible_fake = bayes_classifier.test(testing)
possible_fake = sorted(possible_fake, key=lambda x: x[1])

nb_precision = bayes_classifier.get_precision()
nb_recall = bayes_classifier.get_recall()
nbfMeasure = bayes_classifier.get_fmeasure()
print(f"\nNaive Bayes:\n\tPercent Correct: {percent_correct * 100}\n\tPrecision: {nb_precision}\n\tRecall: {nb_recall}\n\tF-Measure: {nbfMeasure}")
# ------------------------------------------------------------------------------

# train and test using logistic regression -------------------------------------
positive_stems = set()
negative_stems = set()
most_pos, most_neg = bayes_classifier.report_useful_features(300)
for item in most_pos:
    positive_stems.add(item[1])
for item in most_neg:
    negative_stems.add(item[1])

log_reg_classifier = LogisticRegressionClassifier(training)

log_reg_classifier.train(positive_stems, negative_stems)
incorrect = log_reg_classifier.test(testing)

lr_precision = log_reg_classifier.get_precision()
lr_recall = log_reg_classifier.get_recall()
lr_f_measure = log_reg_classifier.get_fmeasure()
print(f"\nLogistic Regression:\n\tPercent Correct: {(1000 - incorrect) / 10}\n\tPrecision: {lr_precision}\n\tRecall: {lr_recall}\n\tF-Measure: {lr_f_measure}")
