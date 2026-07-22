# SPDX-FileCopyrightText: 2019-present SPDX Contributors
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

from concurrent.futures import ThreadPoolExecutor

import redis
import requests
from dotenv import load_dotenv
import os

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
    """Get data from SPDX license list and exception list and set data in Redis.
    """
    # Delete all the keys in the current database
    r.flushdb()

    _build_list(
        'https://spdx.org/licenses/licenses.json',
        'licenses',
        'licenseId',
        'licenseText',
    )
    _build_list(
        'https://spdx.org/licenses/exceptions.json',
        'exceptions',
        'licenseExceptionId',
        'licenseExceptionText',
    )


def _build_list(url, listKey, idField, textField):
    """Helper to download list and set data in Redis.

    Arguments:
        url {string} -- URL of the SPDX list json.
        listKey {string} -- key of the list in the top-level json (e.g. 'licenses', 'exceptions').
        idField {string} -- key of the identifier in each license detail json.
        textField {string} -- key of the license text in each license detail json.
    """
    response = requests.get(url)
    listJson = response.json()
    items = listJson[listKey]
    itemsUrl = [item.get('detailsUrl') for item in items]

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(get_url, itemsUrl))

    for response in responses:
        try:
            itemJson = response.json()
            itemName = itemJson[idField]
            itemText = itemJson[textField]
            normalizeText = normalize(itemText)
            compressedText = compressStringToBytes(normalizeText)
            r.set(itemName, compressedText)
        except Exception as e:
            print(e)
            raise


def is_keys_empty():
    """To check if the keys in redis is present or not.

    Returns:
        bool -- returns if the spdx licenses is present in the redis database or not.
    """
    return True if r.keys('*') == [] else False
