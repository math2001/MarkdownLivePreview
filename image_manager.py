# -*- encoding: utf-8 -*-

import os.path
from threading import Thread
import urllib.request
import base64
import sublime
from .functions import *

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache.txt')
TIMEOUT = 20 # seconds

SEPARATOR = '---%cache%--'

class InternalError(Exception): pass

def load_and_save_image(url, user_callback):
    def callback(content):
        content = to_base64(content=content)
        with open(CACHE_FILE, 'a') as fp:
            fp.write(url + SEPARATOR + content)
            user_callback(content)
    thread = ImageLoader(url, callback)
    thread.start()
    sublime.set_timeout_async(lambda: thread.join(), TIMEOUT * 1000)

def get_base64_saver(loading, url):
    def callback(content):
        loading[url] = to_base64(content=content)
    return callback

def get_cache_for(imageurl):
    if not os.path.exists(CACHE_FILE):
        return
    with open(CACHE_FILE) as fp:
        for line in fp.read().splitlines():
            url, base64 = line.split(SEPARATOR, 1)
            if url == imageurl:
                return base64

def cache(imageurl, base64):
    with open(CACHE_FILE, 'a') as fp:
        fp.write(imageurl + SEPARATOR + base64 + '\n')

class ImageLoader(Thread):

    def __init__(self, url, callback):
        Thread.__init__(self)
        self.url = url
        self.callback = callback

    def run(self):
        page = urllib.request.urlopen(self.url, None, TIMEOUT)
        # self.callback(self.url, page.read())
        self.callback(page.read())


class ImageManager(object):

    """
        Usage:

        >>> image = ImageManager.get('http://domain.com/image.png')
        >>> image = ImageManager.get('http://domain.com/image.png')
        # still loading (this is a comment, no an outputed text), it doesn't
        # run an other request
        >>> image = ImageManager.get('http://domain.com/image.png')
        'data:image/png;base64,....'

    """
    loading = {}

    @staticmethod
    def get(imageurl, user_callback=None):
        # if imageurl in ImageManager.loading.keys():
        #     return None

        cached = get_cache_for(imageurl)
        if cached:
            return cached
        elif imageurl in ImageManager.loading.keys():
            # return None (the file is still loading, already made a request)
            # return string the base64 of the url (which is going to be cached)
            temp_cached = ImageManager.loading[imageurl]
            if temp_cached:
                cache(imageurl, temp_cached)
                del ImageManager.loading[imageurl]
            return temp_cached
        else:
            # load from internet
            ImageManager.loading[imageurl] = None
            callback = get_base64_saver(ImageManager.loading, imageurl)
            loader = ImageLoader(imageurl, callback)
            loader.start()
            sublime.set_timeout_async(lambda: loader.join(), TIMEOUT * 1000)
