#!/usr/bin/env python3
"""The storyboard sheet, without Pillow: lays a folder of PNG stills out as one captioned grid.

The skill's board.py does this with Pillow. This machine has no Pillow (and Remotion's bundled ffmpeg has no tile
filter), so this reads and writes PNG with the standard library alone: zlib for the pixels, nearest-neighbour for the
downscale (still on a storyboard, it never ships in a render).

    python scripts/sheet.py out/rewind/board -o out/rewind/storyboard.png [--cols 4] [--width 480]
    python scripts/sheet.py out/rewind/board -o out/rewind/storyboard.png --labels

Reads every .png in the folder, sorted by name, and writes the sheet. With --labels it draws each shot's name in a
built-in 5x7 pixel font (enough for ids, sizes and frame numbers, which is all a board needs).
"""

import argparse
import struct
import sys
import zlib
from pathlib import Path

# ---------- PNG in/out ----------


def read_png(path):
    data = Path(path).read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise SystemExit(f'sheet: {path} is not a PNG')
    i, idat, w, h, bitd, ct = 8, b'', None, None, None, None
    while i < len(data):
        ln = struct.unpack('>I', data[i:i + 4])[0]
        typ = data[i + 4:i + 8]
        chunk = data[i + 8:i + 8 + ln]
        i += 12 + ln
        if typ == b'IHDR':
            w, h, bitd, ct = struct.unpack('>IIBB', chunk[:10])
        elif typ == b'IDAT':
            idat += chunk
        elif typ == b'IEND':
            break
    if bitd != 8:
        raise SystemExit(f'sheet: {path} is {bitd}-bit, expected 8')
    nch = {0: 1, 2: 3, 4: 2, 6: 4}[ct]
    raw = zlib.decompress(idat)
    stride = w * nch
    out = bytearray(h * stride)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if f == 1:
            for x in range(nch, stride):
                line[x] = (line[x] + line[x - nch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - nch] if x >= nch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - nch] if x >= nch else 0
                b = prev[x]
                c = prev[x - nch] if x >= nch else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, nch, bytes(out)


def write_png(path, w, h, px):
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw += b'\x00' + px[y * stride:(y + 1) * stride]

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
        + chunk(b'IDAT', zlib.compress(bytes(raw), 6))
        + chunk(b'IEND', b'')
    )


# ---------- a 5x7 font, for labels ----------

GLYPHS = {
    'A': '01110100011000111111100011000110001', 'B': '11110100011000111110100011000111110',
    'C': '01110100011000010000100001000101110', 'D': '11110100011000110001100011000111110',
    'E': '11111100001000011110100001000011111', 'F': '11111100001000011110100001000010000',
    'G': '01110100011000010111100011000101111', 'H': '10001100011000111111100011000110001',
    'I': '11111001000010000100001000010011111', 'J': '00111000100001000010000101001001100',
    'K': '10001100101010011000101001001010001', 'L': '10000100001000010000100001000011111',
    'M': '10001110111010110101100011000110001', 'N': '10001110011010110011100011000110001',
    'O': '01110100011000110001100011000101110', 'P': '11110100011000111110100001000010000',
    'Q': '01110100011000110001101011100101111', 'R': '11110100011000111110101001001010001',
    'S': '01111100001000001110000010000111110', 'T': '11111001000010000100001000010000100',
    'U': '10001100011000110001100011000101110', 'V': '10001100011000110001100010101000100',
    'W': '10001100011000110101101011010101010', 'X': '10001100010101000100010101000110001',
    'Y': '10001100010101000100001000010000100', 'Z': '11111000010001000100010001000011111',
    '0': '01110100011001110101110011000101110', '1': '00100011000010000100001000010001110',
    '2': '01110100010000100010001000100011111', '3': '11111000100010000010000011000101110',
    '4': '00010001100101010010111110001000010', '5': '11111100001111000001000011000101110',
    '6': '00110010001000011110100011000101110', '7': '11111000010001000100010000100001000',
    '8': '01110100011000101110100011000101110', '9': '01110100011000101111000010001001100',
    '-': '00000000000000011111000000000000000', '.': '00000000000000000000000000000110000',
    ' ': '00000000000000000000000000000000000', '#': '01010010100111110101001111101010010',
    ':': '00000011000011000000000110000110000', '/': '00001000100001000100010000100010000',
}


def draw_text(px, w, h, x0, y0, text, scale=2, rgb=(246, 239, 227)):
    """Blit `text` into an RGB buffer, one 5x7 glyph at a time."""
    cx = x0
    for ch in text.upper():
        g = GLYPHS.get(ch, GLYPHS[' '])
        for r in range(7):
            for c in range(5):
                if g[r * 5 + c] == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            x, y = cx + c * scale + dx, y0 + r * scale + dy
                            if 0 <= x < w and 0 <= y < h:
                                o = (y * w + x) * 3
                                px[o:o + 3] = bytes(rgb)
        cx += 6 * scale


# ---------- the sheet ----------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('folder')
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--cols', type=int, default=4)
    ap.add_argument('--width', type=int, default=440, help='each tile width, in pixels')
    ap.add_argument('--labels', action='store_true')
    ap.add_argument('--bg', default='0B0916')
    args = ap.parse_args()

    # natural order, so shot 2 lands before shot 10
    def key(f):
        return [int(''.join(c for c in part if c.isdigit()) or 0) if any(c.isdigit() for c in part) else part.lower()
                for part in __import__('re').split(r'(\d+)', f.stem)]

    files = sorted(Path(args.folder).glob('*.png'), key=key)
    if not files:
        raise SystemExit(f'sheet: no PNGs in {args.folder}')

    bg = bytes.fromhex(args.bg)
    tiles = []
    for f in files:
        w, h, nch, px = read_png(f)
        step = max(1, round(w / args.width))
        tw, th = w // step, h // step
        t = bytearray(tw * th * 3)
        for y in range(th):
            sy = y * step
            for x in range(tw):
                s = (sy * w + x * step) * nch
                o = (y * tw + x) * 3
                if nch == 4:
                    a = px[s + 3] / 255.0
                    for k in range(3):
                        t[o + k] = int(px[s + k] * a + bg[k] * (1 - a))
                elif nch == 3:
                    t[o:o + 3] = px[s:s + 3]
                elif nch == 1:
                    t[o] = t[o + 1] = t[o + 2] = px[s]
                else:
                    t[o] = t[o + 1] = t[o + 2] = px[s]
        tiles.append((tw, th, t, f.stem))

    tw = max(t[0] for t in tiles)
    th = max(t[1] for t in tiles)
    cols = max(1, min(args.cols, len(tiles)))
    rows = (len(tiles) + cols - 1) // cols
    gap, pad, cap = 12, 18, 26 if args.labels else 0
    W = pad * 2 + cols * tw + (cols - 1) * gap
    H = pad * 2 + rows * (th + cap) + (rows - 1) * gap
    canvas = bytearray(bg * (W * H))

    for i, (twl, thl, t, name) in enumerate(tiles):
        r, c = divmod(i, cols)
        x0 = pad + c * (tw + gap)
        y0 = pad + r * (th + cap + gap)
        for y in range(thl):
            o = ((y0 + y) * W + x0) * 3
            canvas[o:o + twl * 3] = t[y * twl * 3:(y + 1) * twl * 3]
        if args.labels:
            draw_text(canvas, W, H, x0 + 2, y0 + thl + 6, name, scale=2, rgb=(255, 226, 122))

    write_png(args.out, W, H, bytes(canvas))
    print(f'sheet: {len(tiles)} tiles -> {args.out}  ({W}x{H})')


if __name__ == '__main__':
    main()
