from .normalize import normalize
from .sorensen_dice import get_dice_coefficient
from .utils import (checkTextStandardLicense, decompressBytesToString,
                   getListedLicense)


def get_close_matches(inputText, licenseData, threshold=0.9):
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
    limit = len(normalizedInputText) * threshold/100.0
    for key in licenseData.keys():
        try:
            licenseName = key.decode('utf-8')
            normalizedLicenseText = decompressBytesToString(licenseData.get(key))
        except IOError:
            licenseName = key
            normalizedLicenseText = normalize(licenseData.get(key))
        score = get_dice_coefficient(normalizedInputText, normalizedLicenseText)

        if score == 1.0:
            perfectMatches[licenseName] = score
        else:
            matches[licenseName] = score
    if perfectMatches:
        return perfectMatches
    matches = {licenseName: score for licenseName, score in matches.items() if score <= limit}
    return matches


def get_matching_string(matches, inputText):
    """Return the matching string with all of the license IDs matched with the input license text if none matches then it returns empty string.
    
    Arguments:
        matches {dictionary} -- Contains the license IDs(which matched with the input text) with their respective sorensen dice score as valus.
        inputText {string} -- license text input by the user.
    
    Returns:
        string -- matching string containing the license IDs that actually matched else returns empty string.
    """
    if not matches:
        matchingString = 'There is not enough confidence threshold for the text to match against the SPDX License database.'
        return matchingString
    
    elif all(score == 1.0 for score in matches.values()):
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
