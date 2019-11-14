""" A small script to convert the images into base64 data """

# FIXME: ignore this script and the original images in .gitignore so that it pushes to
#        the GitHub repository but not package control

from base64 import b64encode

with open('404.png', 'rb') as png, open('404.base64', 'wb') as base64:
    base64.write(b64encode(png.read()))

with open('loading.png', 'rb') as png, open('loading.base64', 'wb') as base64:
    base64.write(b64encode(png.read()))
