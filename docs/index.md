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

That's it. That's all you need to do to preview your markdown!

### Settings

To edit MarkdownLivePreview's settings, you just need to search in the command palette
`Preferences: MarkdownLivePreview Settings`, or from the menus:
*Preferences → Package Settings → MarkdownLivePreview → Settings*

Do not edit the left file (by default, you cannot), but the right one. This right file will
override the default one (on the left), and will be saved in your `User` folder, which makes it easy
to back up.

- `markdown_live_preview_on_open`: if set to `true`, as soon as you open a markdown file, the
preview window will popup (thanks to[@ooing][] for its [suggestion][@ooing suggestion]). Default to
`false`
- `load_from_internet_when_starts`: every images that starts with any of the string specified in
this list will be loaded from internet. Default to `["http://", "https://"]`
- `header_action`: If you're writing a blog with some markdown and a static website generator, you
probably have a YAML header. By default, this header will be displayed in a `pre` block. If you want
to hide it, then just change the value to `remove`. Thanks to [@tanhanjay][] for
[letting me know][front-matter-issue]!
- `keep_open_when_opening_preview`: Each time the preview window is opened, the original markdown
view is closed. If you want to keep it opened, just set this setting to `true`

### Custom CSS

If you want to, you can add custom `CSS` to the MarkdownLivePreview's default stylesheet.

Just search for `MarkdownLivePreview: Edit Custom CSS File` in the command palette
(<kbd>ctrl+shift+p</kbd>). It will open a file in which you can add some CSS that will be *added* to
the normal CSS.

!!! bug
    Comments in the CSS is interpreted weirdly by Sublime Text's phantoms. After a few tests, I
    think that everything that is bellow a comment is ignored.

    If you want to be sure that your CSS works, don't put any comments in it

#### Share your tweaks!

If you think that other users would enjoy your added CSS, then raise an issue, or PR the
[GitHub repo][] to share your tweaks!

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

Here's what I'd recommend for your MarkdownLivePreviewSyntax's settings (and what I use):

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

And here's what you'll get (With the awesome [Boxy Theme][] and its [Monokai Color Scheme][]):

![MarkdownLivePreview Screenshoot](imgs/syntax-specific-settings.png)

!!! tip
    On Windows at least, you can press <kbd>alt</kbd> to focus (so show) the menus, even if they're
    originally hidden.

That's it! I hope you'll enjoy using this package! If it's the case, please let your friends know
about it, and even myself by sending me a [tweet][] or staring the repo!
<iframe
src="https://ghbtns.com/github-btn.html?user=math2001&repo=MarkdownLivePreview&type=star&count=true&size=large"
frameborder="0" scrolling="0" style="width: 120px; height: 30px; vertical-align: bottom"></iframe>

[st]: https://sublimetext.com
[Markdown Extended]: https://packagecontrol.io/packages/Markdown%20Extended
[pck-con]: https://packagecontrol.io
[install-pck-con]: https://packagecontrol.io/installation
[tweet]: https://twitter.com/_math2001
[GitHub repo]: https://github.com/math2001/MarkdownLivePreview/issues
[@ooing]: https://github.com/ooing
[@ooing suggestion]: https://github.com/math2001/MarkdownLivePreview/issues/7#issue-199464852
[@tanhanjay]: https://github.com/tanhanjay
[front-matter-issue]: https://github.com/math2001/MarkdownLivePreview/issues/17
[Boxy Theme]: https://packagecontrol.io/packages/Boxy%20Theme
[Monokai Color Scheme]: https://github.com/ihodev/sublime-boxy#boxy-monokai--predawn
