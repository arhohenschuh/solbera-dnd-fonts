# D&D House Style — Font and Formatting Standard

The typography standard for adventure nodes, chapters and handouts produced from
[../templates/5e Module_Format.docx](../templates/5e%20Module_Format.docx).
It imitates the look of the 2014-era 5th Edition books
using freely licensed substitutes for the commercial faces Wizards of the Coast
used.

**Status:** current. Supersedes the Andada SC / TeX Gyre Bonum stack (v1) and the
Mr Eaves stack (v2).

---

## The one colour

`#920000` — maroon. Every piece of display type, every border, every tier label
and every table header uses it. Body text is black. **There is no second red.**

Table colours, applied as direct cell shading rather than a theme table style so
they survive any theme:

| role | colour |
| --- | --- |
| header row fill | `#920000`, white bold text |
| body row banding | `#F2DBDB` on alternating rows, first data row white |
| cell borders | `#D99594` |

All cells, header and body, are vertically centred.

---

## The font stack

Six faces. Each stands in for the commercial face Wizards actually used.

| Role | Word style | Font — type this name exactly | Size | Colour |
| --- | --- | --- | --- | --- |
| Module / chapter title | Title, Heading 1 | Nodesto Caps Condensed | 28 pt | #920000 |
| Spine heading | Heading 2 | Baskervville Caps | 18.5 pt | #920000 |
| Area key / feature block | Heading 3 | Baskervville Caps | 15 pt | #920000 + thin maroon rule |
| Nested option | Heading 4 | Baskervville Caps | 13.5 pt | #920000 |
| Body prose | Core Body, Core Bulleted | Bookinsanity Remake | 10 pt | black |
| Run-in label | bold run in Core Body | Bookinsanity Remake **Bold** | 10 pt | black |
| Read-aloud | Boxed Text | Bookinsanity Remake | 9 pt | black, full maroon box |
| Epigraph | Epigraph | Zatanna Misdirection | 10 pt italic | black |
| Sidebar / Tuning headline | Sidebar Headline | Scaly Sans Caps | 12 pt | #920000 |
| Sidebar / Tuning body | Sidebar Body, Sidebar Bulleted | Scaly Sans Remake | 10 pt | black, tier labels bold maroon |
| Stat block name | Stat Block Heading | Nodesto Caps Condensed | 12 pt | #920000 |
| Stat block type line | Stat Block Metadata | Scaly Sans Remake *Italic* | 10 pt | black |
| Table header row | direct formatting | Scaly Sans Caps, bold | 9 pt | white on #920000 |
| Table body | direct formatting | Scaly Sans Remake | 9 pt | black |
| Running footer | footer | Scaly Sans Caps | 10 pt | black |
| Legal / colophon | Legalese | Scaly Sans Remake | 7 pt | black |

The split follows how Wizards used the originals: Modesto Condensed for titles,
Mrs Eaves Small Caps for headings, Bookmania for body, Scala Sans for tables and
info boxes, Scala Sans Caps for captions and page numbers, Dai Vernon Misdirect
for in-character quotes.

### Why these point sizes differ from v2

Heading sizes are matched on **cap height**, not on nominal point size. Cap
height per em differs sharply between faces, so the same point size produces
visibly different headings:

| face | cap height / em | multiplier vs Mr Eaves |
| --- | --- | --- |
| Mr Eaves SC Remake | 0.602 | 1.00 |
| Baskervville Caps | 0.713 | 0.845 |
| Andada SC | 0.710 | 0.848 |
| TeX Gyre Bonum | 0.681 | 0.884 |

Heading 2 at 22 pt in Mr Eaves equals 18.5 pt in Baskervville Caps. If you ever
swap the heading face again, multiply by the figure above rather than keeping
the point size.

---

## Running footer

Every page, right-aligned, Scaly Sans Caps 10 pt:

    <node number and name> -Page <n>

for example `N04: The Gralhund Villa -Page 1`.

---

## Fixed node spine

    Title
      Epigraph
      Revelations
      Overview
      Main Scenario  (Features / Random Encounters / Adversary Roster)
      Locations of The …            (S)
        S1 … Sn area keys
      Developments
      Clues  (Evidence / Leads)

