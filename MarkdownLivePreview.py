# -*- encoding: utf-8 -*-

import sys
import os.path
import sublime
import sublime_plugin

from .MLPApi import *
from .setting_names import *
from .functions import *

class MarkdownLivePreviewListener(sublime_plugin.EventListener):

    def on_modified(self, view):
        window = view.window()
        vsettings = view.settings()
        if vsettings.get(PREVIEW_ENABLED):
            id = vsettings.get(PREVIEW_ID)
            if id is None or get_view_from_id(window, id) is None:
                preview = create_preview(view)
            return

    def on_activated(self, view):
        # if view is md_view and has no preview
        # -> create preview
        window = view.window()
        vsettings = view.settings()
        if vsettings.get(PREVIEW_ENABLED):
            id = vsettings.get(PREVIEW_ID)
            if id is None or get_view_from_id(window, id) is None:
                preview = create_preview(view)
            return

        # if view is preview
        # -> do nothing
        if vsettings.get(IS_PREVIEW):
            return
        # if view is not the md_view or the preview
        # remove preview if any
        for view, settings in find_preview(window):
            settings.set(IS_HIDDEN, True)
            view.close()
