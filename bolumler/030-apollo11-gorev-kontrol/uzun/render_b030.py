#!/usr/bin/env python3
"""B030: kare hassasiyetli 20 sahne/25 çizim + 4 ayrı kart.
Arşiv normal hızda; Türkçe anlatı yalnız 1.06x. Alt yazı yok, sadece
zaman/temsil ve arşiv kaydı etiketleri. Çalışma dosyaları .cache'de.
Çalıştırma: python bolumler/030-apollo11-gorev-kontrol/uzun/render_b030.py
"""
from pathlib import Path
import sys, json, math, subprocess, hashlib, wave, re
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'araclar'))
from video_yap import narr_isle, sure_al, ass_zaman
B=Path(__file__).resolve().parents[1]
WORK=Path.home()/'.cache/b030-render';WORK.mkdir(parents=True,exist_ok=True)
FF=str(ROOT/'araclar/bin/ffmpeg'); FONT=str(ROOT/'araclar/fonts/Montserrat-ExtraBold.ttf')
OUT=B/'uzun/merakli-030-uzun-apollo11-gorev-kontrol.mp4'
FPS=30;XF=12;SPEED=1.06
p=json.loads((B/'uzun/plan.taslak.json').read_text());scenes=p['sahneler']

def run(args):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True)
    if r.returncode:raise RuntimeError(f'ffmpeg exit={r.returncode}: '+r.stderr[-5000:])
    return r

def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def wav_seconds(f):
    with wave.open(str(f)) as w:return w.getnframes()/w.getframerate()
def card(name,rows):
    dest=B/'uzun/kartlar'/f'{name}.png';dest.parent.mkdir(exist_ok=True)
    im=Image.new('RGB',(1920,1080),'#101f24');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1920,17),fill='#d93636');d.rectangle((0,1063,1920,1080),fill='#d93636')
    for text,y,size,color in rows:
        font=ImageFont.truetype(FONT,size)
        while d.textbbox((0,0),text,font=font)[2]>1740:
            size-=2;font=ImageFont.truetype(FONT,size)
        bb=d.textbbox((0,0),text,font=font);x=(1920-bb[2])/2
        d.text((x,y),text,font=font,fill=color)
    im.save(dest);return dest
intro=card('giris',[('EĞER 1969’DA OLSAYDIM',250,92,'white'),('HOUSTON’DA SON DAKİKALAR',420,78,'#ef5252'),('MERAKLI · APOLLO 11',670,44,'#d7e5df')])
date=card('tarih',[('20 TEMMUZ 1969',265,108,'white'),('HOUSTON · GÖREV KONTROLÜ',445,64,'#ef5252'),('Meraklı kurgu · Çizimler temsili',665,38,'#d7e5df')])
closing=card('kapanis',[('SEN HANGİ MASADA OLURDUN?',240,82,'white'),('VERİYİ OKUMAK',430,52,'#ef5252'),('HABERLEŞMEK · SİSTEMİ SINAMAK',550,50,'white'),('Seçimini yorumlara yaz.',750,38,'#d7e5df')])
subscribe=card('abone',[('KANALIMA ABONE',290,104,'white'),('OLMAYI UNUTMAYIN!',460,104,'#ef5252'),('MERAKLI · EĞER ORADA OLSAYDIM',750,40,'#d7e5df')])
clips=[];st=[];tracks=[]
def append(image,frames,id):
    start=clips[-1]['end_frame']-XF if clips else 0
    x={'id':id,'image':str(image.relative_to(ROOT)),'frames':frames,'start_frame':start,'end_frame':start+frames}
    clips.append(x);return x
append(intro,105,'giris');append(date,75,'tarih')
archive=ROOT/'bolumler/030-apollo11-gorev-kontrol/uzun/arsiv-sesleri/eagle-has-landed-islenmis.mp3'
run(['-i',archive,'-ar',48000,'-ac',2,'-c:a','pcm_s16le',WORK/'archive.wav'])
archive_length=wav_seconds(WORK/'archive.wav');radio=None
for i,s in enumerate(scenes):
    target=WORK/f'narr-{s["id"]}.wav';narr_isle(str(ROOT/s['anlatim']),str(target),SPEED)
    n=wav_seconds(target);extra=(archive_length+1.0) if s['id']=='s15' else 0
    frames=math.ceil((n+1.1+extra)*FPS)
    start=clips[-1]['end_frame']-XF
    if 'gorsel2' in s:
        a=round(frames*.5);c1=append(ROOT/s['gorsel'],a,s['id']);c2=append(ROOT/s['gorsel2'],frames-a+XF,s['id']+'b')
        change=c2['start_frame']/FPS+XF/FPS/2
    else:append(ROOT/s['gorsel'],frames,s['id']);change=None
    nb=start/FPS+.5;ne=nb+n;end=(start+frames)/FPS
    record={'id':s['id'],'start':start/FPS,'narration_start':nb,'narration_end':ne,'end':end,'second_image_midpoint':change,'narration_speed':SPEED,'narration_pcm_seconds':n,'narration_source_sha256':sha(ROOT/s['anlatim'])}
    tracks.append({'file':str(target),'t':nb,'gain_db':0,'type':'narration','scene':s['id'],'duration':n})
    if s['id']=='s15':
        rb=ne+.5;archive_end=rb+archive_length
        radio={'start':rb,'end':archive_end,'duration':archive_length,'speed':1.0,'source_sha256':sha(archive),'scene':'s15'}
        assert archive_end<end-.4
        tracks.append({'file':str(WORK/'archive.wav'),'t':rb,'gain_db':3,'type':'archive','scene':'s15','duration':archive_length})
        record['archive']=radio
    st.append(record);print('TIMELINE',s['id'],round(start/FPS,3),round(end,3),flush=True)
