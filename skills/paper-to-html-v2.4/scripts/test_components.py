"""Isolated component assembler and durable queue integration checks (no browser claims)."""
from pathlib import Path
import tempfile,subprocess,sys,json,socket,time,urllib.request,urllib.error,concurrent.futures,base64
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    t=Path(tmp);content=t/'content.html'
    content.write_text('<section id="abstract" data-section="01摘要"><h1>组件测试</h1><p id="p1" data-highlight-block>测试文字</p></section><section id="cards" data-section="02知识卡"><details id="card1" data-reader-card><summary>测试卡</summary><p>测试内容</p></details></section>',encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'scripts/build_reader.py'),'--content',str(content),'--paper-id','isolated-component-test','--out',str(t/'paper-reading.html')],check=True)
    s=(t/'paper-reading.html').read_text('utf-8');assert 'reader-return' in s and '<script src=' not in s
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close();base=f'http://127.0.0.1:{port}'
    proc=subprocess.Popen([sys.executable,str(ROOT/'assets/reader-components/reading_server.py'),'--root',str(t),'--port',str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    def api(payload=None,origin=None):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        req=urllib.request.Request(base+'/api/notes',data=None if payload is None else json.dumps(payload).encode(),headers=headers)
        with urllib.request.urlopen(req,timeout=5) as r:return json.load(r)
    try:
        for _ in range(50):
            try:api();break
            except urllib.error.URLError:time.sleep(.1)
        else:raise AssertionError('Server failed to start')
        assert urllib.request.urlopen(base+'/paper-reading.html').read()==(t/'paper-reading.html').read_bytes()
        note={'id':'one','kind':'question','section':'abstract','content':'原始问题','attachments':[]}
        api(note);api(note);assert len(api()['notes'])==1
        api({**note,'action':'update','content':'修改问题'});n=api()['notes'][0];assert n['edit_history'][0]['content']=='原始问题'
        api({'action':'delete','id':'one'});assert api()['notes'][0]['status']=='deleted'
        api({'action':'restore','id':'one'});assert api()['notes'][0]['status']=='pending'
        def create(i):return api({**note,'id':f'parallel-{i}','content':f'问题{i}'})
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(create,range(12)))
        assert len(api()['notes'])==13
        try:api(note,origin='https://foreign.invalid');raise AssertionError('Foreign origin accepted')
        except urllib.error.HTTPError as e:assert e.code==403
        try:api({**note,'id':'bad','section':'absent'});raise AssertionError('Invalid section accepted')
        except urllib.error.HTTPError as e:assert e.code==400
        png='data:image/png;base64,'+base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'test').decode()
        api({**note,'id':'attachment','attachments':[{'name':'test.png','data':png}]})
        assert len(json.loads((t/'reading-notes.json').read_text('utf-8'))['notes'])==14
        print('PASS: single-file assembly; live queue create/idempotence/edit-history/delete/restore/12 concurrent submissions/attachment persistence/origin and section checks.')
    finally:
        proc.terminate();proc.wait(timeout=5)
