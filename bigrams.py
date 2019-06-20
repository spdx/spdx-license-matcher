import nltk


def generate_bigrams(text):
    """Tokenizes normalized license text into a list of bigrams.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        list -- A list of bigrams formed from the normalized license text.
    """
    nltk_tokens = nltk.word_tokenize(text)
    return list(nltk.bigrams(nltk_tokens))
