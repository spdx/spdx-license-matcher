import argparse
import sys

import redis
from pyfiglet import figlet_format

from compare import compare, key_with_max_val
from get_set_data import get_set_data
from utils import colors


def main():
    if not len(sys.argv):
        print("ERROR: No file provided. Please provide a file. For more info try the --help flag.")
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description='SPDX License Match tool help.')
    parser.add_argument(
        "filename", help="Please provide a file with License text.")
    args = parser.parse_args()
    filename = args.filename
    f = open(filename, "r")
    inputText = f.read()
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    if r.keys('*') == []:
        # if data is not already set in the redis
        get_set_data()
    license, dice = compare(inputText)
    print(colors('\nSTATUS', 92))
    print('Input license text matches with that of {} with a dice coefficient of {}'.format(
        license, dice))


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    print(colors(figlet_format('SPDX License Match Tool v1.0', font='standard'), 92))
    print('\n')
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
