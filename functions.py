# -*- encoding: utf-8 -*-
import base64
import os.path
import sublime
import re
from .image_manager import ImageManager
from .lib.pygments_from_theme import pygments_from_theme
from bs4 import BeautifulSoup, Comment as html_comment

def plugin_loaded():
    global error404, loading, DEFAULT_STYLE, USER_STYLE_FILE
    loading = sublime.load_resource('Packages/MarkdownLivePreview/loading.txt')
    error404 = sublime.load_resource('Packages/MarkdownLivePreview/404.txt')

    DEFAULT_STYLE = sublime.load_resource('Packages/MarkdownLivePreview/default.css')
    USER_STYLE_FILE = os.path.join(sublime.packages_path(), 'User', "MarkdownLivePreview.css")

MATCH_YAML_HEADER = re.compile(r'^([\-\+])\1{2}\n(?P<content>.+)\n\1{3}\n', re.DOTALL)

def strip_html_comments(html):
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup.find_all(text=lambda text: isinstance(text, html_comment)):
        element.extract()
    return str(soup)

def manage_header(md, action):
    matchobj = MATCH_YAML_HEADER.match(md)
    if not matchobj:
        return md
    if action == 'remove':
        return md[len(matchobj.group(0)):]
    elif action == 'wrap_in_pre':
        return '<pre><code>' + matchobj.group('content') + '</code></pre>' \
        + md[len(matchobj.group(0)):]

    raise ValueError('Got an unknown action: "{}"'.format(action))

def get_preview_name(md_view):
    file_name = md_view.file_name()
    name = md_view.name() \
           or os.path.basename(file_name) if file_name else None \
           or 'Untitled'
    return name + ' - Preview'

def replace_img_src_base64(html, basepath):
    soup = BeautifulSoup(html, 'html.parser')
    load_from_internet_starters = get_settings().get('load_from_internet_when_starts')
    for img in soup.find_all('img'):
        if img['src'].startswith('data:image/'):
            continue
        elif img['src'].startswith(tuple(load_from_internet_starters)):
            image = ImageManager.get(img['src']) or loading
        else: # this is a local image
            image = to_base64(os.path.join(basepath, img['src']))

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


def _pre_with_spaces(code):
    for tag in code.find_all(text=True):
        tag.replace_with(BeautifulSoup(str(tag).replace('\t', ' ' * 4).replace(' ', '<i class="space">.</i>').replace('\n', '<br />'), 'html.parser'))
    return code

def pre_with_br(html):
    """Because the phantoms of sublime text does not support <pre> blocks
    this function replaces every \n with a <br> in a <pre>"""
    soup = BeautifulSoup(html, 'html.parser')
    for pre in soup.find_all('pre'):
        code = pre.find('code')
        code.replace_with(_pre_with_spaces(code))
    return str(soup)


def get_style(color_scheme):
    css = DEFAULT_STYLE
    if os.path.exists(USER_STYLE_FILE):
        with open(USER_STYLE_FILE) as fp:
            css += '\n' + fp.read() + '\n'
    if color_scheme:
        css += pygments_from_theme(sublime.load_resource(color_scheme))
    return ''.join([line.strip() + ' ' for line in css.splitlines()])
