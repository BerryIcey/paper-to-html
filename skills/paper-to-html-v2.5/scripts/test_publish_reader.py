from pathlib import Path
import tempfile,json
from publish_reader import publish
with tempfile.TemporaryDirectory() as t:
    root=Path(t);src=root/'working.html';src.write_text('<body data-reader-release="legacy"><h1>First</h1></body>','utf-8');desktop=root/'desktop/latest.html'
    notes=root/'reading-notes.json';notes.write_text('preserve','utf-8')
    publish(root,src,'Demo',desktop)
    text=(root/'paper-reading.html').read_text('utf-8')
    assert 'data-reader-release' not in text and 'data-backup-count' not in text, 'removed release UI metadata must not be published'
    assert not (root/'reader-versions.json').exists() and not (root/'reader-settings.json').exists() and not (root/'versions').exists()
    # Retired settings must not re-enable histories or affect overwrite.
    legacy=root/'versions';legacy.mkdir();old=legacy/'existing.html';old.write_text('keep-existing','utf-8')
    (root/'reader-settings.json').write_text('{"backup_count":2}','utf-8')
    for title in ['Second','Third']:
        src.write_text('<body><h1>'+title+'</h1></body>','utf-8');publish(root,src,'Demo',desktop)
    assert 'Third' in (root/'paper-reading.html').read_text('utf-8')
    assert desktop.read_bytes()==(root/'paper-reading.html').read_bytes()
    assert old.read_text('utf-8')=='keep-existing' and len(list(legacy.iterdir()))==1
    assert not (root/'reader-versions.json').exists() and notes.read_text('utf-8')=='preserve'
    before=(root/'paper-reading.html').read_bytes();blocker=root/'not-a-directory';blocker.write_text('block','utf-8')
    try:publish(root,src,'Demo',blocker/'latest.html');raise AssertionError('Desktop failure ignored')
    except FileExistsError:pass
    assert (root/'paper-reading.html').read_bytes()==before
    src.write_text('<body><img src="missing.png"></body>','utf-8')
    try:publish(root,src,'Demo');raise AssertionError('External image accepted')
    except ValueError:pass
print('PASS overwrite-only publication, ignored retired settings, preserved existing archives/notes, desktop sync and failure preservation')
