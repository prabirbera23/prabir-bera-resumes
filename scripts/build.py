"""Build three resume designs from Markdown. Requires only Python 3."""
from pathlib import Path
import html, re, json
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'site'

def inline(text):
    text=html.escape(text)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text).replace('\n','<br>')

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
            if text==field['text']:
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
        if sidebar_changed:
            source=re.sub(r'<image x="0" y="0" width="210.55" height="792"[^>]*/?>','',source)
        # Keep edited contact text and destinations consistent.
        source=re.sub(r'href="mailto:[^"]*"([^>]*>)([^<]+)</a>',lambda m:'href="mailto:'+html.escape(html.unescape(m.group(2)),quote=True)+'"'+m.group(1)+m.group(2)+'</a>',source)
        source=re.sub(r'href="tel:[^"]*"([^>]*>)([^<]+)</a>',lambda m:'href="tel:'+re.sub(r'[^+\d]','',html.unescape(m.group(2)))+'"'+m.group(1)+m.group(2)+'</a>',source)
        (DEST/f'{name}.html').write_text(source,encoding='utf-8')
        print(f'Built {name}.html ({len(fields)} editable fields)')
    (DEST/'index.html').write_text((ROOT/'templates'/'index.html').read_text(encoding='utf-8'),encoding='utf-8')
    (DEST/'.nojekyll').write_text('',encoding='utf-8')

if __name__=='__main__':build()
