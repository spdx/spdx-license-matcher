import difflib
import sys

import jellyfish
import requests

from utils import colors


def generate_diff(licenseId, inputLicenseText):
    """Generate difference of the input license text with that of SPDX license.
    
    Arguments:
        licenseId {string} -- license id that closely matches with the input license text.
        inputLicenseText {string} -- license text input by the user.
    """
    try:
        res = requests.get('https://spdx.org/licenses/{}.json'.format(licenseId))
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    originalLicenseText = res.json()['licenseText']
    levDis = get_levenshtein_distance(originalLicenseText, inputLicenseText)
    bigger = max(len(originalLicenseText), len(inputLicenseText))
    similarityPercentage = round((bigger - levDis) / bigger * 100, 2)
    print(colors('\nThe given license text matches {}% with that of {} based on Levenstein distance.'.format(similarityPercentage, licenseId), 94))

    for line in difflib.unified_diff(originalLicenseText.splitlines(), inputLicenseText.splitlines()):
        if line[0] == '+':
            line = colors(line, 92)
        if line[0] == '-':
            line = colors(line, 91)
        if line[0] == '@':
            line = colors(line, 90)
        print(line)


def get_levenshtein_distance(text1, text2):
    """Levenshtein distance is a string metric for measuring the difference between two sequences.
    
    Arguments:
        text1 {string} -- string 1
        text2 {string} -- string 2
    
    Returns:
        float -- levenshtein distance between the two given texts.
    """
    return jellyfish.levenshtein_distance(text1, text2)
