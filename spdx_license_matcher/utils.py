# SPDX-FileCopyrightText: 2019-present SPDX Contributors
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import gzip
import os
from contextlib import contextmanager
from io import BytesIO

import jpype

# Do not remove this line, it is required to import the Java classes.
import jpype.imports  # type: ignore[import]  # noqa: F401
import requests


def _ensure_jvm():
    if not jpype.isJVMStarted():
        dirpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        classpath = os.path.join(dirpath, "tool.jar")
        jpype.startJVM(classpath=[classpath], convertStrings=False)
        from org.spdx.library import SpdxModelFactory

        SpdxModelFactory.init()


@contextmanager
def _jvm_thread():
    JThread = jpype.JClass("java.lang.Thread")
    JThread.attachAsDaemon()
    try:
        yield
    finally:
        JThread.detach()


def colors(string, color):
    """To make things colorful

    Arguments:
        string {string} -- string to be colored.
        color {integer} -- color
    """
    return "\033[%sm%s\033[0m" % (color, string)


def decompressBytesToString(inputBytes):
    """Decompress the given byte array (which must be valid
    compressed gzip data) and return the decoded text (utf-8).

    Arguments:
        inputBytes {bytes} -- A valid compressed gzip byte array

    Returns:
        string -- utf-8 decoded text
    """
    buf = BytesIO()
    stream = BytesIO(inputBytes)
    decompressor = gzip.GzipFile(fileobj=stream, mode='r')
    while True:  # until EOF
        chunk = decompressor.read(8192)
        if not chunk:
            decompressor.close()
            buf.seek(0)
            return buf.read().decode("utf-8")
        buf.write(chunk)
    return None


def compressStringToBytes(inputString):
    """Read the given string, encode it in utf-8, compress
    the data and return it as a byte array.

    Arguments:
        inputString {[type]} -- inputString is the license text of the license.

    Returns:
        byte -- A compressed gzip byte array.
    """
    buf = BytesIO()
    buf.write(inputString.encode("utf-8"))
    buf.seek(0)
    stream = BytesIO()
    compressor = gzip.GzipFile(fileobj=stream, mode='w')
    while True:  # until EOF
        chunk = buf.read(8192)
        if not chunk:  # EOF?
            compressor.close()
            return stream.getvalue()
        compressor.write(chunk)


def getListedLicense(licenseId):
    """Get a SPDX listed license if the given SPDX license ID is present in the SPDX license list otherwise null.

    Arguments:
        licenseId {string} -- SPDX listed license ID

    Returns:
        string -- SPDX listed license or null
    """
    _ensure_jvm()
    with _jvm_thread():
        from org.spdx.library import LicenseInfoFactory

        return LicenseInfoFactory.getListedLicenseByIdCompatV2(licenseId)


def isListedException(licenseId):
    """Check if the given SPDX ID is a SPDX listed license exception ID
    (as opposed to a license ID).

    Arguments:
        licenseId {string} -- SPDX ID to check.

    Returns:
        bool -- True if the ID is a listed license exception ID.
    """
    _ensure_jvm()
    with _jvm_thread():
        from org.spdx.library import LicenseInfoFactory

        return bool(LicenseInfoFactory.isSpdxListedExceptionId(licenseId))


def getListedException(licenseId):
    """Get a SPDX listed license exception if the given ID is present in the
    SPDX exception list otherwise null.

    Arguments:
        licenseId {string} -- SPDX listed license exception ID

    Returns:
        string -- SPDX listed license exception or null
    """
    _ensure_jvm()
    with _jvm_thread():
        from org.spdx.library import LicenseInfoFactory

        return LicenseInfoFactory.getListedExceptionV2ById(licenseId)


def checkTextStandardLicense(license, compareText):
    """Compares the license text to the license text of SPDX Standard License.

    Arguments:
        license {string} -- SPDX standard license.
        compareText {string} -- Text to compare with the standard license.

    Returns:
        bool -- True if a difference is found, False if texts match.
    """
    _ensure_jvm()
    with _jvm_thread():
        from org.spdx.utility.compare import LicenseCompareHelper

        diff = LicenseCompareHelper.isTextStandardLicense(license, compareText)
        return bool(diff.isDifferenceFound())


def checkTextStandardException(licenseException, compareText):
    """Compares the given text to the text of an SPDX listed license exception.

    Arguments:
        licenseException {string} -- SPDX standard license exception.
        compareText {string} -- Text to compare with the standard license exception.

    Returns:
        bool -- True if a difference is found, False if texts match.
    """
    _ensure_jvm()
    with _jvm_thread():
        from org.spdx.utility.compare import LicenseCompareHelper

        diff = LicenseCompareHelper.isTextStandardException(licenseException, compareText)
        return bool(diff.isDifferenceFound())


def get_spdx_license_text(licenseId):
    """Get the text of the closely matched SPDX license or license exception.

    Arguments:
        licenseId {string} -- License ID or Exception ID of the closely matched text.

    Returns:
        string -- returns the spdx license text.
    """
    try:
        # License: https://spdx.org/licenses/MIT.json
        # License exception: https://spdx.org/licenses/389-exception.json
        res = requests.get(f"https://spdx.org/licenses/{licenseId}.json")
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        raise
    except requests.exceptions.RequestException:
        raise
    licenseJson = res.json()
    if 'licenseText' in licenseJson:
        return licenseJson['licenseText']
    if 'licenseExceptionText' in licenseJson:
        return licenseJson['licenseExceptionText']
    raise KeyError(f"No licenseText or licenseExceptionText found for '{licenseId}'")
