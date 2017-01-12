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

So, once you've run it, it will open a new window, with only your markdown file, with the preview. Once you're done, close whichever file and it'll close the entire window.

*Notice that it will close the entire window if you close __whichever__ file. It means that if you open a random file in this window, and then close it, it'll close the entire window still*

### Settings

- `markdown_live_preview_on_open`: if set to `true`, as soon as you open a markdown file, the preview window will popup (thanks to [@ooing](https://github.com/ooing) for its [suggestion](https://github.com/math2001/MarkdownLivePreview/issues/7#issue-199464852)). Default to `false`
- `load_from_internet_when_starts`: every images that starts with any of the string specified in this list will be loaded from internet. Default to `["http://", "https://"]`

Note: To edit your settings, search up in the command palette `Preferences: MarkdownLivePreview Settings`, or by using the menu: `Preferences → Packages Settings → MarkdownLivePreview → Settings` ;. It's not your global settings, but only the `MarkdownLivePreview`'s one

### Syntax Specific Settings

This in an other "type" of setting. :laughing: If you have a look at the syntax of the preview file (not the markdown one, really the preview), you'll see that the syntax is `MarkdownLivePreviewSyntax`. This mean that you can specify specific settings for this specific syntax (such as `word_wrap: true`, `rulers: []`, etc).

To do so, you can

1. focus the *preview* (<kbd>ctrl+2</kbd> to focus the second group, so, by default, the preview's group)
2. search up in the command palette `Preferences: Settings Syntax Specific`. It's in the *right* file that you can add the settings you want (not the left one).

Note: MarkdownLivePreview will actualy look in this file for settings that aren't supported by default. Here they are:

- `show_tabs`
- `show_minimap`
- `show_status_bar`
- `show_sidebar`
- `show_menus`

They talk for themself, don't they? All of them takes a boolean (`true` or `false`). Note that those settings are *window* specific, not just view specific (that's why they aren't supported). It means that they'll affect the entire window, and every view in it. 

Here is an example of syntax specific settings for MarkdownLivePreviewSyntax:

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

And here's what you'll get:

![MarkdownLivePreview Screenshoot](screenshoots/syntax-specific-settings.png)

*Note: to close a file, you can do <kbd>ctrl+w</kbd> (on Mac OS, it's <kbd>cmd+w</kbd>)*

### Clear the cache

MarkdownLivePreview caches every images it loads from internet (otherwise, you'd never see your images, or you'd need to have a *really* fast internet connection :smile:). So, if for some reason you want to clear the cache (a simple file), you can do so from the command palette by running `

### Demo

![demo](demo.gif)

### Custom css

It is possible to set your own css. But, be carefull, you have to respect [those rules](http://www.sublimetext.com/docs/3/minihtml.html#css). Just go to `Preferences → Package Settings → MarkdownLivePreview → Style - CSS`. It will open a css file, here: `$packages/User/MarkdownLivePreview.css`. Just save it and it will automatically use it instead of the default one.

### Somethings wrong!!

If you find that something's wrong with this package, you can let me know by raising an issue on the [GitHub issue tracker][github-issue-tracker]

### How to open the [README](http://github.com/math2001/MarkdownLivePreview/README.md)

Some of the package add a command in the menus, others in the command palette, or other nowhere. None of those options are really good, especially the last one on ST3 because the packages are compressed. But, fortunately, there is plugin that exists and **will solve this problem** for us (and he has a really cute name, don't you think?): [ReadmePlease](https://packagecontrol.io/packages/ReadmePlease).



[markdown-extended]: https://packagecontrol.io/packages/Markdown%20Extended
[github-issue-tracker]: https://github.com/math2001/MarkdownLivePreview/issues
