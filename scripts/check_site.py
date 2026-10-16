#!/usr/bin/env python3
"""Dependency-free checks for missing assets, invalid anchors, semantics and design references."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images, self.headings = [], [], [], []
        self.language = None
        self.mains = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag == 'main':
            self.mains += 1
        if re.fullmatch('h[1-6]', tag):
            self.headings.append(tag)
        if tag in ('a', 'link'):
            self.links.append(attrs.get('href', ''))
        if tag == 'img':
            self.images.append(attrs)


def main():
    page = Page()
    page.feed((ROOT / 'index.html').read_text())
    assert page.language == 'ja' and page.mains == 1
    assert page.headings == ['h1', 'h2', 'h3', 'h2', 'h2'], page.headings
    assert len(page.ids) == len(set(page.ids)), 'Duplicate IDs'
    for link in page.links:
        assert link, 'Empty link'
        if link.startswith('#'):
            assert link[1:] in page.ids, link
        elif link.startswith('/'):
            assert (ROOT / link.lstrip('/')).exists(), link
        else:
            assert urlsplit(link).scheme in ('https', 'mailto'), link
    assert 'mailto:contact@secondloop.co.jp' in page.links
    assert 'https://imagebgm.secondloopapps.com/' in page.links
    for img in page.images:
        assert 'alt' in img and img.get('width') and img.get('height'), img
        assert (ROOT / img['src'].lstrip('/')).is_file(), img
    css = ''.join(path.read_text() for path in (ROOT / 'assets').glob('*.css'))
    defined = set(re.findall(r'(--[\w-]+)\s*:', css))
    used = set(re.findall(r'var\((--[\w-]+)', css))
    assert used <= defined, f'Undefined CSS tokens: {used - defined}'
    mapping = json.loads((ROOT / 'design/handoff.json').read_text())
    assert mapping['source']['fileKey'] == 'HVfBJvdRq2H356JIguk7Kh'
    assert (ROOT / 'CNAME').read_text().strip() == 'secondloop.co.jp'
    print('Site checks passed: headings, anchors, links, assets, CSS tokens, Figma mapping and domain.')


if __name__ == '__main__':
    main()
