import React from 'react';

const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));

export const Fader: React.FC<{
  label: string;
  value: number;
  level: number;
  onChange: (v: number) => void;
  muted: boolean;
  onMute: () => void;
  color: string;
}> = ({ label, value, level, onChange, muted, onMute, color }) => (
  <div className="fader">
    <div className="fader-top">
      <button className={`mute ${muted ? 'on' : ''}`} onClick={onMute} title="mute">
        {muted ? 'M' : '·'}
      </button>
      <span className="fader-label">{label}</span>
      <span className="fader-value">{Math.round(value * 100)}</span>
    </div>
    <input
      type="range"
      min={0}
      max={1.2}
      step={0.01}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      style={{ accentColor: color }}
    />
    <div className="meter">
      {Array.from({ length: 18 }).map((_, i) => {
        const on = !muted && level > i / 18;
        return <i key={i} className={on ? 'lit' : ''} style={{ background: on ? color : undefined }} />;
      })}
    </div>
  </div>
);

export const Pad: React.FC<{ label: string; hint: string; onPlay: () => void; color: string }> = ({ label, hint, onPlay, color }) => (
  <button className="pad" onClick={onPlay} style={{ borderColor: `${color}55` }}>
    <span className="pad-dot" style={{ background: color }} />
    <span className="pad-label">{label}</span>
    <span className="pad-hint">{hint}</span>
  </button>
);

export const Knob: React.FC<{ label: string; value: number; min: number; max: number; step?: number; unit?: string; onChange: (v: number) => void }> = ({
  label, value, min, max, step = 1, unit = '', onChange,
}) => (
  <label className="knob">
    <span className="knob-label">{label}</span>
    <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} />
    <span className="knob-value">
      {value}
      {unit}
    </span>
  </label>
);

export { clamp };