Area keys open with Boxed read-aloud text, then run-in labels. Creature names
are bolded inline. The *Tuning the Encounter* block is a Sidebar Headline plus
four bullets in fixed order — **Frail / Baseline / Strong / Hard to kill** — with
the labels bold and maroon.

---

## Where the fonts come from

Four are used as published. Two are local builds — one because Word cannot
switch on the OpenType features it needs, one because a punctuation mark was
drawn for a kind of setting we do not use.

| Font | Source | Licence | Modified? |
| --- | --- | --- | --- |
| **Nodesto Caps Condensed** | [../fonts/custom/Nodesto Caps Condensed/README.txt](../fonts/custom/Nodesto%20Caps%20Condensed/README.txt) | CC BY-SA 4.0 | **yes — built here** |
| Bookinsanity Remake | Solbera D&D font set | CC BY-SA 4.0 | no |
| Scaly Sans Remake | Solbera D&D font set | CC BY-SA 4.0 | no |
| Scaly Sans Caps | Solbera D&D font set | CC BY-SA 4.0 | no |
| Zatanna Misdirection | Solbera D&D font set | CC BY-SA 4.0 | no |
| **Baskervville Caps** | [../fonts/custom/Baskervville Caps/README.txt](../fonts/custom/Baskervville%20Caps/README.txt) | SIL OFL 1.1 | **yes — built here** |

[Bonum SC](../fonts/custom/Bonum%20SC/README.txt) also sits in this repository.
It is a working alternative, not part
of the standard: it is a Bookman, and Bookinsanity is a Bookman too, so the two
stacked read as a mistake rather than a pairing. Keep it only if you ever move
the body face off Bookinsanity.

### Why Baskervville Caps exists

Mrs Eaves is a Baskerville revival. Baskervville (ANRT Nancy) is one too, which
makes it the closest libre stand-in in register. But its published SC release is
unusable in Word as shipped, for three separate reasons — all fixed in the build
documented in [../fonts/custom/Baskervville Caps/README.txt](../fonts/custom/Baskervville%20Caps/README.txt):

1. Its small caps live behind the `smcp` feature. Word has no `smcp` control,
   and its *Small caps* checkbox fakes them by shrinking real capitals. Frozen
   into the cmap so the lowercase slots hold the drawn small caps.
2. Its figures default to oldstyle. Area keys mix a capital with digits (`L1:`,
   `D2.`), and the printed books set that digit at full cap height — verified
   against a scan of *Descent into Avernus*, where the capital D and the digit 1
   measure identically. `lnum` frozen in.
3. Upstream wires the small-caps lookup into `ccmp` as well as `smcp`. `ccmp` is
   default-on, so the parentheses and colon render at small-cap size in *any*
   application. That lookup was removed from `ccmp`.

Plus one refinement: six punctuation marks — `:` `;` `-` `–` `—` `·` — use the
font's `case` forms, which sit correctly among capitals. The default colon tops
out at 0.61 of cap height and reads as sunken; the case form sits at 0.71.

### Why the Nodesto build exists

Set a title with a colon in it — `Appendix: Wild Magic Table` — and the stock
Nodesto colon floats. Both dots sit clear of the baseline *and* clear of the cap
line, so beside these very heavy condensed capitals the mark reads as a small
detached cluster rather than as punctuation belonging to the line.

| | stock Nodesto | Baskervville Caps | the build |
| --- | --- | --- | --- |
| lower dot bottom | 0.214 cap | 0.000 cap | **0.000 cap** |
| upper dot top | 0.797 cap | 0.707 cap | **0.723 cap** |
| dot diameter | 0.165 cap | 0.177 cap | **0.177 cap** |
| gap between dots | 0.254 cap | 0.369 cap | **0.369 cap** |

Nodesto has no `GSUB` table at all — no features, no alternates, 115 glyphs — so
there was no `case` form to freeze the way there was in Baskervville. The dots
were moved in the outline instead. Two glyphs per weight, colon and semicolon;
no other outline, metric, kern or advance width was touched, so line breaks and
text length are unchanged.

Dot diameter is now 0.177 of cap in Regular and Italic, which is Nodesto's own
cap stem width — the standard colon-to-stem relationship. Bold and Bold Italic
already drew 0.190 and kept theirs, since a bolder weight should have heavier
dots; their gap closes up to 0.343 cap to hold the same 0.723 span.

