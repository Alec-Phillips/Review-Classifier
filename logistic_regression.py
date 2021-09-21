
import math
positives = {'good', 'great', 'awesome', 'beautiful', 'amazed', 'recommend',
                'easy', 'works', 'love', 'fast', 'superior', 'best', 'correctly', 'happy'}

negatives = {'bad', 'ineffective', 'maddening', 'flaws', 'clogged', 'problem',
                'worse', 'defective', 'issue', 'junk', 'trash', 'ridiculous',
                'frustrated', 'disappointed', 'crap', 'unusable', 'irritating',
                'errors', 'horrible'}



def number_positive(words):
    count = 0
    for word in words:
        if word in positives:
            count += 1
    return count

def number_negative(words):
    count = 0
    for word in words:
        if word in negatives:
            count += 1
    return count

def contains_not(words):
    if 'not' in words:
        return 1
    return 0


features = [number_positive, number_negative, contains_not]
weights = [5, -5, -1.5]

bias = .1


text = 'this is a bad product'
words = ['crap', 'awesome', 'great', 'bad', 'good']

feature_results = []
for i, feature_func in enumerate(features):
    feature_results.append(feature_func(words))

print(feature_results)

z = bias
for i, weight in enumerate(weights):
    z += weight * feature_results[i]

print(z)

prob_pos = 1/(1+(math.e**(-1*z)))

print(prob_pos)

