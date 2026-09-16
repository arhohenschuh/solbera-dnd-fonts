Baskervville Caps
=================

Two-style small-caps build of Baskervville SC (ANRT, SIL OFL 1.1), made for the
D&D House Style Word template.

  BaskervvilleCaps-Regular.ttf
  BaskervvilleCaps-Bold.ttf

Installs as family "Baskervville Caps", Version 1.201
(upstream Baskervville SC is 1.100; this derivative carries the next minor).


WHY
---
Mrs Eaves, the face Wizards use for headings in the 5e books, is a Baskerville
revival. Baskervville is a Baskerville revival too (ANRT, Nancy), which makes it
the closest libre stand-in in register — closer than Andada or Bonum.

Baskervville ships its small caps behind the OpenType `smcp` feature and its
cap-height figures behind `lnum`, and Word can switch on neither. The variable
axis was instantiated at 400 and 700, then both features were applied
permanently to the cmap.

Two corrections were needed beyond the plain freeze.

1. `smcp` was applied to LOWERCASE LETTERS ONLY, and `lnum` to DIGITS ONLY.
   Baskervville's smcp set also contains small-cap-sized punctuation, so a
   blanket freeze shrinks the parentheses, brackets, colon, quotes and
   ampersand to small-cap proportions. 66 non-letter glyphs were left alone.

2. Upstream Baskervville SC wires its small-caps lookup (GSUB lookup 30) into
   BOTH `smcp` and `ccmp`. `ccmp` is a default-on feature that every shaper
   applies unconditionally, so in the shipped font the parentheses render at
   small-cap size in *any* application, whether or not small caps were asked
   for. That lookup has been removed from the ccmp feature here; ccmp keeps
   its legitimate lookups (2, 4, 6, 8). This is an upstream bug, not a
   consequence of the freeze - the unmodified font behaves the same way.

Measured after the fix, at cap height 214 px: the parenthesis rises 25 px above
the capitals (Andada SC: 16 px, Mr Eaves: 33 px). Before the fix it sat 39 px
BELOW them.

3. (v1.201) Six punctuation marks were switched to their `case` forms, which
   Baskervville draws for setting among capitals:

     :  ;  -  en dash  em dash  middot

   The default colon tops out at 0.61 of cap height, which reads as sunken
   between capitals; the case form sits at 0.71 (Andada SC: 0.66). Dot size is
   identical in both - only the position and the gap between the dots change.
   Parentheses, brackets and quotation marks were deliberately NOT switched:
   the parens have no case form, and the quote marks' case forms are drawn for
   all-caps setting, which would be wrong for German low quotes.

Measured after the build (units per 1000 em):

  cap height    713
  small caps    460   (0.645 of cap)
  digits        715   (1.003 of cap)  <- the point of the exercise
  parentheses   796   (1.12 of cap)   <- left untouched, as they should be

Typing "a" now yields a small-cap A. Digits stand at full cap height, so an
area key like "L1:" or "D2." matches the printed books, where the capital and
the digit measure identically.

German: ä ö ü map to small-cap glyphs; ß maps to germandbls.sc.

Nothing else was changed — no outline, metric or kern.


LICENCE
-------
Baskervville is (c) 2018 The Baskervville Project Authors
(https://github.com/anrt-type/ANRT-Baskervville), SIL Open Font License 1.1.
No Reserved Font Name is declared, but the family has been renamed anyway so
this build cannot be confused with the upstream release. The OFL requires that
this derivative also be distributed under the OFL.
