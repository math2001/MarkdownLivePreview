""" A small script to convert the images into base64 data """

import struct
from base64 import b64encode


def get_image_size(fhandle):
    """https://stackoverflow.com/a/20380514/6164984"""
    head = fhandle.read(24)
    if len(head) != 24:
        return

    # always going to be png
    check = struct.unpack(">i", head[4:8])[0]
    if check != 0x0D0A1A0A:
        raise ValueError("invalid check (?)")

    width, height = struct.unpack(">ii", head[16:24])
    return width, height


def make_cache(image_name):
    with open("{}.png".format(image_name), "rb") as png, open(
        "{}.base64".format(image_name), "wb"
    ) as base64:
        width, height = get_image_size(png)
        png.seek(0)
        base64.write(bytes("{}\n{}\n".format(width, height), encoding="utf-8"))
        base64.write(b'data:image/png;base64,')
        base64.write(b64encode(png.read()))


make_cache("404")
make_cache("loading")
