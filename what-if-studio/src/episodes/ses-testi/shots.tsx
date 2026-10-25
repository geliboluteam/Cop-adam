import React from 'react';
import {
  Hero, Mug, Study, Desk, Kitchen, KitchenIsland, KITCHEN, islandTop, stand, Rooftop, TitleCard, Sparkle,
  Pose, basePose, poseAt, faceAt, kf, clamp, easeOut, easeIn, camT, LOOKS, LEG_LEN, FONT, ShotProps,
} from '../../engine';

// A sound test: three shots whose only job is to show the picture and the sound agreeing. Nothing here needs
// ElevenLabs: the stems come from scripts/gen-audio.py (see audio.json), and every hit in that file is a frame in
// this one. The yellow meter bottom right is driven by the same frame numbers, so if the pulse and the sound drift
// apart you see it before you hear it.
//
//   node ? no:  python scripts/gen-audio.py ses-testi     then open "SesTesti" in the studio
//
// Each shot is a pure function of its own clock t (frames), as every shot in this engine is.

const PIP = LOOKS.pipHood;

/** The hits, in each shot's own clock: the meter pulses on exactly these frames. */
const HITS: Record<string, number[]> = { T1: [24], T2: [18, 42], T3: [0, 15, 51] };

/** A little VU strip: bars that jump on a hit and fall away. Screen space (not camera space), bottom right. */
const Meter: React.FC<{ t: number; hits: number[]; label: string }> = ({ t, hits, label }) => {
  const bars = 16;
  return (
    <g>
      {Array.from({ length: bars }).map((_, i) => {
        let amp = 0.05;
        for (const h of hits) {
          const d = t - h;
          if (d >= -1) amp += 0.85 * Math.exp(-Math.abs(d) / 7) * Math.abs(Math.sin(i * 1.7 + d * 0.9));
        }
        const hgt = 5 + 74 * clamp(amp);
        return (
          <rect
            key={i}
            x={1636 + i * 12}
            y={1004 - hgt}
            width={7}
            height={hgt}
            rx={3}
            fill={i % 4 === 0 ? '#FF8A3D' : '#FFE27A'}
            opacity={0.3 + 0.6 * clamp(amp)}
          />
        );
      })}
      <text x={1812} y={1034} textAnchor="end" fontFamily={FONT.ui} fontSize={19} fill="#F6EFE3" opacity={0.55}>
        {label}
      </text>
    </g>
  );
};

// ---------- T1: study, wide: Pip sets the mug down on the desk (the pop lands on frame 24) ----------
const DESK_Y = 700;
export const T1: React.FC<ShotProps> = ({ t }) => {
  const pose = poseAt(t, [
    { f: 0, p: { x: 850, y: 704, yaw: 0.3, look: 0.45, armR: { a: 66, b: -34 }, armL: { a: 12, b: -8 } } },
    { f: 10, p: { armR: { a: 48, b: -18 } }, ease: easeIn },
    { f: 22, p: { armR: { a: 26, b: 4 } }, ease: easeIn },
    { f: 27, p: { armR: { a: 12, b: -4 } }, ease: easeOut },
    { f: 60, p: { x: 862, headTilt: -3, look: -0.25 } },
  ]);
  const clink = t >= 24 ? Math.sin((t - 24) * 1.6) * 4 * Math.exp(-(t - 24) / 7) : 0;
  return (
    <g transform={camT(kf(t, [[0, 990], [60, 1006]]), 575, kf(t, [[0, 1.0], [60, 1.12]]))}>
      <Study t={t} id="tt1" veil={0.3} />
      <Hero look={PIP} pose={{ ...pose, ...faceAt(t, [[0, 'neutral'], [26, 'happy']]) }} shadow={0} rimId="rimR" />
      <Desk x0={560} x1={1400} y={DESK_Y} />
      <Mug x={1046} y={DESK_Y} rot={clink} steam={t > 24 ? 1 : 0.5} f={t} />
      <Sparkle x={1046} y={DESK_Y - 110} t={t - 24} s={0.9} />
      <Meter t={t} hits={HITS.T1} label="voice + sfx + music" />
    </g>
  );
};

