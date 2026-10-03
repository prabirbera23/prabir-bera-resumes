"""Shared validation and rendering for the private resume editor."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate(data, schema=None):
    if not isinstance(data, dict) or data.get('version') != 1 or data.get('resume') != 'cdp':
        raise ValueError('This file is not a CDP editor document.')
    schema = schema or json.loads((ROOT/'content/cdp.json').read_text(encoding='utf-8'))
    if len(data.get('groups', [])) != len(schema['groups']):
        raise ValueError('The resume sections do not match this template.')
    for group, original in zip(data['groups'], schema['groups']):
        if group.get('title') == 'Technical skills' and isinstance(group.get('fields'), list):
            present={f.get('id') for f in group['fields'] if isinstance(f,dict)}
            for expected in original['fields']:
                if expected['id'] in ('f108','f109','f110','f111') and expected['id'] not in present:
                    group['fields'].append(dict(expected))
        if group.get('title') != original['title'] or len(group.get('fields', [])) != len(original['fields']):
            raise ValueError('The resume fields do not match this template.')
        for field, expected in zip(group['fields'], original['fields']):
            if any(field.get(k) != expected[k] for k in ('id','label','type')):
                raise ValueError('A field definition has changed. Edit its text only.')
            value = field.get('value')
            if field['type'] == 'list':
                if not isinstance(value,list) or len(value)>30:raise ValueError('Use at most 30 bullets per section.')
                values=value
            else: values=[value]
            if any(not isinstance(v,str) or len(v)>6000 for v in values):
                raise ValueError('A text field is too long (maximum 6,000 characters).')
    if len(json.dumps(data).encode())>200000:raise ValueError('This resume is too large.')
    return data

def rich(value):
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',html.escape(value)).replace('\n','<br>')

def render(data):
    validate(data)
    source=(ROOT/'templates/cdp-editor.html').read_text(encoding='utf-8')
    for group in data['groups']:
        for field in group['fields']:
            pattern=r'(<(?P<tag>[\w]+)\b[^>]*\bdata-editor-id="'+field['id']+r'"[^>]*>).*?(</(?P=tag)>)'
            def replace(m):
                value=field['value']
                if field['type']=='list':body=''.join('<li>'+rich(v)+'</li>' for v in value)
                elif m['tag']=='ul':body=''.join('<li>'+rich(re.sub(r'^\s*(?:[•-]|\*(?!\*))\s+','',v))+'</li>' for v in value.splitlines() if v.strip())
                elif m['tag']=='text':body=html.escape(value.replace('**',''))
                else:body=rich(value)
                return m[1]+body+m[3]
            source,count=re.subn(pattern,replace,source,count=1,flags=re.S)
            if count!=1:raise ValueError('Template field missing: '+field['id'])
    script='''<script>function refreshResume(){const d=new Date();document.getElementById('resume-updated-date').textContent='Resume Updated on: '+d.toLocaleString('en-US',{month:'long'})+', '+d.getFullYear();document.querySelectorAll('text[data-max-width]').forEach(t=>{const w=t.getComputedTextLength(),m=+t.dataset.maxWidth;if(w>m)t.setAttribute('font-size',+t.getAttribute('font-size')*m/w);});}document.fonts.ready.then(refreshResume);window.addEventListener('beforeprint',refreshResume);</script>'''
    return source.replace('</body>',script+'</body>')

