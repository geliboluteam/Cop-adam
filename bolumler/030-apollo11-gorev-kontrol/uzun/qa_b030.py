#!/usr/bin/env python3
"""B030 teknik QA: tam decode, ses ölçümü, faststart, 29 klip eşlemesi,
20 kaynak metin/ses hash ve 25 PNG. Bağımsız insan dinlemesi değildir.
"""
from pathlib import Path
import subprocess,sys,re,json,hashlib,struct
from PIL import Image,ImageChops,ImageStat
ROOT=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parents[1]
W=Path.home()/'.cache/b030-qa';W.mkdir(exist_ok=True,parents=True)
F=str(ROOT/'araclar/bin/ffmpeg');OUT=B/'uzun/merakli-030-uzun-apollo11-gorev-kontrol.mp4'
t=json.loads((B/'uzun/ZAMAN-CIZELGESI.json').read_text());p=json.loads((B/'uzun/plan.taslak.json').read_text());a=json.loads((B/'ANLATIM-SURE-OLCUMU.json').read_text());m=json.loads((B/'URETIM-DURUMU.json').read_text())
hashf=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
assert len(p['sahneler'])==20 and sum(1+('gorsel2' in x) for x in p['sahneler'])==25
assert t['scene_count']==20 and t['scene_image_count']==25 and t['separate_card_count']==4 and len(t['clips'])==29
for x in m['images']:
 assert hashf(ROOT/x['file'])==x['sha256']
 with Image.open(ROOT/x['file']) as im:assert im.size==(1920,1080);im.verify()
for c,s in zip(a['clips'],p['sahneler']):
 assert c['voice_id']=='voice-03' and c['id']==s['id']
 assert hashf(ROOT/c['file'])==c['sha256']
 assert hashlib.sha256(s['anlatim_metin'].encode()).hexdigest()==c['source_text_sha256']
 assert s['_karakter_min']>=4
assert t['subtitles'] is False and t['music_used'] is False
assert t['archive']['speed']==1.0 and t['narration_speed']==1.06
assert hashf(ROOT/'bolumler/030-apollo11-gorev-kontrol/uzun/arsiv-sesleri/eagle-has-landed-islenmis.mp3')==t['archive']['source_sha256']
probe=subprocess.run([F,'-hide_banner','-i',str(OUT)],capture_output=True,text=True).stderr
print(probe,flush=True)
match=re.search(r'Duration: (\d+):(\d+):(\d+\.?\d*)',probe);assert match
seconds=int(match[1])*3600+int(match[2])*60+float(match[3]);assert 300<=seconds<=720 and abs(seconds-t['total_seconds'])<.08
assert '1920x1080' in probe and '30 fps' in probe and 'Video: h264' in probe and 'Audio: aac' in probe and '48000 Hz, stereo' in probe
assert OUT.stat().st_size<95_000_000
atoms=[]
with OUT.open('rb') as f:
 pos=0
 while pos<OUT.stat().st_size:
  f.seek(pos);head=f.read(8)
  if len(head)<8:break
  size,kind=struct.unpack('>I4s',head)
  if size==1:size=struct.unpack('>Q',f.read(8))[0]
  if size==0:size=OUT.stat().st_size-pos
  assert size>=8
  atoms.append({'type':kind.decode('ascii'),'offset':pos,'size':size});pos+=size
assert next(x['offset'] for x in atoms if x['type']=='moov')<next(x['offset'] for x in atoms if x['type']=='mdat')
r=subprocess.run([F,'-hide_banner','-v','error','-threads','2','-i',str(OUT),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr
print('FULL_AV_DECODE_PASS',flush=True)
r=subprocess.run([F,'-hide_banner','-i',str(OUT),'-vn','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);assert r.returncode==0
loud=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)[-1])
assert -15.0<=float(loud['input_i'])<=-13.0 and float(loud['input_tp'])<=-1.0
print('LOUDNESS',loud,flush=True)

def frame(at,dest):
 r=subprocess.run([F,'-hide_banner','-loglevel','error','-y','-ss',f'{at:.6f}','-i',str(OUT),'-frames:v','1','-vf','scale=1280:720','-q:v','3',str(dest)],capture_output=True,text=True);assert r.returncode==0 and not r.stderr
 im=Image.open(dest).convert('RGB');assert sum(ImageStat.Stat(im).stddev)>30;return im
# Verify every picture actually appears, not merely that 25 files exist.
checks=[]
for i,c in enumerate(t['clips']):
 at=(c['start_frame']+c['end_frame'])/60
 actual=frame(at,W/f'clip{i:02}.jpg')
 expected=Image.open(ROOT/c['image']).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
 diff=ImageStat.Stat(ImageChops.difference(actual.crop((0,100,1280,720)),expected.crop((0,100,1280,720)))).mean
 mad=sum(diff)/3
 assert mad<9,(c['id'],mad)
 checks.append({'id':c['id'],'at_seconds':round(at,6),'mean_absolute_rgb_difference_below_header':round(mad,4),'result':'PASS'})
 print('PICTURE_MATCH',c['id'],round(mad,3),flush=True)
shots=[('01-giris',1.3),('02-tarih',4.1),('03-s01-modern',7.3),('04-s04b',132),('05-s09',294),('06-s12b',407),('07-s14',464),('08-kayit-oncesi',t['archive']['start']-.25),('09-gercek-kayit',520),('10-kayit-sonrasi',t['archive']['end']+.25),('11-ilk-adim',610),('12-yukselis',636),('13-donus24temmuz',650),('14-s20',678),('15-kapanis',692.4),('16-abone',696)]
qdir=B/'uzun/qa-kareleri';qdir.mkdir(exist_ok=True)
for name,at in shots:frame(at,qdir/f'{name}.jpg')
# Non-overlap of actual speech intervals, not merely clip boundaries.
voices=sorted([x for x in t['tracks'] if x['type'] in ('narration','archive')],key=lambda x:x['t'])
for aa,bb in zip(voices,voices[1:]):assert aa['t']+aa['duration']<=bb['t']
for x in t['tracks']:
 if x['type']=='modern_analogy':assert not (x['t']<t['archive']['end'] and x['t']+x['duration']>t['archive']['start'])
report={'status':'TEKNIK_QA_PASS_GORSEL_KARE_INCELEMESI_AYRI','file':str(OUT.relative_to(ROOT)),'sha256':hashf(OUT),'bytes':OUT.stat().st_size,'duration_seconds':seconds,'duration_timeline_seconds':t['total_seconds'],'width':1920,'height':1080,'fps':30,'video_codec':'H.264','audio_codec':'AAC','audio_sample_rate':48000,'audio_channels':2,'full_av_decode':'PASS','faststart':True,'mp4_atoms':atoms,'loudness':loud,'all_29_picture_matches':checks,'source_png_count':25,'scene_count':20,'separate_cards':4,'narrations':20,'voice_id':'voice-03','subtitles':False,'archive_normal_speed':True,'archive_no_narration_overlap':True,'archive_no_foley_overlap':True,'source_content_limitations':'No human listening performed. Archival provenance and publisher caption/primary context checked; PocketSphinx radio ASR was unreliable, not used as a transcript.','critical_frames':[{'file':str((qdir/f'{name}.jpg').relative_to(ROOT)),'at_seconds':round(at,6)} for name,at in shots]}
(B/'TEKNIK-QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('TECHNICAL_QA_DONE',seconds,OUT.stat().st_size,report['sha256'],flush=True)
