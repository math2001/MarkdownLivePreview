import os.path
import sublime

def get_resource(resource):
    path = 'Packages/MarkdownLivePreview/resources/' + resource
    abs_path = os.path.join(sublime.packages_path(), '..', path)
    if os.path.isfile(abs_path):
        with open(abs_path, 'r') as fp:
            return fp.read()
    return sublime.load_resource(path)

resources = {}

def plugin_loaded():
    resources["base64_loading_image"] = get_resource('loading.base64')
    resources["base64_404_image"] = get_resource('404.base64')
    resources["stylesheet"] = get_resource('stylesheet.css')
