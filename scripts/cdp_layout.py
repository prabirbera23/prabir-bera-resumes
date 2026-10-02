import re

def compact_cdp(source):
    pages=source.split('<section class="page">')
    def tables(page):
        rows={}
        for m in re.finditer(r'<foreignObject x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)">(.*?)</foreignObject>',page,re.S):
            if 'class="flow-cell"' not in m[5]:continue
            content=re.search(r'class="flow-cell"[^>]*>(.*?)</div>',m[5],re.S)[1]
            rows.setdefault(float(m[2]),[]).append((float(m[1]),float(m[3]),float(m[4]),content))
        groups=[];last_end=None
        for y,cells in sorted(rows.items()):
            if last_end is None or y-last_end>5:groups.append([])
            groups[-1].append((y,sorted(cells)));last_end=y+max(c[2] for c in cells)
        result=[]
        for group in groups:
            output='<div class="compact-table">'
            for y,cells in group:
                width=sum(c[1] for c in cells)
                company=any('Company Name:' in c[3] for c in cells)
                output+='<div class="compact-row'+(' company-row' if company else '')+'">'
                for x,w,h,content in cells:output+=f'<div class="compact-cell" style="width:{100*w/width}%">{content}</div>'
                output+='</div>'
            result.append(output+'</div>')
        return result
    older=tables(pages[3]);last=tables(pages[4])
    acc=re.search(r'<table class="accenture-table">.*?</table>',pages[2],re.S)[0]
    style='''<style>.cdp-flow{padding:25px 32px;box-sizing:border-box;font:9px/1.25 Arial,Helvetica,sans-serif;color:#172b3a}.cdp-flow h2{font-size:13px;color:#176b76;margin:0 0 12px}.cdp-flow h3{font-size:12px;color:#176b76;margin:12px 0 6px}.compact-table{margin-bottom:12px;border-top:.5px solid #555;border-left:.5px solid #555}.compact-row{display:flex}.compact-cell{box-sizing:border-box;border-right:.5px solid #555;border-bottom:.5px solid #555;padding:3px 4px;overflow-wrap:break-word}.company-row{background:#edf3f5}.cdp-flow .accenture-table{width:100%;border-collapse:collapse;table-layout:fixed;font:inherit;margin-bottom:12px}.cdp-flow .accenture-table th,.cdp-flow .accenture-table td{border:.5px solid #555;padding:3px 4px;text-align:left;vertical-align:top}.cdp-flow ul{margin:0;padding-left:12px}.cdp-flow li{margin-bottom:3px}</style>'''
    def page(content):return '<section class="page"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 612 792" width="100%" height="100%"><foreignObject width="612" height="792"><div xmlns="http://www.w3.org/1999/xhtml" class="cdp-flow">'+style+content+'</div></foreignObject></svg></section>'
    second=page('<style>.cdp-flow.page-two{font-size:8.8px;line-height:1.25}.page-two .compact-cell{padding:2.5px 4px}.page-two .compact-table{margin-bottom:12px}.page-two .accenture-table th,.page-two .accenture-table td{padding:3px 4px}.page-two li{margin-bottom:3px}</style><h2>PROFESSIONAL EXPERIENCE — CONTINUED</h2>'+acc+''.join(older[:3])).replace('class="cdp-flow"','class="cdp-flow page-two"')
    footer=re.search(r'<svg\b[^>]*>(.*?)</svg>',pages[4],re.S)[1]
    footer=re.sub(r'<foreignObject\b.*?</foreignObject>','',footer,flags=re.S)
    footer=re.sub(r'<text\b[^>]*>Play Tabla.*?</text>','',footer,flags=re.S)
    footer=re.sub(r'<text\b[^>]*y="(?:615[^"]*|62[0-9][^"]*)"[^>]*>.*?</text>', '', footer, flags=re.S)
    footer='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 610 612 182" class="cdp-bottom-footer" style="position:absolute;left:32px;bottom:20px;width:548px;height:164px">'+footer+'</svg>'
    third=page('<style>.cdp-flow.page-three{position:relative;height:792px;font-size:8.5px;line-height:1.2}.compact-cell{padding:2px 4px}.compact-table{margin-bottom:9px}.cdp-flow h3{margin:9px 0 5px}</style>'+older[3]+last[0]+'<h3>PROFESSIONAL TRAINING / DEVELOPMENT</h3>'+last[1]+'<h3>TECHNICAL SKILLS</h3>'+last[2]+'<p>Play Tabla | Traveling | Swimming</p>'+footer).replace('class="cdp-flow"','class="cdp-flow page-three"')
    return pages[0]+'<section class="page">'+pages[1]+second+third+source[source.rfind('</section>')+10:]