append(closing,105,'kapanis');append(subscribe,120,'abone')
total=clips[-1]['end_frame']/FPS
assert 300<=total<=720
# Genuine CC0 modern recordings, explicitly NOT 1969 documentary room sound.
foley=[('s01','cloth',1.5,1.4),('s03','paper',10,.6),('s05','paper',8,.6),('s07','pencil',12,1.5),('s10','paper',18,.6),('s17','paper',9,.6),('s20','cloth',2,1.2)]
paths={'paper':'sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pageturn1.opus','pencil':'sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pencil-scratch-1.opus','cloth':'sfx/free-sfx/Owlish/Sound Effects Pack/Cloth, Rustle/320137__owlstorm__blanket-movement-1.opus'}
for j,(sid,kind,t,dur) in enumerate(foley):
    source=ROOT/paths[kind];dest=WORK/f'foley{j}.wav'
    run(['-i',source,'-t',dur,'-af',f'afade=t=in:d=0.03,afade=t=out:st={max(0,dur-.08)}:d=0.08','-ar',48000,'-ac',2,'-c:a','pcm_s16le',dest])
    s=next(x for x in st if x['id']==sid);at=s['start']+t
    assert at+dur<s['narration_end']
    tracks.append({'file':str(dest),'t':at,'gain_db':-27,'type':'modern_analogy','scene':sid,'duration':dur,'source':paths[kind],'source_sha256':sha(source),'license':'CC0 / OwlishMedia','source_url':'https://opengameart.org/content/sound-effects-pack'})
