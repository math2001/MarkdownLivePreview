# -*- encoding: utf-8 -*-
import base64
import os.path
import sublime

file404 = os.path.join(os.path.dirname(__file__), '404.png')

def is_markdown_view(view):
        return 'markdown' in view.scope_name(0)

def to_base64(path=None, content=None):
    if path is None and content is None:
        return to_base64(file404)
    elif content is None and path is not None:
        try:
            with open(path, 'rb') as fp:
                content = fp.read()
        except (FileNotFoundError, OSError):
            return to_base64(file404)

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