// ---------- T2: kitchen, medium over the island: the tap on the worktop (ding on frame 18) ----------
const T2_STAND = stand(KITCHEN, 0.5, 0.42);
const T2_TAP = islandTop(0.56, 0.5);
export const T2: React.FC<ShotProps> = ({ t, len }) => {
  const base: Partial<Pose> = { x: T2_STAND.x, y: T2_STAND.y, scale: T2_STAND.scale, yaw: 0.45, look: 0.6 };
  const pose = poseAt(t, [
    { f: 0, p: { ...base, armR: { a: 104, b: -46 }, armL: { a: 14, b: -8 } } },
    { f: 12, p: { armR: { a: 62, b: -8 } }, ease: easeIn },
    { f: 17, p: { armR: { a: 48, b: 16 } }, ease: easeIn },
    { f: 19, p: { armR: { a: 44, b: 10 } }, ease: easeOut },
    { f: 26, p: { armR: { a: 56, b: -6 } }, ease: easeOut },
    { f: 60, p: { armR: { a: 40, b: -10 }, headTilt: 4 } },
  ]);
  const beat = t >= 18 ? 1 + 0.35 * Math.exp(-(t - 18) / 6) : 1;
  return (
    <g transform={camT(kf(t, [[0, T2_STAND.x - 26], [len, T2_STAND.x + 14]]), 610, kf(t, [[0, 1.82], [len, 1.94]]))}>
      <Kitchen t={t + 40} id="tt2" veil={0.42} />
      <Hero look={PIP} pose={{ ...pose, ...faceAt(t, [[0, 'neutral'], [18, 'happy']]) }} shadow={0} rimId="rimR" />
      <KitchenIsland />
      <g transform={`translate(${T2_TAP.x} ${T2_TAP.y}) scale(${beat})`}>
        <ellipse cx={0} cy={4} rx={30} ry={9} fill="#E9C46A" opacity={0.25} />
      </g>
      <Sparkle x={T2_TAP.x} y={T2_TAP.y - 26} t={t - 18} s={1.1} />
      <Meter t={t} hits={HITS.T2} label="sfx on the contact frame" />
    </g>
  );
};

// ---------- T3: rooftop, the title, then the light goes (boom on the cut, power down as the city dies) ----------
export const T3: React.FC<ShotProps> = ({ t }) => {
  const pose = poseAt(t, [
    { f: 0, p: { x: 960, y: 770, scale: 0.62, yaw: 0, armL: { a: 18, b: 4 }, armR: { a: 18, b: 4 } } },
    { f: 15, p: { armL: { a: 150, b: 10 }, armR: { a: 150, b: 10 } }, ease: easeOut },
  ]);
  const die = clamp((t - 44) / 14);
  return (
    <g transform={camT(960, kf(t, [[0, 520], [60, 548]]), kf(t, [[0, 1.0], [60, 1.08]]))}>
      <Rooftop
        t={t}
        clock
        sunY={690}
        spin={t * 2.4}
        red={die * 0.55}
        crack={clamp((t - 38) / 12)}
        lightsOut={clamp((t - 40) / 16)}
        blackout={clamp((t - 46) / 13)}
        cityLit={2.2}
      />
      <Hero look={PIP} pose={{ ...pose, y: 820 - LEG_LEN * 0.62, ...faceAt(t, [[0, 'happy'], [44, 'worried']]) }} shadow={0.6} rimId="rimR" />
      <TitleCard t={t} lines={['AUDIO, WRITTEN IN CODE', 'SES TESTI']} size={116} />
      <Meter t={t} hits={HITS.T3} label="gen-audio.py" />
    </g>
  );
};