The semicolon follows the colon: upper dot in the same place, comma aligned by
its top to the colon's lower dot. That drops the comma's tail to −159 units in
Regular, where the font's own standalone comma sits at −158 — a one-unit match,
which is independent confirmation that the rule is right rather than a number
picked to look nice.

The build keeps the family name `Nodesto Caps Condensed` and carries Version
1.100 against the Solbera original's 1.0, so it replaces the original on install
and nothing in the template, the skill or the validator has to change. The cost
is that reinstalling from `fonts/solbera/` silently puts the old colon back —
see the warning under Installing.

---

## Installing

Install every `.otf` and `.ttf` from these folders, relative to the repository root:

    fonts/solbera/Bookinsanity/
    fonts/solbera/Scaly Sans/
    fonts/solbera/Scaly Sans Caps/
    fonts/solbera/Zatanna Misdirection/
    fonts/custom/Baskervville Caps/
    fonts/custom/Nodesto Caps Condensed/

**Take Nodesto from `fonts/custom/`, not from `fonts/solbera/`.** Both install
under the same family name, so whichever you install last wins. The custom build
reports Version 1.100 in the font properties dialog; the unfixed original
reports 1.0. If a title's colon ever looks wrong again, check that number first.

Select the files in Explorer, right-click, **Install for all users**. Restart
Word afterwards — it reads the font list once at startup.

If a page comes out in Calibri or Times, a font is missing or was typed under
the wrong name. Check these six strings against the Windows font list before
touching a single style:

    Nodesto Caps Condensed
    Baskervville Caps
    Bookinsanity Remake
    Scaly Sans Remake
    Scaly Sans Caps
    Zatanna Misdirection

Two of the Solbera families install under a name that differs from their
folder — `Bookinsanity Remake`, `Scaly Sans Remake` — which is the commonest way
this goes wrong.

---

## Things that will bite you

**Type headings in normal mixed case.** Nodesto and Baskervville Caps carry
small caps in the lowercase slots. Never apply an all-caps transform: it
flattens the cap-to-small-cap contrast the whole look depends on.

**Never use Word's *Format → Font → Small caps*.** It shrinks real capitals
rather than using the font's drawn small caps, producing lighter, wrongly
proportioned letters beside genuine ones.

**Bookinsanity Bold Italic is orphaned.** It installs as its own family,
`Bookinsanity Remake Smbld Itlc`, style Regular, so bold + italic on Bookinsanity
Remake never reaches it and Word fakes a slant. This is why run-in labels are
**bold only**, not bold italic.

**Document text is unaffected by the small-caps build.** "The Fishery" is stored
as ordinary lowercase characters, so search, copy-paste, cross-references and a
generated table of contents all behave normally.

**Send a PDF, not a .docx,** to anyone who does not have these fonts installed.
Word's *Embed fonts in the file* also works, but check the result on a clean
machine first — OpenType/CFF embedding support varies by Word version.

---

## Licensing

The Solbera faces are CC BY-SA 4.0: credit the author and license derivatives
the same way. The Nodesto build here is such a derivative — the modification is
indicated in its README and in the font's version string, and it stays CC BY-SA.
Baskervville Caps is SIL OFL 1.1 and must stay OFL.

Separately from font licensing: imitating official D&D book typography in a
*distributed* product can raise trade-dress questions even when every font is
freely licensed. Personal and table use is not a concern.

---

## History

| version | heading face | body face | note |
| --- | --- | --- | --- |
| v1 | Andada SC | TeX Gyre Bonum | original house style |
| v2 | Mr Eaves SC Remake | Bookinsanity Remake | moved to the Solbera set; digits sat at small-cap height, so `L1:` and `S1.` broke |
| v3 | Baskervville Caps | Bookinsanity Remake | Baskerville register like Mrs Eaves, cap-height digits, corrected parentheses and colon |
| **v3.1** | **Baskervville Caps** | **Bookinsanity Remake** | current — same stack; Nodesto's floating colon and semicolon rebuilt to seat on the baseline (font Version 1.100). No style, size or colour changed, so v3 documents need no migration |
