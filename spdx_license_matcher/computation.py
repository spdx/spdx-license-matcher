from .bigrams import generate_bigrams
from .normalize import normalize
from .sorensen_dice import get_dice_coefficient
from .utils import (checkTextStandardLicense, decompressBytesToString,
                   getListedLicense)


def get_close_matches(inputText, licenseData, threshold=0.9, limit=0.99):
    """Normalizes the given license text and forms bigrams before comparing it
    with a database of known licenses.

    Arguments:
        text {string} -- text is the license text input by the user.

    Returns:
        dictionary -- dictionary with license name as key and dice coefficient as value.
    """
    matches = {}
    perfectMatches = {}
    normalizedInputText = normalize(inputText)
    aBigram = generate_bigrams(normalizedInputText)
    for key in licenseData.keys():
        try:
            licenseName = key.decode('utf-8')
            normalizedLicenseText = decompressBytesToString(licenseData.get(key))
        except AttributeError:
            licenseName = key
            normalizedLicenseText = normalize(licenseData.get(key))
        bBigram = generate_bigrams(normalizedLicenseText)
        score = get_dice_coefficient(aBigram, bBigram)

        if limit < score or score == 1.0:
            perfectMatches[licenseName] = score
        else:
            matches[licenseName] = score
    if perfectMatches:
        return perfectMatches
    matches = {licenseName: score for licenseName, score in matches.items() if threshold<score<1.0}
    return matches


def get_matching_string(matches, inputText, limit=0.99):
    """Return the matching string with all of the license IDs matched with the input license text if none matches then it returns empty string.
    
    Arguments:
        matches {dictionary} -- Contains the license IDs(which matched with the input text) with their respective sorensen dice score as valus.
        limit {float} -- limit at which we will consider the match as a perfect match.
        inputText {string} -- license text input by the user.
    
    Returns:
        string -- matching string containing the license IDs that actually matched else returns empty string.
    """
    if not matches:
        matchingString = 'There is not enough confidence threshold for the text to match against the SPDX License database.'
        return matchingString
    
    elif 1.0 in matches.values() or all(limit < score for score in matches.values()):
        matchingString = 'The following license ID(s) match: ' + ", ".join(matches.keys())
        return matchingString
    
    else:
        for licenseID in matches:
            listedLicense = getListedLicense(licenseID)
            isTextStandard = checkTextStandardLicense(listedLicense, inputText)
            if not isTextStandard:
                matchingString = 'The following license ID(s) match: ' + licenseID
                return matchingString
        else:
            return ''
