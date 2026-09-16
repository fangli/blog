---
title: 'A place for notes'
date: 2026-09-10T09:00:00-07:00
categories: [Projects]
contentLanguage: en
description: 'An example project journal, with a local image, a caption, and an embedded video.'
example: true
cover: portrait.jpg
---

A personal site can start with a small ambition: make it easy to publish something worth keeping.

This example shows how a project post can combine words and media. The image lives beside this Markdown file, so the post and its assets travel together.

## An image beside the words

![Fang Li outdoors by a lake, wearing a wide-brimmed hat and sunglasses.](portrait.jpg)

The Markdown for the image is simply:

```markdown
![A useful description of the image](portrait.jpg)
```

For a visible caption, use Hugo's figure shortcode:

{{< figure src="portrait.jpg" alt="Fang Li outdoors by a lake." caption="A local image, kept in the same folder as the post." width="320" >}}

## A little motion

Video is optional, user-controlled, and never starts automatically. This short, silent flower clip is a public-domain sample hosted by MDN.

{{< video src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4" title="A short flower clip — MDN's public-domain video example" type="video/mp4" >}}

Use a file in the post folder for a small clip, or an external URL for a larger one:

```text
{{</* video src="clip.mp4" title="A short project demonstration" */>}}
```

YouTube embeds are available too:

```text
{{</* youtube id="VIDEO_ID_HERE" title="Your video title" */>}}
```

## What belongs in a project journal?

A useful starting point is the problem, the smallest working idea, and what changed after trying it. A photograph or short demonstration often explains more than a long feature list.

For the full writing and publishing instructions, see the README in this site's GitHub repository.
