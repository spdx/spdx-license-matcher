from concurrent.futures import ThreadPoolExecutor

import redis
import requests

from normalize import normalize
from utils import compressStringToBytes


def get_url(url):
    """GET URL and return response"""
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    headers = {'User-Agent': user_agent }
    res = requests.get(url, headers=headers)
    return res


def get_set_data():
    """ Get data from SPDX license list and set data in redis.
    """
    url = 'https://spdx.org/licenses/licenses.json'
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    # Delete all the keys in the current database
    r.flushdb()

    response = requests.get(url)
    licensesJson = response.json()
    licenses = licensesJson['licenses']
    licensesUrl = [license.get('detailsUrl') for license in licenses]

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(get_url, licensesUrl))

    for response in responses:
        try:
            licenseJson = response.json()
            licenseName = licenseJson['licenseId']
            licenseText = licenseJson['licenseText']
            normalizeText = normalize(licenseText)
            compressedText = compressStringToBytes(normalizeText)
            r.set(licenseName, compressedText)
        except Exception as e:
            print(e)
            raise


if __name__ == "__main__":
    get_set_data()
