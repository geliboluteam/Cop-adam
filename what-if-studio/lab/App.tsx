import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createLab, type Lab, type LabOptions, type SfxKind, HITS, PHRASES, PROGRESSIONS, labDefaults } from './synth';
import { Stage, SHOT_INFO, LOOP_FRAMES, FPS, shakeAt } from './Stage';
import { Fader, Pad, Knob } from './Controls';
import { Timeline } from './Timeline';

// The lab: the episode's picture with the sound built in the browser, so every part of the mix can be moved while it
// plays. Nothing here is pre-rendered: change the pitch, the key or the reverb and the next bar is already different.

const LOOP_S = LOOP_FRAMES / FPS;
const CHORD_STEP = LOOP_S / 4;

/** Everything the scheduler places, in loop seconds. One list, so the sound and the picture can't disagree. */
type Ev = { t: number; go: (lab: Lab, at: number) => void };
const EVENTS: Ev[] = [
  ...HITS.map<Ev>((h) => ({ t: h.f / FPS, go: (lab, at) => lab.hit(h.kind, at) })),
  ...PHRASES.map<Ev>((p) => ({ t: p.at, go: (lab, at) => lab.say(p, at) })),
  ...[0, 1, 2, 3].map<Ev>((i) => ({ t: i * CHORD_STEP, go: (lab, at) => lab.chord(i, at, CHORD_STEP) })),
].sort((a, b) => a.t - b.t);

const PADS: { kind: SfxKind; label: string; color: string }[] = [
  { kind: 'pop', label: 'pop', color: '#FFE27A' },
  { kind: 'ding', label: 'ding', color: '#7FD4FF' },
  { kind: 'whoosh', label: 'whoosh', color: '#5BE08A' },
  { kind: 'click', label: 'click', color: '#F6EFE3' },
  { kind: 'boom', label: 'boom', color: '#FF8A3D' },
  { kind: 'power_down', label: 'power down', color: '#FF5A4A' },
];

