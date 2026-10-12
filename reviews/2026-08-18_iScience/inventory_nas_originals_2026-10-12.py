"""Inventory discovered original-image NAS locations without reading full image data."""
from pathlib import Path
from collections import Counter
import os
import csv
import json
OUT=Path(__file__).resolve().parent/'image_archive_inventory_2026-10-12'
ROOTS={
 'exp1_ashley_copy':Path('/Volumes/Stier_Lab/3. Wound_Type_Airbrush_Dremel_2022 (Ashley copy)/3. Wound_Type_Airbrush_Dremel_2022/Wound comparison study'),
 'exp2_porites_originals':Path('/Volumes/Stier_Lab/Moorea 2025/Moorea 2025/Wound-Type 2025/Porites Wound Type'),
 'nas_manuscript_figures_2025':Path('/Volumes/Stier_Lab/Moorea 2025/Moorea 2025/Wound-Type 2025/Wound-Type manuscript Figures'),
 'nas_manuscript_figures_mirror':Path('/Volumes/Stier_Lab/coral-regeneration/Manuscripts/B_wound_type/figures'),
 'porites_tiff_exports_early':Path('/Volumes/Stier_Lab/coral_regeneration_photos_videos/Porites TIFS'),
 'porites_early_microscope_aux':Path('/Volumes/Stier_Lab/coral_regeneration_photos_videos/Porites_Drem_2_D2_BF_3.2 zoom'),
}
rows=[]; summary=[]; errors=[]
for group,root in ROOTS.items():
    rr=[]
    for folder,dirs,files in os.walk(root,onerror=lambda e:errors.append(str(e))):
        dirs[:]=[d for d in dirs if not d.startswith('.')]
        for name in files:
            if name.startswith('.'): continue
            path=Path(folder)/name
            try: size=path.stat().st_size
            except OSError as e: errors.append(str(e)); continue
            rr.append({'collection':group,'path':str(path),'relative_path':str(path.relative_to(root)),'name':name,'extension':path.suffix.lower(),'bytes':size})
    rows.extend(rr)
    entry={'collection':group,'root':str(root),'files':len(rr),'bytes':sum(r['bytes'] for r in rr),'extensions':dict(Counter(r['extension'] for r in rr))}
    summary.append(entry); print(json.dumps(entry),flush=True)
with (OUT/'nas_originals.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['collection','path','relative_path','name','extension','bytes']); w.writeheader(); w.writerows(rows)
(OUT/'nas_originals_summary.json').write_text(json.dumps({'collections':summary,'errors':errors},indent=2))
