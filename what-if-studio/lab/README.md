# Ses laboratuvarı (the lab)

`npm run lab` → http://localhost:3440

The episode's picture with its sound **built live in the browser** (Web Audio), so every part of the mix can be
touched while it loops. Nothing is pre-rendered: change the pitch and the next phrase is already different.

| In the page | What it does |
|---|---|
| ▶ / boşluk | starts the 6 s loop; the picture and the sound are scheduled off one clock |
| Mikser | voice / sfx / music faders with live RMS meters; `M` mutes a stem; master and reverb send |
| Ses tasarımı | voice pitch (90–230 Hz) and the chord progression (Am / Dm / Em) — audible on the next event |
| Pedler | play any effect dry, right now (keys `1`–`6`) |
| Vuruşlar | the hit list; click a row to jump to its frame and fire it |
| Zaman çizelgesi | voice phrases, sfx hits, chords; click to scrub, click a dot to hear its hit |

## Things worth trying

1. Mute music, then bring the sfx fader up — the hits are dry enough to hear the room tone alone.
2. Drag voice pitch from 90 to 230 while it loops: the same vowels become another character.
3. Change the chord to Em and listen for the switch at the next bar (chords are scheduled 150 ms ahead).
4. Push reverb to 80% and the boom at f120 turns into a hall.
5. Scrub to f118, press play: the boom lands on the cut, the same frame the title card pops.
6. Set voice and music to 0 and use only the pads to build a pass by hand.

## Where it lives

- `lab/synth.ts` — the sound engine: formant voice, the effects, the chord bed, the reverb, the meters. The same
  design as `scripts/gen-audio.py` (the offline WAV version), but every value is a live node here.
- `lab/Stage.tsx` — draws the studio's own shots (`src/episodes/ses-testi/shots.tsx`), so there is nothing duplicated.
- `lab/Timeline.tsx` — the loop as a picture; `lab/App.tsx` — the transport and the scheduler.

Ship it as a file: `npx vite build --config vite.lab.config.ts` writes a static `lab/dist/`.
