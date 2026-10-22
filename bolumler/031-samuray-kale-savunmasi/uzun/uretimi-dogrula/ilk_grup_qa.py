#!/usr/bin/env python3
"""Mevcut B031 seslerinin tam decode/süre/hash kontrolü; insan dinlemesi değildir."""
from pathlib import Path
import hashlib,json,subprocess,re
ROOT=Path(__file__).resolve().parents[4];B=Path(__file__).resolve().parents[2]
F=ROOT/'araclar/bin/ffmpeg';plan=json.loads((B/'uzun/plan.taslak.json').read_text());clips=[]
for s in plan['sahneler']:
 p=ROOT/s['anlatim']
 if not p.exists():continue
 r=subprocess.run([str(F),'-hide_banner','-nostats','-i',str(p),'-af','silencedetect=noise=-40dB:d=0.15','-ar','48000','-ac','1','-f','s16le','pipe:1'],capture_output=True)
 assert r.returncode==0,(p,r.stderr.decode(errors='replace'))
 log=r.stderr.decode(errors='replace');assert 'error' not in log.lower(),log
 duration=len(r.stdout)/96000;assert duration>10
 match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',log);container=int(match[1])*3600+int(match[2])*60+float(match[3])
 starts=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',log)];ends=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',log)]
 lead=max(0,ends[0]-.08) if starts and starts[0]<.02 and ends and ends[0]<2.5 else 0
 tail=min(duration,starts[-1]+.12) if starts and ends and abs(ends[-1]-duration)<.1 and starts[-1]>duration-3 else duration
 assert tail>lead
 clips.append({'id':s['id'],'file':s['anlatim'],'voice_id':'voice-03','language':'tr','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_text_sha256':hashlib.sha256(s['anlatim_metin'].encode()).hexdigest(),'full_decode':'PASS','raw_duration_seconds':round(container,6),'decoded_pcm_seconds':round(duration,6),'trim_start':round(lead,6),'trim_end':round(tail,6),'silence_trimmed_1x_seconds':round(tail-lead,6),'trim_status':'proposed edge-silence trim; sourceMP3unchanged'})
 print('FULL_DECODE_PASS',s['id'],round(duration,3),flush=True)
report={'status':'MEVCUT_SESLER_TAM_DECODE_PASS_TUM_PAKET_DEGIL','voice_id':'voice-03','count':len(clips),'target_count':20,'total_raw_seconds':round(sum(c['raw_duration_seconds'] for c in clips),6),'total_decoded_pcm_seconds':round(sum(c['decoded_pcm_seconds'] for c in clips),6),'total_silence_trimmed_1x_seconds':round(sum(c['silence_trimmed_1x_seconds'] for c in clips),6),'final_speed_not_set':True,'source_mp3s_changed':False,'independent_listening_performed':False,'clips':clips,'note':'Yalnız üretilmiş sesler. Finalvideo süresi değil. Tam decode teknik kontroldür, konuşma içeriği insan dinlemesi yapıldı denmez. Önerilen trimler -40dB/0.15ssilencedetect +80msön/120mssonpay; finalmiksölçümüayrı.'}
(B/'ANLATIM-SURE-OLCUMU.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('SOURCE_AUDIO_QA_DONE',len(clips),report['total_decoded_pcm_seconds'])
