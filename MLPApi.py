# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

from .functions import *
from .setting_names import *

def get_preview_name(md_view):
    name = md_view.name() \
           or os.path.basename(md_view.file_name()) \
           or 'Untitled'
    return name + '- Preview'

def create_preview(md_view):
    window = md_view.window()
    md_view_settings = md_view.settings()
    md_view_settings.set(JUST_CREATED, True)

    preview = window.new_file()
    preview.settings().set(IS_PREVIEW, True)
    preview.set_name(get_preview_name(md_view))
    preview.set_scratch(True)
    window.run_command('new_pane') # move to new group

    md_view_settings.set(PREVIEW_ID, preview.id())

    return preview

def hide_preview(md_view):
    window = md_view.window()
    if window is None:
        return
    mdvsettings = md_view.settings()
    preview_id = mdvsettings.get(PREVIEW_ID)
    mdvsettings.erase(PREVIEW_ID)
    preview = get_view_from_id(window, preview_id)
    if preview is None:
        return
    psettings = preview.settings()
    psettings.set(IS_HIDDEN, True)
    sublime.set_timeout(preview.close(), 250)
