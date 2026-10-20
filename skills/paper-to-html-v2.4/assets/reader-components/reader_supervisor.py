"""Single project reader supervisor; run it outside the assistant's process tree."""
import argparse,os,sys,time,subprocess
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import urlopen
import json

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--port',type=int,default=18765)
    parser.add_argument('--stop',action='store_true')
    args=parser.parse_args();root=args.root.resolve();port=args.port
    stop=root/f'.reader-supervisor-{port}.stop'
    pidfile=root/f'.reader-server-{port}.pid'
    if args.stop:stop.touch();return 0
    lock=root/f'.reader-supervisor-{port}.lock'
    with lock.open('a+b') as guard:
        if guard.tell()==0:guard.write(b'0');guard.flush()
        guard.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(guard.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(guard.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError:return 0
        stop.unlink(missing_ok=True)
        logpath=root/f'.reader-service-{port}.log'
        def log(text):
            with logpath.open('a',encoding='utf-8') as output:
                output.write(datetime.now(timezone.utc).isoformat()+' '+text+'\n')
        def healthy():
            try:
                with urlopen(f'http://127.0.0.1:{port}/api/health',timeout=2) as response:
                    result=json.load(response)
                    return result.get('ok') is True and result.get('port')==port
            except Exception:return False
        child=None
        try:
            while not stop.exists():
                # An already running reader may be adopted without starting a second writer.
                if healthy():time.sleep(.5);continue
                with logpath.open('ab') as output:
                    child=subprocess.Popen([sys.executable,str(root/'reading_server.py'),'--root',str(root),'--port',str(port)],cwd=root,stdout=output,stderr=output,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
                temp=pidfile.with_suffix('.pid.tmp');temp.write_text(str(child.pid),'ascii');os.replace(temp,pidfile)
                log(f'started reader pid={child.pid}')
                while child.poll() is None and not stop.exists():time.sleep(.25)
                if stop.exists():break
                log(f'reader exited code={child.returncode}; restarting')
                pidfile.unlink(missing_ok=True);child=None
                time.sleep(.5)
        finally:
            if child is not None and child.poll() is None:
                child.terminate()
                try:child.wait(timeout=3)
                except subprocess.TimeoutExpired:child.kill();child.wait(timeout=3)
            pidfile.unlink(missing_ok=True)
            log('supervisor stopped')
        return 0

if __name__=='__main__':raise SystemExit(main())
