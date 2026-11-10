"""Build the engineer resume in the original CDP layout."""
import json
import re
from pathlib import Path

from editor_model import render

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "site" / "cdp-engineer-original.html"


def build():
    template = json.loads((ROOT / "content" / "cdp.json").read_text(encoding="utf-8"))
    engineer = json.loads((ROOT / "content" / "cdp-engineer.json").read_text(encoding="utf-8"))
    values = {
        "f001": "C O N T A C T", "f002": "field-005", "f003": "field-006",
        "f004": "field-007", "f005": "field-004", "f006": "E D U C A T I O N",
        "f007": "MASTER’S IN COMPUTER", "f008": "MANAGEMENT (PUNE UNIVERSITY)",
        "f009": "Master", "f010": "2012", "f011": "PGDM IN MARKETING",
        "f012": "Sinhgad Institute of Management", "f013": "2012",
        "f014": "PRABIR", "f015": "BERA", "f016": "CUSTOMER DATA", "f017": "& MARTECH",
        "f018": "ASSOCIATE PRODUCT OWNER — TWILIO SEGMENT CDP",
        "f019": "**SPRINGER NATURE | PUNE**", "f020": "field-014",
        "f021": "field-016",
        "f022": [f"field-{n:03}" for n in range(17, 23)],
        "f023": "• **field-070**\n• **field-071**",
        "f024": "**CDP & Data Architecture**",
        "f025": "Twilio Segment, unified customer profiles, Sources & Destinations, identity resolution, audience activation",
        "f026": "**APIs & Integrations**",
        "f027": "Segment Public APIs, REST APIs, JSON, Postman, Zapier, data integrations",
        "f028": "**Data Quality & Governance**",
        "f029": "SQL, BigQuery, Snowflake, data quality, metadata, consent management, web analytics",
        "f030": "**Marketing Platforms**",
        "f031": "Braze, Salesforce Marketing Cloud, Pardot, HubSpot, Adobe Campaign",
        "f032": "**Development & Analytics**",
        "f033": "JavaScript, HTML, CSS, AMPscript, Liquid, Google Tag Manager",
        "f034": "**Product & Collaboration**",
        "f035": "Product ownership, stakeholder collaboration, campaign enablement, cross-functional delivery",
        "f036": "**ACCENTURE — E-COMMERCE CLIENT**", "f037": "December 2020",
        "f038": "April 2024", "f039": "", "f040": "SFMC / Pardot Technical Lead",
        "f041": [f"field-{n:03}" for n in range(26, 31)],
        "f042": [f"field-{n:03}" for n in range(32, 35)],
        "f043": "Capgemini", "f044": "January 2018", "f045": "December 2020",
        "f046": "", "f047": "Campaign Manager (Global)",
        "f048": "field-039", "f049": "field-040\nfield-041",
        "f050": "TÜV Nord", "f051": "September 2017", "f052": "December 2017",
        "f053": "", "f054": "Corporate Communications Specialist",
        "f055": "field-045", "f056": "",
        "f057": "Lloyd’s Register", "f058": "January 2016", "f059": "July 2017",
        "f060": "", "f061": "Marketing Communications Officer",
        "f062": "field-049", "f063": "",
        "f064": "Shavo Technologies Pvt. Ltd.", "f065": "September 2014",
        "f066": "December 2015", "f067": "", "f068": "Marketing Coordinator",
        "f069": "field-053",
        "f070": "Perennial Technologies Pvt. Ltd.", "f071": "August 2013",
        "f072": "August 2014", "f073": "", "f074": "TM Marketing Communication",
        "f075": "field-057",
        "f076": "Twilio Segment", "f077": "Certified Marketer",
        "f078": "Braze", "f079": "Certified Practitioner",
        "f080": "Salesforce Marketing Cloud", "f081": "Email Specialist",
        "f082": "Salesforce", "f083": "Pardot Specialist",
        "f084": "Google", "f085": "Exploring and Preparing Your Data with BigQuery",
        "f086": "Google Ads", "f087": "Search Certification",
        "f088": "Learning Catalyst", "f089": "Integrated Digital Marketing · Pune",
        "f090": "", "f091": "",
        "f092": "Web Development", "f093": "HTML, CSS, JavaScript",
        "f094": "Query & Scripting Languages", "f095": "SQL, AMPscript, Liquid",
        "f096": "CMS Platforms", "f097": "Joomla, WordPress, Tridion",
        "f098": "Marketing Automation Platforms", "f099": "Braze, Pardot, Mailchimp, HubSpot, Adobe Campaign, Salesforce Marketing Cloud",
        "f100": "CRM Platforms", "f101": "Salesforce, HubSpot",
        "f102": "Tools & Workflow", "f103": "Zapier, Jira, Workfront, Postman, Microsoft 365, Power Automate, Power BI, Adobe Creative Suite",
        "f108": "Cloud & Data Platforms", "f109": "Google Cloud Platform, BigQuery, Snowflake",
        "f110": "AI Tools", "f111": "ChatGPT, Codex, Claude AI, Claude Code, Perplexity AI",
        "f104": "Playing tabla | Traveling | Swimming",
        "f105": "Scan for My LinkedIn Profile", "f106": "Scan for My GitHub Portfolio",
        "f107": "References available on request.",
    }

    for group in template["groups"]:
        for field in group["fields"]:
            value = values[field["id"]]
            if isinstance(value, str) and value.startswith("field-"):
                value = engineer[value]
            elif isinstance(value, list):
                value = [engineer[item] for item in value]
            else:
                value = re.sub(r"field-\d{3}", lambda m: engineer[m.group()], value)
            field["value"] = value

    html = render(template)
    DEST.parent.mkdir(exist_ok=True)
    DEST.write_text(html, encoding="utf-8")
    print("Built cdp-engineer-original.html")


if __name__ == "__main__":
    build()

