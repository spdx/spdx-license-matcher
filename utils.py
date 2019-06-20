import gzip

from io import StringIO, BytesIO


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
        [string] -- utf-8 decoded text
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
