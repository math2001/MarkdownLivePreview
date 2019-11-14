import base64
import os.path
from functools import lru_cache
from .lib.markdown2 import Markdown
from bs4 import BeautifulSoup

__all__ = ('markdown2html', )

markdowner = Markdown()

# FIXME: put a nice picture please :^)
BASE64_LOADING_IMAGE = 'loading image!'
BASE64_404_IMAGE = '404 not found :-('

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
            base64 = get_base64_image(path)
        except FileNotFoundError as e:
            print("{!r} not found {!r}".format(path, e))
            base64 = BASE64_404_IMAGE
        except LoadingError:
            # the image is loading
            base64 = BASE64_LOADING_IMAGE

        img_element['src'] = base64

    # FIXME: how do tables look? should we use ascii tables?

    return str(soup)

# FIXME: This is an in memory cache. 20 seems like a fair bit of images... Should it be
#        bigger? Should the user be allowed to chose? There definitely should be a limit
#        because we don't wanna use to much memory, we're a simple markdown preview plugin
@lru_cache(maxsize=20)
def get_base64_image(path):
    if path.startswith('http://') or path.startswith('https://'):
        return 'loading of the internet!'

    with open(path, 'rb') as fp:
        return 'data:image/png;base64,' + base64.b64encode(fp.read()).decode('utf-8')

