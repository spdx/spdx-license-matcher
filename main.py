import argparse

from pyfiglet import figlet_format

from compare import compare
from utils import colors


def main():
    parser = argparse.ArgumentParser(description='SPDX License Match tool help.')
    parser.add_argument("filename", help="Please provide a file with License text to match against the SPDX License database.")
    args = parser.parse_args()
    filename = args.filename
    with open(filename) as file:
        inputText = file.read()
    inputText = bytes(inputText, 'utf-8').decode('unicode-escape')
    license, score = compare(inputText)
    print(colors('STATUS', 92))
    print('Input license text matches with that of {} with a dice coefficient of {}'.format(license, score))


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    print(colors(figlet_format('SPDX License Match Tool v1.0', font='standard'), 92))
    print('\n')
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
