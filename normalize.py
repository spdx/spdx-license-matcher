import unicodedata
import re


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


def normalize_unicode(text):
    """Normalize unicode normalizes license text with NFC or
    Normal form composed and return composed character.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text normalized with NFC
    """
    return unicodedata.normalize('NFC', text)


def normalize_url(text):
    """To avoid a possibility of a non-match due to urls not being same.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with all the urls replaced with a normalized url.
    """
    return re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'https://normalized/url', text)


def to_lowercase(text):
    """To avoid a possibility of a non-match due to upper cases or
    lower cases of the same words, both the cases will be treated as lower case.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with all the letters default to lower case.
    """
    return text.lower()


def remove_copyright_statement(text):
    """To avoid a license mismatch merely because the copyright notice is
    different. The copyright notice, for the purposes of matching a license
    to the SPDX License List, should be ignored because it is not part of the 
    substantive license text.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with copyright statement removed.
    """
    return re.sub("((?<=\n\n)|.*)Copyright.+(?=\n\n)|Copyright.+\\n\\n", "", text)


def fix_copyright_symbol(text):
    """By using a default copyright symbol (c)", we can avoid the possibility of a mismatch.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text in which all possible variations of copyright symbols are replaced with (C).
    """
    return re.sub(r"[©Ⓒⓒ]", "(C)", text)


def cleanup_bullets_numbering(text):
    """To avoid the possibility of a non-match due to the otherwise same license
    using bullets instead of numbers, number instead of letter, or no bullets
    instead of bullet, etc., for a list of clauses.

    Arguments:
        text {string} -- text is the license text of the license.
    Returns:
        string -- license text with all the list items removed.
    """
    return re.sub("\s((\d+\.\s)+|(\([0-9a-z]+\)\s)+|(\*\s)+)", " ", text)


def remove_license_name_or_title(text):
    """To avoid a license mismatch merely because the name or title of the license
    is different than how the license is usually referred to or different than the
    SPDX full name. This also avoids a mismatch if the title or name of the license
    is simply not included.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with license name or title removed.
    """
    return re.sub(".*?\\n\\n", "", text, 1)


def replace_varietal_words(text):
    """English uses different spelling for some words. By identifying the spelling
    variations for words found or likely to be found in licenses, we avoid the
    possibility of a non-match due to the same word being spelled differently.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with the varietal words replaced.
    """
    for initial, final in VARIETAL_WORDS_SPELLING.items():
        text = text.replace(initial, final)
    return text


def whitespaces(text):
    """To avoid the possibility of a non-match due to different spacing of
    words, line breaks, or paragraphs.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with all the different spacing, line breaks,
        or paragraphs replaced with a blank space.
    """
    text = " ".join(text.split())
    return text


def normalize(text):
    """Normalize the license text with all the SPDX license list matching guidelines.

    Arguments:
        text {string} -- text is the license text of the license.

    Returns:
        string -- license text with nomalized with all the SPDX matching guidelines.
    """
    text = remove_license_name_or_title(text)
    text = normalize_unicode(text)
    text = normalize_url(text)
    text = fix_copyright_symbol(text)
    text = remove_copyright_statement(text)
    text = to_lowercase(text)
    text = cleanup_bullets_numbering(text)
    text = replace_varietal_words(text)
    text = whitespaces(text)
    return text
