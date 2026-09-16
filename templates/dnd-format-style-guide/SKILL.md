---
name: dnd-format-style-guide
description: "Apply and validate D&D House Style version 3 for Word (.docx) adventure nodes, chapters, modules, area keys, stat blocks, and handouts. Uses the bundled current Word template: Nodesto titles, Baskervville Caps headings, Bookinsanity prose, Scaly Sans tables, Scaly Sans Caps captions and footers, Zatanna epigraphs, and maroon #920000. Covers named styles, boxed read-aloud, bold run-in labels, four-tier encounter tuning, banded tables, running footers, and the fixed node spine. Use when creating, formatting, restyling, or checking D&D Word documents, applying the house style or module format, laying out dnd-node-* or dnd-area-* content, or migrating v1/v2 documents to v3."
metadata:
  version: "3.0.0"
---

# dnd-format-style-guide — House formatting for adventure chapters (v3)

This skill owns **how an adventure node looks and is structured** in the D&D
House Style: the named Word style system, the single maroon `#920000` accent,
the house font set, boxed read-aloud text, bold run-in labels, the four-tier
*Tuning The Encounter* block, shaded tables, a running footer, and the fixed
section spine.

Two jobs:

1. **FORMAT / GENERATE** — turn adventure content into a styled `.docx`.
2. **VALIDATE** — check existing content against the guide and report deviations.

> This skill governs **formatting**, not narrative content. Building the
> *content* of a node or its keyed areas belongs to the `dnd-node-*` and
> `dnd-area-*` skills. This is the presentation layer they hand off to.

## Version history, and what it means for the bundled files

| version | headings | body | why it moved |
| --- | --- | --- | --- |
| v1 | Andada SC | TeX Gyre Bonum | original |
| v2 | Mr Eaves SC Remake | Bookinsanity Remake | moved to the Solbera set for a closer 5e look |
| **v3** | **Baskervville Caps** | Bookinsanity Remake | Mr Eaves draws its figures at small-cap height, so every area key (`L1:`, `S1.`, `D2.`) came out with a capital 25% taller than its own digit |

The maroon `#920000` accent, all table colours, every style name and the spine
are unchanged across all three versions. Only typefaces and heading point sizes
move.

**Version 3 is the current house style.** The bundled template, reference guide,
builder, and validator all use v3. The template is an exact bundled copy of the
owner's current `5e Module_Format.docx`, not a reconstructed or content-free
approximation. Its sample pages are retained in the bundle for visual reference;
the builder removes them from generated documents.

Use the named styles from that template unchanged. Do not run a v1 builder,
redefine the styles from scratch, or apply a post-build font replacement. V1 and
v2 appear here only as historical context, never as generation defaults.

---

## Bundled assets (read before working — don't work from memory)

- `references/STYLE_GUIDE.md` — the spec for borders, run-in conventions, the
  Tuning block, table colours, the footer, and the node macro-structure.
  **Read this first**; it specifies the v3 fonts and sizes below.
- `references/example_node.json` — a worked content spec showing every block
  type in the correct order. Still accurate; blocks and order are unchanged.
- `references/template.docx` — the current v3 Word template, including its
  specimen content, real named styles, numbering, and page layout.
- `scripts/build_adventure_docx.py` — the builder. Renders a JSON block list
  into a styled `.docx` using the required bundled template. It preserves the
  named styles and numbering, clears sample content, and replaces the footer.
- `scripts/validate_adventure_docx.py` — the style checker (CRITICAL / MAJOR /
  MINOR). Checks effective v3 fonts and sizes, including inherited formatting,
  plus borders, tables, tuning, the footer, and the node spine.
- `scripts/test_house_style.py` — executable positive and negative regression
  checks for v3 generation and validation.

---

## Font dependencies

This skill binds to **font names and nothing else**. It names no drive, no
folder, no repository, no download. All it needs from outside itself is that
these six families are installed on the machine that opens the document:

