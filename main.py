import argparse

from pyfiglet import figlet_format

from compare import get_close_matches
from difference import generate_diff, get_similarity_percent
from utils import (checkTextStandardLicense, colors, get_spdx_license_text,
                   getListedLicense)


def main():
    parser = argparse.ArgumentParser(description='SPDX License Match tool help.')
    parser.add_argument("filename", help="Please provide a file with License text to match against the SPDX License database.")
    parser.add_argument('--limit', '-l', type=float, default=0.99, help='limit')
    parser.add_argument('--threshold', '-t', type=float, default=0.9, help='Confidence threshold of the license')
    args = parser.parse_args()
    filename = args.filename
    limit = args.limit
    threshold = args.threshold
    with open(filename) as file:
        inputText = file.read()
    inputText = bytes(inputText, 'utf-8').decode('unicode-escape')
    matches = get_close_matches(inputText, threshold, limit)

    if not matches:
        print('There is not enough confidence threshold for the text to match against the SPDX License database.')

    # When limit < score or if its a perfect match
    elif 1.0 in matches.values() or all(limit < score for score in matches.values()):
        matchingString = 'The following license ID(s) match: ' + ", ".join(matches.keys())
        print(colors(matchingString, 92))
    else:
        for licenseID in matches:
            listedLicense = getListedLicense(licenseID)
            isTextStandard = checkTextStandardLicense(listedLicense, inputText)
            if not isTextStandard:
                matchingString = 'The following license ID(s) match: ' + licenseID
                print(colors(matchingString, 92))
                break
        else:
            licenseID = max(matches, key=matches.get)
            spdxLicenseText = get_spdx_license_text(licenseID)
            similarityPercent = get_similarity_percent(spdxLicenseText, inputText)
            print(colors('\nThe given license text matches {}% with that of {} based on Levenstein distance.'.format(similarityPercent, licenseID), 94))
            differences = generate_diff(spdxLicenseText, inputText)
            for line in differences:
                if line[0] == '+':
                    line = colors(line, 92)
                if line[0] == '-':
                    line = colors(line, 91)
                if line[0] == '@':
                    line = colors(line, 90)
                print(line)


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    print(colors(figlet_format('SPDX License Match Tool v1.0', font='standard'), 92))
    print('\n')
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
