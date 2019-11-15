""" A small script to convert the images into base64 data """

from base64 import b64encode

with open('404.png', 'rb') as png, open('404.base64', 'wb') as base64:
    base64.write(b64encode(png.read()))

with open('loading.png', 'rb') as png, open('loading.base64', 'wb') as base64:
    base64.write(b64encode(png.read()))
