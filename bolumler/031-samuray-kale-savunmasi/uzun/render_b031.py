#!/usr/bin/env python3
"""B031: kare hassasiyetli 20 sahne/25 cizim + 4 ayri kart (giris/tarih/kapanis/abone).
Statik tam kare: her el/ayak korunur, Ken Burns yok. Turkce anlati 1.18x.
Alt yazi yok; yalniz tarih bandi + AI TEMSILI etiketi. Harici SFX/muzik yok.
Calistirma: python bolumler/031-samuray-kale-savunmasi/uzun/render_b031.py
"""
from pathlib import Path
import sys, json, math, subprocess, hashlib, wave, re
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'araclar'))
from video_yap import narr_isle, sure_al, ass_zaman
B=Path(__file__).resolve().parents[1]
WORK=Path.home()/'.cache/b031-render';WORK.mkdir(parents=True,exist_ok=True)
FF=str(ROOT/'araclar/bin/ffmpeg'); FONT=str(ROOT/'araclar/fonts/Montserrat-ExtraBold.ttf')
OUT=B/'uzun/merakli-031-uzun-samuray-kale-savunmasi.mp4'
FPS=30;XF=12;SPEED=1.18;EXTRA=0.9
p=json.loads((B/'uzun/plan.json').read_text());scenes=p['sahneler']

def run(args):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True)
    if r.returncode:raise RuntimeError(f'ffmpeg exit={r.returncode}: '+r.stderr[-5000:])
    return r
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def wav_seconds(f):
    with wave.open(str(f)) as w:return w.getnframes()/w.getframerate()
def card(name,rows):
    dest=B/'uzun/kartlar'/f'{name}.png';dest.parent.mkdir(exist_ok=True)
    im=Image.new('RGB',(1920,1080),'#141a20');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1920,17),fill='#d93636');d.rectangle((0,1063,1920,1080),fill='#d93636')
    for text,y,size,color in rows:
        font=ImageFont.truetype(FONT,size)
        while d.textbbox((0,0),text,font=font)[2]>1740:
            size-=2;font=ImageFont.truetype(FONT,size)
        bb=d.textbbox((0,0),text,font=font);x=(1920-bb[2])/2
        d.text((x,y),text,font=font,fill=color)
    im.save(dest);return dest
intro=card('giris',[('EĞER SAMURAY OLSAYDIM',250,92,'white'),('SALDIRI BAŞLADIĞINDA',420,78,'#ef5252'),('MERAKLI · Osaka',670,44,'#d7e5df')])
date=card('tarih',[('1614 · Osaka',265,108,'white'),('KIŞ SEFERİ',445,64,'#ef5252'),('Meraklı kurgu · Çizimler temsili',665,38,'#d7e5df')])
closing=card('kapanis',[('SEN HANGİ GÖREVİ SEÇERDİN?',240,82,'white'),('HABER ULAŞTIRMAK · DESTEK OLMAK',430,52,'#ef5252'),('GÖREVİNİ SÜRDÜRMEK',550,50,'white'),('Seçimini yorumlara yaz.',750,38,'#d7e5df')])
subscribe=card('abone',[('KANALIMA ABONE',290,104,'white'),('OLMAYI UNUTMAYIN!',460,104,'#ef5252'),('MERAKLI · EĞER ORADA OLSAYDIM',750,40,'#d7e5df')])
clips=[];st=[];tracks=[]
def append(image,frames,id):
    start=clips[-1]['end_frame']-XF if clips else 0
    x={'id':id,'image':str(image.relative_to(ROOT)),'frames':frames,'start_frame':start,'end_frame':start+frames}
    clips.append(x);return x
append(intro,105,'giris');append(date,75,'tarih')
for i,s in enumerate(scenes):
    target=WORK/f'narr-{s["id"]}.wav';narr_isle(str(ROOT/s['anlatim']),str(target),SPEED)
    n=wav_seconds(target)
    frames=math.ceil((n+EXTRA+0.2)*FPS)
    start=clips[-1]['end_frame']-XF
    if 'gorsel2' in s:
        a=round(frames*.5);c1=append(ROOT/s['gorsel'],a,s['id']);c2=append(ROOT/s['gorsel2'],frames-a+XF,s['id']+'b')
        change=c2['start_frame']/FPS+XF/FPS/2
    else:append(ROOT/s['gorsel'],frames,s['id']);change=None
    nb=start/FPS+.5;ne=nb+n;end=(start+frames)/FPS
    st.append({'id':s['id'],'start':start/FPS,'narration_start':nb,'narration_end':ne,'end':end,'second_image_midpoint':change,'narration_speed':SPEED,'narration_pcm_seconds':n,'narration_source_sha256':sha(ROOT/s['anlatim'])})
    tracks.append({'file':str(target),'t':nb,'gain_db':0,'type':'narration','scene':s['id'],'duration':n})
    print('TIMELINE',s['id'],round(start/FPS,3),round(end,3),flush=True)
append(closing,105,'kapanis');append(subscribe,120,'abone')
total=clips[-1]['end_frame']/FPS
print('TOTAL_SECONDS',total,flush=True)
assert 300<=total<=720,total
voices=sorted(tracks,key=lambda x:x['t'])
for a,b in zip(voices,voices[1:]):assert a['t']+a['duration']<=b['t']
timeline={'fps':FPS,'transition_frames':XF,'narration_speed':SPEED,'total_seconds':total,'scene_count':20,'scene_image_count':25,'separate_card_count':4,'scene_timing':st,'clips':clips,'tracks':[{k:v for k,v in x.items() if k!='file'} for x in tracks],'music_used':False,'external_sfx_used':False,'subtitles':False}
(B/'uzun/ZAMAN-CIZELGESI.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Date,Montserrat ExtraBold,28,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,1,0,7,36,36,16,1\nStyle: Type,Montserrat ExtraBold,24,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,1,0,9,36,36,18,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
events=[]
def ev(a,b,style,text):events.append(f'Dialogue: 1,{ass_zaman(a)},{ass_zaman(b)},{style},,0,0,0,,{text}')
for i,(s,t) in enumerate(zip(scenes,st)):
    a=t['start']+XF/FPS/2;b=st[i+1]['start']+XF/FPS/2 if i+1<len(st) else t['end']-XF/FPS/2
    text=s['tarih_bandi'];fs=28
    while ImageFont.truetype(FONT,fs).getlength(text)>1390:fs-=1
    if s['id']=='s19':
        ev(a,t['second_image_midpoint'],'Date','{\\fs28}1614 KIŞI · AYRI AŞAMA')
        ev(t['second_image_midpoint'],b,'Date','{\\fs28}1615 · YAZ SEFERİ · AYRI AŞAMA · TEMSİLÎ')
    else:ev(a,b,'Date',f'{{\\fs{fs}}}'+text)
ev(st[0]['start']+.2,st[-1]['end']-.2,'Type','ÇİZİM: AI TEMSİLÎ')
ass=B/'uzun/etiketler.ass';ass.write_text(header+'\n'.join(events)+'\n')
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
print('MIX_READY',total,flush=True)
for i,c in enumerate(clips):
    dest=WORK/f'clip{i:02}.mp4';c['cache']=str(dest)
    expected=c['frames']/FPS;cache_ok=False
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
        tail=(f"drawbox=x=0:y=0:w=iw:h=62:color=black@0.72:t=fill:enable='between(t,{st[0]['start']+.2},{st[-1]['end']-.2})',"
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
