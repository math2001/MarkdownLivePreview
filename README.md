# MarkdownLivePreview

This is a sublime text **3** plugin that allows you to preview your markdown instantly *in* it!

## Unmaintained

I am now using vim. I don't have the energy or the time to maintain this plugin anymore.

If anyone is interested in maintaining it, fork it, and submit a PR to package control to make it point to your fork.

### Dependencies

**None! There is no dependency!** It uses [markdown2](https://github.com/trentm/python-markdown2) but it's a one file plugin, so it's included in the package.

## Installation

MarkdownLivePreview is available on the default channel of
[PackageControl](http://packagecontrol.io), which means you just have to

1. Open the command palette (`ctrl+shift+p`)
2. Search for: `Package Control: Install Package`
3. Search for: `MarkdownLivePreview`
4. hit <kbd>enter</kbd>

to have MarkdownLivePreview working on your computer. Cool right? You can
[thank package control](https://packagecontrol.io/say_thanks) for this. :wink:

### Usage

You can choose to enable MarkdownLivePreview by pressing <kbd>alt+m</kbd> or selecting in the
command palette `MarkdownLivePreview: Edit Current File`. Note that you need to be editing (simply
having the focus on) a markdown file. Because [Markdown Extended][markdown-extended] did a good job,
it's compatible with this plugin.

So, once you've run it, it will open a new window, with only your markdown file, with the preview.
Once you're done, close whichever file and it'll close the entire window.

*Notice that it will close the entire window if you close __whichever__ file. It means that if you*
*open a random file in this window, and then close it, it'll close the entire window still*

For further infos, please [read the docs](https://math2001.github.io/MarkdownLivePreview/)!

### Demo

![demo](demo.gif)

### Somethings wrong!!

If you find that something's wrong with this package, you can let me know by raising an issue on the
[GitHub issue tracker][github-issue-tracker]

### How to open the [README][]

Some of the package add a command in the menus, others in the command palette, or other nowhere.
None of those options are really good, especially the last one on ST3 because the packages are
compressed. But, fortunately, there is plugin that exists and **will solve this problem** for us
(and he has a really cute name, don't you think?):
[ReadmePlease](https://packagecontrol.io/packages/ReadmePlease).

[markdown-extended]: https://packagecontrol.io/packages/Markdown%20Extended
[github-issue-tracker]: https://github.com/math2001/MarkdownLivePreview/issues
[st-css-rules]: http://www.sublimetext.com/docs/3/minihtml.html#css
[README]: http://github.com/math2001/MarkdownLivePreview/README.md
