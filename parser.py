#
# parser to determine which words we actually care about from the reviews 
#


# import nltk
import string


def get_words(text):
    text = text.lower()
    punctuations = '!?.,&(/);'
    new_text = ''
    for char in text:
        if char in string.punctuation:
            char += ' '
        new_text += char
    text = ''.join([char for char in new_text if char not in punctuations])
    words = text.split()

    return words

def count_words(words, counter):
    for word in words:
        if word in counter:
            counter[word] = counter.get(word) + 1
        else:
            counter[word] = 1


class WordCounts:

    def __init__(self):
        self.word_count_pos = {}
        self.word_count_neg = {}
        self.get_counts()
        self.total_negative = 0
        self.total_positive = 0
        self.get_class_totals()
        self.distinct_words = set()
        self.get_distinct_words()



    def get_counts(self):
        
        i = 1

        while i <= 1000:
            negative_file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
            f = open(negative_file_name)
            text = f.read()
            words = get_words(text)
            count_words(words, self.word_count_neg)
            f.close()

            positive_file_name = 'Homework2-Data/pos/pos_' + str(i) + '.txt'
            f = open(positive_file_name)
            text = f.read()
            words = get_words(text)
            count_words(words, self.word_count_pos)
            f.close()

            i += 1

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


# counts = WordCounts()
# print(counts.word_count_neg)



