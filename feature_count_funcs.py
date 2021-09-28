


def count_pos_stems(pos_stems, review):
    count = 0
    for stem in review:
        if stem in pos_stems:
            count += 1
    return count

def count_neg_stems(neg_stems, review):
    count = 0
    for stem in review:
        if stem in neg_stems:
            count += 1
    return count

feature_count_funcs = [count_pos_stems, count_neg_stems]
