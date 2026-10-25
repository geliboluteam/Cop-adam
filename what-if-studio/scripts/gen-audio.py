#!/usr/bin/env python3
"""Sound, synthesised in code: the three stems of an episode, without an API.

The skill's step 7 (scripts/sfx.py) asks ElevenLabs for the voice and every effect. When there is no key (or you want
to block out the sound before spending credits), this script makes the same three stems offline and leaves them in the
same slots, so the engine, the mix and the picture don't know the difference:

    public/<slug>/voice.wav   a formant-synthesised placeholder "voice" (vowels, not words: it marks the rhythm)
    public/<slug>/sfx.wav     one shot per event, on the frame it names
    public/<slug>/music.wav   a chord bed under the whole episode

Pure standard library: no numpy, no ffmpeg, no network. Everything is deterministic (same audio.json, same WAV), so a
regenerate never moves a hit:

    python scripts/gen-audio.py ses-testi [--out-dir DIR]

Reads src/episodes/<slug>/audio.json (write it; see the one in ses-testi) and prints a level report per stem: peak and
RMS in dBFS, plus the events it placed. The engine's per-stem volumes live in the episode's timeline.json `audio`.
"""

import json
import math
import random
import sys
import wave
from array import array
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # the studio folder
TAU = 2.0 * math.pi

# ---------- buffers ----------


def zeros(n):
    return array('f', bytes(4 * n))


def add(dst, src, at, gain=1.0):
    """Mix src into dst at sample `at` (clips to the buffer, never grows it)."""
    i = max(0, int(at))
    for k in range(len(src)):
        j = i + k
        if j >= len(dst):
            break
        dst[j] += src[k] * gain


def peak(x):
    return max((abs(v) for v in x), default=0.0)


def rms(x):
    if not len(x):
        return 0.0
    return math.sqrt(sum(v * v for v in x) / len(x))


def db(v):
    return -120.0 if v <= 1e-9 else 20.0 * math.log10(v)


def normalize(x, level_db):
    p = peak(x)
    if p > 1e-9:
        g = (10.0 ** (level_db / 20.0)) / p
        for i in range(len(x)):
            x[i] *= g
    return x


# ---------- building blocks ----------


def env(n, sr, a=0.01, d=0.0, s=1.0, r=0.15):
    """attack / decay / sustain / release, in seconds, as a gain curve over n samples."""
    A, D, R = int(a * sr), int(d * sr), int(r * sr)
    S = max(0, n - A - D - R)
    out = array('f', bytes(4 * n))
    for i in range(n):
        if i < A:
            g = i / max(1, A)
        elif i < A + D:
            g = 1.0 - (1.0 - s) * ((i - A) / max(1, D))
        elif i < A + D + S:
            g = s
        else:
            k = (i - A - D - S) / max(1, R)
            g = s * max(0.0, 1.0 - k)
        out[i] = g
    return out


def biquad(x, kind, f0, q, sr, gain_db=0.0):
    """RBJ biquad: kind is 'bp' (band-pass, 0 dB peak) or 'lp' / 'hp'."""
    w = TAU * min(f0, sr * 0.45) / sr
    cw, sw = math.cos(w), math.sin(w)
    alpha = sw / (2.0 * q)
    if kind == 'bp':
        b0, b1, b2 = alpha, 0.0, -alpha
        a0, a1, a2 = 1.0 + alpha, -2.0 * cw, 1.0 - alpha
    elif kind == 'lp':
        b0, b1, b2 = (1.0 - cw) / 2.0, 1.0 - cw, (1.0 - cw) / 2.0
        a0, a1, a2 = 1.0 + alpha, -2.0 * cw, 1.0 - alpha
    else:
        b0, b1, b2 = (1.0 + cw) / 2.0, -(1.0 + cw), (1.0 + cw) / 2.0
        a0, a1, a2 = 1.0 + alpha, -2.0 * cw, 1.0 - alpha
    g = 10.0 ** (gain_db / 20.0)
    b0, b1, b2 = b0 / a0 * g, b1 / a0 * g, b2 / a0 * g
    a1, a2 = a1 / a0, a2 / a0
    y = array('f', bytes(4 * len(x)))
    x1 = x2 = y1 = y2 = 0.0
    for i, v in enumerate(x):
        o = b0 * v + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1 = x1, v
        y2, y1 = y1, o
        y[i] = o
    return y


