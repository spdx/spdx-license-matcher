# Code from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Dice%27s_coefficient
def get_dice_coefficient(a_license, b_license):
    """Sorensen dice coefficient may be calculated for two strings,
    x and y for the purpose of string similarity measure. Dice coefficient
    is defined as 2nt/(na + nb), where nt is the number of character bigrams
    found in both strings, na is the number of bigrams in string a and nb
    is the number of bigrams in string b.

    Arguments:
        a_license {string} --  Normalized license text a.
        b_license {string} -- Normalized license text b.

    Return:
        float -- A statistic used to gauge the similarity of two license texts.
    """
    # Case for empty license text
    if not len(a_license) or not len(b_license):
        return 0.0

    # Case for true duplicates
    if a_license == b_license:
        return 1.0

    # If a != b, and a or b are single chars, then they can't possibly match
    if len(a_license) == 1 or len(b_license) == 1:
        return 0.0

    # Create bigrams
    a_bigram_list = [a_license[i : i + 2] for i in range(len(a_license) - 1)]
    b_bigram_list = [b_license[i : i + 2] for i in range(len(b_license) - 1)]

    a_bigram_list.sort()
    b_bigram_list.sort()

    # Assignments to save function calls
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)

    # Matches is used to count the matches between a_bigram_list and b_bigram_list
    matches = i = j = 0
    while i < lena and j < lenb:
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 1
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1

    score = float(2 * matches) / float(lena + lenb)
    return score