```
Nodesto Caps Condensed
Baskervville Caps
Bookinsanity Remake
Scaly Sans Remake
Scaly Sans Caps
Zatanna Misdirection
```

Write those strings into Word, and into any script, exactly as spelled here.
Several install under a name that differs from how people refer to the face,
which is the commonest way this goes wrong: someone types the colloquial name,
Word substitutes silently, and the page then reads as a broken stylesheet rather
than a missing font. So when a page comes out in Calibri or Times, check these
six spellings against the system font list before touching a single style. Word
caches its font list at startup — restart it after installing anything.

`Baskervville Caps` is a derived build, not a stock download: upstream
Baskervville SC keeps its small caps behind the OpenType `smcp` feature and its
cap-height figures behind `lnum`, and Word can switch on neither. The build that
ships with the house-style font set has both baked into the cmap, plus two
corrections described under *Why the heading face changed*.

---

## The v3 font system

| Role | Word style | Font | Size | Colour |
| --- | --- | --- | --- | --- |
| Node / module title | Title, Heading 1 | Nodesto Caps Condensed | 28 pt | #920000 |
| Spine heading | Heading 2 | Baskervville Caps | 18.5 pt | #920000 |
| Area key / feature block | Heading 3 | Baskervville Caps | 15 pt | #920000 + thin maroon rule |
| Nested option | Heading 4 | Baskervville Caps | 13.5 pt | #920000 |
| Body prose | Core Body, Core Bulleted | Bookinsanity Remake | 10 pt | black |
| Run-in label | bold run inside Core Body | Bookinsanity Remake **Bold** | 10 pt | black |
| Read-aloud | Boxed Text | Bookinsanity Remake | 9 pt | black, full maroon box |
| Epigraph | Epigraph | Zatanna Misdirection | 10 pt italic | black |
| Sidebar / Tuning headline | Sidebar Headline | Scaly Sans Caps | 12 pt | #920000 |
| Sidebar / Tuning body | Sidebar Body, Sidebar Bulleted | Scaly Sans Remake | 10 pt | black; tier labels bold maroon |
| Stat block name | Stat Block Heading | Nodesto Caps Condensed | 12 pt | #920000 |
| Stat block type line | Stat Block Metadata | Scaly Sans Remake *Italic* | 10 pt | black |
| Table header row | direct formatting | Scaly Sans Caps, bold | 9 pt | white on #920000 |
| Table body | direct formatting | Scaly Sans Remake | 9 pt | black |
| Running footer | footer | Scaly Sans Caps | 10 pt | black |
| Legal / colophon | Legalese | Scaly Sans Remake | 7 pt | black |

The split follows how Wizards used the commercial originals: Modesto Condensed
for titles, Mrs Eaves Small Caps for headings, Bookmania for body, Scala Sans
for tables and info boxes, Scala Sans Caps for captions and page numbers, Dai
Vernon Misdirect for in-character quotes.

### Heading sizes are matched on cap height, not point size

This is why v3's heading sizes look smaller than v2's and are not a mistake.
Cap height per em differs sharply between faces, so the same point size gives
visibly different headings:

| face | cap height / em | multiplier vs Mr Eaves |
| --- | --- | --- |
| Mr Eaves SC Remake | 0.602 | 1.00 |
| Baskervville Caps | 0.713 | 0.845 |
| Andada SC | 0.710 | 0.848 |
| TeX Gyre Bonum | 0.681 | 0.884 |

Heading 2 at 22 pt in Mr Eaves equals 18.5 pt in Baskervville Caps. If the
heading face is ever swapped again, multiply by that figure rather than keeping
the point size — and re-derive the multiplier from the new face's actual cap
height rather than trusting a specimen.

### Why the heading face changed

