import React from 'react';
import { ShotFrame } from '../src/engine/episode';
import { T1, T2, T3 } from '../src/episodes/ses-testi/shots';

// The picture: the episode's own three shots, drawn at the frame the transport is on. Each shot is a pure function
// of its clock t, so scrubbing is free: give a shot any t and it draws that moment, forwards or backwards.

const SHOTS = [
  { id: 'T1', C: T1, from: 0, len: 60, label: 'study · the mug goes down' },
  { id: 'T2', C: T2, from: 60, len: 60, label: 'kitchen · the tap' },
  { id: 'T3', C: T3, from: 120, len: 60, label: 'rooftop · the title, then the light goes' },
];

/** The hit that is landing right now (or a beat ago), for the shake. */
export const shakeAt = (frame: number, hits: number[]) => {
  let x = 0;
  let y = 0;
  for (const h of hits) {
    const d = frame - h;
    if (d >= 0 && d < 10) {
      const k = 9 * (1 - d / 10);
      x += Math.sin(d * 2.9) * k;
      y += Math.cos(d * 3.7) * k * 0.7;
    }
  }
  return { x, y };
};

export const Stage: React.FC<{ frame: number; hits: number[] }> = ({ frame, hits }) => {
  const f = ((frame % 180) + 180) % 180;
  const shot = SHOTS.find((s) => f >= s.from && f < s.from + s.len) ?? SHOTS[SHOTS.length - 1];
  const t = f - shot.from;
  const { x, y } = shakeAt(f, hits);
  const C = shot.C;
  return (
    <div className="stage">
      <svg viewBox="0 0 1920 1080" width="100%" style={{ display: 'block', transform: `translate(${x}px, ${y}px)` }}>
        <ShotFrame>
          <C t={t} len={shot.len} f={f} />
        </ShotFrame>
      </svg>
      <div className="vignette" />
      <div className="stage-tag">
        {shot.id} · {shot.label}
      </div>
      <div className="stage-frame">f{Math.round(f).toString().padStart(3, '0')} · t{Math.round(t)}</div>
    </div>
  );
};

export const SHOT_INFO = SHOTS;
export const LOOP_FRAMES = 180;
export const FPS = 30;
