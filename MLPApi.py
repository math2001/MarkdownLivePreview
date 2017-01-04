# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

import os.path
from html.parser import HTMLParser

from .lib import markdown2
from .escape_amp import *
from .functions import *
from .setting_names import *

__folder__ = os.path.dirname(__file__)

STYLE_FILE = os.path.join(os.path.dirname(__folder__), 'User',
                                          'MarkdownLivePreview.css')
DEFAULT_STYLE_FILE = os.path.join(__folder__, 'default.css')

def get_preview_name(md_view):
    name = md_view.name() \
           or os.path.basename(md_view.file_name()) \
           or 'Untitled'
    return name + ' - Preview'

def find_preview(window):
    for view in window.views():
        vsettings = view.settings()
        if vsettings.get(IS_PREVIEW):
            yield view, vsettings

def create_preview(md_view):
    window = md_view.window()
    md_view_settings = md_view.settings()
    md_view_settings.set(JUST_CREATED, True)

    preview = window.new_file()

    psettings = preview.settings()
    psettings.set(IS_PREVIEW, True)
    psettings.set(MD_VIEW_ID, md_view.id())
    preview.set_name(get_preview_name(md_view))
    preview.set_scratch(True)
    md_view_settings.set(PREVIEW_ID, preview.id())
    window.run_command('new_pane') # move to new group
    return preview


    return preview

def hide_preview(view):
    window = view.window()
    vsettings = view.settings()
    if vsettings.get(IS_PREVIEW):
        preview = view
        psettings = vsettings
        md_view_id = vsettings.get(MD_VIEW_ID)
        md_view = get_view_from_id(window, md_view_id)
        if md_view is None:
            raise ValueError('Tried to get md_view from id {} but got None'.format(md_view_id))
        mdvsettings = md_view.settings()

    elif vsettings.get(PREVIEW_ENABLED):
        md_view = view
        preview_id = vsettings.get(PREVIEW_ID)
        preview = get_view_from_id(window, preview_id)
        mdvsettings = vsettings
        if preview is None:
            raise ValueError('Tried to get preview from id {} but got None'.format(preview_id))
        psettings = preview.settings()
    else:
        raise ValueError('Call hide_preview with a view which is not the preview or the md_view')
    psettings.set(IS_HIDDEN, True)
    mdvsettings.erase(PREVIEW_ID)
    sublime.set_timeout(lambda: preview.close(), 250)
    return



    window = md_view.window()
    if window is None:
        return
    mdvsettings = md_view.settings()
    preview_id = mdvsettings.get(PREVIEW_ID)
    if not preview_id:
        return
    mdvsettings.erase(PREVIEW_ID)
    preview = get_view_from_id(window, preview_id)
    if preview is None:
        raise ValueError('Tried to get view from id {} but got None'.format(preview_id))
    psettings = preview.settings()
    psettings.set(IS_HIDDEN, True)
    sublime.set_timeout(preview.close(), 250)

def get_style():
    if os.path.exists(STYLE_FILE):
        with open(STYLE_FILE) as fp:
            return fp.read()

    with open(DEFAULT_STYLE_FILE) as fp:
        content = fp.read()
    content = ''.join([line.strip() for line in content.splitlines()])
    return content + "pre code .space {color: var(--light-bg)}"

def show_html(md_view, preview):
    html = '<style>{}</style>\n{}'.format(get_style(),
            pre_with_br(markdown2.markdown(get_view_content(md_view),
                                           extras=['fenced-code-blocks',
                                                   'no-code-highlighting'])))

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

    # set viewport position

    # 0 < y < 1
    y = md_view.text_to_layout(md_view.sel()[0].begin())[1] / md_view.layout_extent()[1]
    vector = [0, y * preview.layout_extent()[1]]
    # remove half of the viewport_extent.y to center it on the screen (verticaly)
    vector[1] -= preview.viewport_extent()[1] / 2
    vector[1] = mini(vector[1], 0)
    vector[1] += preview.line_height()
    preview.set_viewport_position(vector, animate=False)