# No narration overlaps any other narration or archival speech.
voices=sorted([x for x in tracks if x['type'] in ('narration','archive')],key=lambda x:x['t'])
for a,b in zip(voices,voices[1:]):assert a['t']+a['duration']<=b['t']
assert not any(x['type']=='modern_analogy' and x['t']<radio['end'] and x['t']+x['duration']>radio['start'] for x in tracks)
timeline={'fps':FPS,'transition_frames':XF,'narration_speed':SPEED,'archive_speed':1.0,'total_seconds':total,'scene_count':20,'scene_image_count':25,'separate_card_count':4,'scene_timing':st,'clips':clips,'archive':radio,'tracks':[{k:v for k,v in x.items() if k!='file'} for x in tracks],'music_used':False,'subtitles':False}
(B/'uzun/ZAMAN-CIZELGESI.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
# ASS: labels only, never speech subtitles. Boundary cuts at xfade midpoint
# ensure that old/new date labels cannot overlap during image transitions.
header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Date,Montserrat ExtraBold,28,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,1,0,7,36,36,16,1\nStyle: Type,Montserrat ExtraBold,24,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,1,0,9,36,36,18,1\nStyle: Radio,Montserrat ExtraBold,30,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,1,0,7,36,36,70,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
events=[]
def ev(a,b,style,text):events.append(f'Dialogue: 1,{ass_zaman(a)},{ass_zaman(b)},{style},,0,0,0,,{text}')
for i,(s,t) in enumerate(zip(scenes,st)):
    a=t['start']+XF/FPS/2;b=st[i+1]['start']+XF/FPS/2 if i+1<len(st) else t['end']-XF/FPS/2
    text=s['tarih_bandi'];fs=28
    while ImageFont.truetype(FONT,fs).getlength(text)>1390:fs-=1
    if s['id']=='s19':
        ev(a,t['second_image_midpoint'],'Date','{\\fs28}AY’DAN YÜKSELİŞ VE BULUŞMA · AÇIKLAYICI ŞEMA')
        ev(t['second_image_midpoint'],b,'Date','{\\fs28}24 TEMMUZ 1969 · DÜNYA’YA DÖNÜŞ · TEMSİLÎ')
    else:ev(a,b,'Date',f'{{\\fs{fs}}}'+text)
ev(st[0]['start']+.2,st[-1]['end']-.2,'Type','ÇİZİM: AI TEMSİLÎ')
ev(radio['start'],radio['end'],'Radio','GERÇEK KAYIT · NASA/JSC · İŞLENMİŞ ALINTI')
for cue in tracks:
    if cue['type']=='modern_analogy':
        ev(cue['t'],cue['t']+max(1.8,cue['duration']),'Radio','{\\bord3\\shad0}SES: MODERN ANALOJİ · CC0 FOLEY')
ass=B/'uzun/etiketler.ass';ass.write_text(header+'\n'.join(events)+'\n')
# Mix PCM -> measured two-pass loudness -> AAC. Archive never time-stretched.
inputs=[];filters=[]
for i,x in enumerate(tracks):
    inputs+=['-i',x['file']]
    filters.append(f'[{i}:a]volume={10**(x["gain_db"]/20):.6f},adelay={round(x["t"]*48000)}S:all=1,asetpts=N/SR/TB[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(len(tracks)))+f'amix=inputs={len(tracks)}:normalize=0:duration=longest,apad,atrim=duration={total},asetpts=N/SR/TB[m]')
rawmix=WORK/'rawmix.wav';run([*inputs,'-filter_complex_threads',2,'-filter_complex',';'.join(filters),'-map','[m]','-c:a','pcm_f32le',rawmix])
r=subprocess.run([FF,'-hide_banner','-i',str(rawmix),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);assert r.returncode==0
measure=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)[-1]);(WORK/'loudness-pass1.json').write_text(json.dumps(measure,indent=2))
lf=(f'loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={measure["input_i"]}:measured_TP={measure["input_tp"]}:measured_LRA={measure["input_lra"]}:measured_thresh={measure["input_thresh"]}:offset={measure["target_offset"]}:linear=true:print_format=json,aresample=48000')
run(['-i',rawmix,'-af',lf,'-c:a','aac','-b:a','160k',WORK/'mix.m4a'])
print('MIX_READY',total,'ARCHIVE',radio,flush=True)
# Static full-frame images preserve every foot/hand. Scene transitions only.
for i,c in enumerate(clips):
    dest=WORK/f'clip{i:02}.mp4';c['cache']=str(dest)
    expected=c['frames']/FPS
    cache_ok=False
    if dest.exists():
        probe=subprocess.run([FF,'-i',str(dest)],capture_output=True,text=True)
        mm=re.search(r'Duration: (\d+):(\d+):(\d+\.?\d*)',probe.stderr)
        cache_ok=bool(mm) and abs(int(mm[1])*3600+int(mm[2])*60+float(mm[3])-expected)<=.04
    if not cache_ok:
        run(['-loop',1,'-framerate',1,'-i',ROOT/c['image'],'-frames:v',c['frames'],'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf',22,'-threads',2,'-an',dest])
    print('CLIP_READY',i,c['id'],flush=True)

def combine(group,out,final=False):
    args=[];fs=[]
    for i,(path,frames) in enumerate(group):args+=['-i',path];fs.append(f'[{i}:v]fps=30,settb=AVTB,format=yuv420p[v{i}]')
    cur='[v0]';frames=group[0][1]
    for i in range(1,len(group)):
        fs.append(f'{cur}[v{i}]xfade=transition=fade:duration={XF/FPS}:offset={(frames-XF)/FPS:.9f}[x{i}]');cur=f'[x{i}]';frames+=group[i][1]-XF
    if final:
        pth=str(ass).replace(':','\\:');fonts=str(ROOT/'araclar/fonts')
        r0=radio['start'];r1=radio['end']
        tail=(f"drawbox=x=0:y=0:w=iw:h=62:color=black@0.72:t=fill:enable='between(t,{st[0]['start']+.2},{st[-1]['end']-.2})',"
              f"drawbox=x=25:y=63:w=1180:h=50:color=0x9a2525@0.9:t=fill:enable='between(t,{r0},{r1})',"
              f"subtitles=filename='{pth}':fontsdir='{fonts}',format=yuv420p")
    else:tail='format=yuv420p'
    fs.append(cur+tail+'[out]')
    enc=['-crf',25,'-maxrate','1150k','-bufsize','2300k'] if final else ['-crf',22]
    run([*args,'-filter_complex_threads',2,'-filter_complex',';'.join(fs),'-map','[out]','-r',30,'-frames:v',frames,'-c:v','libx264','-preset','veryfast','-threads',2,*enc,'-pix_fmt','yuv420p','-an',out])
    return out,frames
chunks=[]
for j in range(0,len(clips),5):
    group=[(Path(c['cache']),c['frames']) for c in clips[j:j+5]]
    path=WORK/f'chunk{j//5:02}.mp4'
    expected_frames=sum(frames for _,frames in group)-XF*(len(group)-1)
    if path.exists() and abs(sure_al(str(path))-expected_frames/FPS)<.04:
        chunks.append((path,expected_frames))
    else:
        chunks.append(combine(group,path))
    print('CHUNK_READY',j//5,flush=True)
video,_=combine(chunks,WORK/'picture.mp4',True)
run(['-i',video,'-i',WORK/'mix.m4a','-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',OUT])
print('RENDER_DONE',OUT,OUT.stat().st_size,sure_al(str(OUT)),flush=True)
