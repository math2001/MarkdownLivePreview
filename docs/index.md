# Welcome to MarkdownLivePreview's documentation!

<img src="imgs/MarkdownLivePreview.svg" alt="MarkdownLivePreview's logo"
     style="width: 400px; margin: auto; display: block;">

MarkdownLivePreview is a [Sublime Text 3][st] plugin to preview your markdown as you type,
*right in Sublime Text itself*, without *any* dependency!

It's very easy to use, but there's a few things that you might want to be aware of... So, let's
get started

## Installation

### Using Package Control

You can really easily install MarkdownLivePreview by using [Package Control][pck-con].

If it's not already, you need to [install it][install-pck-con] first.

!!! note
    If you're using the latest build of Sublime Text 3, you can just do
    *Tools → Install Package Control…*

- Open up the command palette (<kbd>ctrl+shift+p</kbd>)
- Search up `Package Control: Install Package` (might take a few seconds)
- In the panel that just showed up, search for `MarkdownLivePreview`

Done! You have now access to every single features of MarkdownLivePreview! :wink:

### Using `git`

```sh
$ cd "%APPDATA%\Sublime Text 3\Packages"             # on Windows
$ cd ~/Library/Application\ Support/Sublime\ Text\ 3 # on Mac
$ cd ~/.config/sublime-text-3                        # on Linux

$ git clone "https://github.com/math2001/MarkdownLivePreview"
```

> So, which one do I pick?!

I depends of what you want to do. If you want to just use MarkdownLivePreview, pick the first
solution, you'll get every update automatically. But if you want to contribute, then choose the
second solution.

## Usage

### Previewing

As told in the introduction, MarkdownLivePreview is very easy to use:

- open a markdown file
- press <kbd>alt+m</kbd>
- or select in the command palette `MarkdownLivePreview: Edit Current File`

!!! note
    The preview of unsaved markdown files is currently not supported. It should be fixed soon.

!!! tip
    [Markdown Extended][] is supported too!

That's it.

### Clearing the cache

MarkdownLivePreview has a cache system to store images you load from internet. You can clear this
cache by searching up in the command palette `MarkdownLivePreview: Clear the cache`.

!!! tip
    The cache is one simple file called `MarkdownLivePreviewCache`, which is located in your temp
    folder. To know where it is, you can open the Sublime Text console (<kbd>ctrl+`</kbd> or
    *View → Show Console*), and paste this in:

    ```python
    import tempfile; print(tempfile.gettempdir())
    ```

### Custom settings for the preview

Sublime Text makes it easy to set custom settings for a specific *type* of view. For example,
`markdown`, `python`, etc. MarkdownLivePreview takes advantage of that: the preview view (the view
on the right) is a specific syntax (called — sorry for the originality —
`MarkdownLivePreviewSyntax`). So, to change this, you can focus the right view, open up the command
palette (<kbd>ctrl+shift+p</kbd>), and search up `Preferences: Settings — Syntax Specific`. In here,
you can specify any settings that is going to be applied only to this view.

### The hacky part

In fact, MarkdownLivePreview parses those settings, and looks for specific ones:

- `show_tabs`
- `show_minimap`
- `show_status_bar`
- `show_sidebar`
- `show_menus`

Those settings aren't supported by default because they affect the entire *window* instead of just
the view. But MarkdownLivePreview will look for them in your *preview*'s settings, and hide/show the
tabs, the minimap, etc...

As you probably guessed those settings takes a bool for value (`true` or `false`).

### Recommendation

Here's what I'd recommend (and use):

```json
{
    "show_menus": false,
    "show_tabs": false,
    "show_minimap": false,
    "gutter": false,
    "rulers": [],
    "word_wrap": true
}
```

!!! note
    On Windows at least, you can press <kbd>alt</kbd> to focus (so show) the menu, even if they're
    originally hidden

That's it! I hope you'll enjoy using this package! If it's the case, please let your friends know
about it, and even myself by sending me a [tweet][] or staring the repo
<iframe
src="https://ghbtns.com/github-btn.html?user=math2001&repo=MarkdownLivePreview&type=star&count=true&size=large"
frameborder="0" scrolling="0" width="160px" height="30px"></iframe>!

[st]: https://sublimetext.com
[Markdown Extended]: https://packagecontrol.io/packages/Markdown%20Extended
[pck-con]: https://packagecontrol.io
[install-pck-con]: https://packagecontrol.io/installation
[tweet]: https://twitter.com/_math2001
