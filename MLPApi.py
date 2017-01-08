# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

import os.path
from html.parser import HTMLParser

from .lib import markdown2 as md2
from .escape_amp import *
from .functions import *
from .setting_names import *

__folder__ = os.path.dirname(__file__)

STYLE_FILE = os.path.join(os.path.dirname(__folder__), 'User',
                         'MarkdownLivePreview.css')


def plugin_loaded():
    global DEFAULT_STYLE_FILE
    DEFAULT_STYLE_FILE = sublime.load_resource('Packages/MarkdownLivePreview/'
                                               'default.css')

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
    preview.set_syntax_file('Packages/MarkdownLivePreview/.sublime/'
                            'MarkdownLivePreview.hidden-tmLanguage')

    return preview

def get_style():
    content = ''.join([line.strip() + ' ' for line in DEFAULT_STYLE_FILE.splitlines()])
    return content + "pre code .space {color: var(--light-bg)}"

def show_html(md_view, preview):
    html = []
    html.append('<style>\n{}\n</style>'.format(get_style()))
    html.append(pre_with_br(md2.markdown(get_view_content(md_view),
                                         extras=['fenced-code-blocks',
                                                 'no-code-highlighting'])))

    html = '\n'.join(html)

    # the option no-code-highlighting does not exists
    # in the official version of markdown2 for now
    # I personaly edited the file (markdown2.py:1743)

    html = html.replace('&nbsp;', '&nbspespace;') # save where are the spaces

    html = HTMLParser().unescape(html)

    html = escape_amp(html)

    # exception, again, because <pre> aren't supported by the phantoms
    html = html.replace('&nbspespace;', '<i class="space">.</i>')
    html = replace_img_src_base64(html)
    preview.erase_phantoms('markdown_preview')
    preview.add_phantom('markdown_preview',
                         sublime.Region(-1),
                         html,
                         sublime.LAYOUT_BLOCK,
                         lambda href: sublime.run_command('open_url',
                                                          {'url': href}))

    return
    # set viewport position
    # 0 < y < 1
    y = md_view.text_to_layout(md_view.sel()[0].begin())[1] / md_view.layout_extent()[1]
    vector = [0, y * preview.layout_extent()[1]]
    # remove half of the viewport_extent.y to center it on the screen (verticaly)
    vector[1] -= preview.viewport_extent()[1] / 2
    vector[1] = mini(vector[1], 0)
    vector[1] += preview.line_height()
    preview.set_viewport_position(vector, animate=False)
