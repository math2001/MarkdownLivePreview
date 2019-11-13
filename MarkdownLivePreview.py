import sublime
import sublime_plugin

from .utils import *

def plugin_loaded():
    pass

class MdlpInsertCommand(sublime_plugin.TextCommand):

    def run(self, edit, point, string):
        self.view.insert(edit, point, string)

class OpenMarkdownPreviewCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        """ If the file is saved exists on disk, we close it, and reopen it in a new
        window. Otherwise, we copy the content, erase it all (to close the file without
        a dialog) and re-insert it into a new view into a new window """

        original_view = self.view
        file_name = original_view.file_name()

        syntax_file = original_view.settings().get('syntax')

        if file_name is None:

            # the file isn't saved, we need to restore the content manually
            total_region = sublime.Region(0, original_view.size())
            content = original_view.substr(total_region)
            original_view.erase(edit, total_region)
            original_view.close()

            # FIXME: save the document to a temporary file, so that if we crash,
            #        the user doesn't lose what he wrote

        else:
            original_view.close()

        sublime.run_command('new_window')
        window = sublime.active_window()

        window.run_command('set_layout', {
            'cols': [0.0, 0.5, 1.0],
            'rows': [0.0, 1.0],
            'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]
        })

        window.focus_group(0)
        if file_name:
            new_view = window.open_file(file_name)
        else:
            new_view = window.new_file()
            new_view.run_command('mdlp_insert', {'point': 0, 'string': content})

        new_view.set_syntax_file(syntax_file)

    def is_enabled(self):
        # FIXME: is this the best way there is to check if the current syntax is markdown?
        #        should we only support default markdown?
        #        what about "md"?
        return 'markdown' in self.view.settings().get('syntax').lower()

