# -*- encoding: utf-8 -*-
import base64
import os.path
import sublime
import re
from .image_manager import ImageManager
from bs4 import BeautifulSoup, Comment as html_comment

def plugin_loaded():
    global error404, loading
    loading = sublime.load_resource('Packages/MarkdownLivePreview/loading.txt')
    error404 = sublime.load_resource('Packages/MarkdownLivePreview/404.txt')

def strip_html_comments(html):
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup.find_all(text=lambda text: isinstance(text, html_comment)):
        element.extract()
    return str(soup)


def get_preview_name(md_view):
    file_name = md_view.file_name()
    name = md_view.name() \
           or os.path.basename(file_name) if file_name else None \
           or 'Untitled'
    return name + ' - Preview'

def replace_img_src_base64(html, basepath):
    """Really messy, but it works (should be updated)"""


    soup = BeautifulSoup(html)
    load_from_internet_starters = get_settings().get('load_from_internet_when_starts')
    for img in soup.find_all('img'):
        if img['src'].startswith('data:image/'):
            continue
        elif img['src'].startswith(tuple(load_from_internet_starters)):
            image = ImageManager.get(img['src']) or loading
        else: # this is a local image
            image = to_base64(os.path.join(basepath, src))

        img['src'] = image

    return str(soup)

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
    if not isinstance(id, int):
        return
    for view in window.views():
        if view.id() == id:
            return view

def get_settings():
    return sublime.load_settings('MarkdownLivePreview.sublime-settings')

def pre_with_br(html):
    """Because the phantoms of sublime text does not support <pre> blocks
    this function replaces every \n with a <br> in a <pre>"""
    soup = BeautifulSoup(html)
    for pre in soup.find_all('pre'):
        code = pre.find('code')
        code.replaceWith(BeautifulSoup(''.join(str(node) for node in pre.contents) \
                      .replace('\n', '<br/>').replace(' ', '<i class="space">.</i>'), 'html.parser'))
    return str(soup)
