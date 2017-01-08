# -*- encoding: utf-8 -*-

import os.path
import tempfile
import sublime
from threading import Thread
import urllib.request, urllib.error
from .functions import *

CACHE_FILE = os.path.join(tempfile.gettempdir(),
                          'MarkdownLivePreviewCache.txt')
TIMEOUT = 20 # seconds

SEPARATOR = '---%cache%--'

def get_base64_saver(loading, url):
    def callback(content):
        if isinstance(content, urllib.error.HTTPError):
            if content.getcode() == 404:
                loading[url] = 404
                return
        elif isinstance(content, urllib.error.URLError):
            if (content.reason.errno == 11001 and
                content.reason.strerror == 'getaddrinfo failed'):
                loading[url] = 404
                return
            return sublime.error_message('An unexpected error has occured: ' +
                                         str(content))
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
        try:
            page = urllib.request.urlopen(self.url, None, TIMEOUT)
        except Exception as e:
            self.callback(e)
        else:
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

        cached = get_cache_for(imageurl)
        if cached:
            return cached
        elif imageurl in ImageManager.loading.keys():
            # return None (the file is still loading, already made a request)
            # return string the base64 of the url (which is going to be cached)
            temp_cached = ImageManager.loading[imageurl]
            if temp_cached == 404:
                return to_base64('404.png')
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
