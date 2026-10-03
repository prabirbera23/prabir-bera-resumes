# Prabir Bera — resume designs

The published site contains a landing page and three independent HTML resume designs.

## View and share your resumes

**[Open the resume landing page](https://prabirbera23.github.io/prabir-bera-resumes/)** — use this link to share all three designs.

| Design | Live resume | Edit Markdown |
|---|---|---|
| Clean two-page layout | [View resume](https://prabirbera23.github.io/prabir-bera-resumes/clean.html) | [clean.md](content/clean.md) |
| Original grey-sidebar layout | [View resume](https://prabirbera23.github.io/prabir-bera-resumes/original.html) | [original.md](content/original.md) |
| Blue two-column layout | [View resume](https://prabirbera23.github.io/prabir-bera-resumes/blue.html) | [blue.md](content/blue.md) |

## Edit the CDP resume with Resume Studio

Double-click **Start Resume Editor.cmd** to open the private browser-based editor on your computer. Edit complete fields, preview the three-page layout, save local drafts, and publish through a GitHub connection. No hosting account is required. See [editor instructions](editor/README.md).

The CDP version now uses `content/cdp.json`. Its older Markdown file is retained for reference; use the editor for future CDP changes.

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


## Resume filenames

All four resume designs use `PRABIR_BERA_MAR_TECH_ASSOCIATE_MANAGER_12_YEARS_PUNE_OCT2026` as their PDF filename, with only the uppercase three-letter month and four-digit year changing to the reader's current local month/year. The fixed prefix must remain unchanged for future resumes. Shared `scripts/resume_naming.py` applies this rule to the website build and editor previews; use `apply_resume_naming(html)` in every future resume renderer. The editor's HTML and JSON downloads use the same filename with their respective extensions. Use the browser's **Save as PDF** destination to preserve clickable links and use the suggested filename.
