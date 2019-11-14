import concurrent.futures
import urllib.request
import base64
import os.path

from functools import lru_cache, partial
from bs4 import BeautifulSoup
from .lib.markdown2 import Markdown

__all__ = ('markdown2html', )

markdowner = Markdown()

# FIXME: how do I choose how many workers I want? Does thread pool reuse threads or
#        does it stupidly throw them out? (we could implement something of our own)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

# FIXME: put a nice picture please :^)
BASE64_LOADING_IMAGE = 'loading image!'
BASE64_404_IMAGE = '404 not found :-('

images_cache = {}

class LoadingError(Exception):
    pass

def markdown2html(markdown, basepath, re_render):
    """ converts the markdown to html, loads the images and puts in base64 for sublime
    to understand them correctly. That means that we are responsible for loading the
    images from the internet. Hence, we take in re_render, which is just a function we 
    call when an image has finished loading to retrigger a render (see #90)
    """
    html = markdowner.convert(markdown)

    soup = BeautifulSoup(html, "html.parser")
    for img_element in soup.find_all('img'):
        src = img_element['src']

        # already in base64, or something of the like
        # FIXME: what other types are possible? Are they handled by ST? If not, could we
        #        convert it into base64? is it worth the effort?
        if src.startswith('data:image/'):
            continue

        if src.startswith('http://') or src.startswith('https://'):
            path = src
        elif src.startswith('file://'):
            path = src[len('file://'):]
        else:
            # expanduser: ~ -> /home/math2001
            # realpath: simplify that paths so that we don't have duplicated caches
            path = os.path.realpath(os.path.expanduser(os.path.join(basepath, src)))

        try:
            base64 = get_base64_image(path, re_render)
        except FileNotFoundError as e:
            print("{!r} not found {!r}".format(path, e))
            base64 = BASE64_404_IMAGE
        except LoadingError:
            # the image is loading
            base64 = BASE64_LOADING_IMAGE

        img_element['src'] = base64

    # FIXME: how do tables look? should we use ascii tables?

    return str(soup)

def get_base64_image(path, re_render):

    def callback(url, future):
        # this is "safe" to do because callback is called in the same thread as 
        # add_done_callback:
        # > Added callables are called in the order that they were added and are always
        # > called in a thread belonging to the process that added them
        # > --- Python docs
        images_cache[url] = future.result()
        # we render, which means this function will be called again, but this time, we
        # will read from the cache
        re_render()

    if path.startswith('http://') or path.startswith('https://'):
        if path in images_cache:
            return images_cache[path]
        executor.submit(load_image, path).add_done_callback(partial(callback, path))
        return 'loading of the internet!'

    with open(path, 'rb') as fp:
        return 'data:image/png;base64,' + base64.b64encode(fp.read()).decode('utf-8')

# FIXME: This is an in memory cache. 20 seems like a fair bit of images... Should it be
#        bigger? Should the user be allowed to chose? There definitely should be a limit
#        because we don't wanna use to much memory, we're a simple markdown preview plugin
# NOTE: > The LRU feature performs best when maxsize is a power-of-two. --- python docs
@lru_cache(maxsize=2 ** 4)
def load_image(url):
    with urllib.request.urlopen(url, timeout=60) as conn:
        content_type = conn.info().get_content_type()
        if 'image' not in content_type:
            raise ValueError("{!r} doesn't point to an image, but to a {!r}".format(url, content_type))
        return 'data:image/png;base64,' + base64.b64encode(conn.read()).decode('utf-8')