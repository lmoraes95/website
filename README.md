# Leon Moraes — website

A static personal site with Home, About Me, Portfolio, Blog, and Contact. The homepage navigation scrolls between sections; section links open the longer pages.

No package installation or build step is required. Serve the entire directory so links and `assets/animation.mp4` work. The animation links to `https://www.instagram.com/un.familiar_ground/`.

## Edit the site

The root HTML files are the pages served to visitors. Each has inline styles and JavaScript. Edit those files directly and keep any matching `content/*.html` fragments and `content/pages.json` metadata in sync.

- `index.html`: homepage layout, text, animation link, and latest-post preview.
- `blog.html`: blog listing. Add or edit entries in the `post-list` element.
- `voter-id.html`: the first blog post, including the supplied source links.
- `about.html`, `portfolio.html`, `contact.html`: longer section pages.
- `content/*.html`: matching body fragments, useful when editing or reusing content.
- `content/pages.json`: page titles, descriptions, sections, and return links.
- `templates/page.html` and `templates/page.css`: reference layout and styles for additional pages.

There is no page generator included in this checkout. Editing a fragment or template alone does not update the served pages.

## Add a blog post

1. Copy `voter-id.html` to a new root HTML file with a descriptive name.
2. Update its document title, description, breadcrumb, heading, subtitle, reading time, contents links, and article body. Give each section heading a unique ID.
3. Keep the return link pointing to `blog.html` and the Blog navigation item active.
4. Add the body fragment to `content/` and an entry to `content/pages.json` with `kind: "post"` and `section: "blog"`.
5. Add a linked summary in `blog.html` and `content/blog.html`; update the latest-post preview in `index.html` if appropriate.
6. Open the site through the local server and check navigation, citations, and mobile layout.

## Routes

- `index.html#blog`: the homepage blog section.
- `blog.html`: all blog posts.
- `voter-id.html`: “Voter ID Sounds Reasonable. So What Does It Actually Solve?”
- `studies.html`: compatibility redirect to `blog.html`. The old `index.html#studies` anchor also remains available for bookmarks.

The three original study-note pages and their content fragments have been removed. Existing credential links are on the About Me page.

Cloudflare Web Analytics remains in the live pages. Exclude its requests during automated local checks to avoid sending synthetic visits. Local edits do not publish or deploy the site.
