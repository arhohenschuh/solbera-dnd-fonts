Nodesto Caps Condensed  (house build)
=====================================

Four-style build of Solbera's Nodesto Caps Condensed (CC BY-SA 4.0) with the
colon and semicolon redrawn for all-caps setting. Made for the D&D House Style
Word template.

  Nodesto Caps Condensed.otf            (Regular)
  NodestoCapsCondensed-Italic.otf
  NodestoCapsCondensed-Bold.otf
  NodestoCapsCondensed-Bold Italic.otf

Installs as family "Nodesto Caps Condensed", Version 1.100
(the unmodified Solbera release is Version 1.0).

  !! SAME FAMILY NAME AS UPSTREAM. Install these four files and they replace
     the Solbera originals in the Windows font folder - which is the point, so
     the template and the skill need no change. But it also means that
     reinstalling from fonts/solbera/Nodesto Caps Condensed/ silently puts the
     old colon back. Install Nodesto from THIS folder. Check Version 1.100 in
     the font properties dialog if a title ever looks wrong again.


WHY
---
Nodesto stands in for Modesto Condensed, the face Wizards use for chapter and
appendix titles. Set a title with a colon in it -

    Appendix: Wild Magic Table

- and the colon floats. Both dots sit clear of the baseline and clear of the
cap line, so beside these very heavy condensed capitals the mark reads as a
small detached cluster rather than as punctuation belonging to the line.

Measured in the unmodified font (Regular, cap height 1433 units of 2048):

  lower dot bottom    306    0.214 of cap height   <- floating
  upper dot top      1142    0.797 of cap height
  dot diameter        236    0.165 of cap height
  gap between dots    364    0.254 of cap height   <- tight

For comparison, Baskervville Caps - the heading face these titles sit above -
seats its lower dot ON the baseline, rises to 0.707 of cap, and opens the gap
to 0.369 of cap.

Nodesto has no GSUB table at all: no features, no alternates, 115 glyphs. There
is no `case` form to freeze the way there was in Baskervville, so the dots had
to be moved in the outline itself.


WHAT WAS CHANGED
----------------
Two glyphs per style - colon and semicolon. Nothing else: no other outline, no
metric, no kern, no advance width. The colon and semicolon keep their original
advance widths, so line breaks and text length are unaffected.

The rule applied:

  * the pair seats on the baseline and rises to 0.723 of cap height
  * dot diameter 0.177 of cap in Regular and Italic. That is Nodesto's own cap
    stem width (measured 0.175), which is the standard colon-to-stem
    relationship. Bold and Bold Italic already draw 0.190 and keep theirs - a
    bolder weight should have heavier dots.
  * the gap is whatever is left over, so the bolder weights close up naturally
  * semicolon: the upper dot lands exactly where the colon's does, and the
    comma is aligned by its TOP to the colon's lower dot, which gives the comma
    back its descender

After the build:

                        Regular / Italic      Bold / Bold Italic
  cap height              1433                  1453
  lower dot bottom           0  (baseline)         0  (baseline)
  upper dot top           1036  (0.723 cap)     1051  (0.723 cap)
  dot diameter             254  (0.177 cap)      276  (0.190 cap)
  gap between dots         529  (0.369 cap)      499  (0.343 cap)
  semicolon comma bottom  -159                  -148

That semicolon comma bottom is the check worth knowing about: the font's own
standalone comma glyph sits at -158 in Regular and -178 in Bold. The rebuilt
semicolon comma lands within a unit of the Regular one, which is independent
confirmation that the alignment rule is the right one rather than a number
picked to look nice.

Italic and Bold Italic: each dot is scaled about its own centre and moved
vertically only, so the slant offset between the two dots is preserved.


LICENCE
-------
Nodesto Caps Condensed is by Solbera, Creative Commons Attribution-ShareAlike
4.0 International (CC BY-SA 4.0). This is a modified version; CC BY-SA requires
that the modification be indicated (it is, here and in the version string) and
that this derivative be distributed under the same licence.

The unmodified originals are kept in fonts/solbera/Nodesto Caps Condensed/.
