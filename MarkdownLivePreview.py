import sublime
import sublime_plugin

from .lib.markdown2 import Markdown
from .utils import *

def plugin_loaded():
    pass

MARKDOWN_VIEW_INFOS = "markdown_view_infos"
PREVIEW_VIEW_INFOS = "preview_view_infos"
# FIXME: put this as a setting for the user to choose?
DELAY = 500 # ms

# original_view: the view in the regular editor, without it's own window
# markdown_view: the markdown view, in the special window
# preview_view: the preview view, in the special window
# original_window: the regular window
# preview_window: the window with the markdown file and the preview

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

        syntax_file = original_view.settings().get('syntax')

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


        sublime.run_command('new_window')
        preview_window = sublime.active_window()

        preview_window.run_command('set_layout', {
            'cols': [0.0, 0.5, 1.0],
            'rows': [0.0, 1.0],
            'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]
        })

        preview_window.focus_group(1)
        preview_view = preview_window.new_file()
        preview_view.set_scratch(True)
        preview_view.settings().set(PREVIEW_VIEW_INFOS, {})


        preview_window.focus_group(0)
        if file_name:
            markdown_view = preview_window.open_file(file_name)
        else:
            markdown_view = preview_window.new_file()
            markdown_view.run_command('mdlp_insert', {'point': 0, 'string': content})
            markdown_view.set_scratch(True)

        MarkdownLivePreviewListener.phantom_sets[markdown_view.id()] = sublime.PhantomSet(preview_view)
        MarkdownLivePreviewListener._update_preview(MarkdownLivePreviewListener, markdown_view)

        markdown_view.set_syntax_file(syntax_file)
        markdown_view.settings().set(MARKDOWN_VIEW_INFOS, {
            "original_window_id": original_window_id
        })

    def is_enabled(self):
        # FIXME: is this the best way there is to check if the current syntax is markdown?
        #        should we only support default markdown?
        #        what about "md"?
        return 'markdown' in self.view.settings().get('syntax').lower()

class MarkdownLivePreviewListener(sublime_plugin.EventListener):

    markdowner = Markdown()

    phantom_sets = {
        # markdown_view.id(): phantom set
    }

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
            # FIXME: this is duplicated code. How should it be generalized?
            total_region = sublime.Region(0, markdown_view.size())
            self.content = markdown_view.substr(total_region)
            markdown_view.erase(edit, total_region)
        else:
            self.content = None

    def on_close(self, markdown_view):
        """ Use the information saved to restore the markdown_view as an original_view
        """
        infos = markdown_view.settings().get(MARKDOWN_VIEW_INFOS)
        if not infos:
            return

        assert markdown_view.id() == self.markdown_view.id(), \
        "pre_close view.id() != close view.id()"

        self.preview_window.run_command('close_window')

        # find the window with the right id
        original_window = next(window for window in sublime.windows() \
                               if window.id() == infos['original_window_id'])
        if self.file_name:
            original_window.open_file(self.file_name)
        else:
            assert markdown_view.is_scratch(), "markdown view of an unsaved file should " \
            "be a scratch"
            # note here that this is called original_view, because it's what semantically
            # makes sense, but this original_view.id() will be different than the one
            # that we closed first to reopen in the preview window
            # shouldn't cause any trouble though
            original_view = original_window.new_file()
            original_view.run_command('mdlp_insert', {'point': 0, 'string': self.content})

            original_view.set_syntax_file(markdown_view.settings().get('syntax'))

    # here, views are NOT treated independently, which is theoratically wrong
    # but in practice, you can only edit one markdown file at a time, so it doesn't really
    # matter.
    # @min_time_between_call(.5)
    def on_modified_async(self, markdown_view):
        infos = markdown_view.settings().get(MARKDOWN_VIEW_INFOS)
        if not infos:
            return

        self._update_preview(markdown_view)

    def _update_preview(self, markdown_view):
        total_region = sublime.Region(0, markdown_view.size())
        markdown = markdown_view.substr(total_region)

        html = self.markdowner.convert(markdown)

        # FIXME: replace images

        self.phantom_sets[markdown_view.id()].update([
            sublime.Phantom(sublime.Region(0), html, sublime.LAYOUT_BLOCK,
                lambda href: sublime.run_command('open_url', {'url': href}))
            ])

