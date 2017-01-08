# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

from .MLPApi import *
from .setting_names import *
from .functions import *

class NewMarkdownLivePreviewCommand(sublime_plugin.ApplicationCommand):

    def run(self):

        """Inspired by the edit_settings command"""

        current_view = sublime.active_window().active_view()
        file_name = current_view.file_name()
        current_view.close()
        if file_name is None:
            return sublime.error_message('Not supporting unsaved file for now')

        sublime.run_command('new_window')
        self.window = sublime.active_window()
        self.window.settings().set(PREVIEW_WINDOW, True)
        self.window.run_command('set_layout', {
            'cols': [0.0, 0.5, 1.0],
            'rows': [0.0, 1.0],
            'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]
        })
        self.window.focus_group(1)
        preview = create_preview(self.window, current_view)

        self.window.focus_group(0)
        md_view = self.window.open_file(file_name)
        mdsettings = md_view.settings()

        mdsettings.set(PREVIEW_ENABLED, True)
        mdsettings.set(PREVIEW_ID, preview.id())

    def is_enabled(self):
        return is_markdown_view(sublime.active_window().active_view())

class MarkdownLivePreviewListener(sublime_plugin.EventListener):

    def update(self, view):
        if not is_markdown_view(view): # faster than getting the settings
            return
        vsettings = view.settings()
        if not vsettings.get(PREVIEW_ENABLED):
            return
        id = vsettings.get(PREVIEW_ID)
        if id is None:
            raise ValueError('The preview id is None')
        preview = get_view_from_id(view.window(), id)
        if preview is None:
            raise ValueError('The preview is None (id: {})'.format(id))

        show_html(view, preview)
        return view, preview

    def on_modified(self, view):
        self.update(view)

    def on_window_command(self, window, command, args):
        if command == 'close' and window.settings().get(PREVIEW_WINDOW):
            return 'close_window', {}

    def on_load_async(self, view):
        try:
            md_view, preview = self.update(view)
        except TypeError:
            return
        window = preview.window()
        psettings = preview.settings()

        show_tabs = psettings.get('show_tabs')
        show_minimap = psettings.get('show_minimap')
        show_status_bar = psettings.get('show_status_bar')
        show_sidebar = psettings.get('show_sidebar')
        show_menus = psettings.get('show_menus')

        if show_tabs is not None:
            window.set_tabs_visible(show_tabs)
        if show_minimap is not None:
            window.set_minimap_visible(show_minimap)
        if show_status_bar is not None:
            window.set_status_bar_visible(show_status_bar)
        if show_sidebar is not None:
            window.set_sidebar_visible(show_sidebar)
        if show_menus is not None:
            window.set_menu_visible(show_menus)
