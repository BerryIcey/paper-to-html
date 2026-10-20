"""Validate the deliberately limited static payload before deployment."""
from pathlib import Path
import hashlib,json,re
r=Path(__file__).resolve().parents[1]/'site';manifest=json.loads((r/'attribution.json').read_text('utf8'));html=(r/'index.html').read_text('utf8')
assert manifest['doi'].startswith('https://doi.org/') and manifest['license'].startswith('https://creativecommons.org/licenses/')
assert manifest['personal_notes_included'] is False and manifest['private_attachments_included'] is False
assert hashlib.sha256((r/'index.html').read_bytes()).hexdigest()==manifest['public_html_sha256'],'Update the reviewed attribution manifest when replacing the reader'
assert 'data-public-preview="true"' in html and '公开静态预览' in html
assert not re.search(r'file:///|[CD]:[\\/]|127\.0\.0\.1|localhost|data:application/pdf',html)
assert re.search(r'<div[^>]*id="reader-note-list"[^>]*>\s*</div>',html),'Private notes must not be embedded'
allowed={'index.html','.nojekyll','attribution.json'}|{'assets/'+name for name in manifest['images']}
actual={p.relative_to(r).as_posix() for p in r.rglob('*') if p.is_file()}
assert actual==allowed,('Unexpected public files',actual-allowed)
for name,record in manifest['images'].items():
 p=r/'assets'/name;assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256']
print('PASS public payload: attributed HTML, image hashes, file allowlist, static-only notes and no local paths.')