def onepole_lp(x, fc, sr):
    k = 1.0 - math.exp(-TAU * fc / sr)
    y = array('f', bytes(4 * len(x)))
    acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc)
        y[i] = acc
    return y


def osc(freq, n, sr, shape='sine'):
    """A steady tone; freq may be a callable f(t) for glides and vibrato."""
    out = array('f', bytes(4 * n))
    phase = 0.0
    for i in range(n):
        f = freq(i / sr) if callable(freq) else freq
        phase += f / sr
        if phase >= 1.0:
            phase -= 1.0
        if shape == 'sine':
            out[i] = math.sin(TAU * phase)
        elif shape == 'tri':
            out[i] = 2.0 * abs(2.0 * (phase - math.floor(phase + 0.5))) - 1.0
        else:  # saw, the glottal source
            out[i] = 2.0 * phase - 1.0
    return out


def noise(n, seed=1):
    r = random.Random(seed)
    return array('f', [r.uniform(-1.0, 1.0) for _ in range(n)])


def reverb(x, sr, mix=0.24):
    """Schroeder: four combs in parallel, then two allpasses. Cheap, but it puts the sound in a room."""
    out = array('f', bytes(4 * len(x)))
    combs = [(0.0297, 0.86), (0.0371, 0.84), (0.0411, 0.82), (0.0437, 0.80)]
    wet = zeros(len(x))
    for sec, fb in combs:
        d = max(1, int(sec * sr))
        delay = zeros(d)
        j = 0
        for i, v in enumerate(x):
            dv = delay[j]
            wet[i] += dv * 0.25
            delay[j] = v + dv * fb
            j = (j + 1) % d
    for sec, g in [(0.005, 0.7), (0.0017, 0.7)]:
        d = max(1, int(sec * sr))
        delay = zeros(d)
        j = 0
        for i, v in enumerate(wet):
            dv = delay[j]
            o = -g * v + dv
            delay[j] = v + g * o
            wet[i] = o
            j = (j + 1) % d
    for i in range(len(x)):
        out[i] = x[i] * (1.0 - mix) + wet[i] * mix
    return out


# ---------- the voice: vowels, not words ----------

FORMANTS = {
    'a': (700, 1100, 2500),
    'e': (530, 1840, 2480),
    'i': (270, 2290, 3010),
    'o': (570, 840, 2410),
    'u': (300, 870, 2240),
}


