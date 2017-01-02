# -*- encoding: utf-8 -*-

import os.path
from threading import Thread
import urllib.request
import base64
import sublime

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache.txt')
TIMEOUT = 20

SEPARATOR = '---%cache%--'

class InternalError(Exception): pass

def to_base64(path=None, content=None):
    if content is None and path is not None:
        try:
            with open(path, 'rb') as fp:
                content = fp.read()
        except FileNotFoundError:
            return to_base64(os.path.join(os.path.dirname(__file__), '404.png'))

    return 'data:image/png;base64,' + ''.join([chr(el) for el in list(base64.standard_b64encode(content))])

def load_and_save_image(url, user_callback):
    def callback(content):
        content = to_base64(content=content)
        with open(CACHE_FILE, 'a') as fp:
            fp.write(url + SEPARATOR + content)
            user_callback(content)
    thread = ImageLoader(url, callback)
    thread.start()
    sublime.set_timeout_async(lambda: thread.join(), TIMEOUT)

class ImageLoader(Thread):

    def __init__(self, url, callback):
        Thread.__init__(self)
        self.url = url
        self.callback = callback

    def run(self):
        page = urllib.request.urlopen(self.url, None, TIMEOUT)
        self.callback(page.read())


class ImageManager(object):

    currently_loading = []

    @staticmethod
    def get(imageurl, user_callback):
        if imageurl in ImageManager.currently_loading:
            return None
        def callback(content):
            try:
                ImageManager.currently_loading.remove(imageurl)
            except ValueError:
                sublime.error_message('Internal error: Trying to remove an URL'
                                      'from loading_url, but not found. Please'
                                      'report to the issue tracker.')
                sublime.run_command('open_url', {
                    'url': 'https://github.com/math2001/MarkdownLivePreview/'
                           'issues/new'     
                })

            user_callback(content)

        ImageManager.currently_loading.append(imageurl)
        try:
            with open(CACHE_FILE, 'r') as fp:
                lines = fp.readlines()
        except FileNotFoundError:
            pass
        else:
            for line in lines:
                url, base64 = line.split(SEPARATOR, 1)
                if url == imageurl:
                    return callback(base64)
                else:
                    print(url + '\n' + imageurl)
        load_and_save_image(imageurl, callback)
