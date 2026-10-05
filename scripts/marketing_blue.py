"""Keep Blue experience and reuse shared badges and supporting resume sections."""
import re
from cdp_clean import render_clean_cdp

def add_shared_blue_sections(source,data):
    cdp=render_clean_cdp(data)
    badges=re.search(r'<div class="badge-row">.*?</div>',cdp,re.S)[0]
    source=source.replace('</header>','</header>'+badges,1)
    start=cdp.index('<h2>Professional Training / Development</h2>')
    end=cdp.index('<div class="page-number">3 / 3</div>',start)
    supporting=cdp[start:end]
    split=supporting.index('<h2>Technical Skills</h2>')
    training,supporting=supporting[:split],supporting[split:]
    pages=list(re.finditer(r'<section class="page">(.*?)</section>',source,re.S))
    if len(pages)!=2:raise ValueError('Expected two Blue resume pages')
    second=pages[1][1]
    second,count=re.subn(r'<aside>.*?</aside>','<aside class="shared-training">'+training+'</aside>',second,count=1,flags=re.S)
    if count!=1:raise ValueError('Blue supporting sidebar missing')
    source=source[:pages[1].start(1)]+second+source[pages[1].end(1):]
    source=source.replace('1 / 2','1 / 3').replace('2 / 2','2 / 3')
    source=source.replace('</main>','<section class="page shared-support"><div class="continuation">PRABIR BERA · Marketing Automation</div>'+supporting+'<div class="footer">Prabir Bera · 3 / 3</div></section></main>',1)
    css='''
    :root{--accent:#3482ff;--line:#d6e6fc;--muted:#687078}
    .badge-row{display:flex;gap:10px;margin:-8px 0 22px;align-items:center}.badge{height:38px;width:auto}
    .shared-support{display:flex;flex-direction:column}.shared-support h2,.shared-training h2{color:#3482ff;font-weight:600;font-size:11px;margin:0 0 9px}
    .details{width:100%;border-collapse:collapse;font-size:11px;margin-bottom:12px}.details th,.details td{padding:5px 7px;border-bottom:1px solid #d6e6fc;text-align:left;vertical-align:top}.details th{width:34%;font-weight:600}.shared-training .details{font-size:10.7px}.shared-training .details th{width:58%;padding-left:0}.shared-training .details td{padding-right:0}.shared-support .details+.details{margin-top:-12px}
    .education-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:18px}.education-grid p{margin:2px 0;font-size:11.5px}.education-grid .label{font-weight:600}.shared-support>p{margin:0}
    .resume-footer{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:auto;padding-top:24px}.reference{background:#edf4ff;border-radius:4px;padding:10px 12px;margin:0 0 10px}.profiles{display:flex;gap:22px;text-align:center;font-size:10px}.profile img{width:62px;height:62px;display:block;margin:0 auto 5px}.profile a{display:block;color:#3482ff;text-decoration:underline;margin-top:4px}.updated{font-weight:600;font-size:10px}.shared-support>h2:not(:first-child){margin-top:12px}.shared-support>footer+h2{margin-top:0}
    @media print{.details tr,.resume-footer,.education-grid{break-inside:avoid}.shared-support{height:297mm}.shared-support>*{flex-shrink:0}}
    @media(max-width:600px){.education-grid{grid-template-columns:1fr}.resume-footer{flex-direction:column;align-items:flex-start;margin-top:30px}.profiles{gap:20px}.profile{max-width:145px}.details{font-size:10.7px}}
    '''
    source=source.replace('</style>',css+'</style>',1)
    update=re.search(r'<script>function updateResumeDate\(\).*?</script>',cdp,re.S)[0]
    source=source.replace('</body>',update+'</body>',1)
    source=re.sub(r'(<div class="toolbar">\s*<span>).*?(</span>)',r'\1Prabir Bera · Blue design · 3 pages\2',source,count=1,flags=re.S)
    return source

