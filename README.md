# Leon Moraes — website

## Edit the site

- `index.html`: homepage content, styles, and scroll navigation. This remains a self-contained page and supplies the shared visual styles to the page builder.
- `content/*.html`: longer page content and study notes, as HTML fragments.
- `content/pages.json`: page titles, descriptions, navigation sections, and return links.
- `templates/page.html`: shared secondary-page layout.
- `templates/page.css`: styles specific to the longer pages.
- `scripts/build_pages.py`: standard-library Python builder. It embeds styles into each output, adds heading anchors and a contents list, and calculates reading time for notes.

After changing the shared homepage styles, content, metadata, or templates, regenerate the secondary pages:

```sh
python3 scripts/build_pages.py
python3 scripts/build_pages.py --check
```

The root `about.html`, `portfolio.html`, `studies.html`, `contact.html`, and `studies-*.html` files are generated. Edit their source fragments and rebuild, rather than editing generated output. Commit the generated files with their sources so static hosting can serve the site without running a build.

## Add a study note

1. Create `content/studies-your-topic.html` with the body of your note. Use `h2` for sections; the template supplies the page's `h1`.
2. Add its metadata in `content/pages.json`, following an existing note. Set `kind` to `note`, `section` to `studies`, and `return_url` to `studies.html`.
3. Add a linked entry to `content/studies.html` using the existing `post-row` structure.
4. Run `python3 scripts/build_pages.py` and `python3 scripts/build_pages.py --check`.

## Page map

- `index.html` — short introduction with Home / About Me / Portfolio / Studies / Contact anchors.
- `about.html` — longer introduction and interests.
- `portfolio.html` — empty project shelf.
- `studies.html` — study-note index and existing credentials.
- `studies-better-questions.html` — asking useful questions before modeling.
- `studies-community-impact.html` — evaluating community impact beyond averages.
- `studies-show-your-work.html` — reproducible analysis.
- `contact.html` — email and existing social links.
