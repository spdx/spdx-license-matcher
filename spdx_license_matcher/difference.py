import difflib

import jellyfish


def generate_diff(originalLicenseText, inputLicenseText):
    """Generate difference of the input license text with that of SPDX license.

    Arguments:
        originalLicenseText {string} -- SPDX license text of the closely matched license.
        inputLicenseText {string} -- license text input by the user.

    Returns:
        list -- list of lines containing the difference between the two license texts.
    """
    lines = []
    for line in difflib.unified_diff(originalLicenseText.splitlines(), inputLicenseText.splitlines()):
        lines.append(line)
    return lines


def get_similarity_percent(text1, text2):
    """Levenshtein distance, a string metric for measuring the difference between two sequences, is used to calculate the similarity percentage between two license texts.

    Arguments:
        text1 {string} -- string 1
        text2 {string} -- string 2

    Returns:
        float -- similarity percentage between the two given texts.
    """
    levDis = jellyfish.levenshtein_distance(text1, text2)
    bigger = max(len(text1), len(text2))
    similarityPercentage = round((bigger - levDis) / bigger * 100, 2)
    return similarityPercentage
