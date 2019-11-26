# MarkdownLivePreview

A simple plugin to preview your markdown as you type right in Sublime Text.
No dependencies!

## How to install

It's available on package control!

## Setting a keybinding

The open the preview, you can search up in the command palette
(<kbd>ctrl+shift+p</kbd>) `MarkdownLivePreview: Open Preview`. But if you
prefer to have a shortcut, add this to your keybindings file:

```json
{
    "keys": ["alt+m"],
    "command": "open_markdown_preview"
}
```

## How to contribute

If you know what feature you want to implement, or what bug you wanna fix, then
go ahead and hack! Maybe raise an issue before hand so that we can talk about
it if it's a big feature.

But if you wanna contribute just to say thanks, and don't really know what you
could be working on, then there are a bunch of `FIXME`s all over this package.
Just pick one and fix it :-)

```
$ git clone https://github.com/math2001/MarkdownLivePreview
$ cd MarkdownLivePreview
$ grep -R FIXME
```

### Hack it!

1. Fork this repo
2. Make your own branch (the name of the branch should be the feature you are
   implementing eg. `improve-tables`, `fix-crash-on-multiple-preview`
3. All your code should be formated by black.
4. Send a PR!