def voice_phrase(sr, vowels, dur, f0, seed=1):
    """A glottal saw through three formant band-passes, one vowel at a time, with a fall in pitch.

    It is not speech: it is the shape of a line of speech, which is exactly what a block-out needs (how long the
    sentence is, where it lands, how it ends).
    """
    n = int(dur * sr)

    def pitch(t):
        fall = 1.0 - 0.16 * (t / dur)
        bite = 1.0 + 0.05 * math.sin(TAU * 5.4 * t)  # a little vibrato, so it reads as a voice not a synth
        return f0 * fall * bite

    src = osc(pitch, n, sr, 'saw')
    src = onepole_lp(src, 1600, sr)  # tilt the source before the formants, or it buzzes
    # breathe: a touch of noise on the same envelope keeps it from sounding like a test tone
    br = noise(n, seed)
    br = biquad(biquad(br, 'bp', 1400, 1.2, sr), 'bp', 2600, 1.4, sr)
    out = zeros(n)
    per = max(1, n // max(1, len(vowels)))
    for vi, v in enumerate(vowels):
        f1, f2, f3 = FORMANTS.get(v, FORMANTS['a'])
        a = vi * per
        b = min(n, a + per + int(0.03 * sr))  # a small overlap so the vowels join
        seg = src[a:b]
        if not len(seg):
            continue
        e = env(len(seg), sr, a=min(0.03, dur / 6), d=0.02, s=0.85, r=min(0.09, dur / 5))
        mixed = zeros(len(seg))
        for (fc, q, gain_db, g) in [(f1, 9.0, 6.0, 1.0), (f2, 11.0, 2.0, 0.55), (f3, 13.0, -2.0, 0.22)]:
            f = biquad(seg, 'bp', fc, q, sr, gain_db)
            for i in range(len(f)):
                mixed[i] += f[i] * g
        bseg = br[a:b]
        for i in range(len(mixed)):
            mixed[i] = (mixed[i] + bseg[i] * 0.02) * e[i]
        add(out, mixed, a)
    out = onepole_lp(out, 5200, sr)
    return reverb(out, sr, mix=0.18)


# ---------- the effects ----------


def sfx(sr, kind, dur=None, seed=1):
    if kind == 'pop':
        n = int(0.14 * sr)
        t = osc(lambda x: 420 + 900 * math.exp(-x * 70), n, sr, 'sine')
        return [v * e for v, e in zip(t, env(n, sr, 0.002, 0.02, 0.4, 0.1))]
    if kind == 'ding':
        n = int((dur or 0.9) * sr)
        out = zeros(n)
        for k, (f, g) in enumerate([(1240, 1.0), (1860, 0.45), (2790, 0.22)]):
            tone = osc(f, n, sr, 'sine')
            e = env(n, sr, 0.004, 0.10, 0.22, 0.65)
            for i in range(n):
                out[i] += tone[i] * e[i] * g
        return reverb(out, sr, 0.3)
    if kind == 'whoosh':
        n = int((dur or 0.5) * sr)
        nz = noise(n, seed)
        # a swept band-pass: the air passing the ear
        out = zeros(n)
        CH = 8
        for c in range(CH):
            a, b = c * n // CH, (c + 1) * n // CH
            fc = 380 + 4200 * (c / (CH - 1)) ** 1.4
            f = biquad(nz[a:b], 'bp', fc, 1.6, sr)
            add(out, f, a - int(0.02 * sr))
        e = env(n, sr, 0.06, 0.05, 0.7, 0.30)
        return [v * g for v, g in zip(out, e)]
    if kind == 'boom':
        n = int((dur or 1.1) * sr)
        low = osc(lambda x: 58 - 16 * min(1.0, x / 0.7), n, sr, 'sine')
        thud = biquad(noise(n, seed + 7), 'lp', 240, 0.9, sr)
        e = env(n, sr, 0.003, 0.16, 0.32, 0.85)
        out = [(low[i] * 0.9 + thud[i] * 0.35) * e[i] for i in range(n)]
        return reverb(out, sr, 0.26)
    if kind == 'click':
        n = int(0.06 * sr)
        nz = biquad(noise(n, seed), 'bp', 2400, 2.0, sr)
        e = env(n, sr, 0.001, 0.008, 0.2, 0.03)
        return [v * g for v, g in zip(nz, e)]
    if kind == 'power_down':
        n = int((dur or 1.2) * sr)
        tone = osc(lambda x: 320 * math.exp(-x * 2.4) + 40, n, sr, 'tri')
        e = env(n, sr, 0.01, 0.2, 0.5, 0.8)
        out = [v * g for v, g in zip(tone, e)]
        return reverb(out, sr, 0.22)
    if kind == 'room_tone':
        n = int((dur or 2.0) * sr)
        nz = biquad(biquad(noise(n, seed), 'lp', 480, 0.7, sr), 'hp', 70, 0.7, sr)
        e = env(n, sr, 0.35, 0.0, 1.0, 0.45)
        return [v * g * 0.5 for v, g in zip(nz, e)]
    raise SystemExit(f'gen-audio: unknown effect "{kind}"')


# ---------- the music bed ----------

# The same four-bar progressions the lab offers (lab/synth.ts PROGRESSIONS): audio.json's `mix.key` picks one.
PROGRESSIONS = {
    'Am': [
        {'name': 'Am', 'notes': [['A', 2, 1.0], ['C', 3, 0.5], ['E', 3, 0.45]]},
        {'name': 'F', 'notes': [['F', 2, 1.0], ['A', 2, 0.55], ['C', 3, 0.45]]},
        {'name': 'C', 'notes': [['C', 3, 1.0], ['E', 3, 0.5], ['G', 3, 0.4]]},
        {'name': 'G', 'notes': [['G', 2, 1.0], ['B', 2, 0.55], ['D', 3, 0.45]]},
    ],
    'Dm': [
        {'name': 'Dm', 'notes': [['D', 3, 1.0], ['F', 3, 0.5], ['A', 3, 0.45]]},
        {'name': 'Bb', 'notes': [['A#', 2, 1.0], ['D', 3, 0.55], ['F', 3, 0.45]]},
        {'name': 'F', 'notes': [['F', 2, 1.0], ['A', 2, 0.5], ['C', 3, 0.4]]},
        {'name': 'C', 'notes': [['C', 3, 1.0], ['E', 3, 0.5], ['G', 3, 0.4]]},
    ],
    'Em': [
        {'name': 'Em', 'notes': [['E', 2, 1.0], ['G', 2, 0.5], ['B', 2, 0.45]]},
        {'name': 'C', 'notes': [['C', 3, 1.0], ['E', 3, 0.55], ['G', 3, 0.4]]},
        {'name': 'G', 'notes': [['G', 2, 1.0], ['B', 2, 0.5], ['D', 3, 0.45]]},
        {'name': 'D', 'notes': [['D', 3, 1.0], ['F#', 3, 0.5], ['A', 3, 0.4]]},
    ],
}

STEPS = {  # semitones above the key's root, so a chord is written as names
    'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11,
}


def note_hz(name, octave):
    return 440.0 * 2.0 ** ((STEPS[name] - 9) / 12.0 + (octave - 4))


def music(cfg, sr, secs):
    n = int(secs * sr)
    out = zeros(n)
    chords = cfg['chords']
    step = secs / len(chords)
    for ci, ch in enumerate(chords):
        start = ci * step
        dur = step * 1.02  # overlap a hair, so the bed breathes instead of clicking
        for ni, (nm, oc, g) in enumerate(ch['notes']):
            f = note_hz(nm, oc)
            ln = int(dur * sr)
            det = osc(lambda x, f=f: f * (1.0 + 0.0016 * math.sin(TAU * 0.7 * x)), ln, sr, 'tri')
            tone = osc(f, ln, sr, 'sine')
            e = env(ln, sr, a=min(0.5, dur * 0.35), d=0.1, s=0.75, r=min(0.55, dur * 0.4))
            trem = [1.0 for _ in range(ln)]
            for i in range(ln):
                trem[i] = 0.85 + 0.15 * math.sin(TAU * 0.9 * i / sr + ni)
            seg = [(tone[i] * 0.7 + det[i] * 0.3) * e[i] * trem[i] * g for i in range(ln)]
            add(out, seg, int(start * sr))
    # a low pulse on the bar line: the heartbeat under the bed
    bar = secs / max(1, cfg.get('bars', len(chords)))
    t = 0.0
    while t < secs - 0.2:
        ln = int(0.5 * sr)
        p = osc(lambda x: 54 - 10 * min(1.0, x / 0.35), ln, sr, 'sine')
        e = env(ln, sr, 0.004, 0.1, 0.25, 0.35)
        add(out, [v * g * 0.5 for v, g in zip(p, e)], int(t * sr))
        t += bar
    out = onepole_lp(out, 3600, sr)
    return reverb(out, sr, mix=0.3)


# ---------- write ----------


def write_wav(path, x, sr):
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = array('h', bytes(2 * len(x)))
    for i, v in enumerate(x):
        s = max(-1.0, min(1.0, v))
        pcm[i] = int(s * 32000)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit('usage: python scripts/gen-audio.py <slug> [--out-dir DIR]')
    slug = args[0]
    cfg_path = ROOT / 'src' / 'episodes' / slug / 'audio.json'
    if not cfg_path.exists():
        raise SystemExit(f'gen-audio: no {cfg_path}')
    cfg = json.loads(cfg_path.read_text())
    out_dir = ROOT / 'public' / slug
    if '--out-dir' in args:
        out_dir = Path(args[args.index('--out-dir') + 1])

    # The `mix` block is what the lab writes: it is the one place the two agree. The key picks the progression
    # (unless the file spells its own chords), the pitch scales every phrase's f0 from the 150 Hz base.
    mix = cfg.get('mix', {})
    key = mix.get('key')
    if key and key in PROGRESSIONS:
        cfg['music']['chords'] = PROGRESSIONS[key]
    pitch_scale = float(mix.get('pitch', 150)) / 150.0

    sr = cfg.get('sampleRate', 32000)
    secs = float(cfg['seconds'])
    n = int(secs * sr)

    # voice
    vcfg = cfg.get('voice', {})
    voice = zeros(n)
    for i, ph in enumerate(vcfg.get('phrases', [])):
        seg = voice_phrase(sr, ph['vowels'], float(ph['dur']), float(ph.get('f0', 148)) * pitch_scale, seed=11 + i)
        add(voice, seg, int(float(ph['at']) * sr) if 'at' in ph else int(sum(p['dur'] for p in vcfg['phrases'][:i]) * sr))
    normalize(voice, vcfg.get('levelDb', -6))

    # effects
    scfg = cfg.get('sfx', {})
    sfxb = zeros(n)
    placed = []
    for i, ev in enumerate(scfg.get('events', [])):
        seg = sfx(sr, ev['kind'], ev.get('dur'), seed=101 + i)
        at = int(float(ev['at']) * sr)
        add(sfxb, seg, at, ev.get('gain', 1.0))
        placed.append((ev['kind'], float(ev['at'])))
    normalize(sfxb, scfg.get('levelDb', -12))

    # music
    mus = music(cfg['music'], sr, secs)
    normalize(mus, cfg['music'].get('levelDb', -20))

    write_wav(out_dir / 'voice.wav', voice, sr)
    write_wav(out_dir / 'sfx.wav', sfxb, sr)
    write_wav(out_dir / 'music.wav', mus, sr)

    print(f'gen-audio: {slug} -> {out_dir}  ({secs:.2f} s, {sr} Hz, mono 16-bit)')
    print(f'  mix: key {key or "(chords from the file)"}, voice pitch {float(mix.get("pitch", 150)):.0f} Hz'
          f' -> f0 x{pitch_scale:.3f}')
    for name, x in [('voice', voice), ('sfx', sfxb), ('music', mus)]:
        print(f'  {name:6s} peak {db(peak(x)):7.2f} dBFS   rms {db(rms(x)):7.2f} dBFS   {len(x) / sr:.2f} s')
    if placed:
        print('  sfx placed: ' + ', '.join(f'{k}@{t:.2f}s' for k, t in placed))
    if vcfg.get('phrases'):
        print('  voice: ' + ', '.join(f"{p['dur']:.2f}s of {'-'.join(p['vowels'])}" for p in vcfg['phrases']) +
              '   (vowels only: a placeholder for the ElevenLabs take, not words)')


if __name__ == '__main__':
    main()
