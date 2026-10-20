"""Render a PDF figure clip directly at chosen dpi; requires PyMuPDF."""
import argparse,json
from pathlib import Path
import pymupdf as f
p=argparse.ArgumentParser();p.add_argument('pdf');p.add_argument('--page',type=int,required=True);p.add_argument('--clip',type=float,nargs=4,required=True);p.add_argument('--dpi',type=int,default=450);p.add_argument('--out',required=True);a=p.parse_args()
d=f.open(a.pdf);page=d[a.page-1];clip=f.Rect(a.clip)
if clip.is_empty or not page.rect.contains(clip):raise SystemExit('clip must lie within PDF page')
pix=page.get_pixmap(clip=clip,dpi=a.dpi,alpha=False);Path(a.out).parent.mkdir(parents=True,exist_ok=True);pix.save(a.out)
print(json.dumps({'page':a.page,'dpi':a.dpi,'width':pix.width,'height':pix.height,'drawings_in_page':len(page.get_drawings()),'note':'Rendering raster sources cannot restore missing detail.'}))
