import sublime
import sublime_plugin
import html
from . import markdown2

# Main sublime tools function

def md(*t, **kwargs):
    sublime.message_dialog(kwargs.get('sep', '\n').join([str(el) for el in t]))

def sm(*t, **kwargs):
    sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs):
    sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

class MarkdownInPopupCommand(sublime_plugin.EventListener):
    def run(self, view):
        view.show_popup('<h1> hello </h1>', sublime.HIDE_ON_MOUSE_MOVE_AWAY, 1)
        return
        ph = sublime.Phantom(sublime.Region(0), "<h1> hello </h1>", sublime.LAYOUT_INLINE, None)
        ph_set = sublime.PhantomSet(sublime.active_window().active_view(), 'tests')
        ph_set.update([ph])

    def get_view_content(self, view):
        return view.substr(sublime.Region(0, view.size()))

    def on_modified(self, current_view):
        current_view_settings = current_view.settings()
        if 'markdown' not in current_view_settings.get('syntax').lower():
            return
        if current_view_settings.get('markdown_preview_enabled', False) is not True:
            return
        w = current_view.window()
        html = """<style>
            body {
                padding:10px;
                font-family: "Open Sans", sans-serif;
                background-color: #fff;
                font-size: 15px;
            }
            blockquote {
                font-style: italic;
                display: block;
                margin-left: 30px;
                border: 1px solid red;
            }
        </style>"""
        html += markdown2.markdown(self.get_view_content(current_view))
        view_id = current_view_settings.get('markdown_preview_id', None)
        def create_preview_panel():
            focus_group, focus_view = w.get_view_index(current_view)
            preview = w.new_file()
            w.run_command('new_pane')
            view_id = preview.id()
            current_view_settings.set('markdown_preview_id', view_id)
            w.focus_group(focus_group)
            w.focus_view(current_view)
            return preview

        def show_html(view, html):
            view.settings().set('gutter', False)
            view.erase_phantoms('markdown_preview')
            self.phantom_id = view.add_phantom('markdown_preview',
                             sublime.Region(0),
                             html,
                             sublime.LAYOUT_INLINE,
                             lambda href: sublime.run_command('open_url', {'url': href}))

        for view in w.views():
            if view.id() == view_id:
                show_html(view, html)
                break
        else:
            preview = create_preview_panel()
            show_html(preview, html)



# class MarkdownInPopupCommand(sublime_plugin.EventListener):
class MarkdownInPopupCommandc:

    def update_phantom(self, content, preview_view):
        ph = sublime.Phantom(sublime.Region(0), content, sublime.LAYOUT_BLOCK)
        self.phantom_set.update([ph])

    def on_modified(self, view):
        content = """
        <style>
            body {
                margin:10px;
            }
            blockquote {
                font-style: italic;
                display: block;
                margin: 10px;
            }
        </style>
        """
        content += markdown2.markdown(view.substr(sublime.Region(0, view.size())))

        # self.update_phantom(content)
