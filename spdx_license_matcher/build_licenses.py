from concurrent.futures import ThreadPoolExecutor

import redis
import requests
from dotenv import load_dotenv
import os
from urllib.parse import urljoin

from spdx_license_matcher.normalize import normalize
from spdx_license_matcher.utils import compressStringToBytes

load_dotenv()

r = redis.StrictRedis(host=os.environ.get(key="SPDX_REDIS_HOST", default="localhost"), port=6379, db=0)


def get_url(url):
    """GET URL and return response"""
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    headers = {'User-Agent': user_agent }
    res = requests.get(url, headers=headers)
    return res


def build_spdx_licenses():
    """ Get data from SPDX license list and set data in redis.
    """
    url = 'https://spdx.org/licenses/licenses.json'

    # Delete all the keys in the current database
    r.flushdb()

    response = requests.get(url)
    licensesJson = response.json()
    licenses = licensesJson['licenses']
    licensesUrl = [urljoin(url, license.get('reference')) for license in licenses]

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


def is_keys_empty():
    """To check if the keys in redis is present or not.

    Returns:
        bool -- returns if the spdx licenses is present in the redis database or not.
    """
    return True if r.keys('*') == [] else False
