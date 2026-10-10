#!/usr/bin/env python3
"""Build standalone secondary pages using only the Python standard library."""

from html import escape, unescape
from pathlib import Path
import argparse
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
NAVIGATION = [('home', 'Home', 'index.html'), ('about', 'About Me', 'about.html'),
              ('portfolio', 'Portfolio', 'portfolio.html'), ('studies', 'Studies', 'studies.html'),
              ('contact', 'Contact', 'contact.html')]


def text_content(markup):
    return unescape(re.sub(r'<[^>]+>', '', markup)).strip()


def render_pages():
    homepage = (ROOT / 'index.html').read_text()
    styles = re.search(r'<style>(.*?)</style>', homepage, re.S).group(1).strip()
    favicon = re.search(r'<link rel="icon"[^>]+>', homepage).group(0)
    page_styles = (ROOT / 'templates/page.css').read_text()
    template = (ROOT / 'templates/page.html').read_text()
    metadata = json.loads((ROOT / 'content/pages.json').read_text())
    outputs = {}
    for page in metadata:
        slug = page['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError(f'Invalid page slug: {slug}')
        content = (ROOT / 'content' / f'{slug}.html').read_text()
        headings = []
        used_ids = set()

        def add_heading_id(match):
            title = text_content(match.group(1))
            base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'section'
            identifier = base
            counter = 2
            while identifier in used_ids:
                identifier = f'{base}-{counter}'
                counter += 1
            used_ids.add(identifier)
            headings.append((identifier, title))
            return f'<h2 id="{identifier}">{match.group(1)}</h2>'

        content = re.sub(r'<h2>(.*?)</h2>', add_heading_id, content, flags=re.S)
        toc = ''
        if headings and page['kind'] != 'collection':
            toc = '<ol aria-label="On this page">' + ''.join(
                f'<li><a href="#{identifier}">{escape(title)}</a></li>'
                for identifier, title in headings) + '</ol>'
        reading_minutes = max(1, math.ceil(len(text_content(content).split()) / 200))
        reading_label = (f'{reading_minutes} MIN READ' if page['kind'] == 'note'
                         else 'THE NOTEBOOK' if page['kind'] == 'collection' else 'A LITTLE MORE CONTEXT')
        nav = []
        for section, label, url in NAVIGATION:
            current = ' aria-current="page"' if section == page['section'] else ''
            nav.append(f'<a href="{url}"{current}>{label}</a>')
        breadcrumbs = '<a href="index.html">Home</a><span aria-hidden="true">/</span>'
        if page['kind'] == 'note':
            breadcrumbs += '<a href="studies.html">Studies</a><span aria-hidden="true">/</span>'
        breadcrumbs += f'<span>{escape(page["title"])}</span>'
        variables = {
            'TITLE': escape(page['title']), 'DESCRIPTION': escape(page['description']),
            'FAVICON': favicon, 'STYLES': styles, 'PAGE_STYLES': page_styles,
            'NAVIGATION': ''.join(nav), 'BREADCRUMBS': breadcrumbs,
            'EYEBROW': escape(page['eyebrow']), 'READING_LABEL': reading_label,
            'CONTENTS': toc, 'CONTENT': content,
            'RETURN_URL': escape(page['return_url'], quote=True),
            'RETURN_LABEL': escape(page['return_label']), 'SECTION': page['section'],
        }
        output = re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: variables[m.group(1)], template)
        if re.search(r'\{\{[A-Z_]+\}\}', output):
            raise ValueError(f'Unresolved template field: {slug}')
        outputs[ROOT / f'{slug}.html'] = output
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated pages need rebuilding')
    args = parser.parse_args()
    outputs = render_pages()
    stale = []
    for path, output in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != output:
                stale.append(path.name)
        else:
            path.write_text(output)
    if stale:
        parser.exit(1, 'Rebuild required: ' + ', '.join(stale) + '\nRun python3 scripts/build_pages.py\n')
    print(f'{len(outputs)} standalone pages ' + ('up to date.' if args.check else 'built.'))


if __name__ == '__main__':
    main()
