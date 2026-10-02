# Prabir Bera — three resume designs

The published site contains a landing page and three independent HTML resume designs.

## Edit your resume on GitHub

1. Open `content/clean.md`, `content/blue.md`, or `content/original.md`.
2. Click the pencil to edit.
3. Change the text below the relevant `##` heading. Keep the field ID in the heading unchanged.
4. Commit your change to `main`.
5. Wait for **Build and publish resumes** in the Actions tab to finish. Your existing shareable URL updates automatically.

Edits affect only the chosen version. Edit all three Markdown files if you want the same change everywhere. Clean and blue content supports `**bold**`. Blank text removes that field's content; do not remove its heading.

The original design preserves the previous fixed-position PDF layout, including the icon-line fix. Its content is edited line by line. Longer replacement text may overlap or require a layout adjustment, so preview before sharing. Sidebar edits replace the image-backed sidebar text with selectable SVG text. Badges, icons, and the QR code remain graphics; their destination is not changed by editing contact text.

## Build locally

With Python 3 installed, run:

```sh
python scripts/build.py
python -m http.server 8000 --directory site
```

Open `http://localhost:8000`. No packages or build dependencies are needed. HTML files in `site/` are generated; edit the Markdown source instead.

## Structure

- `content/`: the three editable Markdown resumes
- `templates/`: layout templates and original content mapping
- `scripts/build.py`: converts Markdown content into the three layouts
- `.github/workflows/pages.yml`: builds and publishes GitHub Pages after each commit

Choose **GitHub Actions** under Settings → Pages → Source to enable automatic publishing.
