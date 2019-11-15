import copy
import os.path
import concurrent.futures
import urllib.request
import base64
import bs4

from functools import lru_cache, partial

from .lib.markdown2 import Markdown

__all__ = ('markdown2html', )

markdowner = Markdown(extras=['fenced-code-blocks'])

# FIXME: how do I choose how many workers I want? Does thread pool reuse threads or
#        does it stupidly throw them out? (we could implement something of our own)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

images_cache = {}

class LoadingError(Exception):
    pass

def markdown2html(markdown, basepath, re_render, resources):
    """ converts the markdown to html, loads the images and puts in base64 for sublime
    to understand them correctly. That means that we are responsible for loading the
    images from the internet. Hence, we take in re_render, which is just a function we 
    call when an image has finished loading to retrigger a render (see #90)
    """
    html = markdowner.convert(markdown)

    soup = bs4.BeautifulSoup(html, "html.parser")
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
            base64 = resources['base64_404_image']
        except LoadingError:
            base64 = resources['base64_loading_image']

        img_element['src'] = base64

    # remove comments, because they pollute the console with error messages
    for comment_element in soup.find_all(text=lambda text: isinstance(text, bs4.Comment)):
        comment_element.extract()

    # FIXME: how do tables look? should we use ascii tables?

    # pre aren't handled by ST3. The require manual adjustment
    for pre_element in soup.find_all('pre'):
        # select the first child, <code>
        code_element = next(pre_element.children)

        # FIXME: this method sucks, but can we do better?
        fixed_pre = str(code_element) \
            .replace(' ', '<i class="space">.</i>') \
            .replace('\n', '<br />')

        code_element.replace_with(bs4.BeautifulSoup(fixed_pre, "html.parser"))

    # FIXME: highlight the code using Sublime's syntax

    # FIXME: report that ST doesn't support <br/> but does work with <br />... WTF?
    return "<style>\n{}\n</style>\n\n{}".format(resources['stylesheet'], soup).replace('<br/>', '<br />')

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
        raise LoadingError()

    # FIXME: use some kind of cache for this as well, because it decodes on every
    #        keystroke here...
    with open(path, 'rb') as fp:
        return 'data:image/png;base64,' + base64.b64encode(fp.read()).decode('utf-8')

# FIXME: wait what the hell? Why do I have two caches? (lru and images_cache)
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
