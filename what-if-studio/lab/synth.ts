// The lab's sound. The episode's three stems, synthesised live in Web Audio instead of rendered to WAV by
// scripts/gen-audio.py: same voices, same effects, same chord bed, but every knob can move while it plays.
//
// The picture is the episode's own shots (they are pure functions of a frame), so the lab is the real thing with a
// mixing desk bolted on:
//
//   voice  a glottal saw through three formant band-passes, one vowel at a time (speech-shaped, not words)
//   sfx    noise and tones through biquads, on the frames the actions land
//   music  a chord bed with a low pulse on the bar line
//
// Routing: source -> stem gain -> (analyser, dry -> master, send -> reverb -> master) -> compressor -> out.

import audio from '../src/episodes/ses-testi/audio.json';

export type Stem = 'voice' | 'sfx' | 'music';
export type SfxKind = 'pop' | 'ding' | 'whoosh' | 'click' | 'boom' | 'power_down' | 'room_tone';

export const VOWELS: Record<string, [number, number, number]> = {
  a: [700, 1100, 2500],
  e: [530, 1840, 2480],
  i: [270, 2290, 3010],
  o: [570, 840, 2410],
  u: [300, 870, 2240],
};

/** The voice's lines, in seconds: the block-out from audio.json (vowels, not words). */
export const PHRASES = audio.voice.phrases as { at: number; vowels: string[]; dur: number; f0: number }[];

/** What each hit is for. The frames come from audio.json's `at`, so the picture and the sound cannot drift. */
const HIT_NOTE: Record<string, string> = {
  'room_tone@0': 'room tone under the loop',
  'pop@0.8': 'the mug meets the desk',
  'whoosh@1.98': 'the cut to the kitchen',
  'click@2.42': 'the tap',
  'ding@2.6': 'the ding on the contact frame',
  'boom@4': 'the title lands on the cut',
  'ding@4.55': 'the title accent',
  'power_down@5.35': 'the city goes dark',
};

/** Every hit the episode has, in frames: the same list scripts/gen-audio.py renders. */
export const HITS: { f: number; kind: SfxKind; note: string }[] = (audio.sfx.events as { kind: string; at: number }[]).map((e) => ({
  f: Math.round(e.at * 30),
  kind: e.kind as SfxKind,
  note: HIT_NOTE[`${e.kind}@${e.at}`] ?? e.kind,
}));

const NOTE: Record<string, number> = { C: 0, 'C#': 1, D: 2, 'D#': 3, E: 4, F: 5, 'F#': 6, G: 7, 'G#': 8, A: 9, 'A#': 10, B: 11 };
const hz = (name: string, oct: number) => 440 * Math.pow(2, (NOTE[name] - 9) / 12 + (oct - 4));

export const PROGRESSIONS: Record<string, { name: string; notes: [string, number, number][] }[]> = {
  Am: [
    { name: 'Am', notes: [['A', 2, 1.0], ['C', 3, 0.5], ['E', 3, 0.45]] },
    { name: 'F', notes: [['F', 2, 1.0], ['A', 2, 0.55], ['C', 3, 0.45]] },
    { name: 'C', notes: [['C', 3, 1.0], ['E', 3, 0.5], ['G', 3, 0.4]] },
    { name: 'G', notes: [['G', 2, 1.0], ['B', 2, 0.55], ['D', 3, 0.45]] },
  ],
  Dm: [
    { name: 'Dm', notes: [['D', 3, 1.0], ['F', 3, 0.5], ['A', 3, 0.45]] },
    { name: 'Bb', notes: [['A#', 2, 1.0], ['D', 3, 0.55], ['F', 3, 0.45]] },
    { name: 'F', notes: [['F', 2, 1.0], ['A', 2, 0.5], ['C', 3, 0.4]] },
    { name: 'C', notes: [['C', 3, 1.0], ['E', 3, 0.5], ['G', 3, 0.4]] },
  ],
  Em: [
    { name: 'Em', notes: [['E', 2, 1.0], ['G', 2, 0.5], ['B', 2, 0.45]] },
    { name: 'C', notes: [['C', 3, 1.0], ['E', 3, 0.55], ['G', 3, 0.4]] },
    { name: 'G', notes: [['G', 2, 1.0], ['B', 2, 0.5], ['D', 3, 0.45]] },
    { name: 'D', notes: [['D', 3, 1.0], ['F#', 3, 0.5], ['A', 3, 0.4]] },
  ],
};

export type LabOptions = { voice: number; sfx: number; music: number; master: number; send: number; f0: number; key: string };

const MIX = audio.mix as { pitch: number; key: string; voice: number; sfx: number; music: number; master: number; send: number };
const DEFAULTS: LabOptions = {
  voice: MIX.voice,
  sfx: MIX.sfx,
  music: MIX.music,
  master: MIX.master,
  send: MIX.send,
  f0: MIX.pitch,
  key: MIX.key,
};

