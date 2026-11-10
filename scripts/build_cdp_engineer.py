"""Build the Ooredoo-targeted CDP & Marketing Data resume."""
from pathlib import Path
import html, json, re
from resume_naming import apply_resume_naming

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "site"
TEMPLATE = ROOT / "templates" / "clean.html"
CONTENT = ROOT / "content" / "cdp-engineer.json"

def rich(value):
    escaped = html.escape(value)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped.replace("\n", "<br>")

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
                            "<title>Prabir Bera | Marketing Technology Product Engineer</title>")
    source = source.replace('href="mailto:Prabirjob23@gmail.com"',
                            'href="mailto:' + values["field-005"] + '"')
    source = source.replace('href="tel:+919975288822"',
                            'href="tel:' + re.sub(r"[^+\d]", "", values["field-006"]) + '"')
    source = apply_resume_naming(source)
    DEST.mkdir(exist_ok=True)
    (DEST / "cdp-engineer.html").write_text(source, encoding="utf-8")
    print("Built cdp-engineer.html")

if __name__ == "__main__":
    build()
