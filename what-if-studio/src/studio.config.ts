// The studio's settings. Every episode renders at this size and frame rate.
export const STUDIO = {
  fps: 30,
  width: 1920,
  height: 1080,
  /**
   * A local display face for titles, as a file in public/ (your brand font, say). null uses Bricolage Grotesque
   * from Google Fonts. Example: { family: 'My Brand Font', file: 'fonts/MyBrandFont.woff2', weight: '200 700' }
   */
  titleFont: null as null | { family: string; file: string; weight: string },
  /**
   * Load the three faces from public/fonts/ instead of Google Fonts. true renders without a network connection
   * (which is what a CLI render needs in a sandbox); false fetches Bricolage Grotesque, Fragment Mono and Kalam
   * from Google at render time. The faces are the same; the bytes are the Fontsource builds of the same OFL fonts.
   */
  localFonts: true,
};
