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

class MarkdownLivePreviewListener_:

    def __init__(self, *args, **kwargs):
        super(MarkdownLivePreviewListener, *args, **kwargs)
        self.last_deactivated_view = None

    def on_modified(self, md_view):
        if not is_markdown_view(md_view):
            return
        window = md_view.window()
        md_view_settings = md_view.settings()
        if md_view_settings.get(PREVIEW_ENABLED) is not True:
            return
        id = md_view_settings.get(PREVIEW_ID)
        if not id:
            MarkdownLivePreviewListener.md_view = md_view
            create_preview(md_view)
            MarkdownLivePreviewListener.has_preview = True
            # window.focus_view(md_view)
        return
        if True:
           pass
        else:
            preview = get_view_from_id(window, id)
            if preview is None:
                raise ValueError('Glastetting preview from id: got None')
            show_html(md_view, preview)

    def on_pre_close(self, view):
        return
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
            sublime.set_timeout(lambda: preview.close(), 250)

    def on_deactivated(self, view):
        settings = view.settings()
        if settings.get(IS_PREVIEW) or settings.get(PREVIEW_ENABLED):
            self.last_deactivated_view = view

    def on_activated(self, view):
        vsettings = view.settings()
        if vsettings.get(IS_PREVIEW) is True:
            return
        if vsettings.get(PREVIEW_ENABLED):
            id = vsettings.get(PREVIEW_ID)
            if vsettings.get(JUST_CREATED) is True:
                vsettings.erase(JUST_CREATED)
                return
            if id is not None:
                return
            create_preview(view)
            # view.window().focus_view(view)
            return


        if self.last_deactivated_view:
            window = view.window()
            focused_view = window.active_view()
            hide_preview(self.last_deactivated_view)
            window.focus_view(focused_view)
