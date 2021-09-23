#
# parser to determine which words we actually care about from the reviews 
#


import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# words = word_tokenize('this is a sentence')
# print(words)

import string


def get_words(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [ps.stem(word) for word in words]
    words = [word for word in words if word not in string.punctuation]
    return words
    # punctuations = '!?.,&(/)-;'
    # new_text = ''
    # for char in text:
    #     if char in string.punctuation:
    #         char += ' '
    #     new_text += char
    # text = ''.join([char for char in new_text if char not in punctuations])
    # words = text.split()

    # return words

def count_words(words, counter, total):
    for word in words:
        if word in counter:
            counter[word] = counter.get(word) + 1
        else:
            counter[word] = 1
        if word in total:
            total[word] = total.get(word) + 1
        else:
            total[word] = 1


class DataPoint:
    '''
    each 'data point' consists of a document and its associated class
    in this case, document = review, class = pos/neg
    '''

    def __init__(self, d, c):
        '''
        d = document/review
        c = class (positive or negative)
        '''
        self.d = d
        self.c = c

    # def __repr__(self):
    #     print(self.d, self.c)


class Data:
    '''
    container to store all the data and its classification
    this can then be split and run through the classifier
    '''

    def __init__(self):
        '''
        data is the list of DataPoint objects
        '''
        self.data = []

    # def __repr__(self):
    #     for data_point in self.data:
    #         print(data_point)

    def add_data_point(self, data_point):
        self.data.append(data_point)

class WordCounts:
    '''
    holds the mappings of word to their associated count
    has one mapping for positive and one for negative
    has all the data needed to compute the naive bayes classification
    '''

    def __init__(self):
        self.word_count_pos = {}
        self.word_count_neg = {}
        self.word_count_total = {}
        self.total_negative = 0
        self.total_positive = 0
        self.distinct_words = set()
        self.setup()

    def setup(self):
        self.get_counts()
        self.clean_data()
        self.get_class_totals()
        self.get_distinct_words()



    def get_counts(self):

        # negative_ratings_file = open('Homework2-Data/ratings/negative.txt')
        # negative_ratings = [int(x[-3]) for x in negative_ratings_file.read().splitlines()]

        # positive_ratings_file = open('Homework2-Data/ratings/positive.txt')
        # positive_ratings = [int(x[-3]) for x in positive_ratings_file.read().splitlines()]
        i = 1

        while i <= 1000:
            negative_file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
            f = open(negative_file_name)
            text = f.read()
            words = get_words(text)
            count_words(words, self.word_count_neg, self.word_count_total)
            f.close()

            positive_file_name = 'Homework2-Data/pos/pos_' + str(i) + '.txt'
            f = open(positive_file_name)
            text = f.read()
            words = get_words(text)
            count_words(words, self.word_count_pos, self.word_count_total)
            f.close()

            i += 1


    def clean_data(self):

        temp_list = []
        for word in self.word_count_pos:
            if self.word_count_pos.get(word) < 1 or self.word_count_pos.get(word) > 1000:
                temp_list.append(word)
        for word in temp_list:
            del self.word_count_pos[word]

        temp_list = []
        for word in self.word_count_neg:
            if self.word_count_neg.get(word) < 1 or self.word_count_neg.get(word) > 1000:
                temp_list.append(word)
        for word in temp_list:
            del self.word_count_neg[word]


    def get_class_totals(self):
        for word in self.word_count_neg:
            self.total_negative += self.word_count_neg.get(word)
        for word in self.word_count_pos:
            self.total_positive += self.word_count_pos.get(word)

    def get_distinct_words(self):
        for word in self.word_count_neg:
            self.distinct_words.add(word)
        for word in self.word_count_pos:
            self.distinct_words.add(word)


def retrieve_data(data_container):
    
    i = 1
        
    while i <= 1000:
        negative_file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
        f = open(negative_file_name)
        text = f.read()
        f.close()
        new_neg_data_point = DataPoint(text.lower(), 'neg')
        data_container.add_data_point(new_neg_data_point)

        positive_file_name = 'Homework2-Data/pos/pos_' + str(i) + '.txt'
        f = open(positive_file_name)
        text = f.read()
        f.close()
        new_pos_data_point = DataPoint(text.lower(), 'pos')
        data_container.add_data_point(new_pos_data_point)

        i += 1

def train():
    data = Data()
    retrieve_data(data)
    print(data)

train()






