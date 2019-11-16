"""
Terminology
original_view: the view in the regular editor, without it's own window
markdown_view: the markdown view, in the special window
preview_view: the preview view, in the special window
original_window: the regular window
preview_window: the window with the markdown file and the preview
"""

import time
import os.path
import struct
import sublime
import sublime_plugin

from functools import partial

from .markdown2html import markdown2html

MARKDOWN_VIEW_INFOS = "markdown_view_infos"
PREVIEW_VIEW_INFOS = "preview_view_infos"
SETTING_DELAY_BETWEEN_UPDATES = "delay_between_updates"

resources = {}


def plugin_loaded():
    global DELAY
    resources["base64_404_image"] = parse_image_resource(get_resource("404.base64"))
    resources["base64_loading_image"] = parse_image_resource(
        get_resource("loading.base64")
    )
    resources["stylesheet"] = get_resource("stylesheet.css")
    # FIXME: how could we make this setting update without restarting sublime text
    #        and not loading it every update as well
    DELAY = get_settings().get(SETTING_DELAY_BETWEEN_UPDATES)


class MdlpInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, point, string):
        self.view.insert(edit, point, string)


class OpenMarkdownPreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        """ If the file is saved exists on disk, we close it, and reopen it in a new
        window. Otherwise, we copy the content, erase it all (to close the file without
        a dialog) and re-insert it into a new view into a new window """

        original_view = self.view
        original_window_id = original_view.window().id()
        file_name = original_view.file_name()

        syntax_file = original_view.settings().get("syntax")

        if file_name:
            original_view.close()
        else:
            # the file isn't saved, we need to restore the content manually
            total_region = sublime.Region(0, original_view.size())
            content = original_view.substr(total_region)
            original_view.erase(edit, total_region)
            original_view.close()
            # FIXME: save the document to a temporary file, so that if we crash,
            #        the user doesn't lose what he wrote

        sublime.run_command("new_window")
        preview_window = sublime.active_window()

        preview_window.run_command(
            "set_layout",
            {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
            },
        )

        preview_window.focus_group(1)
        preview_view = preview_window.new_file()
        preview_view.set_scratch(True)
        preview_view.settings().set(PREVIEW_VIEW_INFOS, {})
        preview_view.set_name("Preview")
        # FIXME: hide number lines on preview

        preview_window.focus_group(0)
        if file_name:
            markdown_view = preview_window.open_file(file_name)
        else:
            markdown_view = preview_window.new_file()
            markdown_view.run_command("mdlp_insert", {"point": 0, "string": content})
            markdown_view.set_scratch(True)

        markdown_view.set_syntax_file(syntax_file)
        markdown_view.settings().set(
            MARKDOWN_VIEW_INFOS, {"original_window_id": original_window_id,},
        )

    def is_enabled(self):
        # FIXME: is this the best way there is to check if the current syntax is markdown?
        #        should we only support default markdown?
        #        what about "md"?
        # FIXME: what about other languages, where markdown preview roughly works?
        return "markdown" in self.view.settings().get("syntax").lower()


class MarkdownLivePreviewListener(sublime_plugin.EventListener):

    phantom_sets = {
        # markdown_view.id(): phantom set
    }

    # we schedule an update for every key stroke, with a delay of DELAY
    # then, we update only if now() - last_update > DELAY
    last_update = 0

    # FIXME: maybe we shouldn't restore the file in the original window...

    def on_pre_close(self, markdown_view):
        """ Close the view in the preview window, and store information for the on_close
        listener (see doc there)
        """
        if not markdown_view.settings().get(MARKDOWN_VIEW_INFOS):
            return

        self.markdown_view = markdown_view
        self.preview_window = markdown_view.window()
        self.file_name = markdown_view.file_name()

        if self.file_name is None:
            total_region = sublime.Region(0, markdown_view.size())
            self.content = markdown_view.substr(total_region)
            markdown_view.erase(edit, total_region)
        else:
            self.content = None

    def on_load_async(self, markdown_view):
        infos = markdown_view.settings().get(MARKDOWN_VIEW_INFOS)
        if not infos:
            return

        preview_view = markdown_view.window().active_view_in_group(1)

        self.phantom_sets[markdown_view.id()] = sublime.PhantomSet(preview_view)
        self._update_preview(markdown_view)

    def on_close(self, markdown_view):
        """ Use the information saved to restore the markdown_view as an original_view
        """
        infos = markdown_view.settings().get(MARKDOWN_VIEW_INFOS)
        if not infos:
            return

        assert (
            markdown_view.id() == self.markdown_view.id()
        ), "pre_close view.id() != close view.id()"

        del self.phantom_sets[markdown_view.id()]

        self.preview_window.run_command("close_window")

        # find the window with the right id
        original_window = next(
            window
            for window in sublime.windows()
            if window.id() == infos["original_window_id"]
        )
        if self.file_name:
            original_window.open_file(self.file_name)
        else:
            assert markdown_view.is_scratch(), (
                "markdown view of an unsaved file should " "be a scratch"
            )
            # note here that this is called original_view, because it's what semantically
            # makes sense, but this original_view.id() will be different than the one
            # that we closed first to reopen in the preview window
            # shouldn't cause any trouble though
            original_view = original_window.new_file()
            original_view.run_command(
                "mdlp_insert", {"point": 0, "string": self.content}
            )

            original_view.set_syntax_file(markdown_view.settings().get("syntax"))

    # here, views are NOT treated independently, which is theoretically wrong
    # but in practice, you can only edit one markdown file at a time, so it doesn't really
    # matter.
    # @min_time_between_call(.5)
    def on_modified_async(self, markdown_view):

        infos = markdown_view.settings().get(MARKDOWN_VIEW_INFOS)
        if not infos:
            return

        # we schedule an update, which won't run if an
        sublime.set_timeout(partial(self._update_preview, markdown_view), DELAY)

    def _update_preview(self, markdown_view):
        # if the buffer id is 0, that means that the markdown_view has been closed
        # This check is needed since a this function is used as a callback for when images
        # are loaded from the internet (ie. it could finish loading *after* the user
        # closes the markdown_view)
        if time.time() - self.last_update < DELAY / 1000:
            return

        if markdown_view.buffer_id() == 0:
            return

        self.last_update = time.time()

        total_region = sublime.Region(0, markdown_view.size())
        markdown = markdown_view.substr(total_region)

        preview_view = markdown_view.window().active_view_in_group(1)
        viewport_width = preview_view.viewport_extent()[0]

        basepath = os.path.dirname(markdown_view.file_name())
        html = markdown2html(
            markdown,
            basepath,
            partial(self._update_preview, markdown_view),
            resources,
            viewport_width,
        )

        self.phantom_sets[markdown_view.id()].update(
            [
                sublime.Phantom(
                    sublime.Region(0),
                    html,
                    sublime.LAYOUT_BLOCK,
                    lambda href: sublime.run_command("open_url", {"url": href}),
                )
            ]
        )


def get_settings():
    return sublime.load_settings("MarkdownLivePreview.sublime-settings")


def get_resource(resource):
    path = "Packages/MarkdownLivePreview/resources/" + resource
    abs_path = os.path.join(sublime.packages_path(), "..", path)
    if os.path.isfile(abs_path):
        with open(abs_path, "r") as fp:
            return fp.read()
    return sublime.load_resource(path)


def parse_image_resource(text):
    width, height, base64_image = text.splitlines()
    return base64_image, (int(width), int(height))


# try to reload the resources if we save this file
try:
    plugin_loaded()
except OSError:
    pass
