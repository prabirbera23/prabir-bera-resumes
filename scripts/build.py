"""Build three resume designs from Markdown. Requires only Python 3."""
from pathlib import Path
import html, re, json
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'site'

def inline(text):
    text=html.escape(text)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text).replace('\n','<br>')

def original_typography(field, text):
    """Reflow each printed line in readable fonts, retaining its position."""
    attrs=field['attrs'].copy()
    x=float(attrs['x']); y=float(attrs['y']); size=float(attrs['font-size'])
    if attrs.get('font-family')=='Wingdings':
        return ''.join('<text '+ ' '.join(f'{k}="{html.escape(v,quote=True)}"' for k,v in {**attrs,'x':str(g[0]),**(g[2] if len(g)>2 else {})}.items())+'>'+html.escape(g[1])+'</text>' for g in field['glyphs'])
    sidebar=field.get('sidebar',False)
    if sidebar and text=='c':return ''
    # These two source lines were clipped in the original sidebar artwork.
    if sidebar and 175<y<210 and text in ['ASSOCIATE','MANAGER']:return ''
    family='Arial, Helvetica, sans-serif'
    if size>=15:
        size*=.92
        attrs['font-weight']='700' if not sidebar or size>25 else '400'
        if sidebar and size>25:text=text.replace(' ','')
    attrs['font-family']=family
    attrs['font-size']=str(size)
    attrs['font-style']='normal'
    attrs['fill']='#176b76' if size>=14 and size<25 else '#172b3a'
    if text=='ACHIEVEMENTS':attrs['fill']='#176b76'
    if sidebar and text in ['MARKETING','TECHNOLOGY']:attrs['fill']='#176b76'
    attrs['data-max-width']=str(max(15,(196 if sidebar else 594)-x))
    bullet=''
    if text.startswith('• '):
        bullet=f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{attrs["fill"]}">•</text>'
        attrs['x']=str(x+18);attrs['data-max-width']=str(594-x-18)
        text=text[2:]
    # Preserve emphasis from the source while switching to natural word spacing.
    glyphs=field.get('glyphs',[])
    bold_chars=[];cursor=0
    if text==field['text'] or field['text'].startswith('• '):
        for g in glyphs:
            if g[1]=='•':continue
            pos=text.find(g[1],cursor)
            if pos<0:continue
            weight=(g[2] if len(g)>2 else {}).get('font-weight',field['attrs'].get('font-weight','400'))
            if weight=='700':bold_chars.append(pos)
            cursor=pos+1
    fragments=[];start=0
    for i in range(len(text)+1):
        if i==len(text) or (i>start and ((i in bold_chars)!=((i-1) in bold_chars))):
            segment=html.escape(text[start:i])
            fragments.append('<tspan font-weight="700">'+segment+'</tspan>' if start in bold_chars else segment)
            start=i
    return bullet+'<text '+ ' '.join(f'{k}="{html.escape(v,quote=True)}"' for k,v in attrs.items())+'>'+''.join(fragments)+'</text>'

def table_typography(field, text):
    """Keep each table glyph in its cell while updating the font face."""
    if text!=field['text']:return original_typography(field,text)
    pieces=[]
    for glyph in field['glyphs']:
        attrs=field['attrs'].copy();attrs['x']=str(glyph[0])
        if len(glyph)>2:attrs.update(glyph[2])
        if attrs.get('font-family') not in ['Wingdings','Symbol']:
            attrs['font-family']='Arial, Helvetica, sans-serif'
        attrs['fill']='#176b76' if float(attrs['font-size'])>=15 or field['text'] in ['TECHNICAL SKILLS:','INTERESTS:'] else '#172b3a'
        pieces.append('<text '+ ' '.join(f'{k}="{html.escape(v,quote=True)}"' for k,v in attrs.items())+'>'+html.escape(glyph[1])+'</text>')
    return ''.join(pieces)

