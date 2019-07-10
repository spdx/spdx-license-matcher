import redis

from bigrams import generate_bigrams
from normalize import normalize
from sorensen_dice import get_dice_coefficient
from utils import decompressBytesToString


def get_close_matches(inputText, threshold, limit):
    """Normalizes the given license text and forms bigrams before comparing it
    with a database of known licenses.

    Arguments:
        text {string} -- text is the license text input by the user.

    Returns:
        dictionary -- dictionary with license name as key and dice coefficient as value.
    """
    normalizedInputText = normalize(inputText)
    aBigram = generate_bigrams(normalizedInputText)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    matches = {}
    perfectMatches = {}
    for key in r.keys('*'):
        licenseName = key.decode('utf-8')
        normalizedLicenseText = decompressBytesToString(r.get(key))
        bBigram = generate_bigrams(normalizedLicenseText)
        score = get_dice_coefficient(aBigram, bBigram)

        # if score is greater then the limit or if its a perfect match then just stop the loop
        if limit < score or score == 1.0:
            perfectMatches[licenseName] = score
            print(perfectMatches)
        else:
            matches[licenseName] = score
    if perfectMatches:
        return perfectMatches
    matches = {licenseName: score for licenseName, score in matches.items() if threshold<score<1.0}
    return matches
