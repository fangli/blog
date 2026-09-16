#!/usr/bin/env python3
"""Check the real production build plus pagination and draft behavior."""
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlparse
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[k] for k in ('href', 'src', 'poster') if attrs.get(k))


def build(destination, *args):
    subprocess.run(['hugo', '--gc', '--minify', '--panicOnWarning',
                    '--destination', str(destination), *args], cwd=ROOT, check=True)


with TemporaryDirectory(prefix='fangli-check-') as tmp:
    work = Path(tmp)
    output = work / 'public'
    build(output)
    for page in output.rglob('*.html'):
        for link in Document(page.read_text()).links:
            parsed = urlparse(link)
            if parsed.scheme not in ('', 'http', 'https') or not parsed.path:
                continue
            if parsed.netloc and parsed.netloc != 'fang.li':
                continue
            target = (output / unquote(parsed.path.lstrip('/'))
                      if parsed.path.startswith('/') else page.parent / unquote(parsed.path))
            assert target.is_file() or (target / 'index.html').is_file(), (page, link)
    for feed in output.rglob('*.xml'):
        ET.parse(feed)
    for category in ('life', 'software', 'projects', 'ai'):
        assert (output / category / 'index.html').is_file(), category
        assert (output / category / 'index.xml').is_file(), category
    assert '<html lang=zh-CN>' in (output / 'posts/welcome/index.html').read_text()
    assert 'aria-current=location>Software' in (output / 'posts/small-functions/index.html').read_text()

    # A copied content tree keeps generated test posts out of the real site.
    content = work / 'content'
    shutil.copytree(ROOT / 'content', content)
    subprocess.run(['hugo', 'new', 'content', '--contentDir', str(content),
                    'posts/archetype-check/index.md'], cwd=ROOT, check=True)
    created = (content / 'posts/archetype-check/index.md').read_text()
    assert "categories: ['Life']" in created and 'draft: true' in created
    for i in range(12):
        (content / 'posts' / f'pagination-check-{i}.md').write_text(
            f'---\ntitle: Pagination check {i}\ndate: 2025-01-01\ncategories: [Life]\n---\nTest.\n')
    (content / 'posts' / 'draft-check.md').write_text(
        '---\ntitle: Draft check\ndate: 2025-01-01\ndraft: true\n---\nPrivate draft.\n')
    paginated = work / 'paginated'
    build(paginated, '--contentDir', str(content))
    assert (paginated / 'page/2/index.html').is_file()
    assert (paginated / 'life/page/2/index.html').is_file()
    assert 'Older posts' in (paginated / 'index.html').read_text()
    assert 'Newer posts' in (paginated / 'page/2/index.html').read_text()
    assert '/life/page/2/' in (paginated / 'life/index.html').read_text()
    assert not (paginated / 'posts/draft-check').exists()
    assert 'Draft check' not in (paginated / 'index.xml').read_text()
print('Passed: production build, internal links, XML feeds, categories, language, navigation, pagination, and drafts.')
