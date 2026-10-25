import { defineEpisode, Timeline } from '../../engine';
import timeline from './timeline.json';
import { T1, T2, T3 } from './shots';

// The audio test: no ElevenLabs, no download. Three stems synthesised by scripts/gen-audio.py, three shots whose
// actions land on the frames the sound is cued to. Open it in the studio and the sound plays with the picture.
export const sesTesti = defineEpisode('SesTesti', {
  timeline: timeline as Timeline,
  shots: { T1, T2, T3 },
});