export const App: React.FC = () => {
  const labRef = useRef<Lab | null>(null);
  const iface = useCallback((): Lab => {
    if (!labRef.current) labRef.current = createLab();
    return labRef.current;
  }, []);

  const [opt, setOpt] = useState<LabOptions>({ ...labDefaults });
  const [playing, setPlaying] = useState(false);
  const [frame, setFrame] = useState(26);
  const [levels, setLevels] = useState({ voice: 0, sfx: 0, music: 0 });
  const [mutes, setMutes] = useState({ voice: false, sfx: false, music: false });
  const [lastHit, setLastHit] = useState<string>('—');

  // transport lives in refs: requestAnimationFrame must not wait for React
  const anchor = useRef(0); // ctx time that corresponds to loop second 0
  const sched = useRef({ idx: 0, base: 0 });
  const raf = useRef<number | null>(null);

  const applyOpts = useCallback(
    (next: Partial<LabOptions>) => {
      setOpt((prev) => {
        const merged = { ...prev, ...next };
        iface().setOpts(next);
        if (next.voice !== undefined || next.sfx !== undefined || next.music !== undefined) {
          const m = { voice: merged.voice, sfx: merged.sfx, music: merged.music };
          iface().setOpts(m);
        }
        return merged;
      });
    },
    [iface],
  );

  // muting is just a fader at zero, so the meter and the mix stay in one place
  useEffect(() => {
    iface().setOpts({ voice: mutes.voice ? 0 : opt.voice, sfx: mutes.sfx ? 0 : opt.sfx, music: mutes.music ? 0 : opt.music });
  }, [mutes, opt.voice, opt.sfx, opt.music, iface]);

  const tick = useCallback(() => {
    const lab = iface();
    const now = lab.now();
    const elapsed = Math.max(0, now - anchor.current);
    const hor = now + 0.15;
    let { idx, base } = sched.current;
    // schedule anything the next 150 ms will need, skipping what a seek left behind
    for (let guard = 0; guard < 64; guard++) {
      const ev = EVENTS[idx];
      const at = base + ev.t;
      if (at > hor) break;
      if (at >= now - 0.03) ev.go(lab, at);
      idx++;
      if (idx >= EVENTS.length) {
        idx = 0;
        base += LOOP_S;
      }
    }
    sched.current = { idx, base };
    setFrame(((elapsed % LOOP_S) * FPS) % LOOP_FRAMES);
    setLevels(lab.levels());
    raf.current = requestAnimationFrame(tick);
  }, [iface]);

  const play = useCallback(() => {
    const lab = iface();
    lab.ensure();
    anchor.current = lab.now() - frame / FPS;
    sched.current = { idx: 0, base: anchor.current };
    setPlaying(true);
    if (raf.current === null) raf.current = requestAnimationFrame(tick);
  }, [frame, iface, tick]);

  const pause = useCallback(() => {
    setPlaying(false);
    if (raf.current !== null) cancelAnimationFrame(raf.current);
    raf.current = null;
    labRef.current?.suspend();
  }, []);

  useEffect(() => () => {
    if (raf.current !== null) cancelAnimationFrame(raf.current);
  }, []);

  const seek = useCallback(
    (f: number) => {
      const lab = iface();
      const target = ((f % LOOP_FRAMES) + LOOP_FRAMES) % LOOP_FRAMES;
      anchor.current = lab.now() - target / FPS;
      sched.current = { idx: 0, base: anchor.current };
      setFrame(target);
    },
    [iface],
  );

  const hit = useCallback(
    (kind: SfxKind) => {
      iface().play(kind);
      setLastHit(kind);
    },
    [iface],
  );

  // space: play/pause, arrows: a frame at a time, 1-6: the pads
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.tagName === 'SELECT') return;
      if (e.code === 'Space') {
        e.preventDefault();
        playing ? pause() : play();
      } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        seek(Math.round(frame) + 1);
      } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        seek(Math.round(frame) - 1);
      } else if (/^Digit[1-6]$/.test(e.code)) {
        const p = PADS[Number(e.code.slice(5)) - 1];
        if (p) hit(p.kind);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [playing, play, pause, seek, frame, hit]);

  const hits = useMemo(() => HITS.map((h) => h.f), []);
  void shakeAt;

  return (
    <div className="app">
      <header>
        <div>
          <h1>Ses Laboratuvarı</h1>
          <p className="sub">
            The episode's picture, its sound built live in the browser. Move a fader or a pad while it loops: nothing is
            pre-rendered.
          </p>
        </div>
        <div className="badge">
          <span>{LOOP_S.toFixed(1)} s loop</span>
          <span>{EVENTS.length} scheduled events</span>
          <span>{PROGRESSIONS[opt.key as keyof typeof PROGRESSIONS] ? opt.key : 'Am'}</span>
        </div>
      </header>

      <main>
        <section className="left">
          <Stage frame={frame} hits={hits} />

          <div className="transport">
            <button className={`play ${playing ? 'on' : ''}`} onClick={playing ? pause : play}>
              {playing ? '❚❚  Duraklat' : '▶  Çal'}
            </button>
            <button className="ghost" onClick={() => { seek(0); }}>
              ⤺ başa
            </button>
            <div className="scrub-wrap">
              <input
                className="scrub"
                type="range"
                min={0}
                max={LOOP_FRAMES - 1}
                value={Math.round(frame)}
                onChange={(e) => seek(Number(e.target.value))}
              />
              <div className="marks">
                {SHOT_INFO.map((s) => (
                  <span key={s.id} className="cut" style={{ left: `${(s.from / LOOP_FRAMES) * 100}%` }} />
                ))}
                {HITS.map((h, i) => (
                  <button
                    key={i}
                    className={`mark ${lastHit === h.kind ? 'hot' : ''}`}
                    style={{ left: `${(h.f / LOOP_FRAMES) * 100}%` }}
                    title={`${h.kind} · f${h.f} · ${h.note}`}
                    onClick={() => hit(h.kind)}
                  />
                ))}
              </div>
            </div>
            <span className="tc">
              {(frame / FPS).toFixed(2)}s / f{Math.round(frame)}
            </span>
          </div>

          <Timeline frame={frame} keyName={opt.key} onSeek={seek} onHit={(i) => { const h = HITS[i]; seek(h.f); hit(h.kind); }} />

          <div className="shadow-row">
            <span className="k">Klavye</span>
            <span>boşluk: çal/duraklat</span>
            <span>← →: 1 kare</span>
            <span>1–6: pedler</span>
          </div>
        </section>

        <aside className="right">
          <div className="card">
            <h2>Mikser</h2>
            <Fader label="voice" value={opt.voice} level={levels.voice} muted={mutes.voice} onMute={() => setMutes((m) => ({ ...m, voice: !m.voice }))} onChange={(v) => applyOpts({ voice: v })} color="#FFE27A" />
            <Fader label="sfx" value={opt.sfx} level={levels.sfx} muted={mutes.sfx} onMute={() => setMutes((m) => ({ ...m, sfx: !m.sfx }))} onChange={(v) => applyOpts({ sfx: v })} color="#FF8A3D" />
            <Fader label="music" value={opt.music} level={levels.music} muted={mutes.music} onMute={() => setMutes((m) => ({ ...m, music: !m.music }))} onChange={(v) => applyOpts({ music: v })} color="#7FD4FF" />
            <div className="knobs">
              <Knob label="master" value={Math.round(opt.master * 100)} min={0} max={100} onChange={(v) => applyOpts({ master: v / 100 })} unit="%" />
              <Knob label="reverb" value={Math.round(opt.send * 100)} min={0} max={80} onChange={(v) => applyOpts({ send: v / 100 })} unit="%" />
            </div>
          </div>

          <div className="card">
            <h2>Ses tasarımı</h2>
            <div className="row">
              <Knob label="voice pitch" value={opt.f0} min={90} max={230} onChange={(v) => applyOpts({ f0: v })} unit=" Hz" />
              <label className="select">
                <span>akor</span>
                <select value={opt.key} onChange={(e) => applyOpts({ key: e.target.value })}>
                  {Object.keys(PROGRESSIONS).map((k) => (
                    <option key={k} value={k}>{k} — {PROGRESSIONS[k].map((c) => c.name).join(' ')}</option>
                  ))}
                </select>
              </label>
            </div>
            <p className="note">Değişiklikler 150 ms içinde, bir sonraki olayda duyulur.</p>
          </div>

          <div className="card">
            <h2>Pedler</h2>
            <div className="pads">
              {PADS.map((p) => (
                <Pad key={p.kind} label={p.label} hint={p.kind === 'ding' ? '0.9 s' : ''} color={p.color} onPlay={() => hit(p.kind)} />
              ))}
            </div>
            <button className="ghost wide" onClick={() => iface().playVoice()}>voice'u tek başına duy</button>
            <button className="ghost wide" onClick={() => iface().playMusic()}>akoru tek başına duy</button>
          </div>

          <div className="card">
            <h2>Vuruşlar</h2>
            <table>
              <tbody>
                {HITS.map((h, i) => (
                  <tr key={i} onClick={() => { seek(h.f); hit(h.kind); }} className={lastHit === h.kind ? 'hot' : ''}>
                    <td className="mono">f{h.f.toString().padStart(3, '0')}</td>
                    <td className="mono dim">{h.kind}</td>
                    <td className="dim">{h.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </aside>
      </main>
    </div>
  );
};
