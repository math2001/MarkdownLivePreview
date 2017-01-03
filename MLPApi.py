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

    preview = window.new_file()
    preview.set_name(get_preview_name(md_view))
    preview.set_scratch(True)
    preview.settings().set(IS_PREVIEW, True)
    window.run_command('new_pane') # move to new group

    md_view_settings.set(PREVIEW_ID, preview.id())

    return preview