def build():
    DEST.mkdir(exist_ok=True)
    for name in ['clean','blue','original']:
        md=(ROOT/'content'/f'{name}.md').read_text(encoding='utf-8')
        values={}
        pattern=r'^## ([\w-]+)[^\n]*\n(.*?)(?=^## |\Z)'
        for m in re.finditer(pattern,md,re.M|re.S):
            if m.group(1) in values:raise ValueError('Duplicate field '+m.group(1))
            values[m.group(1)]=m.group(2).strip()
        if name=='original':
            fields={}
            for part in sorted((ROOT/'templates'/'original-fields').glob('*.json')):
                fields.update(json.loads(part.read_text(encoding='utf-8')))
        else:
            fields=json.loads((ROOT/'templates'/f'{name}.json').read_text(encoding='utf-8'))
        if set(values)!=set(fields):raise ValueError(f'{name}: missing or unknown field IDs: {set(values)^set(fields)}')
        source=(ROOT/'templates'/f'{name}.html').read_text(encoding='utf-8')
        sidebar_changed=False
        for key,field in fields.items():
            text=values[key]
            if name=='original':replacement=original_typography(field,text) if key.startswith('page-1-') else table_typography(field,text)
            elif text==field['text']:
                if 'glyphs' not in field:replacement=field['original']
                else:
                    pieces=[]
                    for glyph in field['glyphs']:
                        attrs=field['attrs'].copy()
                        attrs['x']=str(glyph[0])
                        if len(glyph)>2:attrs.update(glyph[2])
                        pieces.append('<text '+ ' '.join(f'{k}="{html.escape(v,quote=True)}"' for k,v in attrs.items())+'>'+html.escape(glyph[1])+'</text>')
                    replacement=''.join(pieces)
            elif field['mode']=='html':replacement=inline(text)
            else:
                attrs=field['attrs'].copy()
                replacement='<text '+ ' '.join(f'{k}="{html.escape(v,quote=True)}"' for k,v in attrs.items())+'>'+html.escape(text.replace('\n',' '))+'</text>'
                sidebar_changed |= field.get('sidebar',False)
            source=source.replace('{{'+key+'}}',replacement)
        if sidebar_changed or name=='original':
            source=re.sub(r'<image x="0" y="0" width="210.55" height="792"[^>]*/?>','',source)
        if name=='original':
            source=source.replace('background:#e9edf0','background:#eaf0f3').replace('background:#505050','background:#176b76')
            def palette(m):
                tag=m.group()
                tag=tag.replace('fill="rgb(128,128,128)"','fill="#edf3f5"').replace('fill="rgb(127,127,127)"','fill="#edf3f5"')
                tag=tag.replace('stroke="rgb(191,191,191)"','stroke="#d5e0e4"').replace('stroke="rgb(128,128,128)"','stroke="#d5e0e4"')
                coords=re.search(r'd="[ML] ([\d.]+)',tag)
                if coords and 215<float(coords.group(1))<245:tag=tag.replace('fill="#edf3f5"','fill="#176b76"')
                path_data=re.search(r'd="([^"]+)"',tag)
                if path_data:
                    points=[float(v) for v in re.findall(r'-?\d+\.\d+',path_data.group(1))]
                    if len(points)>=4:
                        xs=points[::2];ys=points[1::2]
                        if max(xs)<210 and max(xs)-min(xs)<30 and max(ys)-min(ys)<35:
                            tag=tag.replace('fill="rgb(255,255,255)"','fill="#176b76"')
                return tag
            source=re.sub(r'<path\b[^>]*>',palette,source)
            source=source.replace('</body>', '<script>function fitResumeText(){document.querySelectorAll("text[data-max-width]").forEach(t=>{const max=+t.dataset.maxWidth;const width=t.getComputedTextLength();if(width>max){t.setAttribute("font-size",(+t.getAttribute("font-size")*max/width).toFixed(3));}});}document.fonts.ready.then(fitResumeText);</script></body>')
        # Keep edited contact text and destinations consistent.
        source=re.sub(r'href="mailto:[^"]*"([^>]*>)([^<]+)</a>',lambda m:'href="mailto:'+html.escape(html.unescape(m.group(2)),quote=True)+'"'+m.group(1)+m.group(2)+'</a>',source)
        source=re.sub(r'href="tel:[^"]*"([^>]*>)([^<]+)</a>',lambda m:'href="tel:'+re.sub(r'[^+\d]','',html.unescape(m.group(2)))+'"'+m.group(1)+m.group(2)+'</a>',source)
        (DEST/f'{name}.html').write_text(source,encoding='utf-8')
        print(f'Built {name}.html ({len(fields)} editable fields)')
    (DEST/'index.html').write_text((ROOT/'templates'/'index.html').read_text(encoding='utf-8'),encoding='utf-8')
    (DEST/'.nojekyll').write_text('',encoding='utf-8')

if __name__=='__main__':build()
