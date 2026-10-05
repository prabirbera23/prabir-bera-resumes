"""Reuse the CDP clean supporting sections in the Marketing Automation layout."""
import re
from cdp_clean import render_clean_cdp

def add_shared_sections(source, data):
    cdp=render_clean_cdp(data)
    css=re.search(r'<style>(.*?)</style>',cdp,re.S)[1]
    source=source.replace('</style>',css+'</style>',1)
    badges=re.search(r'<div class="badge-row">.*?</div>',cdp,re.S)[0]
    source=source.replace('</header>',badges+'</header>',1)
    start=cdp.index('<h2>Professional Training / Development</h2>')
    end=cdp.index('<div class="page-number">3 / 3</div>',start)
    supporting=cdp[start:end]
    split=supporting.index('<h2>Technical Skills</h2>')
    training=supporting[:split]
    supporting=supporting[split:]
    pattern=r'<h2>Certifications &amp; Professional Development</h2>.*?(?=<div class="page-number">)'
    source,count=re.subn(pattern,'',source,count=1,flags=re.S)
    if count!=1:raise ValueError('Marketing Automation supporting sections missing')
    source=source.replace('1 / 2','1 / 3').replace('2 / 2','2 / 3')
    source=re.sub(r'(<div class="page-number">[^<]*2 / 3</div>)',lambda m:training+m[1],source,count=1)
    source=source.replace('</main>','<section class="page">'+supporting+'<div class="page-number">3 / 3</div></section></main>',1)
    update=re.search(r'<script>function updateResumeDate\(\).*?</script>',cdp,re.S)[0]
    source=source.replace('</body>',update+'</body>',1)
    source=re.sub(r'(<div class="toolbar">\s*<span>).*?(</span>)',r'\1Prabir Bera · Marketing Automation · 3 pages\2',source,count=1,flags=re.S)
    return source

