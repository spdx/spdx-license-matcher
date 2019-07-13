def generate_bigrams(text):
    """Tokenizes normalized license text into a list of bigrams.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        list -- A list of bigrams formed from the normalized license text.
    """
    # Break the sentence into tokens as well as remove empty tokens if any
    tokens = text.split(" ")

    # Use the zip function to generate bigrams
    # Returns a list of bigrams
    bigrams = zip(*[tokens[i:] for i in range(2)])
    return list(bigrams)
