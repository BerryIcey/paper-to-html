"""Real isolated routing checks for reader health and linked source PDF."""
from pathlib import Path
import tempfile,subprocess,sys,socket,time,json
from urllib.request import urlopen,Request
from urllib.error import HTTPError,URLError
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);root.joinpath('paper-reading.html').write_text('<html>reader</html>','utf-8')
    pdf=b'%PDF-1.4\nroute fixture only\n';root.joinpath('source-paper.pdf').write_bytes(pdf)
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    proc=subprocess.Popen([sys.executable,str(ROOT/'assets/reader-components/reading_server.py'),'--root',str(root),'--port',str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    base=f'http://127.0.0.1:{port}'
    def request(route,headers=None):
        try:
            with urlopen(Request(base+route,headers=headers or {}),timeout=3) as response:return response.status,response.headers,response.read()
        except HTTPError as error:return error.code,error.headers,error.read()
    try:
        for _ in range(40):
            try:
                if request('/favicon.ico')[0]==204:break
            except URLError:time.sleep(.1)
        else:raise AssertionError('reader startup failed')
        status,headers,body=request('/source-paper.pdf')
        assert status==200,f'linked source PDF expected 200, got {status}'
        assert headers['Content-Type'].startswith('application/pdf') and body==pdf
        status,_,body=request('/api/health')
        assert status==200,f'health endpoint expected 200, got {status}'
        assert json.loads(body)=={'ok':True,'port':port}
        assert request('/api/health',{'Origin':'https://foreign.invalid'})[0]==403
        assert request('/private-file.json')[0]==404
        root.joinpath('source-paper.pdf').unlink()
        assert request('/source-paper.pdf')[0]==404
        print('PASS: linked PDF bytes/mime, health, origin restriction, missing PDF and restricted routes')
    finally:proc.terminate();proc.wait(timeout=5)
