# -*- encoding: utf-8 -*-

import sys
import os.path
import sublime
import sublime_plugin

from .MLPApi import *
from .setting_names import *
from .functions import *

class MarkdownLivePreviewListener(sublime_plugin.EventListener):

    def __init__(self, *args, **kwargs):
        super(MarkdownLivePreviewListener, *args, **kwargs)
        self.last_deactivated_view = None

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
            print('normal, create preview')
            MarkdownLivePreviewListener.md_view = md_view
            create_preview(md_view)
            MarkdownLivePreviewListener.has_preview = True
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
            if preview is None:
                print('preview is None', id)
            preview_settings = preview.settings()
            preview_settings.erase(IS_PREVIEW)
            preview_settings.erase(MD_VIEW_ID)
            sublime.set_timeout(lambda: preview.close(), 250)

    def on_deactivated(self, view):
        self.last_deactivated_view = view
        return
        vsettings = view.settings()
        if vsettings.get(IS_PREVIEW) is True:
            return
        if vsettings.get(PREVIEW_ENABLED):
            id = vsettings.get(IS_PREVIEW)
            if id is not None:
                return
            create_preview(view)


    def on_activated(self, view):
        vsettings = view.settings()
        if vsettings.get(IS_PREVIEW) is True:
            return
        if vsettings.get(PREVIEW_ENABLED):
            id = vsettings.get(PREVIEW_ID)
            if vsettings.get(JUST_CREATED) is True:
                vsettings.erase(JUST_CREATED)
                print("MarkdownLivePreview.py:84", 'dont create, just created')
                return
            if id is not None:
                print("MarkdownLivePreview.py:86", "dont create, already have a preview id")
                return
            print("MarkdownLivePreview.py:87", 'create preview')
            return create_preview(view)

        if self.last_deactivated_view:
            hide_preview(self.last_deactivated_view)


        return
        def just_created_preview():
            return MarkdownLivePreviewListener.just_created_preview
        vsettings = view.settings()
        if vsettings.get(PREVIEW_ENABLED) is True:
            if vsettings.get(PREVIEW_ID) is not None:
                print('return because already have a preview')
                return

           # 'view' is the markdown view, which wasn't focus, so didn't have
           # any preview
            MarkdownLivePreviewListener.md_view = view
            MarkdownLivePreviewListener.has_preview = True
            print('create preview')
            MarkdownLivePreviewListener.just_created_preview = True
            create_preview(view)
        elif vsettings.get(IS_PREVIEW) is True or just_created_preview():
            print('do nothing because focus view is the preview')
            MarkdownLivePreviewListener.just_created_preview = False
        elif MarkdownLivePreviewListener.has_preview:
            print('hide preview', view.name().__repr__(), view.file_name())
            hide_preview(MarkdownLivePreviewListener.md_view)
            MarkdownLivePreviewListener.has_preview = False
