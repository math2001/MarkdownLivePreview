# -*- encoding: utf-8 -*-

import sys
import os.path
import sublime
import sublime_plugin

from .MLPApi import *
from .setting_names import *
from .functions import *

class MarkdownLivePreviewListener(sublime_plugin.EventListener):

    def on_load(self, view):
        if not is_markdown_view(view):
            return
        vsettings = view.settings()

    def on_modified(self, md_view):
        if not is_markdown_view(md_view):
            return
        window = md_view.window()
        md_view_settings = md_view.settings()
        if md_view_settings.get(PREVIEW_ENABLED) is not True:
            return

        if not md_view_settings.get(PREVIEW_ID):
            create_preview(md_view)
            window.focus_view(md_view)

    def on_pre_close(self, view):
        vsettings = view.settings()
        window = view.window()
        if vsettings.get(IS_PREVIEW) is True:
            if vsettings.get(IS_HIDDEN) is True:
                return
            mdvsettings = get_view_from_id(window, vsettings.get(MD_VIEW_ID))
            if mdvsettings is None:
                return
            mdvsettings = mdvsettings.settings()
            mdvsettings.erase(PREVIEW_ENABLED)
            mdvsettings.erase(PREVIEW_ID)
            return

        id = vsettings.get(PREVIEW_ID)

        if vsettings.get(PREVIEW_ENABLED) is True and id is not None:
            preview = get_view_from_id(window, id)
            preview_settings = preview.settings()
            preview_settings.erase(IS_PREVIEW)
            preview_settings.erase(MD_VIEW_ID)
            sublime.set_timeout_async(lambda: preview.close(), 250)
