#!/usr/bin/env python3
"""Maintain and validate the publishable data-only music repository (Python stdlib)."""
import argparse,hashlib,json,re,shutil,wave
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'MusicCatalog' if (ROOT/'MusicCatalog').is_dir() else ROOT
CATALOG=BASE/'catalog.json'

def load():return json.loads(CATALOG.read_text())
def write(d):
 d['revision']=datetime.now(timezone.utc).isoformat(timespec='seconds')
 CATALOG.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def add(d,path,track_id,title,genre,bpm,pro,duration=None):
 path=Path(path);data=path.read_bytes();digest=hashlib.sha256(data).hexdigest();ext=path.suffix.lower()
 if ext=='.wav':
  with wave.open(str(path)) as w:duration=w.getnframes()/w.getframerate()
 if duration is None:raise ValueError('--duration is required for MP3/M4A')
 name=f'{track_id}-{digest[:16]}{ext}';target=BASE/'tracks'/name
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
 track=dict(id=track_id,title=title,genre=genre,bpm=bpm,duration=duration,pro=pro,file='tracks/'+name,bytes=len(data),sha256=digest)
 d['tracks']=[t for t in d['tracks'] if t['id']!=track_id]+[track]
def validate():
 d=load();assert d['schemaVersion']==1 and d['revision'] and len(d['tracks'])<=500
 seen=set()
 for t in d['tracks']:
  assert re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',t['id']) and t['id'] not in seen;seen.add(t['id'])
  assert t['title'].get('en') and all(isinstance(v,str) and 0<len(v)<=120 for v in t['title'].values())
  assert isinstance(t['pro'],bool) and isinstance(t['bpm'],int) and 40<=t['bpm']<=220
  assert isinstance(t['genre'],str) and 0<len(t['genre'])<=40 and 10<=t['duration']<=300
  assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*',t['file']) and all(x not in ['', '.', '..'] for x in t['file'].split('/'))
  p=BASE/t['file'];assert p.suffix in ['.wav','.mp3','.m4a'] and p.resolve().is_relative_to(BASE.resolve())
  data=p.read_bytes();assert 0<len(data)<=25_000_000 and len(data)==t['bytes'] and hashlib.sha256(data).hexdigest()==t['sha256']
  if p.suffix=='.wav':
   with wave.open(str(p)) as w:assert abs(w.getnframes()/w.getframerate()-t['duration'])<.1
 assert len(CATALOG.read_bytes())<=1_000_000
 print(f"Validated {len(d['tracks'])} tracks; revision {d['revision']}")
 return d

def main():
 parser=argparse.ArgumentParser();subs=parser.add_subparsers(dest='command',required=True)
 subs.add_parser('seed-bundled');subs.add_parser('validate')
 a=subs.add_parser('add');a.add_argument('audio');a.add_argument('--id',required=True);a.add_argument('--title',required=True);a.add_argument('--title-tr');a.add_argument('--genre',required=True);a.add_argument('--bpm',type=int,required=True);a.add_argument('--pro',action='store_true');a.add_argument('--duration',type=float)
 pub=subs.add_parser('package');pub.add_argument('output')
 args=parser.parse_args()
 if args.command=='seed-bundled':
  cat={'schemaVersion':1,'revision':'initial','tracks':[]}
  names=['Yumuşak ritim','Biraz enerji','Sabah akışı','El çırp','Küçük adımlar','Güne başla']
  translations=json.loads((ROOT/'App/Resources/Localizable.xcstrings').read_text())['strings']
  for i,(track,key) in enumerate(zip(json.loads((ROOT/'Docs/bundled-dance-music.json').read_text())['tracks'],names)):
   title={lang:e['stringUnit']['value'] for lang,e in translations[key]['localizations'].items()}
   add(cat,ROOT/'App/Resources'/(track['id']+'.wav'),track['id'],title,track['style'].title(),track['bpm'],i>=2)
  write(cat)
 elif args.command=='add':
  cat=load();titles={'en':args.title}
  if args.title_tr:titles['tr']=args.title_tr
  add(cat,args.audio,args.id,titles,args.genre,args.bpm,args.pro,args.duration);write(cat)
 elif args.command=='package':
  cat=validate();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
  shutil.copy2(CATALOG,out/'catalog.json')
  for t in cat['tracks']:
   dst=out/t['file'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/t['file'],dst)
  return
 validate()
if __name__=='__main__':main()
