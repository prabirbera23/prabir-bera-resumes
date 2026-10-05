"""Update Original Marketing Automation supporting details from shared CDP data."""
import re
from editor_model import render,rich

def add_shared_original_sections(source,data):
    cdp=render(data)
    fields={f['id']:f for g in data['groups'] for f in g['fields']}
    def field(fid,tag='span'):
        return '<'+tag+' data-editor-id="'+fid+'">'+rich(fields[fid]['value'])+'</'+tag+'>'
    def table(start,end):
        return '<table>'+''.join('<tr>'+field(f'f{i:03}','th')+field(f'f{i+1:03}','td')+'</tr>' for i in range(start,end,2))+'</table>'
    pages=list(re.finditer(r'<section class="page">(.*?)</section>',source,re.S))
    if len(pages)!=3:raise ValueError('Expected three original resume pages')
    first=pages[0][1]
    first=re.sub(r'<image class="uploaded-badge"[^>]*>\s*</image>','',first)
    badges=''.join(re.findall(r'<image class="uploaded-badge"[^>]*>\s*</image>',cdp))
    first=first.replace('</svg>',badges+'</svg>',1)
    def remove_education(m):
        t=m[0];x=re.search(r'\bx="([\d.]+)"',t);y=re.search(r'\by="([\d.]+)"',t)
        return '' if x and y and float(x[1])<200 and 500<float(y[1])<690 else t
    first=re.sub(r'<text\b[^>]*>.*?</text>',remove_education,first,flags=re.S)
    education=''.join(re.search(r'<text\b[^>]*data-editor-id="'+f'f{i:03}'+r'"[^>]*>.*?</text>',cdp,re.S)[0] for i in range(6,14))
    diploma=re.search(r'<text x="44.16" y="646.10"[^>]*>Diploma</text>',cdp)[0]
    first=first.replace('</svg>',education+diploma+'</svg>',1)
    first=re.sub(r'(<image\b[^>]*aria-label="Education"[^>]*y=")([\d.]+)(")',lambda m:m[1]+str(float(m[2])-16)+m[3],first)
    third=pages[2][1]
    opening=re.match(r'<svg\b[^>]*>',third)[0]
    # Preserve the original page-three experience table; replace only content below it.
    elements=re.findall(r'<foreignObject\b[^>]*>.*?</foreignObject>|<path\b[^>]*>.*?</path>|<text\b[^>]*>.*?</text>|<image\b[^>]*>.*?</image>|<rect\b[^>]*>.*?</rect>|<line\b[^>]*/?>',third,re.S)
    kept=[]
    for tag in elements:
        y=re.search(r'\by="([\d.]+)"',tag)
        if y and float(y[1])>=215:continue
        d=re.search(r'\bd="([^"]+)"',tag)
        if d:
            coords=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',d[1])]
            if coords and min(coords[1::2])>=215:continue
        kept.append(tag)
    support='<foreignObject x="32.4" y="215" width="535.6" height="375"><div xmlns="http://www.w3.org/1999/xhtml" class="ma-original-support"><style>.ma-original-support{font:9.3px/1.25 Arial,Helvetica,sans-serif;color:#172b3a}.ma-original-support h2{font-size:13px;color:#176b76;margin:0 0 7px}.ma-original-support table{width:100%;border-collapse:collapse;margin:0 0 10px}.ma-original-support th,.ma-original-support td{border:1px solid #71818a;padding:2.5px 5px;text-align:left;vertical-align:top}.ma-original-support th{width:34%;font-weight:700}.ma-original-support .training th{width:52%}.ma-original-support p{margin:0}.ma-original-support .interests{margin-top:10px}</style><h2>PROFESSIONAL TRAINING / DEVELOPMENT</h2><div class="training">'+table(76,92)+'</div><h2>TECHNICAL SKILLS</h2>'+table(92,104)+table(108,112)+'<h2 class="interests">INTERESTS</h2>'+field('f104','p')+'</div></foreignObject>'
    footer=re.search(r'<svg\b[^>]*class="cdp-bottom-footer"[^>]*>.*?</svg>',cdp,re.S)[0]
    support=support.replace('height="375"','height="445"',1)
    footer=re.sub(r'<svg\b[^>]*>', '<svg class="ma-original-footer" x="23" y="628" width="548" height="164" viewBox="0 0 548 164" xmlns="http://www.w3.org/2000/svg">',footer,count=1)
    third=opening+''.join(kept)+support+footer+'</svg>'
    # Replace in reverse order so source offsets stay valid.
    source=source[:pages[2].start(1)]+third+source[pages[2].end(1):]
    source=source[:pages[0].start(1)]+first+source[pages[0].end(1):]
    return source

