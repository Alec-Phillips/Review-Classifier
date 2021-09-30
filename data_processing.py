
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
nb_precision = bayes_classifier.get_precision()
nb_recall = bayes_classifier.get_recall()
nbfMeasure = bayes_classifier.get_fmeasure()
print(f"\nNaive Bayes:\n\tPrecision: {nb_precision}\n\tRecall: {nb_recall}\n\tF-Measure: {nbfMeasure}")
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
# weights = log_reg_classifier.train(training, positive_stems, negative_stems)
print('')
# for i, weight in enumerate(weights):
#     if i == len(weights) - 1:
#         print(f'Bias: {weight}')
#     else:
#         print(f'Weight {i}: {weight}')

log_reg_classifier.count_bigrams()
pos_bigrams, neg_bigrams = log_reg_classifier.most_useful_bigrams(300)
pos_bigram_set = set()
neg_bigram_set = set()
for item in pos_bigrams:
    pos_bigram_set.add(item[1])
for item in neg_bigrams:
    neg_bigram_set.add(item[1])
# print(pos_bigrams)
# print(neg_bigrams)

def count_feat1(review):
    pos_count = 0
    for word in review:
        if word in positive_stems:
            pos_count += 1
    return pos_count

def count_feat2(review):
    neg_count = 0
    not_count = 0
    for word in review:
        if word in negative_stems:
            neg_count += 1
        if word == "not":
            print('found not')
            not_count += 1
    return neg_count

# def count_feat3(review):
#     count = 0
#     for word in review:
#         if word == "amaz":
#             count += 1
#         if word == "great":
#             count += 1
#         if word == "works":
#             count += 1
#     return count

def count_feat4(review):
    count = 0
    for i in range(len(review) - 1):
        bigram = review[i] + ' ' + review[i + 1]
        if bigram in pos_bigram_set:
            count += 1
    return count

def count_feat5(review):
    count = 0
    for i in range(len(review) - 1):
        bigram = review[i] + ' ' + review[i + 1]
        if bigram in neg_bigram_set:
            count += 1
    return count

feature_count_vectors = []
labels = []
for tup in training:
    review = tup[0]
    feature_counts = []
    feature_counts.append(count_feat1(review))
    feature_counts.append(count_feat2(review))
    # feature_counts.append(count_feat3(review))
    feature_counts.append(count_feat4(review))
    feature_counts.append(count_feat5(review))
    feature_count_vectors.append(feature_counts)
    label = 1 if tup[1] == 'pos' else 0
    labels.append(label)

# for f_c in feature_count_vectors:
#     if f_c[3] != 0 or f_c[4] != 0:
#         print('yes')
weights = log_reg_classifier.gradient_descent(feature_count_vectors, labels)
# print(weights)

testing_feature_count_vectors = []
testing_labels = []
for tup in testing:
    review = tup[0]
    feature_counts = []
    feature_counts.append(count_feat1(review))
    feature_counts.append(count_feat2(review))
    # feature_counts.append(count_feat3(review))
    feature_counts.append(count_feat4(review))
    feature_counts.append(count_feat5(review))
    testing_feature_count_vectors.append(feature_counts)
    label = 1 if tup[1] == 'pos' else 0
    # print(label, tup[1])
    # print(review, feature_counts)
    testing_labels.append(label)

incorrect = log_reg_classifier.test(testing, testing_feature_count_vectors)
print('Percent Correct: ', (1000 - incorrect) / 10)

lr_precision = log_reg_classifier.get_precision()
lr_recall = log_reg_classifier.get_recall()
lr_f_measure = log_reg_classifier.get_fmeasure()
print(f"\nLogistic Regression:\n\tPrecision: {lr_precision}\n\tRecall: {lr_recall}\n\tF-Measure: {lr_f_measure}")
# print(incorrect)






