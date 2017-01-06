# -*- encoding: utf-8 -*-
import base64
import os.path
import sublime
import re
from .image_manager import ImageManager

def plugin_loaded():
    global error404, loading
    loading = sublime.load_resource('Packages/MarkdownLivePreview/loading.txt')
    error404 = sublime.load_resource('Packages/MarkdownLivePreview/404.txt')


def replace_img_src_base64(html):
    """Really messy, but it works (should be updated)"""
    index = -1
    tag_start = '<img src="'
    shtml, html = html, list(html)
    while True:
        index = shtml.find(tag_start, index + 1)
        if index == -1:
            break
        path, end = get_content_till(html, '"', start=index + len(tag_start))
        if ''.join(path).startswith('data:image/'):
            continue
        if ''.join(path).startswith(tuple(get_settings().get('load_from_internet'
                                                    '_when_starts'))):
            image = ImageManager.get(''.join(path))
            image = image or loading

        else:
            # local image
            image = to_base64(''.join(path))
        html[index+len(tag_start):end] = image
        shtml = ''.join(html)
    return ''.join(html)

def is_markdown_view(view):
        return 'markdown' in view.scope_name(0)

def to_base64(path=None, content=None):
    if path is None and content is None:
        return error404
    elif content is None and path is not None:
        try:
            with open(path, 'rb') as fp:
                content = fp.read()
        except (FileNotFoundError, OSError):
            return error404

    return 'data:image/png;base64,' + ''.join([chr(el) for el in list(base64.standard_b64encode(content))])

def md(*t, **kwargs):
    sublime.message_dialog(kwargs.get('sep', '\n').join([str(el) for el in t]))

def sm(*t, **kwargs):
    sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs):
    sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def mini(val, min):
    if val < min:
        return min
    return val

def get_content_till(string, char_to_look_for, start=0):
    i = start
    while i < len(string):
        if string[i] == char_to_look_for:
            return string[start:i], i
        i += 1

def get_view_content(view):
    return view.substr(sublime.Region(0, view.size()))

def get_view_from_id(window, id):
    for view in window.views():
        if view.id() == id:
            return view

def get_settings():
    return sublime.load_settings('MarkdownLivePreview.sublime-settings')

def pre_with_br(html):
    """Because the phantoms of sublime text does not support <pre> blocks
    this function replaces every \n with a <br> in a <pre>"""

    while True:
        obj = re.search(r'<pre>(.*?)</pre>', html, re.DOTALL)
        if not obj:
            break
        html = list(html)
        html[obj.start(0):obj.end(0)] = '<pre >' + ''.join(html[obj.start(1):obj.end(1)]) \
                                            .replace('\n', '<br>') \
                                            .replace(' ', '&nbsp;') + '</pre>'
        html = ''.join(html)
    return html
