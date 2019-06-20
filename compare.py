import redis

from bigrams import generate_bigrams
from normalize import normalize
from sorensen_dice import get_dice_coefficient
from utils import decompressBytesToString


def compare(text):
    """Normalizes the given license text and forms bigrams before comparing it
    with a database of known licenses.

    Arguments:
        text {string} -- text is the license text input by the user.

    Returns:
        string -- license name with the highest dice coefficient.
        float -- max dice coefficient.
    """
    normalizedText = normalize(text)
    print("[+] Nomalizing the license text...")
    aBigram = generate_bigrams(normalizedText)
    print("[+] Forming bigrams from the normalized text...")
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    print("[+] Comparing with the SPDX License List...")
    diceCoefficients = {}
    for key in r.keys('*'):
        licenseName = key.decode('utf-8')
        licenseText = decompressBytesToString(r.get(key))
        normalizeLicenseText = normalize(licenseText)
        bBigram = generate_bigrams(normalizeLicenseText)
        diceCoefficients[licenseName] = get_dice_coefficient(aBigram, bBigram)
    license, max_dice = key_with_max_val(diceCoefficients)
    return license, max_dice


def key_with_max_val(dictionary):
    """Creates a list of dictionary's keys and values

    Arguments:
        dictionary {dictionary} -- dictionary with license names as keys and 
        associated dice coefficients as values.

    Returns:
        integer -- Returns the maximum value present in the dictionary.
        string -- Key associated with the maximum value.
    """
    v = list(dictionary.values())
    k = list(dictionary.keys())
    return k[v.index(max(v))], max(v)
