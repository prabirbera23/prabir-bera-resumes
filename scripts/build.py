"""Build three resume designs from Markdown. Requires only Python 3."""
from pathlib import Path
import html, re, json
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'site'
GLYPH_WIDTHS={'Century Gothic|400|M': 0.9192, 'Century Gothic|400|A': 0.7399, 'Century Gothic|400|R': 0.6072, 'Century Gothic|400|T': 0.4267, 'Century Gothic|400|E': 0.5371, 'Century Gothic|400|C': 0.8131, 'Century Gothic|400|H': 0.6836, 'Century Gothic|400|S': 0.4989, 'Century Gothic|400|O': 0.8695, 'Century Gothic|400|I': 0.2261, 'Century Gothic|400|N': 0.7403, 'Century Gothic|400|G': 0.8725, 'Century Gothic|700|S': 0.5203, 'Century Gothic|700|P': 0.5605, 'Century Gothic|700|R': 0.5806, 'Century Gothic|700|I': 0.2799, 'Century Gothic|700|N': 0.7402, 'Century Gothic|700|G': 0.8407, 'Century Gothic|700|E': 0.5205, 'Century Gothic|700|A': 0.7399, 'Century Gothic|700|T': 0.4199, 'Century Gothic|700|U': 0.6411, 'Century Gothic|700|-': 0.4206, 'Century Gothic|700|(': 0.3804, 'Century Gothic|700|p': 0.6602, 'Century Gothic|700|r': 0.3207, 'Century Gothic|700|.': 0.2802, 'Century Gothic|700|2': 0.5605, 'Century Gothic|700|0': 0.5605, 'Century Gothic|700|4': 0.5612, 'Century Gothic|700|t': 0.3004, 'Century Gothic|700|o': 0.6411, 'Century Gothic|700|e': 0.6411, 'Century Gothic|700|s': 0.4405, 'Century Gothic|700|n': 0.6008, 'Century Gothic|700|)': 0.3804, 'Century Gothic|700|B': 0.5806, 'Symbol|400|•': 0.3503, 'Century Gothic|400|B': 0.5743, 'Century Gothic|400|u': 0.6082, 'Century Gothic|400|i': 0.2006, 'Century Gothic|400|l': 0.2006, 'Century Gothic|400|d': 0.6857, 'Century Gothic|400|,': 0.277, 'Century Gothic|400|a': 0.6836, 'Century Gothic|400|n': 0.6104, 'Century Gothic|400|c': 0.6475, 'Century Gothic|400|h': 0.6104, 'Century Gothic|400|m': 0.9383, 'Century Gothic|400|g': 0.673, 'Century Gothic|400|e': 0.6507, 'Century Gothic|400|p': 0.6825, 'Century Gothic|400|s': 0.3885, 'Century Gothic|400|t': 0.3397, 'Century Gothic|400|o': 0.6549, 'Century Gothic|400|r': 0.3015, 'Century Gothic|400|j': 0.2038, 'Century Gothic|400|y': 0.5371, 'Century Gothic|700|a': 0.6602, 'Century Gothic|700|z': 0.4607, 'Century Gothic|700|H': 0.6807, 'Century Gothic|700|u': 0.6008, 'Century Gothic|700|b': 0.6602, 'Century Gothic|400|k': 0.5021, 'Century Gothic|400|b': 0.6825, 'Century Gothic|400|f': 0.3142, 'Century Gothic|400|z': 0.4257, 'Century Gothic|400|.': 0.277, 'Century Gothic|400|P': 0.5923, 'Century Gothic|400|-': 0.3322, 'Century Gothic|400|K': 0.5912, 'Century Gothic|400|L': 0.4628, 'Century Gothic|400|Y': 0.5923, 'Century Gothic|400|w': 0.8311, 'Century Gothic|400|v': 0.5552, 'Century Gothic|400|q': 0.6825, 'Century Gothic|400|2': 0.5552, 'Century Gothic|700|Z': 0.5, 'Century Gothic|700|i': 0.2405, 'Century Gothic|700|g': 0.6602, 'Century Gothic|700|m': 0.9405, 'Century Gothic|700|l': 0.2405, 'Century Gothic|700|c': 0.6413, 'Century Gothic|700|w': 0.8004, 'Century Gothic|700|C': 0.7802, 'Century Gothic|700|D': 0.7006, 'Century Gothic|400|3': 0.5547, 'Century Gothic|400|@': 0.8672, 'Century Gothic|400|+': 0.6064, 'Century Gothic|400|9': 0.5547, 'Century Gothic|400|1': 0.5547, 'Century Gothic|400|7': 0.5553, 'Century Gothic|400|5': 0.5553, 'Century Gothic|400|8': 0.5552, 'Century Gothic|400|F': 0.4851, 'Century Gothic|400|/': 0.4374, 'Century Gothic|400|D': 0.7452, 'Century Gothic|700|F': 0.4809, 'Century Gothic|700|M': 0.9001, 'Century Gothic|700|d': 0.6602, 'Century Gothic|700|,': 0.28, 'Century Gothic|400|x': 0.4809, 'Century Gothic|700|J': 0.48, 'Century Gothic|700|y': 0.5801, 'Century Gothic|700|Q': 0.8407, 'Century Gothic|700|L': 0.4402, 'Century Gothic|400|(': 0.3694, 'Century Gothic|400|J': 0.483, 'Century Gothic|400|)': 0.3694, 'Century Gothic|700|h': 0.6008, 'Century Gothic|700|k': 0.5801, 'Century Gothic|400|U': 0.6552, 'Century Gothic|700|’': 0.2808, 'Century Gothic|700|O': 0.8398, 'Century Gothic|700|V': 0.7006, 'Century Gothic|700|Y': 0.621, 'Century Gothic|400|0': 0.5552, 'Wingdings|400|▪': 0.3545, 'Century Gothic|400|"': 0.3099, 'Century Gothic|700|f': 0.2799, 'Century Gothic|700|x': 0.5605, 'Century Gothic|700|K': 0.6201, 'Century Gothic|400|“': 0.5021, 'Century Gothic|400|”': 0.484, 'Century Gothic|700|v': 0.5605, "Century Gothic|400|'": 0.1979, 'Century Gothic|700|:': 0.2802, 'Century Gothic|400|’': 0.3514, 'Century Gothic|700|X': 0.6804, 'Century Gothic|400|4': 0.5547, "Century Gothic|700|'": 0.2208, 'Century Gothic|400|6': 0.5553, 'Century Gothic|700|±': 0.5498, 'Century Gothic|700|%': 0.8609, 'Century Gothic|700|j': 0.2601, 'Century Gothic|700|5': 0.5605, 'Century Gothic|400|V': 0.7023, 'Century Gothic|400|:': 0.2772, 'Century Gothic|700|W': 0.9001, 'Century Gothic|400|W': 0.9606, 'Century Gothic|400|Q': 0.8715, 'Century Gothic|400|&': 0.7568, 'Century Gothic|400||': 0.6719, 'Times New Roman|700|F': 0.6114, 'Times New Roman|700|e': 0.4448, 'Times New Roman|700|b': 0.5562, 'Times New Roman|700|r': 0.4448, 'Times New Roman|700|u': 0.5562, 'Times New Roman|700|a': 0.501, 'Times New Roman|700|y': 0.501, 'Times New Roman|400|6': 0.501}

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

