"""Inventory source images on Drive and NAS without modifying or downloading them."""
from pathlib import Path
from collections import Counter, defaultdict, deque
import csv
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'image_archive_inventory_2026-10-12'
OUT.mkdir(exist_ok=True)
NAS = Path('/Volumes/Stier_Lab/coral-regeneration/Projects')
PROJECTS = {
    'exp1_2022': ('3. Wound_Type_Airbrush_Dremel_2022','17ynlZHpUySEW4NzFUJJZjhEVF-OqKFD3'),
    'wound_type_2025': ('19. Wound_type_2025','1vm3IcmAfuZXF6cFQ3NTBTI0IA3cN5qIe'),
    'histology_2025': ('21. Wound_type_histology_2025','1j89PWbxYHYL7vmiFnzOBTm2gEwEBBaTq'),
    'final_figures': ('FINAL FIGURES','15DJbDGTCVDoEwz4kcCkBZZg_o844nfyL'),
}
IMAGE_EXT = {'.jpg','.jpeg','.heic','.tif','.tiff','.png','.bmp','.czi','.nd2','.vsi','.oir','.oib','.svs','.lif'}
def classify(path):
    s=path.lower()
    if 'island experiment' in s: return 'other_experiment_island'
    if 'a pulchra' in s: return 'other_experiment_acropora_pulchra'
    if any(x in s for x in ['final figures','timeline','figure','photoshop','illustrator']): return 'derived_or_figure_candidate'
    if Path(path).suffix.lower() in IMAGE_EXT: return 'source_image_candidate'
    return 'supporting_or_other'
def write_csv(name,records):
    keys=sorted(set().union(*(r.keys() for r in records))) if records else []
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(records)
nas=[]; errors=[]
for group,(name,_) in PROJECTS.items():
    if group=='final_figures': continue
    base=NAS/name
    for folder,dirs,files in os.walk(base,onerror=lambda e:errors.append(str(e))):
        dirs[:]=[d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.') or file.startswith('._'): continue
            path=Path(folder)/file
            try: size=path.stat().st_size
            except OSError as e: errors.append(str(e)); continue
            rel=str(path.relative_to(base))
            nas.append({'project':group,'relative_path':rel,'path':str(path),'bytes':size,'extension':path.suffix.lower(),'category':classify(rel)})
    print('NAS',group,len([r for r in nas if r['project']==group]),flush=True)
write_csv('nas_files.csv',nas)
drive=[]; folders=[]
for group,(name,id) in PROJECTS.items():
    queue=deque([(id,'')])
    seen=set()
    while queue:
        folder_id,prefix=queue.popleft()
        if folder_id in seen: continue
        seen.add(folder_id)
        token=None
        while True:
            params={'q':f"trashed = false and '{folder_id}' in parents",'pageSize':1000,'fields':'files(id,name,mimeType,size,md5Checksum,modifiedTime,webViewLink,parents),nextPageToken'}
            if token: params['pageToken']=token
            proc=subprocess.run(['gws','drive','files','list','--params',json.dumps(params)],capture_output=True,text=True,timeout=120)
            if proc.returncode: errors.append({'folder':folder_id,'error':proc.stderr+proc.stdout}); break
            response=json.loads(proc.stdout)
            for f in response.get('files',[]):
                rel=prefix+'/'+f['name'] if prefix else f['name']
                row={'project':group,'relative_path':rel,'folder_id':folder_id,**f}
                if f['mimeType']=='application/vnd.google-apps.folder':
                    folders.append(row); queue.append((f['id'],rel))
                else:
                    row['category']=classify(name+'/'+rel)
                    row['extension']=Path(f['name']).suffix.lower()
                    drive.append(row)
            token=response.get('nextPageToken')
            if not token: break
        print('DRIVE',group,prefix or '[root]',len([r for r in drive if r['project']==group]),flush=True)
    write_csv('drive_files.csv',drive)
    (OUT/'drive_folders.json').write_text(json.dumps(folders,indent=2))
summary=[]
for source,records in [('NAS',nas),('Drive',drive)]:
    for group in PROJECTS:
        rows=[r for r in records if r['project']==group]
        if not rows: continue
        by_category=defaultdict(list)
        for row in rows: by_category[row['category']].append(row)
        for category,rr in by_category.items():
            summary.append({'source':source,'project':group,'category':category,'files':len(rr),'bytes':sum(int(r.get('bytes',r.get('size',0))) for r in rr),'extensions':dict(Counter(r['extension'] for r in rr))})
matching=[]
drive_index={(r['project'],r['relative_path']):r for r in drive}
for n in nas:
    d=drive_index.get((n['project'],n['relative_path']))
    if d and d.get('size'):
        matching.append({'project':n['project'],'relative_path':n['relative_path'],'same_size':n['bytes']==int(d['size']),'drive_id':d['id'],'drive_md5':d.get('md5Checksum','')})
write_csv('nas_drive_size_comparison.csv',matching)
(OUT/'summary.json').write_text(json.dumps({'summary':summary,'errors':errors,'size_comparisons':len(matching),'size_mismatches':[r for r in matching if not r['same_size']]},indent=2))
print(json.dumps(summary,indent=2))
print('Errors',len(errors),'size mismatches',sum(not r['same_size'] for r in matching))
