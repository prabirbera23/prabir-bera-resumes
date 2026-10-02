"""Private loopback-only editor. GitHub credentials stay in process memory."""
import argparse
import hashlib
import http.cookies
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import os
from pathlib import Path
import secrets
import socket
import threading
import urllib.request
import urllib.error
import urllib.parse
import webbrowser
import base64
from editor_model import ROOT, validate, render

REPO='prabirbera23/prabir-bera-resumes'
REMOTE='https://api.github.com/repos/'+REPO+'/contents/content/cdp.json'
DRAFT=ROOT/'content/cdp.draft.json'
MAX_BODY=220000

def github(path, token, method='GET', body=None):
    request=urllib.request.Request(path,data=json.dumps(body).encode() if body is not None else None,method=method,
        headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','User-Agent':'Prabir-Resume-Editor','Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(request,timeout=20) as response:return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code in (401,403):raise ValueError('GitHub could not authorize this connection. Check the token and repository permission.') from None
        if error.code in (409,422):raise ValueError('The published resume changed. Load the latest published version before publishing again.') from None
        raise ValueError('GitHub returned an error. Your local draft is safe.') from None
    except (urllib.error.URLError, TimeoutError):
        raise ValueError('This editor cannot reach GitHub. Close the editor, double-click Start Resume Editor.cmd in File Explorer, and try connecting again. Check your internet connection or firewall if it still fails. Your saved draft is safe.') from None

def canonical(data):return json.dumps(data,sort_keys=True,ensure_ascii=False)

class EditorServer(ThreadingHTTPServer):
    allow_reuse_address=False
    def server_bind(self):
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1)
        super().server_bind()
    def __init__(self, port):
        super().__init__(('127.0.0.1',port),Handler)
        self.origin='http://127.0.0.1:'+str(self.server_port)
        self.bootstrap=secrets.token_urlsafe(32)
        self.session=secrets.token_urlsafe(32)
        self.token=None
        self.lock=threading.Lock()
        self.schema=json.loads((ROOT/'content/cdp.json').read_text(encoding='utf-8'))
    def state(self):
        return {'data':self.schema,'draft':json.loads(DRAFT.read_text(encoding='utf-8')) if DRAFT.exists() else None,'connected':bool(self.token)}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def reply(self,status,data,kind='application/json',cookie=None):
        if kind=='application/json':data=json.dumps(data,ensure_ascii=False)
        raw=data.encode('utf-8') if isinstance(data,str) else data
        self.send_response(status)
        self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; frame-src 'self' blob:; connect-src 'self'; frame-ancestors 'self'")
        if cookie:self.send_header('Set-Cookie',cookie)
        self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def authenticated(self):
        c=http.cookies.SimpleCookie()
        try:c.load(self.headers.get('Cookie',''))
        except http.cookies.CookieError:return False
        return 'resume_session' in c and secrets.compare_digest(c['resume_session'].value,self.server.session)
    def valid_host(self):return self.headers.get('Host')==self.server.origin.split('//')[1]
    def do_GET(self):
        if not self.valid_host():return self.reply(403,{'error':'Invalid editor address.'})
        path=urllib.parse.urlsplit(self.path).path
        if path=='/api/health':return self.reply(200,{'app':'prabir-resume-editor'})
        if path in ('/','/editor.js','/editor.css'):
            name={'/':'index.html'}.get(path,path[1:]);kind={'index.html':'text/html','editor.js':'text/javascript','editor.css':'text/css'}[name]
            return self.reply(200,(ROOT/'editor/public'/name).read_bytes(),kind,cookie='resume_session='+self.server.session+'; HttpOnly; SameSite=Strict; Path=/' if path=='/' else None)
        if not self.authenticated():return self.reply(401,{'error':'Open the editor using Start Resume Editor.'})
        if path=='/api/state':return self.reply(200,self.server.state())
        if path=='/api/published':
            if not self.server.token:return self.reply(401,{'error':'Connect GitHub first.'})
            try:
                result=github(REMOTE,self.server.token);data=json.loads(base64.b64decode(result['content']))
                validate(data,self.server.schema);return self.reply(200,{'data':data,'sha':result['sha']})
            except (ValueError,OSError):return self.reply(400,{'error':'Could not load the published resume. Your draft is safe.'})
        self.reply(404,{'error':'Not found.'})
    def do_POST(self):
        if not self.valid_host() or self.headers.get('Origin')!=self.server.origin:return self.reply(403,{'error':'Open the editor on this computer.'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<1 or length>MAX_BODY:return self.reply(413,{'error':'Request is too large.'})
            body=json.loads(self.rfile.read(length))
            path=urllib.parse.urlsplit(self.path).path
            if path=='/api/session':
                if not secrets.compare_digest(str(body.get('key','')),self.server.bootstrap):return self.reply(403,{'error':'Use Start Resume Editor to open a fresh session.'})
                return self.reply(200,{'ok':True},cookie='resume_session='+self.server.session+'; HttpOnly; SameSite=Strict; Path=/')
            if not self.authenticated():return self.reply(401,{'error':'Open the editor using Start Resume Editor.'})
            if path=='/api/quit':
                self.server.token=None
                self.reply(200,{'ok':True})
                threading.Thread(target=self.server.shutdown,daemon=True).start()
                return
            if path=='/api/connect':
                token=body.get('token','').strip()
                if not token or len(token)>500:raise ValueError('Enter your GitHub connection token.')
                profile=github('https://api.github.com/user',token)
                if profile.get('login','').lower()!='prabirbera23':raise ValueError('Connect the prabirbera23 GitHub account.')
                remote=github(REMOTE,token)
                data=json.loads(base64.b64decode(remote['content']));validate(data,self.server.schema)
                self.server.token=token
                return self.reply(200,{'connected':True,'sha':remote['sha'],'data':data})
            if path=='/api/disconnect':self.server.token=None;return self.reply(200,{'ok':True})
            if path in ('/api/draft','/api/preview','/api/publish'):
                data=validate(body.get('data'),self.server.schema)
                if path=='/api/preview':return self.reply(200,render(data),'text/html')
                if path=='/api/draft':
                    with self.server.lock:
                        temp=DRAFT.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');os.replace(temp,DRAFT)
                    return self.reply(200,{'saved':True})
                if not self.server.token:return self.reply(401,{'error':'Connect GitHub before publishing.'})
                sha=body.get('sha','')
                if not isinstance(sha,str) or len(sha)!=40:raise ValueError('Load the published version before publishing.')
                result=github(REMOTE,self.server.token,'PUT',{'message':'Update CDP resume from private editor','branch':'main','sha':sha,'content':base64.b64encode((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()).decode()})
                with self.server.lock:
                    (ROOT/'content/cdp.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
                    self.server.schema=data
                return self.reply(200,{'sha':result['content']['sha'],'commit':result['commit']['sha'],'url':'https://prabirbera23.github.io/prabir-bera-resumes/cdp.html'})
            return self.reply(404,{'error':'Not found.'})
        except ValueError as error:return self.reply(400,{'error':str(error)})
        except (OSError,KeyError,TypeError):return self.reply(500,{'error':'The operation could not complete. Your draft has not been discarded.'})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8766);parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
    try:server=EditorServer(args.port)
    except OSError:
        try:
            with urllib.request.urlopen('http://127.0.0.1:'+str(args.port)+'/api/health',timeout=3) as response:health=json.load(response)
            if health.get('app')!='prabir-resume-editor':raise ValueError()
        except (OSError,ValueError):raise SystemExit('Another application is using the editor port. Close it and try again.')
        if not args.no_browser:webbrowser.open('http://127.0.0.1:'+str(args.port)+'/')
        raise SystemExit(0)
    print('Resume editor is running privately on this computer. Close this window to stop it.',flush=True)
    if not args.no_browser:webbrowser.open(server.origin+'/')
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.token=None;server.server_close()

