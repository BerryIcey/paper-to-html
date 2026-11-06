"""Real crash/recovery/single-instance/clean-stop checks in a temporary project."""
from pathlib import Path
import tempfile,subprocess,sys,socket,time,json,os,signal,shutil
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
supervisor=ROOT/'assets/reader-components/reader_supervisor.py'
assert supervisor.is_file(),'reader supervisor is missing: service cannot recover independently'
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);root.joinpath('paper-reading.html').write_text('<html>reader</html>','utf-8')
    notes=b'{"version":1,"notes":[]}';root.joinpath('reading-notes.json').write_bytes(notes)
    shutil.copyfile(ROOT/'assets/reader-components/reading_server.py',root/'reading_server.py')
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    command=[sys.executable,str(supervisor),'--root',str(root),'--port',str(port)]
    manager=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    pidfile=root/f'.reader-server-{port}.pid';pid=None
    def healthy():
        try:
            with urlopen(f'http://127.0.0.1:{port}/api/health',timeout=1) as r:return json.load(r).get('ok') is True
        except Exception:return False
    def wait(condition,timeout=8):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            if condition():return
            time.sleep(.1)
        raise AssertionError('supervisor did not meet condition before timeout')
    try:
        wait(lambda:pidfile.exists() and healthy());pid=int(pidfile.read_text());os.kill(pid,signal.SIGTERM)
        wait(lambda:pidfile.exists() and int(pidfile.read_text())!=pid and healthy())
        recovered=int(pidfile.read_text());duplicate=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        assert duplicate.wait(timeout=3)==0 and int(pidfile.read_text())==recovered
        assert root.joinpath('reading-notes.json').read_bytes()==notes
        subprocess.run(command+['--stop'],check=True,stdout=subprocess.DEVNULL)
        assert manager.wait(timeout=5)==0
        wait(lambda:not healthy(),timeout=3)
        print('PASS: child crash auto-recovery, singleton, unchanged notes and intentional clean stop')
    finally:
        if manager.poll() is None:manager.terminate();manager.wait(timeout=5)
        if pidfile.exists():
            try:os.kill(int(pidfile.read_text()),signal.SIGTERM)
            except OSError:pass