Area keys mix a capital with digits. The printed books set that digit at full
cap height — verified against a scan of *Baldur's Gate: Descent into Avernus*,
where the capital D and the digit 1 in `D1.` measure identically. Mr Eaves SC
Remake draws its figures at small-cap height instead (454 against a cap height
of 602), so `S1.` and `L1:` always came out wrong, and its empty GSUB offered no
`lnum` to switch. Its colon sits at 0.46 of cap height too, which reads as
sunken between capitals.

Baskervville is, like Mrs Eaves, a Baskerville revival, so it keeps the right
register. In the derived build its digits stand at 1.00 of cap height, its
parentheses at 1.12, and `:` `;` `-` en dash em dash middot use the font's
`case` forms, which sit correctly among capitals.

### Things that will bite you

- **Type headings in normal mixed case.** Nodesto and Baskervville Caps carry
  small caps in the lowercase slots. Never apply an all-caps transform — it
  flattens the cap-to-small-cap contrast the whole look depends on.
- **Never use Word's *Format → Font → Small caps*.** It shrinks real capitals
  instead of using the font's drawn small caps, producing lighter, wrongly
  proportioned letters beside genuine ones.
- **Bookinsanity Bold Italic is orphaned.** It installs as its own family,
  `Bookinsanity Remake Smbld Itlc`, style Regular, so bold + italic on
  Bookinsanity Remake never reaches it and Word fakes a slant. This is why
  run-in labels are **bold only**, not bold italic.
- **Baskervville's small caps are delicate** — 0.645 of cap height, against
  Mr Eaves' 0.72. That is the design, not a defect; it is also why the heading
  sizes above must not be trimmed further.

**Keeping a finished document portable.** A `.docx` styled this way renders
correctly only where those six families are installed. If it goes to someone who
doesn't have them, send a PDF — the reliable choice, and what a table handout
wants anyway — or turn on Word's *File → Options → Save → Embed fonts in the
file* and re-save. Check an embedded file on a clean machine before relying on
it: OpenType/CFF embedding support varies by Word version.

Licensing: the Solbera faces are CC BY-SA 4.0, Baskervville Caps is SIL OFL 1.1.
Credit in the colophon and license derivatives the same way.

---

## How to GENERATE a styled .docx

1. Reuse the project's selected Python environment. Do not prompt for a new
  interpreter on each operation. Ensure `python-docx` and `lxml` are available
  in that environment; install with `python -m pip install python-docx lxml`
  only when needed. Commands below use `python` for that selected interpreter.
2. Assemble the node as a **JSON block list** — see
   `references/example_node.json` for every block type. Blocks render in order:
   `title, h2, h3, h4, epigraph, boxed, body, label, bullet, tuning, table,
   statheading, statmeta, meta`. Inline `**bold**` works in text fields. A
   leading `{"type":"meta","running":"N04: The Gralhund Villa"}` sets the
   running footer; otherwise it derives from `title`.
3. From the skill directory, build and validate:

   ```powershell
   python scripts/build_adventure_docx.py <content.json> <out.docx>
   python scripts/validate_adventure_docx.py <out.docx> --json
   ```

   `--demo` instead of a JSON path emits the built-in sample, the fastest way to
   sanity-check the environment. The template is required; missing it is an
   error, never permission to fall back to blank Word defaults.

Prefer the JSON + script route over hand-building a `.docx`, so the named-style
system stays intact.

After building, open the result and look at page 1 before declaring victory —
a silent font substitution looks like a styling bug, and eyes are the only way
to catch it. Check an area-key heading specifically: if the digit in `L1:` is
shorter than the capital, the heading face did not apply.
The validator checks declared formatting, not installed fonts or Word's glyph
fallback. Inspect the rendered output as well; PDF viewers may substitute
unembedded OpenType fonts even when the document's styles are correct.

### Migrating older documents

Preserve the content and map its roles to the bundled v3 named styles. The
builder accepts JSON blocks, not an existing Word file. Do not claim that
opening or copying a v1/v2 document migrates its direct formatting. For a
document-preserving migration, use the Word/document-editing workflow, clear
stale font and size overrides where appropriate, and apply v3 table and footer
formatting explicitly. Validate and visually compare before replacing the
original. Never reintroduce the removed v1 restyling recipe.

