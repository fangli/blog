# fang.li

A small personal blog built with **Hugo 0.166.0**, published on Cloudflare Workers with native GitHub builds. Posts are Markdown; there is no JavaScript framework or theme dependency.

## Write a post

Install Hugo **0.166.0 or newer** from [Hugo's releases](https://github.com/gohugoio/hugo/releases). The production version is recorded in `.hugo-version` and pinned in Cloudflare's `HUGO_VERSION` build variable.

```sh
hugo new content posts/my-new-post/index.md
hugo server --buildDrafts
```

Open the local address Hugo prints. A new post starts as a draft. Edit its Markdown:

```yaml
---
title: 'A small observation'
date: '2026-09-15T09:00:00-07:00'
draft: false
categories: ['Life']
contentLanguage: en
description: 'One or two sentences for the list and sharing previews.'
---
```

Write underneath that header. Set `draft: false` when ready, then commit and push:

```sh
git add content/
git commit -m "Add a small observation"
git push origin main
```

Cloudflare builds and publishes the site after every push to `main`. A failed build leaves the previous deployment live. Drafts and future-dated posts are excluded from production; a future-dated post needs another build after its date to appear.

Use `contentLanguage: zh-CN` for Chinese. Posts in both languages share one feed. Set `toc: true` for an optional table of contents. Keep folder names short and stable: `posts/my-new-post/index.md` publishes at `/posts/my-new-post/`. An optional `slug` can override that last segment.

## Categories and navigation

The initial categories are **Life**, **Software**, **Projects**, and **AI**. Give each post one primary category. Hugo supports more than one if that becomes useful, but one keeps the navigation clear.

Hugo's native category taxonomy generates `/life/`, `/software/`, `/projects/`, and `/ai/`. Changing a category does not change a post's URL.

To add a category, create `content/categories/travel/_index.md`:

```yaml
---
title: Travel
slug: travel
description: Notes from elsewhere.
weight: 50
menus:
  main:
    weight: 50
---
```

Then use `categories: ['Travel']` in a post. That one category file controls its title, URL, introduction, and navigation position. Use unique slugs; root-level names such as `posts`, `categories`, and `page` are reserved for site pages.

## Images and video

Keep images beside the post:

```text
content/posts/my-new-post/
  index.md
  photo.jpg
```

```markdown
![Describe what's in the image](photo.jpg)
```

Local raster images wider than 1600 pixels are resized by the Markdown image hook. Alt text matters; write a useful description. For a visible caption:

```go-html-template
{{< figure src="photo.jpg" alt="A description" caption="A short caption." >}}
```

For a local clip or externally hosted video:

```go-html-template
{{< video src="clip.mp4" title="A short demo" type="video/mp4" >}}
```

The player supports optional `poster`, `captions` (a WebVTT URL), and `lang`. Use hosted video for large files: Workers static assets have a per-file limit, and large video files make the Git history heavy. The example uses an external MDN sample.

For YouTube, use its 11-character video ID:

```go-html-template
{{< youtube id="YOUR_VIDEO_ID" title="A descriptive title" >}}
```

Videos have controls and never autoplay. YouTube embeds use the privacy-enhanced domain and lazy loading. Ordinary HTML in Markdown is disabled; use shortcodes for embeds.

## Code and formatting

Use fenced code blocks with a language, such as `python`, `go`, `sh`, or `javascript`. Hugo highlights them at build time. Code blocks and tables scroll horizontally on small screens.

The four included posts are explicitly marked as examples. They show Chinese/English text, links, quotes, lists, tables, code, a table of contents, images, and video. Edit them freely or delete their folders. Remove `example: true` to remove the example notice.

## Layout and appearance

- The site is capped at **68rem (1088px)**, with responsive side margins.
- Only the homepage has the approximately one-third profile / two-thirds post layout.
- Category and article pages use the full main content area.
- Mobile layouts stack, with all category links visible.
- Light/dark mode follows the operating system by default. The footer's theme icon cycles Auto (half-filled circle) → Light (sun) → Dark (moon) and remembers the selection.
- Each list paginates after ten posts. Change `pagination.pagerSize` in `hugo.toml`.
- RSS: `/index.xml` for all posts, `/life/index.xml` and equivalents for categories.
- Canonical URLs, social metadata, sitemap, robots.txt, and a custom 404 are generated automatically.

## Development and structure

```sh
hugo server --buildDrafts    # Live preview including drafts
hugo --gc --minify          # Production build into public/
python3 scripts/check.py    # Verify routes, pagination, drafts, and feeds
```

| Location | Purpose |
| --- | --- |
| `hugo.toml` | Site identity, category URLs, pagination, Markdown settings |
| `content/posts/` | Markdown page bundles and their media |
| `content/categories/` | Category descriptions and menu entries |
| `archetypes/posts.md` | Template for a new post |
| `layouts/` | Home, list, category, article, and 404 templates |
| `layouts/_partials/` | Shared header, footer, metadata, and post list |
| `layouts/_markup/` | Markdown image rendering |
| `layouts/shortcodes/` | Video embeds |
| `assets/css/` | Layout tokens and light/dark syntax styles |
| `assets/js/` | Theme preference only; navigation needs no JavaScript |
| `static/` | Avatar and Cloudflare response headers |
| `wrangler.jsonc` | Cloudflare static hosting and domain configuration |

Syntax colors in `assets/css/syntax.css` are generated from Hugo's `github` and `github-dark` Chroma styles. Regenerate them with `python3 scripts/syntax.py`. Layout and appearance are otherwise plain CSS. There is no Node dependency installation required to build the blog.

## Deployment

Cloudflare project: **fang-li-blog**. Production repository: **fangli/blog**, branch **main**.

Build configuration:

- Build command: `hugo --gc --minify`
- Deploy command: `npx wrangler@4.105.0 deploy`
- Root directory: repository root
- Build variable: `HUGO_VERSION=0.166.0`
- Static asset directory: `public` (configured in `wrangler.jsonc`)

Cloudflare's GitHub connection handles publishing. No Cloudflare API token is stored in this repository or in GitHub Actions. View deployment logs and roll back to an earlier version from the Cloudflare dashboard.

If a push does not start a build, check that the **Cloudflare Workers and Pages** GitHub App has access to `fangli/blog` in GitHub → Settings → Applications. A public repository can be cloned without that permission, but automatic builds require it.

For a Hugo upgrade, update `.hugo-version`, `module.hugoVersion.min` in `hugo.toml`, and Cloudflare's `HUGO_VERSION` together, then verify locally. The deployment uses a fixed version so a tool release cannot unexpectedly change your blog.
