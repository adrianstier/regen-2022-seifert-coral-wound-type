"""Inspect filename coverage and representative headers without altering images."""
from pathlib import Path
import csv
import json
import re
from collections import Counter
from PIL import Image
import subprocess
OUT=Path(__file__).resolve().parent/'image_archive_inventory_2026-10-12'
with (OUT/'nas_originals.csv').open() as f: rows=list(csv.DictReader(f))
coverage=[]
for treatment in ['Porites Air Br + Dremmel','Porites Air Brush','Porites Dremmel','Porites Wound Type Uninjured']:
    rr=[r for r in rows if r['collection']=='exp2_porites_originals' and r['relative_path'].split('/')[0]==treatment]
    parsed=[]
    for r in rr:
        m=re.search(r'_(\d+)_D(\d+)',r['name'])
        if m: parsed.append({'id':int(m[1]),'day':int(m[2]),'path':r['path']})
    coverage.append({'treatment_folder':treatment,'files':len(rr),'bytes':sum(int(r['bytes']) for r in rr),'ids':sorted({r['id'] for r in parsed}),'days':sorted({r['day'] for r in parsed}),'unparsed_files':len(rr)-len(parsed)})
rfp_final=[r for r in rows if r['collection']=='exp2_porites_originals' and re.search(r'_(5|18)_D63_',r['name']) and 'RFP' in r['name'].upper()]
samples=[]
for group in ['exp1_ashley_copy','exp2_porites_originals','porites_tiff_exports_early']:
    r=next(r for r in rows if r['collection']==group and r['extension'] in ['.jpg','.tif'])
    with Image.open(r['path']) as im: samples.append({'collection':group,'path':r['path'],'format':im.format,'dimensions':im.size,'mode':im.mode})
ai=Path('/Volumes/Stier_Lab/coral-regeneration/Manuscripts/B_wound_type/figures/Figure6-histology/Fig. 6_V2.ai')
try:
    p=subprocess.run(['/opt/homebrew/bin/pdfimages','-list',str(ai)],capture_output=True,text=True,timeout=120)
    histology={'path':str(ai),'pdfimages_exit_code':p.returncode,'image_inventory':p.stdout,'diagnostics':p.stderr}
except Exception as e: histology={'path':str(ai),'inspection_error':str(e)}
result={'exp2_filename_coverage':coverage,'D63_RFP_files_for_unscored_colonies':rfp_final,'representative_image_headers':samples,'histology_illustrator':histology}
(OUT/'candidate_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
