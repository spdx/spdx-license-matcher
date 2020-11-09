# -*- coding: utf-8 -*-
import re

URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
COPYRIGHT_NOTICE_REGEX = r"((?<=\n)|.*)Copyright.+(?=\n)|Copyright.+\\n"
COPYRIGHT_SYMBOLS = r"[©Ⓒⓒ]"
BULLETS_NUMBERING_REGEX = r"\s(([0-9a-z]\.\s)+|(\([0-9a-z]\)\s)+|(\*\s)+)|(\s\([i]+\)\s)"
COMMENTS_REGEX = r"(\/\/|\/\*|#) +.*"
EXTRANEOUS_REGEX = r"(?is)\s*end of terms and conditions.*"
ADDENDIUM_EXHIBIT_REGEX = r"(?s)(APPENDIX|APADDENDUM|EXHIBIT).*"
VARIETAL_WORDS_SPELLING = {
    'acknowledgment': 'acknowledgement',
    'analogue': 'analog',
    'analyse': 'analyze',
    'artefact': 'artifact',
    'authorisation': 'authorization',
    'authorised': 'authorized',
    'calibre': 'caliber',
    'cancelled': 'canceled',
    'capitalisations': 'capitalizations',
    'catalogue': 'catalog',
    'categorise': 'categorize',
    'centre': 'center',
    'emphasised': 'emphasized',
    'favour': 'favor',
    'favourite': 'favorite',
    'fulfil': 'fulfill',
    'fulfilment': 'fulfillment',
    'initialise': 'initialize',
    'judgment': 'judgement',
    'labelling': 'labeling',
    'labour': 'labor',
    'licence': 'license',
    'maximise': 'maximize',
    'modelled': 'modeled',
    'modelling': 'modeling',
    'offence': 'offense',
    'optimise': 'optimize',
    'organisation': 'organization',
    'organise': 'organize',
    'practise': 'practice',
    'programme': 'program',
    'realise': 'realize',
    'recognise': 'recognize',
    'signalling': 'signaling',
    'sub-license': 'sublicense',
    'sub license': 'sublicense',
    'utilisation': 'utilization',
    'whilst': 'while',
    'wilful': 'wilfull',
    'non-commercial': 'noncommercial',
    'per cent': 'percent',
    'owner': 'holder'
}


def normalize(licenseText):
    """Normalize the license text with all the SPDX license list matching guidelines.

    Arguments:
        licenseText {string} -- licenseText is the license text of the license.

    Returns:
        string -- license text nomalized with all the SPDX matching guidelines.
    """

    # To avoid a possibility of a non-match due to urls not being same.
    licenseText = re.sub(URL_REGEX, 'normalized/url', licenseText)

    # To avoid the license mismatch merely due to the existence or absence of code comment indicators placed within the license text, they are just removed.
    licenseText = re.sub(COMMENTS_REGEX, "", licenseText)

    # To avoid a license mismatch merely because extraneous text that appears at the end of the terms of a license is different or missing.
    licenseText = re.sub(EXTRANEOUS_REGEX, "", licenseText)
    licenseText = re.sub(ADDENDIUM_EXHIBIT_REGEX, "", licenseText)

    # By using a default copyright symbol (c)", we can avoid the possibility of a mismatch.
    licenseText = re.sub(COPYRIGHT_SYMBOLS, "(C)", licenseText)

    # To avoid a license mismatch merely because the copyright notice is different, it is not substantive and is removed.
    licenseText = re.sub(COPYRIGHT_NOTICE_REGEX, "", licenseText)

    # To avoid a possibility of a non-match due to case sensitivity.
    licenseText = licenseText.lower()

    # To remove the license name or title present at the beginning of the license text.
    if 'license' in licenseText.split('\n')[0]:
        licenseText = '\n'.join(licenseText.split('\n')[1:])

    # To avoid the possibility of a non-match due to variations of bullets, numbers, letter, or no bullets used are simply removed.
    licenseText = re.sub(BULLETS_NUMBERING_REGEX, " ", licenseText)

    # To avoid the possibility of a non-match due to the same word being spelled differently.
    for initial, final in list(VARIETAL_WORDS_SPELLING.items()):
        licenseText = licenseText.replace(initial, final)

    # To avoid the possibility of a non-match due to different spacing of words, line breaks, or paragraphs.
    licenseText = " ".join(licenseText.split())
    return licenseText
