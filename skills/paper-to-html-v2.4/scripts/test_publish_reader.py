"""Isolated release retention and failure tests; never use a real paper project."""
from pathlib import Path
import tempfile,json
from publish_reader import publish
with tempfile.TemporaryDirectory() as t:
    root=Path(t);src=root/'working.html';src.write_text('<body><h1>Demo</h1></body>','utf-8');desktop=root/'desktop/latest.html'
    notes=root/'reading-notes.json';notes.write_text('preserve','utf-8')
    publish(root,src,'Demo',desktop)
    assert not (root/'reader-versions.json').exists() and '工作版' in desktop.read_text('utf-8')
    for count in (2,1,0):
        (root/'reader-settings.json').write_text(json.dumps({'backup_count':count}),'utf-8')
        for _ in range(4):publish(root,src,'Demo',desktop)
        manifest=json.loads((root/'reader-versions.json').read_text('utf-8'))
        assert len(manifest['releases'])==count+1
        assert len(list((root/'versions').glob('*.html')))==count+1
        assert desktop.read_bytes()==(root/'paper-reading.html').read_bytes()
    assert manifest['sequence']==12 and notes.read_text('utf-8')=='preserve'
    before=(root/'reader-versions.json').read_bytes();old=[p.name for p in (root/'versions').glob('*.html')]
    blocker=root/'not-a-directory';blocker.write_text('block','utf-8')
    try:publish(root,src,'Demo',blocker/'latest.html');raise AssertionError('Desktop failure was ignored')
    except FileExistsError:pass
    assert (root/'reader-versions.json').read_bytes()==before
    assert all((root/'versions'/name).is_file() for name in old)
    src.write_text('<body><img src="missing.png"></body>','utf-8')
    try:publish(root,src,'Demo');raise AssertionError('External image accepted')
    except ValueError:pass
print('PASS unconfigured working delivery, 0/1/2 retention, monotonic numbering, desktop sync, failure preservation and embedded resources')
