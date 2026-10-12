"""Read image-location notes and preserve bounded discovery evidence locally."""
from pathlib import Path
import json
import subprocess
OUT=Path(__file__).resolve().parent/'image_archive_inventory_2026-10-12'
ids=['1NIIggIV1ZgDpFNyH3Q2FkLkH17j6zJVgWfAGGgBK_qs','1kulo2YEzcnAKZ3_VR7nVSmEeyx7MfjlpgEO0mE7mWrE','1xjF4lmwSnHmAATTGhQOM2L-c-SQq0W_8FJCLu7Fhs4E','1Eo2hBPYTB5OvdvvNczXs1yQJ7wgOGy-3EodHTTW9YqM']
records=[]
def walk(x,text,links):
    if isinstance(x,dict):
        if 'textRun' in x:
            text.append(x['textRun'].get('content',''))
            link=x['textRun'].get('textStyle',{}).get('link',{}).get('url')
            if link: links.append(link)
        for v in x.values(): walk(v,text,links)
    elif isinstance(x,list):
        for v in x: walk(v,text,links)
for id in ids:
    p=subprocess.run(['gws','docs','documents','get','--params',json.dumps({'documentId':id})],capture_output=True,text=True,timeout=120)
    if p.returncode: print(p.stderr+p.stdout); continue
    d=json.loads(p.stdout); text=[]; links=[]; walk(d.get('body',{}),text,links)
    records.append({'id':id,'title':d.get('title'),'text':''.join(text),'links':list(dict.fromkeys(links)),'inline_images':len(d.get('inlineObjects',{}))})
    print(json.dumps(records[-1],indent=2),flush=True)
(OUT/'location_notes.json').write_text(json.dumps(records,indent=2))
