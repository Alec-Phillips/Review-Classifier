#
# parser to determine which words we actually care about from the reviews 
#


import nltk
import string


def parse(text):
    text = text.lower()
    punctuations = '!?.,'
    new_text = ''
    for char in text:
        if char in string.punctuation:
            char += ' '
        new_text += char
    text = ''.join([char for char in new_text if char not in punctuations])
    words = text.split()

    print(words)


word_counter_pos = {}
word_counter_neg = {}


i = 1


while i <= 1000:
    file_name = 'Homework2-Data/neg/neg_' + str(i) + '.txt'
    f = open(file_name)
    text = f.read()
    parse(text)
    f.close()
    break



