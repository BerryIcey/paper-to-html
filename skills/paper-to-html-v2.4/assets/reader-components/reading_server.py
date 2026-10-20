"""Loopback-only paper reader with durable notes. No model/API access."""
import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from threading import Lock
from datetime import datetime, timezone
import uuid
import base64
import re

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
parser.add_argument("--port", type=int, default=18765)
args = parser.parse_args()
ROOT = args.root.resolve()
NOTES = ROOT / 'reading-notes.json'
LOCK = Lock()
PORT = args.port

def save_notes(data):
    temp = NOTES.with_suffix('.json.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, NOTES)

def validate_images(items):
    if not isinstance(items, list) or len(items) > 4:
        raise ValueError('最多附加 4 张截图')
    images=[]
    for item in items:
        raw=item.get('data', '')
        m=re.fullmatch(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)', raw)
        if not m:
            raise ValueError('截图仅支持 PNG、JPEG、WebP')
        blob=base64.b64decode(m[2], validate=True)
        valid=(m[1]=='png' and blob.startswith(b'\x89PNG\r\n\x1a\n') or m[1]=='jpeg' and blob.startswith(b'\xff\xd8\xff') or m[1]=='webp' and blob.startswith(b'RIFF') and blob[8:12]==b'WEBP')
        if not valid or len(blob)>5*1024*1024:
            raise ValueError('截图格式无效或超过 5 MB')
        images.append({'name':str(item.get('name','截图'))[:150], 'data':raw})
    return images

def read_notes():
    if not NOTES.exists():
        return {'version': 1, 'notes': []}
    return json.loads(NOTES.read_text(encoding='utf-8'))

class Handler(BaseHTTPRequestHandler):
    def send(self, status, payload, mime='application/json; charset=utf-8'):
        data = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def allowed(self):
        # Reject foreign browser origins and DNS rebinding hosts.
        host = self.headers.get('Host', '')
        origin = self.headers.get('Origin')
        return host in (f'127.0.0.1:{PORT}', f'localhost:{PORT}') and (
            origin is None or origin in (f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}'))

    def do_GET(self):
        if not self.allowed():
            return self.send(403, {'error': '来源不允许'})
        route = urlsplit(self.path).path
        if route == '/api/settings':
            p=ROOT/'reader-settings.json'
            with LOCK:
                data=json.loads(p.read_text('utf-8')) if p.exists() else {}
            return self.send(200,data)
        if route == '/api/health':
            return self.send(200, {'ok': (ROOT / 'paper-reading.html').is_file(), 'port': PORT})
        if route == '/source-paper.pdf':
            source = ROOT / 'source-paper.pdf'
            if not source.is_file():
                return self.send(404, {'error': '原论文PDF不存在'})
            return self.send(200, source.read_bytes(), 'application/pdf')
        if route == '/api/notes':
            try:
                with LOCK:
                    data = read_notes()
                return self.send(200, data)
            except Exception:
                return self.send(500, {'error': '记录读取失败，请保留输入并稍后重试'})
        if route in ('/', '/paper-reading.html'):
            return self.send(200, (ROOT / 'paper-reading.html').read_bytes(), 'text/html; charset=utf-8')
        if route in ('/reader.css', '/reader.js'):
            p = ROOT / route[1:]
            if not p.is_file(): return self.send(404, {'error': '资源不存在'})
            return self.send(200, p.read_bytes(), 'text/css; charset=utf-8' if p.suffix == '.css' else 'text/javascript; charset=utf-8')
        if route == '/favicon.ico':
            return self.send(204, b'')
        return self.send(404, {'error': '未找到'})

    def do_POST(self):
        if not self.allowed():
            return self.send(403, {'error': '来源不允许'})
        if urlsplit(self.path).path == '/api/settings':
            try:
                size=int(self.headers.get('Content-Length','0'))
                if self.headers.get('Content-Type','').split(';')[0]!='application/json' or not 0<size<=1024: return self.send(400,{'error':'设置无效'})
                data=json.loads(self.rfile.read(size)); count=data.get('backup_count')
                if type(count) is not int or count not in (0,1,2): return self.send(400,{'error':'备份数量仅支持0、1、2'})
                with LOCK:
                    p=ROOT/'reader-settings.json'; tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps({'backup_count':count},ensure_ascii=False),'utf-8');os.replace(tmp,p)
                return self.send(200,{'backup_count':count})
            except Exception: return self.send(400,{'error':'设置保存失败'})
        if urlsplit(self.path).path != '/api/notes':
            return self.send(404, {'error': '未找到'})
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.send(415, {'error': '仅支持 JSON'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 29*1024*1024:
                return self.send(400, {'error': '输入过长或为空'})
            payload = json.loads(self.rfile.read(size))
            action=payload.get('action','create')
            if action in ('delete','restore'):
                with LOCK:
                    data=read_notes()
                    note=next((n for n in data['notes'] if n['id']==payload.get('id')),None)
                    if note is None: return self.send(404, {'error':'记录不存在'})
                    if action=='delete' and note['status']!='pending': return self.send(409, {'error':'只能删除待处理记录'})
                    if action=='restore' and note['status']!='deleted': return self.send(409, {'error':'记录未删除'})
                    note['status']='deleted' if action=='delete' else 'pending'
                    note['updated_at']=datetime.now(timezone.utc).isoformat()
                    save_notes(data)
                return self.send(200, {'note':note})
            if action not in ('create','update'): return self.send(400, {'error':'操作无效'})
            content = payload.get('content', '')
            attachments=validate_images(payload.get('attachments',[]))
            if not isinstance(content, str) or len(content)>6000 or (not content.strip() and not attachments):
                return self.send(400, {'error': '请写文字或附加截图，文字最多 6000 字'})
            kind = payload.get('kind', 'question')
            section = payload.get('section', 'overview')
            if kind not in ('question', 'addition', 'change'):
                return self.send(400, {'error': '类型无效'})
            from html.parser import HTMLParser
            class Sections(HTMLParser):
                def __init__(self): super().__init__(); self.ids = set()
                def handle_starttag(self, tag, attrs):
                    item = dict(attrs)
                    if tag == "section" and "data-section" in item and item.get("id"): self.ids.add(item["id"])
            parsed = Sections(); parsed.feed((ROOT / "paper-reading.html").read_text("utf-8"))
            valid_sections = parsed.ids
            if section not in valid_sections:
                return self.send(400, {'error': '章节无效'})
            request_id = payload.get('id')
            if not isinstance(request_id, str) or len(request_id) > 80 or not request_id:
                request_id = str(uuid.uuid4())
            with LOCK:
                data = read_notes()
                existing = next((n for n in data['notes'] if n['id'] == request_id), None)
                if action=='update':
                    if existing is None: return self.send(404, {'error':'记录不存在'})
                    if existing['status']!='pending': return self.send(409, {'error':'此记录已处理或已删除，请另写一条'})
                    history=existing.setdefault('edit_history',[])
                    history.append({k:existing.get(k) for k in ('content','kind','section','attachments','updated_at')})
                    existing.update(content=content.strip(),kind=kind,section=section,attachments=attachments,updated_at=datetime.now(timezone.utc).isoformat())
                    save_notes(data)
                    return self.send(200, {'note':existing})
                if existing:
                    return self.send(200, {'note': existing})
                note = {'id': request_id, 'kind': kind, 'section': section,
                        'content': content.strip(), 'status': 'pending',
                        'created_at': datetime.now(timezone.utc).isoformat(), 'response': '', 'attachments':attachments}
                data['notes'].append(note)
                save_notes(data)
            return self.send(201, {'note': note})
        except (ValueError, TypeError, AttributeError):
            return self.send(400, {'error': '内容格式无效'})
        except Exception:
            return self.send(500, {'error': '未能保存，请保留输入并重试'})

    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
