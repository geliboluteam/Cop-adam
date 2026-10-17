#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Çöp Adam / MERAKLI serisi video üretim hattı.
Kullanım: python3 araclar/video_yap.py <plan.json> <cikti.mp4>

Akış:
 0) Anlatım: TTS sessizlik sıkıştırma (baş/orta/son duraklar) + otomatik atempo
 1) Zaman çizelgesi (xfade örtüşmeli)
 2) ASS altyazı üretimi
 3) Ses miks (efekt + müzik + anlatı; loudnorm -14 LUFS)
 4) Sahne klipleri: Ken Burns pan/zoom (1080x1920@30)
 5) xfade zinciri + vinyet + film greni + altyazı
 6) Birleştirme (MP4, faststart)

plan.json alanları için bkz. README / mevcut plan dosyaları.
"""
import json, os, re, subprocess, sys, math

from PIL import ImageFont

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = os.path.join(KOK, "araclar", "bin", "ffmpeg")
FONTS = os.path.join(KOK, "araclar", "fonts")
F_KART_TTF = os.path.join(FONTS, "Montserrat-ExtraBold.ttf")


def kart_olc(metin, boyut, maxw):
    """Kart satırı için (fs, satirlar, yukseklik) döndürür.

    Taşma yoksa tek satır; taşıyorsa kelime sarma; yine sığmazsa punto
    küçültme. Yükseklik = satır sayısı × (ascent+descent). Böylece kart
    yazıları HİÇBİR KOŞULDA üst üste binmez (2026-10-17 kullanıcı kuralı).
    """
    def olc(fs, m):
        f = ImageFont.truetype(F_KART_TTF, fs)
        asc, desc = f.getmetrics()
        w = f.getbbox(m)[2] - f.getbbox(m)[0]
        return w, asc + desc

    if not metin:
        return boyut, [""], 0
    w, h = olc(boyut, metin)
    if w <= maxw:
        return boyut, [metin], h
    kelimeler = metin.split()
    for fs in range(boyut, 29, -2):
        f = ImageFont.truetype(F_KART_TTF, fs)
        asc, desc = f.getmetrics()
        satirlar, cur = [], ""
        for k in kelimeler:
            deneme = (cur + " " + k).strip()
            if f.getbbox(deneme)[2] <= maxw or not cur:
                cur = deneme
            else:
                satirlar.append(cur)
                cur = k
        if cur:
            satirlar.append(cur)
        if len(satirlar) <= 3 and all(f.getbbox(s)[2] - f.getbbox(s)[0] <= maxw for s in satirlar):
            return fs, satirlar, (asc + desc) * len(satirlar)
    return 30, [metin], olc(30, metin)[1]


def kart_yerlesim(metin1, metin2, fs1, fs2, W, H, cy):
    """İki kart satırını grup halinde cy merkezine AYRI AYRI istifler.

    Dönüş: (override1, metin1', override2, metin2') — ASS \\pos/\\fs dahil.
    Boş metin gelirse ilgili satır atlanır (None döner).
    """
    fs1b, s1, h1 = kart_olc(metin1, fs1, W * 0.88)
    fs2b, s2, h2 = kart_olc(metin2, fs2, W * 0.88)
    gap = 0.045 * H
    if not metin2:
        o1 = f"{{\\an5\\pos({W // 2},{round(cy)})" + (f"\\fs{fs1b}" if fs1b != fs1 else "") + "}"
        return o1, "\\N".join(s1), None, None
    if not metin1:
        o2 = f"{{\\an5\\pos({W // 2},{round(cy)})" + (f"\\fs{fs2b}" if fs2b != fs2 else "") + "}"
        return None, None, o2, "\\N".join(s2)
    toplam = h1 + gap + h2
    y1 = cy - toplam / 2 + h1 / 2
    y2 = cy + toplam / 2 - h2 / 2
    o1 = f"{{\\an5\\pos({W // 2},{round(y1)})" + (f"\\fs{fs1b}" if fs1b != fs1 else "") + "}"
    o2 = f"{{\\an5\\pos({W // 2},{round(y2)})" + (f"\\fs{fs2b}" if fs2b != fs2 else "") + "}"
    return o1, "\\N".join(s1), o2, "\\N".join(s2)


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

def narr_isle(kaynak, cikti, hiz):
    """TTS durak sıkıştırma + opsiyonel atempo + timestamp temizliği."""
    fc = ("aresample=48000,aformat=channel_layouts=stereo,"
          "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,"
          "silenceremove=stop_periods=-1:stop_duration=0.42:stop_threshold=-42dB,"
          "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.18,areverse")
    if abs(hiz - 1.0) > 1e-3:
        fc += f",atempo={hiz:.4f}"
    fc += ",asetpts=N/SR/TB"
    calis([FFMPEG, "-y", "-i", kaynak, "-af", fc, "-c:a", "pcm_s16le", cikti])

def ass_zaman(t):
    h = int(t//3600); m = int((t%3600)//60); s = t%60
    return f"{h}:{m:02d}:{s:05.2f}"

def parcala(metin):
    metin = metin.strip()
    if len(metin) <= 46:
        return [metin]
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

def ass_sablon(dikey=True):
    if dikey:
        return ASS_SABLON
    return (ASS_SABLON
            .replace("PlayResX: 1080", "PlayResX: 1920")
            .replace("PlayResY: 1920", "PlayResY: 1080")
            .replace("Style: Caption,Montserrat ExtraBold,58,", "Style: Caption,Montserrat ExtraBold,62,")
            .replace(",2,60,60,430,1", ",2,60,60,250,1")
            .replace("Style: BaslikKart,Montserrat ExtraBold,104,", "Style: BaslikKart,Montserrat ExtraBold,88,")
            .replace("Style: BaslikKart2,Montserrat ExtraBold,54,", "Style: BaslikKart2,Montserrat ExtraBold,46,")
            .replace("Style: Kapanis,Montserrat ExtraBold,84,", "Style: Kapanis,Montserrat ExtraBold,70,")
            .replace("Style: KapanisAlt,Montserrat ExtraBold,46,", "Style: KapanisAlt,Montserrat ExtraBold,38,"))

def ass_olustur(plan, zamanlama, yol, dikey=True):
    satirlar = []
    sahneler = plan["sahneler"]
    altyazi_var = plan.get("altyazi", True)  # Bölüm 04+ : false
    for i, sa in enumerate(sahneler):
        bas, nb, ns, son = zamanlama[i]
        metin = sa.get("anlatim_metin", "")
        if altyazi_var and metin:
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
    bk = plan.get("baslik_karti")
    if bk:
        b0, s0 = zamanlama[0][0], zamanlama[0][0]+2.6
        W, H = (1080, 1920) if dikey else (1920, 1080)
        o1, m1, o2, m2 = kart_yerlesim(bk.get("yazi1", ""), bk.get("yazi2", ""),
                                        104 if dikey else 88, 54 if dikey else 46,
                                        W, H, H * 0.46)
        if o1:
            satirlar.append(f"Dialogue: 2,{ass_zaman(b0)},{ass_zaman(s0)},BaslikKart,,0,0,0,,{o1}{m1}")
        if o2:
            satirlar.append(f"Dialogue: 3,{ass_zaman(b0+0.25)},{ass_zaman(s0)},BaslikKart2,,0,0,0,,{o2}{m2}")
    kk = plan.get("kapanis_karti")
    if kk:
        kb, ks = zamanlama[-1][2], zamanlama[-1][3]+0.6
        W, H = (1080, 1920) if dikey else (1920, 1080)
        o1, m1, o2, m2 = kart_yerlesim(kk.get("yazi", ""), kk.get("alt", ""),
                                        84 if dikey else 70, 46 if dikey else 38,
                                        W, H, H * 0.46)
        if o1:
            satirlar.append(f"Dialogue: 4,{ass_zaman(kb+0.15)},{ass_zaman(ks)},Kapanis,,0,0,0,,{o1}{m1}")
        if o2:
            satirlar.append(f"Dialogue: 4,{ass_zaman(kb+0.45)},{ass_zaman(ks)},KapanisAlt,,0,0,0,,{o2}{m2}")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(ass_sablon(dikey) + "\n".join(satirlar) + "\n")

def main():
    plan_yolu = sys.argv[1]
    cikti = sys.argv[2]
    with open(plan_yolu, encoding="utf-8") as f:
        plan = json.load(f)
    sahneler = plan["sahneler"]
    n = len(sahneler)
    XF = 0.5
    giris_ek = 0.9 if plan.get("baslik_karti") else 0.2
    dikey = plan.get("format", "9:16") != "16:9"
    PRESET = plan.get("encode_preset", "medium")
    CRF = plan.get("crf", 20 if dikey else 23)   # uzun video: GitHub 100MB siniri icin daha sikistirma
    MAXRATE = plan.get("maxrate", "1800k" if not dikey else None)
    if dikey:
        VW, VH, OW, OH = 1080, 1920, 2160, 3840
    else:
        VW, VH, OW, OH = 1920, 1080, 3840, 2160

    # ek sureler
    ektop = 0.0
    for i, sa in enumerate(sahneler):
        ek = sa.get("ek_sure", 0.4)
        if i == n-1: ek += 1.6
        ektop += ek
    overhead = giris_ek + 0.35*(n-1) + ektop - XF*(n-1)
    hedef = plan.get("hedef_sure", 57.5)
    hiz_cap = plan.get("hiz_max", 1.25)

    # --- Anlatim isleme: pass A (sessizlik sikistirma, hiz=1) ---
    gecA = [f"{cikti}.nA{i}.wav" for i in range(n)]
    for i, sa in enumerate(sahneler):
        narr_isle(tam_yol(sa["anlatim"]), gecA[i], 1.0)
    dA = [sure_al(g) for g in gecA]
    ham = sum(sure_al(tam_yol(sa["anlatim"])) for sa in sahneler)
    hiz = sum(dA) / max(hedef - overhead, 1.0)
    hiz = max(1.0, min(hiz, hiz_cap))
    print(f"Ham anlatim: {ham:.1f} sn | sıkıştırılmış: {sum(dA):.1f} sn | hız: x{hiz:.3f} (cap {hiz_cap})")

    # --- pass B (nihai hız) ---
    narr_dosya = [f"{cikti}.n{i}.wav" for i in range(n)]
    for i, sa in enumerate(sahneler):
        if abs(hiz-1.0) > 1e-3:
            narr_isle(tam_yol(sa["anlatim"]), narr_dosya[i], hiz)
        else:
            os.replace(gecA[i], narr_dosya[i])
    narr = [sure_al(g) for g in narr_dosya]
    for g in gecA:
        if os.path.exists(g): os.remove(g)

    # --- zaman cizelgesi ---
    zamanlama = []
    bas = 0.0
    for i, sa in enumerate(sahneler):
        a_sure = narr[i]
        ek = sa.get("ek_sure", 0.4)
        if i == 0: ek += giris_ek
        if i == n-1: ek = sa.get("ek_sure", 0.4) + 1.6
        sure = a_sure + ek
        anlatim_bas = bas + (giris_ek if i == 0 else 0.35)
        zamanlama.append((bas, anlatim_bas, anlatim_bas + a_sure, bas + sure))
        bas += sure - XF
    toplam = zamanlama[-1][3]
    print(f"Toplam sure: {toplam:.1f} sn")
    if dikey and toplam > 59.5:
        print(f"UYARI: {toplam:.1f} sn > 59.5 sn (Shorts)! ek_sure/hedef_sure ayarlayın.")

    # --- ASS ---
    ass_yolu = cikti + ".ass"
    ass_olustur(plan, zamanlama, ass_yolu, dikey)

    # --- ses miks ---
    ses_girisler, ses_filtre = [], []
    g_idx = 0
    for i, sa in enumerate(sahneler):
        sahne_bas = zamanlama[i][0]
        ses_girisler += ["-i", narr_dosya[i]]
        d = int(zamanlama[i][1]*1000)
        ses_filtre.append(f"[{g_idx}:a]volume=1.0,adelay={d}:all=1,asetpts=N/SR/TB[a{g_idx}]")
        g_idx += 1
        for ef in sa.get("efektler", []):
            ses_girisler += ["-i", tam_yol(ef["dosya"])]
            g = math.pow(10, ef.get("kazanc_db", -14)/20)
            f = f"[{g_idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.3f}"
            if ef.get("dongu"):
                f += f",aloop=loop=-1:size=2e9,atrim=duration={ef.get('sure',5)}"
            d = int((sahne_bas + ef.get("t", 0))*1000)
            f += f",adelay={d}:all=1,asetpts=N/SR/TB[a{g_idx}]"
            ses_filtre.append(f)
            g_idx += 1
    if plan.get("muzik"):
        ses_girisler += ["-i", tam_yol(plan["muzik"]["dosya"])]
        g = math.pow(10, plan["muzik"].get("kazanc_db", -22)/20)
        fade_out = max(toplam-3, 0.1)
        ses_filtre.append(
            f"[{g_idx}:a]aresample=48000,aformat=channel_layouts=stereo,aloop=loop=-1:size=2e9,volume={g:.3f},"
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
    for g in narr_dosya:
        os.remove(g)
    if os.environ.get("SADECE_MIX"):
        print("SADECE_MIX: video asamasi atlandi."); return

    # --- sahne klipleri (Ken Burns) ---
    klip_yollari = []
    for i, sa in enumerate(sahneler):
        s_bas, _, _, s_son = zamanlama[i]
        d = max(s_son - s_bas, 0.8)
        klip = f"{cikti}.s{i}.mp4"
        klip_yollari.append((klip, d))
        kareler = max(int(d*30), 12)
        if i % 2 == 0:
            z = f"1+{0.11:.4f}*on/{kareler}"
        else:
            z = f"1.11-{0.11:.4f}*on/{kareler}"
        px = 40 if (i % 3 == 0) else -40
        filtre = (
            f"[0:v]scale={OW}:{OH}:force_original_aspect_ratio=increase,crop={OW}:{OH},"
            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)+({px}*on/{kareler})':y='ih/2-(ih/zoom/2)'"
            f":d={kareler}:s={VW}x{VH}:fps=30,format=yuv420p[v]"
        )
        calis([FFMPEG, "-y", "-loop", "1", "-i", tam_yol(sa["gorsel"]),
               "-filter_complex", filtre, "-map", "[v]",
               "-t", f"{d:.3f}", "-r", "30", "-c:v", "libx264", "-preset", PRESET,
               "-crf", "18", "-pix_fmt", "yuv420p", klip])

    # --- xfade + vinyet + altyazi ---
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
    final_args = [FFMPEG, "-y", *girisler, "-filter_complex", ";".join(video_filtre),
                  "-map", "[vf]", "-r", "30", "-c:v", "libx264", "-preset", PRESET,
                  "-crf", str(CRF), "-pix_fmt", "yuv420p"]
    if MAXRATE:
        final_args += ["-maxrate", MAXRATE, "-bufsize", str(int(MAXRATE[:-1])*2) + MAXRATE[-1]]
    final_args.append(gecici)
    calis(final_args)

    # --- birlestir ---
    calis([FFMPEG, "-y", "-i", gecici, "-i", ses_cikti,
           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
           "-movflags", "+faststart", cikti])

    for klip, _ in klip_yollari:
        os.remove(klip)
    os.remove(gecici); os.remove(ses_cikti)
    print(f"BITTI: {cikti}  ({os.path.getsize(cikti)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
