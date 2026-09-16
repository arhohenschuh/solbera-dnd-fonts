Bonum SC
========

Four-style small-caps build of TeX Gyre Bonum, made for the D&D House Style
Word template.

  BonumSC-Regular.otf
  BonumSC-Bold.otf
  BonumSC-Italic.otf
  BonumSC-BoldItalic.otf

Installs in Windows as family "Bonum SC", Version 2.100, with the four standard
styles, so Ctrl+B and Ctrl+I work normally.
(upstream TeX Gyre Bonum is 2.004; this derivative carries the next minor.)


WHAT WAS CHANGED
----------------
The OpenType `smcp` (small capitals) feature of TeX Gyre Bonum was applied
permanently with pyftfeatfreeze (Adam Twardoch, opentype-feature-freezer), so
the small-cap glyphs now sit in the lowercase slots of the cmap. Typing "a"
produces a small-cap A.

This is needed because Microsoft Word has no control for the `smcp` feature —
its Font dialog's "Small caps" checkbox fakes small caps by shrinking real
capitals, which produces visibly lighter, wrongly proportioned letters. With
this build the small caps are the font's own drawn glyphs.

Nothing else was altered: no outline, metric, kerning or feature was changed
apart from the cmap substitution and the name table.

The document text is unaffected. "The Fishery" is still stored as the
characters T-h-e space F-i-s-h-e-r-y, so search, copy-paste, cross-references
and generated tables of contents all behave normally.


WHY THIS BUILD EXISTS
---------------------
Measured from the binaries (units per 1000 em):

  face                          cap    small cap   digit   digit/cap
  Bonum SC                      681    485         681     1.000
  Mr Eaves SC Remake            602    434         454     0.754
  Andada SC                     710    533         672     0.946
  Alegreya SC Medium            647    505         507     0.784

Area-key headings mix a capital with digits ("L1:", "D2."). The printed 5e
books set that digit at full cap height — verified against a scan of Baldur's
Gate: Descent into Avernus, where the capital D and the digit 1 measure
identically. Mr Eaves SC Remake draws its figures at small-cap height instead,
so the digit comes out 25% short. Bonum's figures are already at exactly cap
height, and freezing smcp adds the small caps without disturbing them.

German coverage is complete: ä ö ü map to small-cap glyphs, and ß maps to
germandbls.sc, which renders as two small-cap S — the conventional small-cap
eszett.


LICENCE
-------
TeX Gyre Bonum is (c) 2007-2009 B. Jackowski and J.M. Nowacki (on behalf of
TeX Users Groups), released under the GUST Font License (GFL), a LPPL 1.3c
variant. The GFL permits modification and redistribution provided the modified
font is renamed so it cannot be confused with the original release — hence
"Bonum SC" rather than "TeX Gyre Bonum".

The full licence text ships with the original package at
  ../../vendor/tex-gyre/doc/GUST-FONT-LICENSE.txt
(relative to this folder)
and applies to these files unchanged.
