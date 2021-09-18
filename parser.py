#
# parser to determine which words we actually care about from the reviews 
#


import nltk
import string


def get_words(text):
    text = text.lower()
    punctuations = '!?.,&'
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


word_counter_pos = {}
word_counter_neg = {}
# distinct_words = set()


i = 1


while i <= 1000:
    negative_file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
    f = open(negative_file_name)
    text = f.read()
    words = get_words(text)
    count_words(words, word_counter_neg)
    f.close()

    positive_file_name = 'Homework2-Data/pos/pos_' + str(i) + '.txt'
    f = open(positive_file_name)
    text = f.read()
    words = get_words(text)
    count_words(words, word_counter_pos)
    f.close()

    i += 1


# print(word_counter_pos['the'])




