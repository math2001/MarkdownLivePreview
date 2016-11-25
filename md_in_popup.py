import sublime
import sublime_plugin
from . import markdown2
import os.path

# Main sublime tools function

def md(*t, **kwargs):
    sublime.message_dialog(kwargs.get('sep', '\n').join([str(el) for el in t]))

def sm(*t, **kwargs):
    sublime.status_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def em(*t, **kwargs):
    sublime.error_message(kwargs.get('sep', ' ').join([str(el) for el in t]))

def get_style():
    """Of course, this is temporal, there will be an option to customize the CSS"""
    return """<style>
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

def close_preview(md_view_settings, preview):
    preview.close()
    md_view_settings.erase('markdown_preview_id')
    md_view_settings.erase('markdown_preview_enabled')

def create_preview(window, md_view):
    focus_group, focus_view = window.get_view_index(md_view)
    preview = window.new_file()
    window.run_command('new_pane') # move the preview to a new group
    preview.set_name(os.path.basename(md_view.file_name()) + ' - Preview')

    preview_settings = preview.settings()
    preview_settings.set('gutter', False)
    preview_settings.set('is_markdown_preview', True)
    preview_settings.set('markdown_view_id', md_view.id())

    md_view.settings().set('markdown_preview_id', preview.id())
    window.focus_group(focus_group)
    window.focus_view(md_view)

    return preview, preview_settings

def show_html(md_view, preview):
    html = get_style() + markdown2.markdown(get_view_content(md_view))
    preview.erase_phantoms('markdown_preview')
    preview.add_phantom('markdown_preview',
                         sublime.Region(0),
                         html,
                         sublime.LAYOUT_INLINE,
                         lambda href: sublime.run_command('open_url', {'url': href}))

def get_view_content(view):
    return view.substr(sublime.Region(0, view.size()))

def get_view_from_id(window, id):
    for view in window.views():
        if view.id() == id:
            return view

class MarkdownInPopupCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        settings = view.settings()
        if not 'markdown' in settings.get('syntax').lower():
            return
        settings.add_on_change('markdown_preview_enabled', lambda: self.on_modified(view))

    def on_modified(self, md_view):
        window = md_view.window()
        md_view_settings = md_view.settings()

        if not 'markdown' in md_view_settings.get('syntax').lower():
            return

        markdown_preview_enabled = md_view_settings.get('markdown_preview_enabled') is True
        preview_id = md_view_settings.get('markdown_preview_id', None)

        if not markdown_preview_enabled:
            if preview_id is not None:
                close_preview(md_view_settings, get_view_from_id(window, preview_id))
            return

        if preview_id is None:
            preview, preview_settings = create_preview(window, md_view)
        else:
            preview = get_view_from_id(window, preview_id)
            if not preview:
                md_view_settings.erase('markdown_preview_id')
                md_view_settings.erase('markdown_preview_enabled')
                return
            preview_settings = preview.settings()

        show_html(md_view, preview)

    def on_pre_close(self, view):
        settings = view.settings()
        if settings.get('markdown_preview_enabled') is True:
            preview = get_view_from_id(view.window(), settings.get('markdown_preview_id'))
            if preview:
                sublime.set_timeout_async(lambda: preview.close(), 100)
