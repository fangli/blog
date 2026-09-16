---
title: 'Small functions, clear boundaries'
date: 2026-09-11T09:00:00-07:00
categories: [Software]
contentLanguage: en
description: 'A small code example, and a reminder to make the common case easy to read.'
example: true
toc: true
---

A useful function has a clear job. Its name describes that job, its inputs are explicit, and its output is easy to check.

This example turns a list of notes into a small summary:

```python
from collections import Counter


def count_categories(notes):
    """Count notes by their primary category."""
    return Counter(note["category"] for note in notes)


notes = [
    {"title": "A quiet afternoon", "category": "Life"},
    {"title": "A little command-line tool", "category": "Projects"},
    {"title": "A walk without a destination", "category": "Life"},
]

print(count_categories(notes))
# Counter({'Life': 2, 'Projects': 1})
```

## Make assumptions visible

This function expects each note to have a `category`. That's a deliberate boundary: validation belongs where the notes enter the program.

If the input is less predictable, the implementation should say what happens when a category is missing. There is no universal answer; there is only a choice that should be visible.

## A short comparison

| Choice | Benefit | Trade-off |
| --- | --- | --- |
| Require a category | Clear data model | Validate input first |
| Use a default | Tolerates incomplete notes | Can hide missing metadata |
| Skip incomplete notes | Keeps processing | May lose useful information |

## Leave room to change

Start with the version that is easiest to explain. Add another layer when a real requirement needs it.

A long code line stays inside a scrollable code block on narrow screens:

```sh
hugo server --buildDrafts --disableFastRender --bind 127.0.0.1 --port 1313 --baseURL http://localhost:1313/
```

This example also demonstrates an optional table of contents. Set `toc: true` in a post to show it.
