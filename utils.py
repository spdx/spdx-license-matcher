import gzip
import os
from io import BytesIO

import jpype


def colors(string, color):
    """To make things colorful

    Arguments:
        string {string} -- string to be colored.
        color {integer} -- color
    """
    return("\033[%sm%s\033[0m" % (color, string))


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
    if (jpype.isJVMStarted()==0):

        # If JVM not already started, start it, attach a Thread and start processing the request
        classpath = os.path.join(os.path.abspath("."), "tool.jar")
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s"%classpath, convertStrings=False)

    # Attach a Thread and start processing the request
    jpype.attachThreadToJVM()
    package = jpype.JPackage("org.spdx.rdfparser.license")
    licenseinfofactoryclass = package.LicenseInfoFactory
    try:

        # Call the method getListedLicenseById present in the SPDX Tools
        listed_license = licenseinfofactoryclass.getListedLicenseById(licenseId)
        jpype.detachThreadFromJVM()
        return listed_license
    except:
        jpype.detachThreadFromJVM()
        raise


def checkTextStandardLicense(license, compareText):
    """Compares the license text to the license text of SPDX Standard License.

    Arguments:
        license {string} -- SPDX standard license.
        compareText {string} -- Text to compare with the standard license.

    Returns:
        string -- Difference message if any differences found or None.
    """

    if (jpype.isJVMStarted()==0):

        # If JVM not already started, start it, attach a Thread and start processing the request
        classpath = os.path.join(os.path.abspath("."), "tool.jar")
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s"%classpath, convertStrings=False)

    # Attach a Thread and start processing the request
    jpype.attachThreadToJVM()
    package = jpype.JPackage("org.spdx.compare")
    compareclass = package.LicenseCompareHelper
    try:

        # Call the java method isTextStandardLicense present in the SPDX Tools
        diff = compareclass.isTextStandardLicense(license, compareText)
        isDifferenceFound = jpype.JBoolean(diff.isDifferenceFound())
        jpype.detachThreadFromJVM()
        return isDifferenceFound
    except:
        jpype.detachThreadFromJVM()
        raise