def flow_tables(source, fields, values):
    """Render the PDF table geometry with HTML cells and natural word spacing."""
    pages=source.split('<section class="page">')
    for page_number in range(2,len(pages)):
        page=pages[page_number]
        vertical=[]
        for path in re.findall(r'<path\b[^>]*>',page):
            data=re.search(r'd="([^"]+)"',path)
            if not data:continue
            nums=[float(n) for n in re.findall(r'-?\d+\.\d+',data.group(1))]
            if len(nums)<8:continue
            xs=nums[::2];ys=nums[1::2]
            if max(xs)-min(xs)<1 and max(ys)-min(ys)>3:
                vertical.append((min(xs),min(ys),max(ys)))
        raw=sorted({v for _,a,b in vertical for v in [a,b]})
        bounds=[]
        for y in raw:
            if not bounds or y-bounds[-1]>.8:bounds.append(y)
        cells=[]
        for top,bottom in zip(bounds,bounds[1:]):
            middle=(top+bottom)/2
            xs=[]
            for x in sorted({x for x,a,b in vertical if a<=middle<=b}):
                if not xs or x-xs[-1]>.8:xs.append(x)
            for left,right in zip(xs,xs[1:]):
                if right-left>8:cells.append({'left':left,'top':top,'right':right,'bottom':bottom,'tokens':[]})
        outside=[]
        for key,field in fields.items():
            if not key.startswith(f'page-{page_number}-'):continue
            text=values[key]; cursor=0; glyphs=field['glyphs'];tokens=[]
            if text==field['text']:
                for g in glyphs:
                    pos=text.find(g[1],cursor)
                    if pos<0:continue
                    attrs={**field['attrs'],**(g[2] if len(g)>2 else {})}
                    tokens.append((g[0],float(attrs['y']),text[cursor:pos]+g[1],attrs))
                    cursor=pos+1
                if tokens and cursor<len(text):
                    x,y,t,a=tokens[-1];tokens[-1]=(x,y,t+text[cursor:],a)
            else:
                attrs=field['attrs'].copy()
                tokens=[(float(attrs['x']),float(attrs['y']),text,attrs)]
            for token in tokens:
                x,y,_,_=token
                cell=next((c for c in cells if c['left']<=x<c['right'] and c['top']<y<=c['bottom']+.5),None)
                if cell:cell['tokens'].append(token)
                else:outside.append(token)
        page=re.sub(r'<text\b[^>]*>.*?</text>','',page,flags=re.S)
        rendered=[]
        for cell in cells:
            tokens=sorted(cell['tokens'],key=lambda t:(round(t[1],2),t[0]))
            if not tokens:continue
            spaced=[];previous=None
            for x,y,t,a in tokens:
                if previous and abs(y-previous[1])<.5 and not t.startswith(' '):
                    px,py,pt,pa=previous
                    lookup=pa['font-family']+'|'+pa['font-weight']+'|'+pt[-1]
                    end=px+float(pa['font-size'])*GLYPH_WIDTHS.get(lookup,.55)
                    if x-end>1.3:t=' '+t
                spaced.append((x,y,t,a));previous=(x,y,t,a)
            tokens=spaced
            chunks=[];last_y=None;last_weight=None;run=''
            for x,y,t,a in tokens:
                weight=a.get('font-weight','400')
                if last_y is not None and abs(y-last_y)>.5:t=' '+t.lstrip()
                if weight!=last_weight and run:
                    chunks.append('<strong>'+html.escape(run)+'</strong>' if last_weight=='700' else html.escape(run));run=''
                run+=t;last_weight=weight;last_y=y
            if run:chunks.append('<strong>'+html.escape(run)+'</strong>' if last_weight=='700' else html.escape(run))
            width=cell['right']-cell['left'];height=cell['bottom']-cell['top']
            align='center' if ''.join(t[2] for t in tokens).strip() in ['COURSE NAME','PLACE'] else 'left'
            size=min(10.0,float(tokens[0][3]['font-size']))
            rendered.append(f'<foreignObject x="{cell["left"]}" y="{cell["top"]}" width="{width}" height="{height}"><div xmlns="http://www.w3.org/1999/xhtml" class="flow-cell" role="cell" style="box-sizing:border-box;width:100%;height:100%;padding:2px 5px;font-family:Arial,Helvetica,sans-serif;font-size:{size}px;line-height:1.28;color:#172b3a;text-align:{align};overflow-wrap:break-word;">'+''.join(chunks).strip()+'</div></foreignObject>')
        # Merge heading/footer fragments so no line retains per-letter positioning.
        rows={}
        for token in outside:rows.setdefault(round(token[1],2),[]).append(token)
        for y,tokens in sorted(rows.items()):
            tokens.sort(key=lambda t:t[0]);text=''.join(t[2] for t in tokens)
            attrs=tokens[0][3].copy();attrs['x']=str(tokens[0][0]);attrs['y']=str(y)
            synthetic={'attrs':attrs,'text':text,'glyphs':[]}
            rendered.append(original_typography(synthetic,text))
        page=page.replace('</svg>',''.join(rendered)+'</svg>',1)
        pages[page_number]=page
    return '<section class="page">'.join(pages)

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
            source=flow_tables(source,fields,values)
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
