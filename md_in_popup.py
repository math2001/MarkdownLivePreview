# -*- encoding: utf-8 -*-
import sublime
import sublime_plugin
from . import markdown2
import os.path
import re
import base64

from .escape_amp import *
from html.parser import HTMLParser

# Main sublime tools function

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
        i += 1
        if string[i] == char_to_look_for:
            return string[start:i], i

def to_base64(path):
    with open(path, 'rb') as fp:
        content = fp.read()
    return base64.standard_b64encode(content)

def replace_img_src_base64(html):
    """Really messy, but it works (should be updated)"""
    index = -1
    tag_start = '<img src="'
    counter355 = 0
    shtml = html
    html = list(html)
    while True:
        counter355 += 1
        if counter355 > 100:
            print("end up counter355")
            return False # counter355
        index = shtml.find(tag_start, index + 1)
        if index == -1:
            return ''.join(html)
        path, end = get_content_till(html, '"', start=index + len(tag_start))
        html[index+len(tag_start):end] = 'data:image/png;base64,' + ''.join([chr(el) for el in list(to_base64(''.join(path)))])
    return ''.join(html)


STYLE_FILE = os.path.join(sublime.packages_path(), 'User', 'MarkdownLivePreview.css')
def get_style():
    content = None
    if os.path.exists(STYLE_FILE):
        with open(STYLE_FILE) as fp:
            content = fp.read()
            return content
    if not content:
        content = """
            :root, html, body {
                height: 100%;
            }
            html {
                --light-bg: color(var(--background) blend(#999 85%))
                height: 100%;
            }
            body {
                padding:10px;
                padding-top: 0px;
                font-family: "Open Sans", sans-serif;
                background-color: var(--background);
                font-size: 15px;
            }

            blockquote {
                font-style: italic;
                display: block;
                margin-left: 30px;
                border: 1px solid red;
            }

            code {
                padding-left: 0.2rem;
                padding-right: 0.2rem;
                background-color: var(--light-bg);
                margin: 0;
                border-radius: 3px;
                margin: 5px;
            }

            pre {
                display: block;
                margin-top: 20px;
                line-height: 1.7;
                background-color: var(--light-bg);
                padding-left: 10px;
                width: 100%;
                border-radius: 3px;
            }
            pre code {
                padding-left: 0;
            }
        """
    return content + "pre code .space {color: var(--light-bg)}"

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

def close_preview(md_view_settings, preview):
    preview.close()
    md_view_settings.erase('markdown_preview_id')
    md_view_settings.erase('markdown_preview_enabled')

def create_preview(window, md_view):
    focus_group, focus_view = window.get_view_index(md_view)
    preview = window.new_file()
    window.run_command('new_pane') # move the preview to a new group
    preview.set_name(os.path.basename(md_view.file_name()) + ' - Preview')

    preview_settings = preview.settings()
    preview_settings.set('gutter', False)
    preview_settings.set('is_markdown_preview', True)
    preview_settings.set('markdown_view_id', md_view.id())

    md_view.settings().set('markdown_preview_id', preview.id())
    window.focus_group(focus_group)
    window.focus_view(md_view)

    return preview

def show_html(md_view, preview):
    html = ('<style>{}</style>'.format(get_style()) +
            pre_with_br(markdown2.markdown(get_view_content(md_view),
                        extras=['fenced-code-blocks', 'no-code-highlighting'])))
    # html = """<img src="file://C:/Users/math/Pictures/malwaree high school logo.jpg" alt="Mulwarre High School's Logo" />"""

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
                         lambda href: sublime.run_command('open_url', {'url': href}))

    # 0 < y < 1
    y = md_view.text_to_layout(md_view.sel()[0].begin())[1] / md_view.layout_extent()[1]
    vector = [0, y * preview.layout_extent()[1]]
    # remove half of the viewport_extent.y to center it on the screen (verticaly)
    vector[1] -= preview.viewport_extent()[1] / 2
    vector[1] = mini(vector[1], 0)
    vector[1] += preview.line_height()
    preview.set_viewport_position(vector, animate=False)

def get_view_content(view):
    return view.substr(sublime.Region(0, view.size()))

def get_view_from_id(window, id):
    for view in window.views():
        if view.id() == id:
            return view

class MarkdownInPopupCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        settings = view.settings()
        if not 'markdown' in settings.get('syntax').lower():
            return
        settings.add_on_change('markdown_preview_enabled', lambda: self.on_modified(view))

    def on_modified(self, md_view):
        window = md_view.window()
        md_view_settings = md_view.settings()

        if not 'markdown' in md_view_settings.get('syntax').lower():
            return

        markdown_preview_enabled = md_view_settings.get('markdown_preview_enabled') is True
        preview_id = md_view_settings.get('markdown_preview_id', None)

        if not markdown_preview_enabled:
            if preview_id is not None:
                preview = get_view_from_id(window, preview_id)
                if preview:
                    close_preview(md_view_settings, preview)
            return

        if preview_id is None:
            preview = create_preview(window, md_view)
        else:
            preview = get_view_from_id(window, preview_id)
            if not preview:
                md_view_settings.erase('markdown_preview_id')
                md_view_settings.erase('markdown_preview_enabled')
                return

        show_html(md_view, preview)

    def on_pre_close(self, view):
        settings = view.settings()
        if settings.get('markdown_preview_enabled') is True:
            preview = get_view_from_id(view.window(), settings.get('markdown_preview_id'))
            if preview:
                sublime.set_timeout_async(lambda: preview.close(), 250)
        elif settings.get('is_markdown_preview') is True:
            md_view = get_view_from_id(view.window(), settings.get('markdown_view_id'))
            if md_view:
                def callback():
                    md_view_settings = md_view.settings()
                    md_view_settings.erase('markdown_preview_enabled')
                    md_view_settings.erase('markdown_preview_id')
                sublime.set_timeout_async(callback, 250)
