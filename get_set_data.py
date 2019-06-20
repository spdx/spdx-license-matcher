import json
from re import compile

import grequests
import redis
import requests
from bs4 import BeautifulSoup

from utils import compressStringToBytes


URL = 'https://raw.github.com/spdx/license-list-data/master/json/details/'


def get_set_data():
    """Used to get data from SPDX dataset and set data in redis.
    """
    url = 'https://github.com/spdx/license-list-data/tree/master/json/details'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    aTags = soup.find_all('a', {"title": compile("json")})
    licenses = []
    for aTag in aTags:
        licenses.append(aTag.get('title'))
    licenses_url = [URL+license for license in licenses]
    rs = (grequests.get(u) for u in licenses_url)
    # Send them all at the same time:
    responses = grequests.map(rs)
    for response in responses:
        licenseJson = json.loads(response.content.decode('utf-8'))
        licenseName = licenseJson['licenseId']
        licenseText = licenseJson['licenseText']
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        compressedText = compressStringToBytes(licenseText)
        r.set(licenseName, compressedText)