/** What the file says, for the "write it back / undo" panel: the lab starts here every reload. */
export const fileMix = () => ({ ...DEFAULTS });

export const labDefaults = DEFAULTS;

export function createLab() {
  let ctx: AudioContext | null = null;
  let master: GainNode;
  let comp: DynamicsCompressorNode;
  let convolver: ConvolverNode;
  let wet: GainNode;
  let noise: AudioBuffer;
  const stems = {} as Record<Stem, { gain: GainNode; analyser: AnalyserNode; send: GainNode; buf: Float32Array }>;
  let opts: LabOptions = { ...DEFAULTS };

  /** Built on the first gesture: browsers won't let an AudioContext make a sound before one. */
  const ensure = () => {
    if (ctx) {
      if (ctx.state === 'suspended') void ctx.resume();
      return ctx;
    }
    const C = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    ctx = new C();
    const c = ctx;
    master = c.createGain();
    master.gain.value = opts.master;
    comp = c.createDynamicsCompressor();
    comp.threshold.value = -16;
    comp.knee.value = 12;
    comp.ratio.value = 3;
    comp.attack.value = 0.004;
    comp.release.value = 0.18;
    master.connect(comp);
    comp.connect(c.destination);

    // A small room: an impulse made of noise that dies away in about a second.
    const len = Math.floor(c.sampleRate * 1.4);
    const ir = c.createBuffer(2, len, c.sampleRate);
    for (let ch = 0; ch < 2; ch++) {
      const d = ir.getChannelData(ch);
      for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 3.2);
    }
    convolver = c.createConvolver();
    convolver.buffer = ir;
    wet = c.createGain();
    wet.gain.value = 1;
    convolver.connect(wet);
    wet.connect(master);

    noise = c.createBuffer(1, Math.floor(c.sampleRate * 2), c.sampleRate);
    const nd = noise.getChannelData(0);
    for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;

    (['voice', 'sfx', 'music'] as Stem[]).forEach((s) => {
      const g = c.createGain();
      g.gain.value = opts[s];
      const an = c.createAnalyser();
      an.fftSize = 1024;
      const send = c.createGain();
      send.gain.value = opts.send;
      g.connect(an);
      g.connect(master);
      g.connect(send);
      send.connect(convolver);
      stems[s] = { gain: g, analyser: an, send, buf: new Float32Array(an.fftSize) };
    });
    return ctx;
  };

  const env = (g: GainNode, at: number, a: number, hold: number, r: number, peak = 1) => {
    g.gain.setValueAtTime(0.0001, at);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0002, peak), at + a);
    g.gain.setValueAtTime(Math.max(0.0002, peak), at + a + hold);
    g.gain.exponentialRampToValueAtTime(0.0001, at + a + hold + r);
  };

  /** A vowel: a saw at f0 through three band-passes, with the pitch falling the way a sentence does. */
  const vowel = (at: number, f: [number, number, number], dur: number, f0: number, rel: number) => {
    const c = ctx!;
    const osc = c.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(f0, at);
    osc.frequency.linearRampToValueAtTime(f0 * 0.9, at + dur);
    // vibrato: shallow, 5.4 Hz, so it reads as a voice and not a synth
    const lfo = c.createOscillator();
    lfo.frequency.value = 5.4;
    const lfoAmt = c.createGain();
    lfoAmt.gain.value = 22; // cents
    lfo.connect(lfoAmt);
    lfoAmt.connect(osc.detune);

    const tilt = c.createBiquadFilter();
    tilt.type = 'lowpass';
    tilt.frequency.value = 1600;
    osc.connect(tilt);

    const out = c.createGain();
    const formants: [number, number, number, number][] = [
      [f[0], 9, 6, 1.0],
      [f[1], 11, 2, 0.55],
      [f[2], 13, -2, 0.22],
    ];
    formants.forEach(([freq, q, gainDb, mix]) => {
      const b = c.createBiquadFilter();
      b.type = 'bandpass';
      b.frequency.value = freq;
      b.Q.value = q;
      const g = c.createGain();
      g.gain.value = mix * Math.pow(10, gainDb / 20);
      tilt.connect(b);
      b.connect(g);
      g.connect(out);
    });
    // a breath of noise on the same envelope
    const nz = c.createBufferSource();
    nz.buffer = noise;
    const nb = c.createBiquadFilter();
    nb.type = 'bandpass';
    nb.frequency.value = 1800;
    nb.Q.value = 1.2;
    const ng = c.createGain();
    ng.gain.value = 0.02;
    nz.connect(nb);
    nb.connect(ng);
    ng.connect(out);
    nz.start(at);
    nz.stop(at + dur + rel + 0.05);

    out.connect(stems.voice.gain);
    env(out, at, Math.min(0.03, dur / 6), Math.max(0.01, dur - 0.1), rel, 0.55);
    osc.start(at);
    osc.stop(at + dur + rel + 0.05);
    lfo.start(at);
    lfo.stop(at + dur + rel + 0.05);
  };

  /** One line of the block-out: its vowels in order, with a hair of overlap so they join. */
  const phrase = (at: number, ph: { vowels: string[]; dur: number; f0: number }, pitch: number) => {
    const per = ph.dur / ph.vowels.length;
    ph.vowels.forEach((v, i) => vowel(at + i * per, VOWELS[v] ?? VOWELS.a, per * 1.12, pitch, 0.07));
  };

  const sfxNode = (kind: SfxKind, at: number) => {
    const c = ctx!;
    const out = c.createGain();
    out.connect(stems.sfx.gain);
    if (kind === 'pop') {
      const o = c.createOscillator();
      o.type = 'sine';
      o.frequency.setValueAtTime(420, at);
      o.frequency.exponentialRampToValueAtTime(1320, at + 0.03);
      o.frequency.exponentialRampToValueAtTime(260, at + 0.13);
      o.connect(out);
      env(out, at, 0.004, 0.02, 0.11, 0.5);
      o.start(at);
      o.stop(at + 0.16);
    } else if (kind === 'ding') {
      const partials: [number, number][] = [[1240, 0.5], [1860, 0.22], [2790, 0.11]];
      partials.forEach(([f, g], i) => {
        const o = c.createOscillator();
        o.type = 'sine';
        o.frequency.value = f;
        o.detune.value = i * 3;
        const gg = c.createGain();
        gg.gain.value = g;
        o.connect(gg);
        gg.connect(out);
        env(gg, at, 0.004, 0.09, 0.8 - i * 0.12, 1);
        o.start(at);
        o.stop(at + 1.0);
      });
    } else if (kind === 'whoosh') {
      const dur = 0.5;
      const nz = c.createBufferSource();
      nz.buffer = noise;
      const b = c.createBiquadFilter();
      b.type = 'bandpass';
      b.Q.value = 1.6;
      b.frequency.setValueAtTime(380, at);
      b.frequency.exponentialRampToValueAtTime(4200, at + dur);
      nz.connect(b);
      b.connect(out);
      env(out, at, 0.06, dur * 0.55, dur * 0.4, 0.42);
      nz.start(at);
      nz.stop(at + dur + 0.1);
    } else if (kind === 'click') {
      const nz = c.createBufferSource();
      nz.buffer = noise;
      const b = c.createBiquadFilter();
      b.type = 'bandpass';
      b.frequency.value = 2400;
      b.Q.value = 2;
      nz.connect(b);
      b.connect(out);
      env(out, at, 0.001, 0.006, 0.05, 0.5);
      nz.start(at);
      nz.stop(at + 0.08);
    } else if (kind === 'boom') {
      const o = c.createOscillator();
      o.type = 'sine';
      o.frequency.setValueAtTime(58, at);
      o.frequency.exponentialRampToValueAtTime(40, at + 0.7);
      o.connect(out);
      env(out, at, 0.004, 0.2, 0.9, 0.75);
      o.start(at);
      o.stop(at + 1.2);
      const nz = c.createBufferSource();
      nz.buffer = noise;
      const lp = c.createBiquadFilter();
      lp.type = 'lowpass';
      lp.frequency.value = 240;
      const ng = c.createGain();
      ng.gain.value = 0.35;
      nz.connect(lp);
      lp.connect(ng);
      ng.connect(out);
      env(ng, at, 0.003, 0.12, 0.75, 1);
      nz.start(at);
      nz.stop(at + 1.1);
    } else if (kind === 'power_down') {
      const o = c.createOscillator();
      o.type = 'triangle';
      o.frequency.setValueAtTime(320, at);
      o.frequency.exponentialRampToValueAtTime(45, at + 1.1);
      o.connect(out);
      env(out, at, 0.01, 0.25, 0.9, 0.5);
      o.start(at);
      o.stop(at + 1.3);
    } else if (kind === 'room_tone') {
      const nz = c.createBufferSource();
      nz.buffer = noise;
      nz.loop = true;
      const lp = c.createBiquadFilter();
      lp.type = 'lowpass';
      lp.frequency.value = 480;
      const hp = c.createBiquadFilter();
      hp.type = 'highpass';
      hp.frequency.value = 70;
      nz.connect(lp);
      lp.connect(hp);
      hp.connect(out);
      env(out, at, 0.4, 4.4, 0.6, 0.12);
      nz.start(at);
      nz.stop(at + 5.6);
    }
  };

  /** One chord of the bed: three voices, slowly swelling, with a heartbeat under the bar line. */
  const chordAt = (idx: number, at: number, step: number, key: string) => {
    const c = ctx!;
    const prog = PROGRESSIONS[key] ?? PROGRESSIONS.Am;
    const ch = prog[idx % prog.length];
    ch.notes.forEach(([nm, oct, g]) => {
      const f = hz(nm, oct);
      const o = c.createOscillator();
      o.type = 'sine';
      o.frequency.value = f;
      const o2 = c.createOscillator();
      o2.type = 'triangle';
      o2.frequency.value = f * 1.0016;
      const gg = c.createGain();
      gg.gain.value = g * 0.16;
      const trem = c.createOscillator();
      trem.frequency.value = 0.9;
      const tg = c.createGain();
      tg.gain.value = g * 0.03;
      trem.connect(tg);
      tg.connect(gg.gain);
      o.connect(gg);
      o2.connect(gg);
      gg.connect(stems.music.gain);
      env(gg, at, step * 0.35, step * 0.45, step * 0.6, g * 0.16);
      o.start(at);
      o.stop(at + step * 1.5);
      o2.start(at);
      o2.stop(at + step * 1.5);
      trem.start(at);
      trem.stop(at + step * 1.5);
    });
    const p = c.createOscillator();
    p.type = 'sine';
    p.frequency.setValueAtTime(54, at);
    p.frequency.exponentialRampToValueAtTime(44, at + 0.35);
    const pg = c.createGain();
    pg.gain.value = 0.5;
    p.connect(pg);
    pg.connect(stems.music.gain);
    env(pg, at, 0.005, 0.1, 0.35, 0.2);
    p.start(at);
    p.stop(at + 0.55);
  };

  const music = (at: number, seconds: number, key: string) => {
    const step = seconds / 4;
    for (let i = 0; i < 4; i++) chordAt(i, at + i * step, step, key);
  };

  return {
    /** Schedules one six-second pass of all three stems. */
    scheduleLoop(at: number, seconds: number) {
      PHRASES.forEach((ph) => phrase(at + ph.at, ph, opts.f0 * (ph.f0 / 150)));
      HITS.forEach((h) => sfxNode(h.kind, at + h.f / 30));
      music(at, seconds, opts.key);
    },
    /** The lab's scheduler places events itself, 150 ms ahead, so a seek never overlaps the last loop. */
    hit: (kind: SfxKind, at: number) => sfxNode(kind, at),
    say: (ph: { vowels: string[]; dur: number; f0?: number }, at: number) => phrase(at, { ...ph, f0: ph.f0 ?? 150 }, opts.f0 * ((ph.f0 ?? 150) / 150)),
    chord: (i: number, at: number, step: number) => chordAt(i, at, step, opts.key),
    /** A single hit, for the pads: click one and you hear it now. */
    play(kind: SfxKind) {
      const c = ensure();
      sfxNode(kind, c.currentTime + 0.01);
    },
    playVoice() {
      const c = ensure();
      PHRASES.forEach((ph) => phrase(c.currentTime + 0.05 + ph.at, ph, opts.f0 * (ph.f0 / 150)));
    },
    playMusic() {
      const c = ensure();
      music(c.currentTime + 0.05, 6, opts.key);
    },
    ensure,
    now: () => (ctx ? ctx.currentTime : 0),
    setOpts(next: Partial<LabOptions>) {
      const prev = opts;
      opts = { ...opts, ...next };
      if (!ctx) return;
      const t = ctx.currentTime;
      if (next.voice !== undefined) stems.voice.gain.gain.setTargetAtTime(next.voice, t, 0.02);
      if (next.sfx !== undefined) stems.sfx.gain.gain.setTargetAtTime(next.sfx, t, 0.02);
      if (next.music !== undefined) stems.music.gain.gain.setTargetAtTime(next.music, t, 0.02);
      if (next.master !== undefined) master.gain.setTargetAtTime(next.master, t, 0.02);
      if (next.send !== undefined) {
        const send = next.send;
        (['voice', 'sfx', 'music'] as Stem[]).forEach((s) => stems[s].send.gain.setTargetAtTime(send, t, 0.02));
      }
      void prev;
    },
    getOpts: () => opts,
    /** Live RMS per stem, 0..1: what the meters under the faders show. */
    levels(): Record<Stem, number> {
      const out = { voice: 0, sfx: 0, music: 0 } as Record<Stem, number>;
      if (!ctx) return out;
      (['voice', 'sfx', 'music'] as Stem[]).forEach((s) => {
        const { analyser, buf } = stems[s];
        analyser.getFloatTimeDomainData(buf);
        let sum = 0;
        for (let i = 0; i < buf.length; i++) sum += buf[i] * buf[i];
        out[s] = Math.min(1, Math.sqrt(sum / buf.length) * 3.2);
      });
      return out;
    },
    suspend() {
      void ctx?.suspend();
    },
  };
}

export type Lab = ReturnType<typeof createLab>;
