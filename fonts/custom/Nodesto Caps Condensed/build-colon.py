#!/usr/bin/env python3
"""Rebuild the colon and semicolon of Nodesto Caps Condensed for all-caps setting.

Reads the unmodified Solbera originals from ../../solbera/Nodesto Caps Condensed/
and writes the Version 1.100 build into this folder.  See README.txt for why.

    pip install fonttools
    python3 build-colon.py

Rule:
  * the dot pair seats on the baseline and rises to 0.723 x cap height
  * dot diameter 0.177 x cap -- Nodesto's own cap stem width -- for any weight
    that draws them lighter than that.  Bold already draws 0.190 and keeps it.
  * the gap is the remainder, so bolder weights close up on their own
  * semicolon: upper dot where the colon's is; comma aligned by its TOP to the
    colon's lower dot, which restores the comma's descender
"""
import glob
import os

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

SRC = os.path.join(os.path.dirname(__file__), "..", "..", "solbera",
                   "Nodesto Caps Condensed")
DST = os.path.dirname(os.path.abspath(__file__))
VERSION = 1.100
SPAN_TOP = 0.723
DOT_RATIO = 0.177


def contours(glyphset, name):
    pen = DecomposingRecordingPen(glyphset)
    glyphset[name].draw(pen)
    out, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [(op, args)]
        elif op in ("lineTo", "curveTo", "qCurveTo"):
            cur.append((op, args))
        elif op in ("closePath", "endPath"):
            cur.append((op, args))
            out.append(cur)
            cur = []
    return out


def bounds(contour):
    pts = [a for op, args in contour for a in args if a]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def rebuild(src, dst):
    from fontTools.ttLib import TTFont
    font = TTFont(src)
    glyphset = font.getGlyphSet()
    cmap = font.getBestCmap()
    bp = BoundsPen(glyphset)
    glyphset[cmap[ord("H")]].draw(bp)
    cap = bp.bounds[3]

    colon = sorted(contours(glyphset, cmap[ord(":")]), key=lambda c: bounds(c)[1])
    dot_h = bounds(colon[-1])[3] - bounds(colon[-1])[1]
    scale = max(1.0, DOT_RATIO * cap / dot_h)
    new_dot = dot_h * scale
    lower_top = new_dot                       # lower dot bottom on the baseline
    upper_bottom = SPAN_TOP * cap - new_dot
    assert upper_bottom > lower_top, "dots would overlap"

    charstrings = font["CFF "].cff[font["CFF "].cff.fontNames[0]].CharStrings
    for char in ":;":
        if ord(char) not in cmap:
            continue
        name = cmap[ord(char)]
        cl = sorted(contours(glyphset, name), key=lambda c: bounds(c)[1])
        # anchor the lower contour by its TOP so the semicolon's comma keeps its
        # tail, and the upper contour by its BOTTOM
        anchor = {id(cl[0]): ("top", lower_top), id(cl[-1]): ("bottom", upper_bottom)}
        pen = T2CharStringPen(font["hmtx"][name][0], glyphset)
        for contour in cl:
            b = bounds(contour)
            cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
            edge, target = anchor[id(contour)]
            dy = target - (cy + ((b[3] if edge == "top" else b[1]) - cy) * scale)
            t = (Transform().translate(0, dy)
                            .translate(cx, cy).scale(scale).translate(-cx, -cy))
            for op, args in contour:
                pts = [t.transformPoint(a) if a else None for a in args]
                if pts and pts[0] is not None:
                    getattr(pen, op)(*pts)
                else:
                    getattr(pen, op)()
        old = charstrings[name]
        charstrings[name] = pen.getCharString(private=old.private,
                                              globalSubrs=old.globalSubrs)

    font["head"].fontRevision = VERSION
    note = ("Version %.3f; colon and semicolon repositioned for all-caps setting"
            % VERSION)
    for rec in font["name"].names:
        if rec.nameID == 5:
            rec.string = note
    font["CFF "].cff[font["CFF "].cff.fontNames[0]].version = "%.3f" % VERSION
    font.save(dst)
    return cap, scale, new_dot, upper_bottom - lower_top


if __name__ == "__main__":
    for path in sorted(glob.glob(os.path.join(SRC, "*.otf"))):
        name = os.path.basename(path)
        cap, scale, dot, gap = rebuild(path, os.path.join(DST, name))
        print("%-40s cap=%d scale=%.4f dot=%.1f (%.3f cap) gap=%.1f (%.3f cap)"
              % (name, cap, scale, dot, dot / cap, gap, gap / cap))
