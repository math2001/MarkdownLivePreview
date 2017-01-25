# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

import os.path
from html.parser import HTMLParser

from .lib import markdown2 as md2
from .lib.pre_tables import pre_tables
from .escape_amp import *
from .functions import *
from .setting_names import *
from .image_manager import CACHE_FILE
from random import randint as rnd

__folder__ = os.path.dirname(__file__)

USER_STYLE_FILE = os.path.join(os.path.dirname(__folder__), 'User', 'MarkdownLivePreview.css')

# used to store the phantom's set
windows_phantom_set = {}


def plugin_loaded():
    global DEFAULT_STYLE_FILE
    if os.path.exists(os.path.join(__folder__, 'default.css')):
        with open(os.path.join(__folder__, 'default.css')) as fp:
            DEFAULT_STYLE_FILE = fp.read()
    else:
        DEFAULT_STYLE_FILE = sublime.load_resource('Packages/MarkdownLivePreview/default.css')

def get_preview_name(md_view):
    file_name = md_view.file_name()
    name = md_view.name() \
           or os.path.basename(file_name) if file_name else None \
           or 'Untitled'
    return name + ' - Preview'

def create_preview(window, file_name):
    preview = window.new_file()

    preview.set_name(get_preview_name(file_name))
    preview.set_scratch(True)
    preview.set_syntax_file('Packages/MarkdownLivePreview/.sublime/' + \
                            'MarkdownLivePreviewSyntax.hidden-tmLanguage')

    return preview

def get_style():
    content = ''.join([line.strip() + ' ' for line in DEFAULT_STYLE_FILE.splitlines()])
    if os.path.exists(USER_STYLE_FILE):
        with open(USER_STYLE_FILE) as fp:
            content += '\n' + fp.read() + '\n'
    return content

def markdown2html(md, basepath):
    html = ''
    html += '<style>\n{}\n</style>\n'.format(get_style())
    # pre_with_br
    html += pre_with_br(pre_tables(md2.markdown(md, extras=['fenced-code-blocks',
                                                            'no-code-highlighting', 'tables'])))
    # the option no-code-highlighting does not exists in the official version of markdown2 for now
    # I personaly edited the file (markdown2.py:1743)

    html = html.replace('&nbsp;', '&nbspespace;') # save where are the spaces


    # exception, again, because <pre> aren't supported by the phantoms
    html = html.replace('&nbspespace;', '<i class="space">.</i>')
    html = replace_img_src_base64(html, basepath=os.path.dirname(basepath))
    return html

def show_html(md_view, preview):
    global windows_phantom_set
    html = markdown2html(get_view_content(md_view), os.path.dirname(md_view.file_name()))

    phantom_set = windows_phantom_set.setdefault(preview.window().id(),
                                             sublime.PhantomSet(preview, 'markdown_live_preview'))
    phantom_set.update([sublime.Phantom(sublime.Region(0), html, sublime.LAYOUT_BLOCK,
                                    lambda href: sublime.run_command('open_url', {'url': href}))])

    # lambda href: sublime.run_command('open_url', {'url': href})
    # get the "ratio" of the markdown view's position.
    # 0 < y < 1
    y = md_view.text_to_layout(md_view.sel()[0].begin())[1] / md_view.layout_extent()[1]
    # set the vector (position) for the preview
    vector = [0, y * preview.layout_extent()[1]]
    # remove half of the viewport_extent.y to center it on the screen (verticaly)
    vector[1] -= preview.viewport_extent()[1] / 2
    # make sure the minimum is 0
    vector[1] = 0 if vector[1] < 0 else vector[1]
    # the hide the first line
    vector[1] += preview.line_height()
    preview.set_viewport_position(vector, animate=False)

def clear_cache():
    """Removes the cache file"""
    os.remove(CACHE_FILE)

def release_phantoms_set(view_id=None):
    global windows_phantom_set
    if view_id is None:
        windows_phantom_set = {}
    else:
        del windows_phantom_set[view_id]