## How to author WITHOUT the script

When producing content inside another docx pipeline, apply the **named styles by
name** and let the table above supply the face. Never approximate a heading with
manual size + bold; applying the style is what keeps the document consistent and
re-themeable. For tables, shade the header cell `#920000` with white bold Scaly
Sans Caps, band alternating body rows `#F2DBDB`, give every cell a `#D99594`
border, vertically centre all cells, and set body cells in Scaly Sans Remake.
Add the right-aligned footer `<node number and name> -Page <n>` in Scaly Sans
Caps.

---

## Quick reference

- **One display accent:** `#920000` for all display type, borders, tier labels
  and table headers. Body text is black. There is no second red.
- **Heading levels:** H1 28 pt node title · H2 18.5 pt spine · H3 15 pt area
  keys and feature blocks (thin maroon rule) · H4 13.5 pt nested options.
- **Boxed Text** = read-aloud, full maroon box border, 9 pt.
- **Run-in labels:** mechanical paragraphs open with a **bold** `Label.` run.
- **Creature names** are bolded inline (5e convention).
- **Tuning The Encounter** — Sidebar Headline plus four bullets in fixed order:
  **Frail / Baseline / Strong / Hard to kill**, labels bold and maroon.
- **Tables — three colours, applied as direct cell shading and borders** so they
  survive any theme: header `#920000`, body banding `#F2DBDB` on alternating
  rows (first data row white), cell borders `#D99594`, all cells vertically
  centred.
- **Running footer:** every page, right-aligned, 10 pt —
  `<node number and name> -Page <n>` (e.g. `N04: The Gralhund Villa -Page 1`).
- **Fixed spine:** Title → Epigraph → Revelations → Overview → Main Scenario
  (Features / Random Encounters / Adversary Roster) → Locations of The … (S) →
  S1…Sn area keys → Developments → Clues (Evidence / Leads).

Exact border sizes and the per-area-key rhythm are in
`references/STYLE_GUIDE.md`.

---

## How to VALIDATE existing content

```powershell
python scripts/validate_adventure_docx.py <file.docx> [--node N17] [--json]
```

`--node N17` restricts checks to the chapter whose Heading 1 starts with `N17`.
Shared style definitions, tables, and running footers are checked document-wide.
This checker is for finished nodes, not the template's illustrative sample
pages, which intentionally do not contain the complete node spine. Exit code
is non-zero if any CRITICAL finding is present. Review MAJOR and MINOR findings
as well; exit code zero alone is not a zero-findings report.

The validator checks the six v3 families in their correct roles, heading sizes,
inherited and direct formatting, synthetic caps, read-aloud borders, table
colours and typography, and the running footer. A v1/v2 font finding is a real
failure, not an advisory to ignore or a reason to weaken the checker.

Run the bundled regression suite after changing the skill or its template:

```powershell
python -B -m unittest discover -s scripts -p test_house_style.py -v
```

Beyond what the script sees, confirm by eye:

- **Structure:** spine sections present, correctly named and in order; each area
  key opens with Boxed read-aloud followed by run-in labels.
- **Styles:** headings use the named styles at the right levels (H1 node, H2
  spine, H3 area keys, H4 nested); read-aloud lives in **Boxed Text**, never in
  Core Body.
- **Area keys:** in `L1:` or `D2.` the digit stands at the same height as the
  capital. A short digit means the document is still on the v2 heading face.
- **Fonts:** the six house faces and nothing else — a stray Calibri or Times is
  almost always a font that failed to install, not a deliberate choice.
- **Run-ins and creatures:** mechanical paragraphs lead with a bold `Label.`;
  creature names bolded inline.

Report findings graded CRITICAL / MAJOR / MINOR, each with the offending text
and the fix, so the author can act on them without re-reading the whole guide.