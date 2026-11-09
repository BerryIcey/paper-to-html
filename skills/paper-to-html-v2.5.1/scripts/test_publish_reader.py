from pathlib import Path
import tempfile
from publish_reader import publish
with tempfile.TemporaryDirectory() as t:
    root=Path(t);src=root/'working.html';src.write_text('<body data-reader-release="legacy"><h1>First</h1></body>','utf-8');desktop=root/'desktop/latest.html'
    notes=root/'reading-notes.json';notes.write_text('preserve','utf-8')
    publish(root,src,'Demo')
    text=(root/'paper-reading.html').read_text('utf-8')
    assert 'data-reader-release' not in text and 'data-backup-count' not in text, 'removed release UI metadata must not be published'
    assert not (root/'reader-versions.json').exists() and not (root/'reader-settings.json').exists() and not (root/'versions').exists()
    # Retired settings must not re-enable histories or affect overwrite.
    legacy=root/'versions';legacy.mkdir();old=legacy/'existing.html';old.write_text('keep-existing','utf-8')
    (root/'reader-settings.json').write_text('{"backup_count":2}','utf-8')
    for title in ['Second','Third']:
        src.write_text('<body><h1>'+title+'</h1></body>','utf-8');publish(root,src,'Demo')
    assert 'Third' in (root/'paper-reading.html').read_text('utf-8')
    assert not desktop.exists()
    assert old.read_text('utf-8')=='keep-existing' and len(list(legacy.iterdir()))==1
    assert not (root/'reader-versions.json').exists() and notes.read_text('utf-8')=='preserve'
    pdf=root/'source-paper.pdf';pdf.write_bytes(b'%PDF-1.4 local source')
    src.write_text('<body><a href="source-paper.pdf">PDF</a></body>','utf-8')
    publish(root,src,'Demo')
    assert 'href="source-paper.pdf"' in (root/'paper-reading.html').read_text('utf-8'), 'The local reader must retain its service PDF link'
    assert 'data:application/pdf' not in (root/'paper-reading.html').read_text('utf-8')
    assert pdf.read_bytes()==b'%PDF-1.4 local source'
    before=(root/'paper-reading.html').read_bytes();desktop.parent.mkdir();desktop.write_text('existing desktop copy','utf-8')
    try:publish(root,src,'Demo',desktop);raise AssertionError('Separate desktop HTML publication accepted')
    except ValueError:pass
    assert desktop.read_text('utf-8')=='existing desktop copy'
    assert (root/'paper-reading.html').read_bytes()==before
    pdf.unlink()
    try:publish(root,src,'Demo');raise AssertionError('Missing local PDF accepted')
    except ValueError:pass
    assert (root/'paper-reading.html').read_bytes()==before
    src.write_text('<body><img src="missing.png"></body>','utf-8')
    try:publish(root,src,'Demo');raise AssertionError('External image accepted')
    except ValueError:pass
print('PASS single local-service reader, local PDF link, rejected desktop copies, preserved notes/history and failure preservation')
