"""Build the Ooredoo-targeted CDP & Marketing Data resume."""
from pathlib import Path
import html, json, re
from cdp_clean import render_clean_cdp
from resume_naming import apply_resume_naming

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "site"
TEMPLATE = ROOT / "templates" / "clean.html"
CONTENT = ROOT / "content" / "cdp-engineer.json"
CDP_CONTENT = ROOT / "content" / "cdp.json"

def rich(value):
    escaped = html.escape(value)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped.replace("\n", "<br>")

def scoped_css(css, scope=".clean-page"):
    """Scope clean-resume styling so the engineer resume's first page stays intact."""
    rules = []
    i = 0
    while i < len(css):
        while i < len(css) and css[i].isspace():
            i += 1
        if i >= len(css):
            break
        brace = css.find("{", i)
        if brace < 0:
            rules.append(css[i:])
            break
        header = css[i:brace].strip()
        depth = 1
        end = brace + 1
        while end < len(css) and depth:
            if css[end] == "{":
                depth += 1
            elif css[end] == "}":
                depth -= 1
            end += 1
        body = css[brace + 1:end - 1]
        if header.startswith("@"):
            rules.append(f"{header}{{{scoped_css(body, scope)}}}")
        else:
            selectors = [selector.strip() for selector in header.split(",")]
            scoped = [scope + selector[len(".page"):] if selector.startswith(".page") else f"{scope} {selector}"
                      for selector in selectors]
            rules.append(",".join(scoped) + "{" + body + "}")
        i = end
    return "\n".join(rules)

def replace_with_clean_pages(engineer_html, clean_html):
    """Keep engineer page 1 and use pages 2–3 verbatim from the clean resume."""
    section_re = re.compile(r'<section class="page"[^>]*>.*?</section>', re.S)
    engineer_pages = list(section_re.finditer(engineer_html))
    clean_pages = list(section_re.finditer(clean_html))
    if len(engineer_pages) != 3 or len(clean_pages) != 3:
        raise ValueError(f"Expected three pages in both resumes; found {len(engineer_pages)} and {len(clean_pages)}.")

    replacements = []
    for page_index in (1, 2):
        page = clean_pages[page_index].group()
        page = page.replace('<section class="page">', '<section class="page clean-page">', 1)
        replacements.append((engineer_pages[page_index].start(), engineer_pages[page_index].end(), page))
    for start, end, page in reversed(replacements):
        engineer_html = engineer_html[:start] + page + engineer_html[end:]

    template_css = re.search(r'<style>(.*?)</style>', TEMPLATE.read_text(encoding="utf-8"), re.S).group(1)
    clean_css = re.search(r'<style>(.*?)</style>', clean_html, re.S).group(1)
    if not clean_css.startswith(template_css):
        raise ValueError("Could not isolate clean-resume page styling.")
    clean_only_css = scoped_css(clean_css[len(template_css):])
    engineer_html = engineer_html.replace("</head>", f"<style>{clean_only_css}</style></head>", 1)
    date_script = ('<script>function updateResumeDate(){const date=new Date();'
                   'document.getElementById("resume-updated-date").textContent="Resume Updated on: "+'
                   'date.toLocaleString("en-US",{month:"long"})+", "+date.getFullYear();}'
                   'updateResumeDate();window.addEventListener("beforeprint",updateResumeDate);</script>')
    return engineer_html.replace("</body>", date_script + "</body>", 1)

def build():
    values = json.loads(CONTENT.read_text(encoding="utf-8"))
    source = TEMPLATE.read_text(encoding="utf-8")
    import re
    placeholders = set(re.findall(r"\{\{(field-\d{3})\}\}", source))
    if placeholders != set(values):
        missing = placeholders - set(values)
        unused = set(values) - placeholders
        raise ValueError(f"CDP engineer template/content mismatch. Missing: {sorted(missing)}; unused: {sorted(unused)}")
    for key, value in values.items():
        if not isinstance(value, str):
            raise ValueError("All resume field values must be text.")
        source = source.replace("{{" + key + "}}", rich(value))
    source = source.replace("<title>Prabir Bera | Marketing Automation</title>",
                            "<title>Prabir Bera | Customer Data &amp; MarTech Integrations</title>")
    source = source.replace('href="mailto:Prabirjob23@gmail.com"',
                            'href="mailto:' + values["field-005"] + '"')
    source = source.replace('href="tel:+919975288822"',
                            'href="tel:' + re.sub(r"[^+\d]", "", values["field-006"]) + '"')
    clean_data = json.loads(CDP_CONTENT.read_text(encoding="utf-8"))
    clean_html = render_clean_cdp(clean_data)
    source = replace_with_clean_pages(source, clean_html)
    source = apply_resume_naming(source)
    DEST.mkdir(exist_ok=True)
    (DEST / "cdp-engineer.html").write_text(source, encoding="utf-8")
    print("Built cdp-engineer.html")

if __name__ == "__main__":
    build()

