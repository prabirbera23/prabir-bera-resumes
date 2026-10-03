"""Clean CDP layout, generated from the same content as the original CDP resume."""
from pathlib import Path
import re
from editor_model import rich
from resume_naming import apply_resume_naming

ROOT=Path(__file__).resolve().parents[1]

def render_clean_cdp(data):
    fields={f['id']:f for g in data['groups'] for f in g['fields']}
    def field(fid,tag='span',attrs=''):
        value=fields[fid]['value']
        body=rich(value) if isinstance(value,str) else ''.join('<li>'+rich(v)+'</li>' for v in value)
        return f'<{tag} data-editor-id="{fid}" {attrs}>{body}</{tag}>'
    def bullets(fid):
        value=fields[fid]['value']
        if isinstance(value,list): return field(fid,'ul')
        lines=[re.sub(r'^\s*[•▪-]\s*','',v) for v in value.splitlines() if v.strip()]
        if len(lines)>1 or value.startswith('•'):
            return f'<ul data-editor-id="{fid}">'+''.join('<li>'+rich(v)+'</li>' for v in lines)+'</ul>'
        return field(fid,'p')
    def job(start,end):
        ids=[f'f{i:03}' for i in range(start,end+1)]
        text='<article class="job"><div class="job-heading">'+field(ids[4],'h3')+'</div>'+field(ids[0],'p','class="company"')
        text+='<p class="dates">'+field(ids[1])+' – '+field(ids[2])+' · '+field(ids[3])+'</p><div class="responsibilities">'+bullets(ids[5])+'</div>'
        if len(ids)>6:text+='<p class="label">Achievements</p>'+bullets(ids[6])
        return text+'</article>'
    def table(start,end,cls=''):
        rows=[]
        for i in range(start,end,2):rows.append('<tr>'+field(f'f{i:03}','th')+field(f'f{i+1:03}','td')+'</tr>')
        return f'<table class="details {cls}">'+''.join(rows)+'</table>'
    source=(ROOT/'templates/cdp-editor.html').read_text(encoding='utf-8')
    images=re.findall(r'<image\b[^>]*>',source)
    def image_tag(tag,cls):
        url=re.search(r'(?:href|xlink:href)="([^"]+)"',tag)[1]
        return f'<img class="{cls}" src="{url}" alt="">'
    badges=''.join(image_tag(t,'badge') for t in images if 'uploaded-badge' in t)
    footer_source=source[source.index('class="cdp-bottom-footer"'):]
    qrs=re.findall(r'<image\b[^>]*>',footer_source)[:2]
    css=(ROOT/'templates/clean.html').read_text(encoding='utf-8')
    css=re.search(r'<style>(.*?)</style>',css,re.S)[1]
    css+='''
    .page{font-size:12px;line-height:1.38;padding:13mm 17mm;display:flex;flex-direction:column}
    header{padding-bottom:10px}.contact-title{font-size:9px;color:var(--muted);margin:5px 0}
    .badge-row{display:flex;gap:8px;margin-top:9px}.badge{height:34px;width:auto}
    h2{margin:14px 0 7px}.dates{margin:1px 0 6px}.skills-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 20px}
    .skills-grid h3{font-size:12px;color:var(--accent)}.skills-grid p{font-size:11.5px;margin:3px 0}
    .job{margin-bottom:12px}.job h3{font-size:13px}.company{margin:2px 0}.label{margin:7px 0 2px}
    li{margin:3px 0}.details{width:100%;border-collapse:collapse;font-size:11.5px}.details th,.details td{padding:4px 7px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.details th{width:36%;font-weight:bold}.education-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.education-grid p{margin:2px 0;font-size:11.5px}
    .resume-footer{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:auto;padding-top:16px}.reference{background:#edf3f5;padding:9px 12px;margin-bottom:10px}.profiles{display:flex;gap:22px;text-align:center;font-size:10px}.profile img{width:62px;height:62px;display:block;margin:0 auto 5px}.profile a{display:block;color:var(--accent);text-decoration:underline;margin-top:3px}.updated{font-weight:bold;font-size:10px}
    .page-number{margin-top:10px}@media print{.page{font-size:12px;padding:13mm 17mm}h2{margin-top:14px}.resume-footer{break-inside:avoid}.details tr{break-inside:avoid}}@media(max-width:600px){.skills-grid,.education-grid{grid-template-columns:1fr}.resume-footer{flex-direction:column;align-items:flex-start}.profiles{gap:20px}.dates{white-space:normal}.details{font-size:11px}.page{padding:22px}.contact{overflow-wrap:anywhere}}
    '''
    css+=' .page:last-child .details th,.page:last-child .details td{padding:2px 7px}.training th{width:52%}.page:last-child h2{margin-top:10px}.page>article,.page>table,.page>div,.page>footer,.page>header{flex-shrink:0}'
    header='<header><h1>'+field('f014')+' '+field('f015')+'</h1><p class="headline">'+field('f016')+' '+field('f017')+'</p>'+field('f001','p','class="contact-title"')+'<div class="contact">'+field('f005')+'<a href="mailto:'+fields['f002']['value']+'">'+field('f002')+'</a><a href="tel:'+re.sub(r'[^+\d]','',fields['f003']['value'])+'">'+field('f003')+'</a><a href="https://'+fields['f004']['value']+'">'+field('f004')+'</a></div><div class="badge-row">'+badges+'</div></header>'
    current='<h2>Professional Experience</h2><article class="job">'+field('f018','h3')+field('f019','p','class="company"')+field('f020','p','class="dates"')+field('f021','p')+bullets('f022')+'</article><h2>ACHIEVEMENTS</h2>'+bullets('f023')
    skills='<h2>Core Skills</h2><div class="skills-grid">'+''.join('<section>'+field(f'f{i:03}','h3')+field(f'f{i+1:03}','p')+'</section>' for i in range(24,35,2))+'</div>'
    education=field('f006','h2')+'<div class="education-grid"><div>'+field('f007','p')+field('f008','p','class="label"')+field('f009','p')+field('f010','p')+'</div><div>'+field('f011','p','class="label"')+field('f012','p')+'<p>Diploma</p>'+field('f013','p')+'</div></div>'
    technical=table(92,104)+table(108,112)
    profiles='<div class="profiles">'+''.join('<div class="profile">'+image_tag(qrs[i],'profile-qr')+field(fid)+'<a href="'+url+'">Or click here</a></div>' for i,(fid,url) in enumerate([('f105','https://linkedin.com/in/prabirbera'),('f106','https://github.com/prabirbera23')]))+'</div>'
    footer='<footer class="resume-footer"><div>'+field('f107','p','class="reference"')+'<p class="updated" id="resume-updated-date"></p></div>'+profiles+'</footer>'
    pages=[header+current+skills,'<h2>Professional Experience — Continued</h2>'+job(36,42)+job(43,49)+job(50,56)+job(57,63),job(64,69)+job(70,75)+'<h2>Professional Training / Development</h2>'+table(76,92,'training')+'<h2>Technical Skills</h2>'+technical+education+'<h2>Interests</h2>'+field('f104','p')+footer]
    html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prabir Bera | CDP Clean Resume</title><style>'+css+'</style></head><body><div class="toolbar"><span>Prabir Bera · CDP clean resume · 3 pages</span><button onclick="window.print()">Print / Save as PDF</button></div><main>'+''.join('<section class="page">'+body+f'<div class="page-number">{i+1} / 3</div></section>' for i,body in enumerate(pages))+'</main><script>function updateResumeDate(){const date=new Date();document.getElementById("resume-updated-date").textContent="Resume Updated on: "+date.toLocaleString("en-US",{month:"long"})+", "+date.getFullYear();}updateResumeDate();window.addEventListener("beforeprint",updateResumeDate);</script></body></html>'
    return apply_resume_naming(html)

