def get_dice_coefficient(a_bigram, b_bigram):
    """Sorensen dice coefficient may be calculated for two strings,
    x and y for the purpose of string similarity measure. Dice coefficient
    is defined as 2nt/(na + nb), where nt is the number of character bigrams
    found in both strings, na is the number of bigrams in string a and nb
    is the number of bigrams in string b.

    Arguments:
        a_bigram {list} -- list of bigrams formed by tokenizes normalized license text a.
        b_bigtam {list} -- list of bigrams formed by tokenizes normalized license text b.

    Return:
        float -- A statistic used to gauge the similarity of two license texts.
    """
    # Case for empty license text
    if not len(a_bigram) or not len(b_bigram):
        return 0.0
    # Case for true duplicates
    if a_bigram == b_bigram:
        return 1.0
    # Spl case: if a_bigram != b_bigram, and a_bigram or b_bigram is made up of single characters,
    # then there is no possible match
    if len(a_bigram) == 1 or len(b_bigram) == 1:
        return 0.0

    a_bigram.sort()
    b_bigram.sort()

    # Assignments to save function calls
    lena = len(a_bigram)
    lenb = len(b_bigram)

    # Matches is used to count the matches between a_bigram and b_bigram
    matches = i = j = 0
    while (i < lena and j < lenb):
        if a_bigram[i] == b_bigram[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram[i] < b_bigram[j]:
            i += 1
        else:
            j += 1

    score = float(matches)/float(lena + lenb)
    return score
