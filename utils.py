# import sublime
import time


def get_settings():
    return sublime.get_settings("MarkdownLivePreview.sublime-settings")


def min_time_between_call(timeout, on_block=lambda *args, **kwargs: None):
    """ Enforces a timeout between each call to the function
    timeout is in seconds
    """
    last_call = 0

    def outer(func):
        def wrapper(*args, **kwargs):
            nonlocal last_call

            if time.time() - last_call < timeout:
                time.sleep(timeout - (time.time() - last_call))

            last_call = time.time()
            return func(*args, **kwargs)

        return wrapper

    return outer
