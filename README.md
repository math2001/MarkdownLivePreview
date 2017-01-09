# MarkdownLivePreview

This is a sublime text **3** plugin that allows you to preview your markdown instantly *in* it!

### Dependencies

**None**! There is no dependency! It uses [markdown2](https://github.com/trentm/python-markdown2) but it's a one file plugin, so it's included in the package.

## Installation

MarkdownLivePreview is available on the default channel of [PackageControl](http://packagecontrol.io), which means you just have to

1. Open the command palette (`ctrl+shift+p`)
2. Search for: `Package Control: Install Package`
3. Search for: `MarkdownLivePreview`
4. hit <kbd>enter</kbd>

to have MarkdownLivePreview working on your computer. Cool right? You can [thank package control](https://packagecontrol.io/say_thanks) for this.

### Usage

You can choose to enable MarkdownLivePreview by pressing <kbd>alt+m</kbd> or selecting in the command palette `MarkdownLivePreview: Edit Current File`. Note that you need to be editing (simply having the focus on) a markdown file. Because [Markdown Extended][markdown-extended] did a good job, it's compatible with this plugin.

It will open a new window, with only your markdown file, with the preview. Once your done, close whichever file and it'll close the entire window.

*Notice that it will close the entire window if you close **whichever** file. It means that if you open a random file in this window, and then close it, it'll close the entire window still*

### Settings

- `markdown_live_preview_on_open`: if set to `true`, as soon as you open a markdown file, the preview window will popup (thanks to [@ooing](https://github.com/ooing) for it's [suggestion](https://github.com/math2001/MarkdownLivePreview/issues/7#issue-199464852)). Default to `false`
- `load_from_internet_when_starts`: every images that starts with any of the string specified in this list will be loaded from internet. Default to `["http://", "https://"]`

### In dev

This plugin is not finished, there's still some things to fix (custom css, focus, etc). So, don't run away if you have any trouble, just submit an issue [here](http://github.com/math2001/MarkdownLivePreview/issues).

### Demo

![demo](demo.gif)

### Custom css

It is possible to set your own css. But, be carefull, you have to respect [those rules](http://www.sublimetext.com/docs/3/minihtml.html#css). Just go to `Preferences -> Package Settings -> MarkdownLivePreview`. It will open a css file, here: `$packages/User/MarkdownLivePreview.css`. Just save it and it will automatically use it instead of the default one.

### How to open the [README](http://github.com/math2001/MarkdownLivePreview/README.md)

Some of the package add a command in the menus, others in the command palette, or other nowhere. None of those options are really good, especially the last one on ST3 because the packages are compressed. But, fortunately, there is plugin that exists and **will solve this problem** for us (and he has a really cute name, don't you think?): [ReadmePlease](https://packagecontrol.io/packages/ReadmePlease).



[markdown-extended]: https://packagecontrol.io/packages/Markdown%20Extended
