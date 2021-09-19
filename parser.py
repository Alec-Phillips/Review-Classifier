#
# parser to determine which words we actually care about from the reviews 
#


# import nltk
import string


def get_words(text):
    text = text.lower()
    punctuations = '!?.,&(/)-;'
    new_text = ''
    for char in text:
        if char in string.punctuation:
            char += ' '
        new_text += char
    text = ''.join([char for char in new_text if char not in punctuations])
    words = text.split()

    return words

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


class WordCounts:

    def __init__(self):
        self.word_count_pos = {}
        self.word_count_neg = {}
        self.word_count_total = {}
        self.get_counts()



    def get_counts(self):
        
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
        #temp_list = []
        # for word in self.word_count_total:
        #     if self.word_count_total.get(word)<4 or self.word_count_total.get(word)>554:
        #         temp_list.append(word)
        # for word in temp_list:
        #     del self.word_count_total[word]

        temp_list = []
        for word in self.word_count_pos:
            if self.word_count_pos.get(word) < 4 or self.word_count_pos.get(word) > 450:
                temp_list.append(word)
        for word in temp_list:
            del self.word_count_pos[word]

        temp_list = []
        for word in self.word_count_neg:
            if self.word_count_neg.get(word) < 4 or self.word_count_neg.get(word) > 400:
                temp_list.append(word)
        for word in temp_list:
            del self.word_count_neg[word]

        # new_list = sorted(self.word_count_neg.items(), key=lambda x: x[1], reverse=False)
        #
        # for item in new_list:
        #     print(item)
        # print(new_list)

counter = WordCounts()
counter.clean_data()





