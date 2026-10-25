import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';
import { loadFont as loadBricolage } from '@remotion/google-fonts/BricolageGrotesque';
import { loadFont as loadMono } from '@remotion/google-fonts/FragmentMono';
import { loadFont as loadHand } from '@remotion/google-fonts/Kalam';
import { STUDIO } from '../studio.config';

// Three faces: a heavy display face for the title card, a mono for on-screen readouts (timers, labels, chips),
// and a handwriting face for chalk and notes.
//
// Two ways to load them, picked by STUDIO.localFonts:
//   false (default) - from Google Fonts at render time: needs a connection, nothing to ship.
//   true            - from public/fonts/: the same three OFL faces (Fontsource builds), so a render works offline.
//                     Turn it on when the machine doing the render can't reach fonts.gstatic.com (a sandbox, a
//                     locked-down box); the frames are identical, only where the woff2 comes from changes.

const local = (family: string, file: string, weight: string) =>
  loadFont({ family, url: staticFile(`fonts/${file}`), weight });

if (STUDIO.localFonts) {
  local('Bricolage Grotesque', 'bricolage-grotesque-latin-600-normal.woff2', '600');
  local('Bricolage Grotesque', 'bricolage-grotesque-latin-700-normal.woff2', '700');
  local('Bricolage Grotesque', 'bricolage-grotesque-latin-800-normal.woff2', '800');
  local('Fragment Mono', 'fragment-mono-latin-400-normal.woff2', '400');
  local('Kalam', 'kalam-latin-400-normal.woff2', '400');
  local('Kalam', 'kalam-latin-700-normal.woff2', '700');
} else {
  loadBricolage('normal', { weights: ['600', '700', '800'], subsets: ['latin'] });
  loadMono('normal', { weights: ['400'], subsets: ['latin'] });
  loadHand('normal', { weights: ['400', '700'], subsets: ['latin'] });
}
if (STUDIO.titleFont) loadFont({ family: STUDIO.titleFont.family, url: staticFile(STUDIO.titleFont.file), weight: STUDIO.titleFont.weight });

export const FONT = {
  title: STUDIO.titleFont ? STUDIO.titleFont.family : 'Bricolage Grotesque',
  ui: 'Fragment Mono',
  hand: 'Kalam',
};
