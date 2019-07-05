import argparse

from pyfiglet import figlet_format

from compare import compare
from difference import generate_diff
from utils import checkTextStandardLicense, colors, getListedLicense


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
    result = compare(inputText, limit)

    # When limit < score or if its a perfect match
    if len(result) == 1:
        (license, score) = list(result.items())[0]
        print(colors('STATUS', 92))
        print('Input license text matches with that of {} with a dice coefficient of {}'.format(license, score))

    else:
        close_matches = {licenseName: score for licenseName, score in result.items() if threshold<score<1.0}
        if all(value < threshold for value in result.values()):
            print('There is not enough confidence threshold for the text to match against the SPDX License database.')
        if close_matches:
            licenseID = max(close_matches, key=close_matches.get)
            listedLicense = getListedLicense(licenseID)
            differences = checkTextStandardLicense(listedLicense, inputText)
            if differences:
                generate_diff(licenseID, inputText)
            else:
                print(colors('The given license is a SPDX Standard License.', 92))



if __name__ == "__main__":
    import time
    s = time.perf_counter()
    print(colors(figlet_format('SPDX License Match Tool v1.0', font='standard'), 92))
    print('\n')
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
