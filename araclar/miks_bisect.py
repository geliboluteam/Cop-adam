#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miks bisect: hangi giris amix'i uzatiyor?"""
import json, os, re, subprocess, sys

KOK = "/home/user/Cop-adam"
FFMPEG = f"{KOK}/araclar/bin/ffmpeg"

def sure_al(dosya):
    r = subprocess.run([FFMPEG, "-i", dosya], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", r.stderr)
    h, mnt, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h*3600 + mnt*60 + s

def tam_yol(p):
    return p if os.path.isabs(p) else os.path.join(KOK, p)

def dal_uret(plan, hiz, toplam, indexler):
    """indexler: kullanilacak (sahne_idx, efekt_idx or None for anlatim) listesi"""
    dallar, girisler = [], []
    g = 0
    zamanlama = []  # (sahne_bas) hesabi icin basit tekrar
    # zaman cizelgesini tekrar kur (video_yap ile ayni)
    sahneler = plan["sahneler"]; n = len(sahneler); XF = 0.5
    giris_ek = 0.9 if plan.get("baslik_karti") else 0.2
    raw = [sure_al(tam_yol(sa["anlatim"])) for sa in sahneler]
    narr = [r/hiz for r in raw]
    bas = 0.0
    for i, sa in enumerate(sahneler):
        a = narr[i]; ek = sa.get("ek_sure", 0.7)
        if i == 0: ek += giris_ek
        if i == n-1: ek = sa.get("ek_sure", 0.7) + 1.6
        anlatim_bas = bas + (giris_ek if i == 0 else 0.35)
        zamanlama.append((bas, anlatim_bas))
        bas += a + ek - XF
    # dallar
    for (si, ei) in indexler:
        sa = sahneler[si]
        sahne_bas = zamanlama[si][0]
        if ei is None:
            girisler += ["-i", tam_yol(sa["anlatim"])]
            d = int(zamanlama[si][1]*1000)
            dallar.append(f"[{g}:a]aresample=48000,aformat=channel_layouts=stereo,atempo={hiz:.4f},adelay={d}:all=1[a{g}]")
            g += 1
        else:
            ef = sa["efektler"][ei]
            girisler += ["-i", tam_yol(ef["dosya"])]
            kaz = pow(10, ef.get("kazanc_db", -14)/20)
            f = f"[{g}:a]aresample=48000,aformat=channel_layouts=stereo,volume={kaz:.3f}"
            if ef.get("dongu"):
                f += f",aloop=loop=-1:size=2e9,atrim=duration={ef.get('sure',5)}"
            d = int((sahne_bas + ef.get("t", 0))*1000)
            f += f",adelay={d}:all=1[a{g}]"
            dallar.append(f)
            g += 1
    return girisler, dallar, g

def miks_sure(girisler, dallar, g, etiket):
    if g == 0: return None
    miksis = "".join(f"[a{i}]" for i in range(g))
    fc = ";".join(dallar) + ";" + miksis + f"amix=inputs={g}:normalize=0:duration=longest[amix]"
    cikti = "/tmp/bisect.wav"
    r = subprocess.run([FFMPEG, "-y", *girisler, "-filter_complex", fc,
                        "-map", "[amix]", "-c:a", "pcm_s16le", cikti],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(etiket, "HATA:", r.stderr[-500:]); return None
    d = sure_al(cikti)
    print(f"{etiket}: {d:.2f} sn")
    return d

plan = json.load(open(sys.argv[1], encoding="utf-8"))
hiz = float(sys.argv[2])
toplam = float(sys.argv[3])

# tum (sahne, efekt) ciftleri + anlatimlar
tum = []
for si, sa in enumerate(plan["sahneler"]):
    tum.append((si, None))
    for ei in range(len(sa.get("efektler", []))):
        tum.append((si, ei))

# 1) anlatimlar yalniz
miks_sure(*dal_uret(plan, hiz, toplam, [x for x in tum if x[1] is None]), "ANLATIM")
# 2) efektler yalniz (muziksiz)
efs = [x for x in tum if x[1] is not None]
miks_sure(*dal_uret(plan, hiz, toplam, efs), "EFEKT")
# 3) efektleri tek tek gecer: once dongululer
dongulu = [x for x in efs if plan["sahneler"][x[0]]["efektler"][x[1]].get("dongu")]
miks_sure(*dal_uret(plan, hiz, toplam, dongulu), "DONGULU")
dongusuz = [x for x in efs if x not in dongulu]
miks_sure(*dal_uret(plan, hiz, toplam, dongusuz), "DONGUSUZ")
