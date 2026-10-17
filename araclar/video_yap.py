#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Çöp Adam serisi video üretim hattı.
Kullanım: python3 araclar/video_yap.py <plan.json> <cikti.mp4>

plan.json biçimi:
{
  "baslik_karti": {"yazi1": "EĞER 1453'TE OLSAYDIM", "yazi2": "FETİH ORDUSUNDA İZCİ"},
  "kapanis_karti": {"yazi": "SIRADA NERE?", "alt": "YORUMLARA YAZ"},
  "muzik": {"dosya": "sfx/0ad/music/The_Hellespont.ogg", "kazanc_db": -22},
  "sahneler": [
    {
      "gorsel": "bolumler/001-.../gorseller/s1.png",
      "anlatim": "bolumler/001-.../ses/s1.mp3",
      "metin": "alt yazı metni (opsiyonel, anlatımdan farklıysa)",
      "tarih_bandi": "21-22 NİSAN 1453",
      "efektler": [
        {"dosya": "sfx/.../fire_loop.opus", "t": 0.0, "kazanc_db": -16, "dongu": true, "sure": 9.0}
      ],
      "ek_sure": 0.6
    }, ...
  ]
}
"""
import json, os, re, subprocess, sys, math

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = os.path.join(KOK, "araclar", "bin", "ffmpeg")
FONTS = os.path.join(KOK, "araclar", "fonts")

def calis(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG HATA:\n", r.stderr[-3500:])
        sys.exit(1)
    return r

def sure_al(dosya):
    r = subprocess.run([FFMPEG, "-i", dosya], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", r.stderr)
    if not m:
        print(f"Süre okunamadı: {dosya}"); sys.exit(1)
    h, mnt, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h*3600 + mnt*60 + s

def tam_yol(p):
    return p if os.path.isabs(p) else os.path.join(KOK, p)

def ass_zaman(t):
    h = int(t//3600); m = int((t%3600)//60); s = t%60
    return f"{h}:{m:02d}:{s:05.2f}"

def ass_olustur(plan, zamanlama, yol):
    # zamanlama: her sahne icin (bas, anlatim_bas, anlatim_son, son)
    satirlar = []
    sahneler = plan["sahneler"]
    for i, sa in enumerate(sahneler):
        bas, nb, ns, son = zamanlama[i]
        metin = sa.get("metin") or sa.get("anlatim_metin", "")
        if not metin:
            continue
        # metni <=2 satirlik parcalara bol
        parcalar = parcala(metin)
        toplam_harf = sum(len(p) for p in parcalar)
        t = nb
        for p in parcalar:
            oran = len(p)/max(toplam_harf,1)
            p_son = min(t + (ns-nb)*oran + 0.15, son)
            satirlar.append(f"Dialogue: 0,{ass_zaman(t)},{ass_zaman(p_son)},Caption,,0,0,0,,{p}")
            t = p_son - 0.15
        if sa.get("tarih_bandi"):
            satirlar.append(f"Dialogue: 1,{ass_zaman(bas+0.3)},{ass_zaman(son)},TarihBandi,,0,0,0,,{sa['tarih_bandi']}")
    # baslik karti
    bk = plan.get("baslik_karti")
    if bk:
        b0, s0 = zamanlama[0][0], zamanlama[0][0]+2.6
        satirlar.append(f"Dialogue: 2,{ass_zaman(b0)},{ass_zaman(s0)},BaslikKart,,0,0,0,,{bk.get('yazi1','')}")
        satirlar.append(f"Dialogue: 3,{ass_zaman(b0+0.25)},{ass_zaman(s0)},BaslikKart2,,0,0,0,,{bk.get('yazi2','')}")
    # kapanis karti
    kk = plan.get("kapanis_karti")
    if kk:
        kb, ks = zamanlama[-1][2], zamanlama[-1][3]+0.6
        satirlar.append(f"Dialogue: 4,{ass_zaman(kb+0.15)},{ass_zaman(ks)},Kapanis,,0,0,0,,{kk.get('yazi','')}")
        satirlar.append(f"Dialogue: 4,{ass_zaman(kb+0.45)},{ass_zaman(ks)},KapanisAlt,,0,0,0,,{kk.get('alt','')}")
    icerik = ASS_SABLON + "\n".join(satirlar) + "\n"
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)

def parcala(metin):
    metin = metin.strip()
    if len(metin) <= 46:
        return [metin]
    # noktalama veya ortadan ikiye
    for ayir in ["... ", ". ", "! ", "? ", ", "]:
        idx = metin.find(ayir, 20)
        if 20 < idx < len(metin)-20:
            return [metin[:idx+len(ayir)].strip(), metin[idx+len(ayir):].strip()]
    ort = len(metin)//2
    return [metin[:ort].strip(), metin[ort:].strip()]

ASS_SABLON = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Montserrat ExtraBold,58,&H00FFFFFF,&H000000FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,5,1,2,60,60,430,1
Style: TarihBandi,Montserrat ExtraBold,40,&H00FFFFFF,&H000000FF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,3,0,7,40,40,40,1
Style: BaslikKart,Montserrat ExtraBold,104,&H00FFFFFF,&H000000FF,&H00202020,&H96000000,0,0,0,0,100,100,2,0,1,6,2,5,60,60,60,1
Style: BaslikKart2,Montserrat ExtraBold,54,&H0027C4E8,&H000000FF,&H00202020,&H96000000,0,0,0,0,100,100,1,0,1,4,1,5,60,60,60,1
Style: Kapanis,Montserrat ExtraBold,84,&H00FFFFFF,&H000000FF,&H00202020,&H96000000,0,0,0,0,100,100,1,0,1,6,2,5,60,60,60,1
Style: KapanisAlt,Montserrat ExtraBold,46,&H00D94F45,&H000000FF,&H00202020,&H96000000,0,0,0,0,100,100,1,0,1,4,1,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def main():
    plan_yolu = sys.argv[1]
    cikti = sys.argv[2]
    with open(plan_yolu, encoding="utf-8") as f:
        plan = json.load(f)
    sahneler = plan["sahneler"]
    n = len(sahneler)
    XF = 0.5  # xfade suresi

    # 1) zaman cizelgesi (+ otomatik anlatim hizi)
    giris_ek = 0.9 if plan.get("baslik_karti") else 0.2
    raw = [sure_al(tam_yol(sa["anlatim"])) for sa in sahneler]
    ektop = 0.0
    for i, sa in enumerate(sahneler):
        ek = sa.get("ek_sure", 0.7)
        if i == n-1: ek += 1.6
        ektop += ek
    overhead = giris_ek + 0.35*(n-1) + ektop - XF*(n-1)
    hedef = plan.get("hedef_sure", 57.5)
    hiz = sum(raw) / max(hedef - overhead, 1.0)
    hiz = max(1.0, min(hiz, plan.get("hiz_max", 1.25)))
    narr = [r/hiz for r in raw]
    print(f"Anlatim hizi: x{hiz:.3f} (ham toplam {sum(raw):.1f} sn)")

    zamanlama = []
    bas = 0.0
    for i, sa in enumerate(sahneler):
        a_sure = narr[i]
        ek = sa.get("ek_sure", 0.7)
        if i == 0: ek += giris_ek
        if i == n-1: ek = sa.get("ek_sure", 0.7) + 1.6
        sure = a_sure + ek
        anlatim_bas = bas + (giris_ek if i == 0 else 0.35)
        zamanlama.append((bas, anlatim_bas, anlatim_bas + a_sure, bas + sure))
        bas += sure - XF
    toplam = zamanlama[-1][3]
    print(f"Toplam sure: {toplam:.1f} sn")

    # 2) ASS
    ass_yolu = cikti + ".ass"
    ass_olustur(plan, zamanlama, ass_yolu)

    # 3) ses miks
    ses_girisler, ses_filtre = [], []
    g_idx = 0
    for i, sa in enumerate(sahneler):
        sahne_bas = zamanlama[i][0]
        ses_girisler += ["-i", tam_yol(sa["anlatim"])]
        d = int(zamanlama[i][1]*1000)
        ses_filtre.append(f"[{g_idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                          f"atempo={hiz:.4f},volume=1.0,adelay={d}:all=1,"
                          f"asetpts=N/SR/TB[a{g_idx}]")
        g_idx += 1
        for ef in sa.get("efektler", []):
            ses_girisler += ["-i", tam_yol(ef["dosya"])]
            g = math.pow(10, ef.get("kazanc_db", -14)/20)
            f = f"[{g_idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.3f}"
            if ef.get("dongu"):
                f += f",aloop=loop=-1:size=2e9,atrim=duration={ef.get('sure',5)}"
            d = int((sahne_bas + ef.get("t", 0))*1000)
            f += f",adelay={d}:all=1"
            f += f",asetpts=N/SR/TB[a{g_idx}]"
            ses_filtre.append(f)
            g_idx += 1
    if plan.get("muzik"):
        ses_girisler += ["-i", tam_yol(plan["muzik"]["dosya"])]
        g = math.pow(10, plan["muzik"].get("kazanc_db", -22)/20)
        fade_out = max(toplam-3, 0.1)
        ses_filtre.append(
            f"[{g_idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.3f},"
            f"atrim=duration={toplam:.2f},afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out:.2f}:d=2.8,adelay=0:all=1,"
            f"asetpts=N/SR/TB[a{g_idx}]")
        g_idx += 1
    miksis = "".join(f"[a{i}]" for i in range(g_idx))
    ses_filtre.append(f"{miksis}amix=inputs={g_idx}:normalize=0:duration=longest,"
                      f"atrim=duration={toplam:.2f},apad=whole_dur={toplam:.2f},"
                      f"alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[amix]")
    ses_cikti = cikti + ".mix.m4a"
    calis([FFMPEG, "-y", *ses_girisler, "-filter_complex", ";".join(ses_filtre),
           "-map", "[amix]", "-c:a", "aac", "-b:a", "192k", ses_cikti])
    print(f"Miks suresi: {sure_al(ses_cikti):.2f} sn (hedef {toplam:.2f})")
    if os.environ.get("SADECE_MIX"):
        print("SADECE_MIX: video asamasi atlandi."); return

    # 4) sahne klipleri (Ken Burns)
    klip_yollari = []
    for i, sa in enumerate(sahneler):
        s_bas, _, _, s_son = zamanlama[i]
        d = max(s_son - s_bas, 0.8)
        klip = f"{cikti}.s{i}.mp4"
        klip_yollari.append((klip, d))
        kareler = max(int(d*30), 12)
        zoom_in = (i % 2 == 0)
        if zoom_in:
            z = f"1+{0.11:.4f}*on/{kareler}"
        else:
            z = f"1.11-{0.11:.4f}*on/{kareler}"
        # hafif yatay pan (sagdan sola / soldan saga sirayla)
        px = 40 if (i % 3 == 0) else -40
        filtre = (
            f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)+({px}*on/{kareler})':y='ih/2-(ih/zoom/2)'"
            f":d={kareler}:s=1080x1920:fps=30,format=yuv420p[v]"
        )
        calis([FFMPEG, "-y", "-loop", "1", "-i", tam_yol(sa["gorsel"]),
               "-filter_complex", filtre, "-map", "[v]",
               "-t", f"{d:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "medium",
               "-crf", "18", "-pix_fmt", "yuv420p", klip])

    # 5) xfade zinciri + altyazi + vinyet
    girisler = []
    for klip, _ in klip_yollari:
        girisler += ["-i", klip]
    video_filtre = []
    onceki = "[0:v]"
    offset = 0.0
    for i in range(1, n):
        offset += klip_yollari[i-1][1] - XF
        etiket = f"[vx{i}]"
        video_filtre.append(f"{onceki}[{i}:v]xfade=transition=fade:duration={XF}:offset={offset:.3f}{etiket}")
        onceki = etiket
    ass_gorunur = ass_yolu.replace("\\", "/").replace(":", "\\:")
    video_filtre.append(
        f"{onceki}vignette=PI/4.5,noise=alls=4:allf=t+u,"
        f"subtitles=filename='{ass_gorunur}':fontsdir='{FONTS}',format=yuv420p[vf]"
    )
    gecici = cikti + ".video.mp4"
    calis([FFMPEG, "-y", *girisler, "-filter_complex", ";".join(video_filtre),
           "-map", "[vf]", "-r", "30", "-c:v", "libx264", "-preset", "medium",
           "-crf", "20", "-pix_fmt", "yuv420p", gecici])

    # 6) birlestir
    calis([FFMPEG, "-y", "-i", gecici, "-i", ses_cikti,
           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
           "-movflags", "+faststart", cikti])

    # temizlik
    for klip, _ in klip_yollari:
        os.remove(klip)
    os.remove(gecici); os.remove(ses_cikti)
    print(f"BITTI: {cikti}  ({os.path.getsize(cikti)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
