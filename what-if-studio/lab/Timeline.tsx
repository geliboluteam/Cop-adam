import React, { useRef } from 'react';
import { HITS, PHRASES, PROGRESSIONS } from './synth';
import { LOOP_FRAMES, FPS, SHOT_INFO } from './Stage';

// The loop as a picture: what the scheduler will place, when. Three lanes (voice, sfx, music), the cuts above,
// the playhead over everything. Click anywhere to jump.

const LOOP_S = LOOP_FRAMES / FPS;
const pct = (t: number) => `${(t / LOOP_S) * 100}%`;

export const Timeline: React.FC<{ frame: number; keyName: string; onSeek: (f: number) => void; onHit: (i: number) => void }> = ({
  frame,
  keyName,
  onSeek,
  onHit,
}) => {
  const ref = useRef<HTMLDivElement>(null);
  const jump = (e: React.PointerEvent) => {
    const box = ref.current?.getBoundingClientRect();
    if (!box) return;
    const p = Math.min(1, Math.max(0, (e.clientX - box.left) / box.width));
    onSeek(Math.round(p * (LOOP_FRAMES - 1)));
  };
  const prog = PROGRESSIONS[keyName] ?? PROGRESSIONS.Am;
  const step = 2.0;
  return (
    <div className="timeline">
      <div className="tl-head">
        <h2>Zaman çizelgesi</h2>
        <span className="dim">tıkla: o kareye git · noktalar: vuruşları duy</span>
      </div>
      <div className="tl-body" ref={ref} onPointerDown={jump}>
        <div className="tl-cuts">
          <div className="tl-gutter" />
          {SHOT_INFO.map((s) => (
            <div key={s.id} className="tl-shot" style={{ left: pct(s.from / FPS), width: pct(s.len / FPS) }}>
              {s.id}
            </div>
          ))}
        </div>
        <div className="tl-lane voice">
          <span className="tl-name">voice</span>
          <div className="tl-track">
          {PHRASES.map((p, i) => (
            <div key={i} className="blk voice" style={{ left: pct(p.at), width: pct(p.dur) }} title={`${p.vowels.join('-')} · ${p.dur}s`}>
              {p.vowels.join('·')}
            </div>
          ))}
          </div>
        </div>
        <div className="tl-lane sfx">
          <span className="tl-name">sfx</span>
          <div className="tl-track">
          {HITS.map((h, i) => (
            <button
              key={i}
              className="tl-dot"
              style={{ left: pct(h.f / FPS) }}
              title={`${h.kind} · f${h.f} · ${h.note}`}
              onPointerDown={(e) => {
                e.stopPropagation();
                onHit(i);
              }}
            >
              <i />
              <b>{h.kind}</b>
            </button>
          ))}
          </div>
        </div>
        <div className="tl-lane music">
          <span className="tl-name">music</span>
          <div className="tl-track">
          {prog.map((c, i) => (
            <div key={i} className="blk music" style={{ left: pct(i * step), width: pct(step) }}>
              {c.name}
            </div>
          ))}
          </div>
        </div>
        <div className="playhead" style={{ left: `calc(52px + (100% - 52px) * ${frame / FPS / LOOP_S})` }} />
      </div>
    </div>
  );
};
