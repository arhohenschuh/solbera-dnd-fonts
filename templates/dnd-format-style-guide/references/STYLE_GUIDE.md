# D&D House Style — Canonical Formatting Guide (v3)

This is the authoritative formatting spec for D&D / TTRPG adventure chapters
("nodes") in this house style. It governs **how content is structured and
styled**, not what the content says. Everything here is self-contained; the
skill needs no external files.

The single source of truth for the rendered look is the named **paragraph
style system** captured in `references/template.docx`. The bundled builder
(`scripts/build_adventure_docx.py`) uses that required template and preserves
its styles and numbering. The bundle is the owner's current
`5e Module_Format.docx`, including specimen pages; generated documents contain
the supplied content instead of those samples. No v1 font migration is needed.

---

## 1. Six font families, one accent color

| Purpose | Value |
| --- | --- |
| Titles / stat block names | **Nodesto Caps Condensed** |
| Headings 2-4 | **Baskervville Caps** (drawn small caps) |
| Body prose / run-in labels / read-aloud | **Bookinsanity Remake** |
| Sidebar body / table body / metadata / legal | **Scaly Sans Remake** |
| Sidebar headlines / table headers / captions / footer | **Scaly Sans Caps** |
| Epigraphs | **Zatanna Misdirection**, italic |
| The one accent color | **#920000 (maroon)** — used for *all* display type, borders, and tier labels |
| Body text color | **#000000 (black)** |

There is exactly **one** red. Never introduce a second shade — always
`#920000 (maroon)`.

---

## 2. Named paragraph styles

Use these Word styles by name. Never hand-format headings with bold+size;
apply the style so the whole document stays consistent and re-themeable.

| Style | Font | Size | Weight/Style | Color | Notes |
| --- | --- | --- | --- | --- | --- |
| `Title` | Nodesto Caps Condensed | 28 | — | maroon | Book/adventure title only |
| `Heading 1` | Nodesto Caps Condensed | 28 | drawn small caps | maroon | **Node title** — `N17: Haunted Halls of Slaughter` |
| `Heading 2` | Baskervville Caps | 18.5 | drawn small caps | maroon | Structural spine sections; **no** bottom border |
| `Heading 3` | Baskervville Caps | 15 | drawn small caps | maroon | Area keys (`S1: …`) & feature blocks; **thin maroon underline** (bottom border sz 4) |
| `Heading 4` | Baskervville Caps | 13.5 | drawn small caps | maroon | Nested options under an H3 |
| `Heading 5` | Bookinsanity Remake | 10 | bold | black | Inline bold run-in variant (rarely needed) |
| `Heading 6` | — | 10 | bold | — | Bold heading in sidebar context |
| `Core Body` | Bookinsanity Remake | 10 | regular | black | Default prose; 6 pt before/after |
| `Core Bulleted` | Bookinsanity Remake | 10 | regular | black | `•` bullet list (carries real numbering) |
| `Boxed Text` | Bookinsanity Remake | 9 | regular | black | **Read-aloud** — full maroon box border (all 4 sides, sz 8) |
| `Epigraph` | Zatanna Misdirection | 10 | *italic* | black | In-character quotes; 0 spacing |
| `Sidebar Body` | Scaly Sans Remake | 10 | regular | black | Sidebar prose |
| `Sidebar Bulleted` | Scaly Sans Remake | 10 | regular | black | Sidebar/Tuning bullets |
| `Sidebar Headline` | Scaly Sans Caps | 12 | **bold** | maroon | The `Tuning The Encounter` header |
| `Stat Block Heading` | Nodesto Caps Condensed | 12 | — | maroon | Monster/stat-block title |
| `Stat Block Metadata` | Scaly Sans Remake | 10 | *italic* | black | Size/type/alignment line |
| `Legalese` | Scaly Sans Remake | 7 | — | black | Fine print |

Type headings in normal mixed case. Never use Word's synthetic Small caps or
All caps: the heading fonts already contain drawn small caps. Run-in labels use
Bookinsanity bold only, not bold italic. Its bold-italic file installs as a
separate family and must not be reached through synthetic formatting.

**Border details**
- `Boxed Text`: `single`, sz **8**, color `920000`, space 4, on **top/left/bottom/right**; `keepLines`.
- `Heading 3`: `single`, sz **4**, color `920000`, space 1, **bottom only** (a thin underline).
- `Heading 2`: bottom border explicitly **off**.

---

## 3. Run-level conventions (inside Core Body)

- **Run-in label paragraphs** are the workhorse. A paragraph opens with a
  **bold** `Label.` run, then continues in regular weight:
  > **Atmosphere.** The air feels cold and dank…
  Common labels: Atmosphere, Lighting, Walls, Floors, Ceiling, Doors,
  Denizens, Loot, Purpose, Description, History, Developments, Secret Door.
  (In the source, the bold label is sometimes preceded by a `\t` tab — cosmetic.)
- **Creature/stat references are bolded mid-sentence** per 5e convention:
  **skeleton**, **zombie**, **gray ooze**, **wight**.
- **Tuning tier labels** are bold **and maroon**, in fixed order:
  **Frail:**, **Baseline:**, **Strong:**, **Hard to kill:**

In builder JSON, wrap inline emphasis in `**double asterisks**`.

---

## 4. The Tuning The Encounter block

Every scalable encounter carries a four-tier difficulty block:

```
Tuning The Encounter            ← Sidebar Headline (12pt bold maroon)
• Frail:        …               ← Sidebar Bulleted, "Frail:" bold+maroon
• Baseline:     …
• Strong:       …
• Hard to kill: …
```

Order is fixed and all four tiers should appear. Baseline = the as-written
stat block; Frail = weaker; Strong / Hard to kill = escalations.
The builder rejects incomplete tier sets and keeps the headline with all four
bullets when the block fits on a page, instead of stranding the last tier.

---

## 5. Tables

Encounter, random-encounter, and roster tables use **three house colors,
applied by direct cell shading and direct cell borders** — not a theme table
style. (The default Office theme's Accent 2 is orange, so `Grid Table 4 -
Accent 2` renders orange; shade and border cells directly instead so the look
is theme-independent.)

- **Header row:** solid **#920000 (maroon)** fill, font **Scaly Sans Caps**, 9 pt,
  **white** (`#FFFFFF`) bold text.
- **Body rows:** **#F2DBDB (light pink)** banding on alternating rows (first
  data row white, second shaded, and so on); the remaining rows stay white.
  Text is **Scaly Sans Remake**, 9 pt, black.
- **All cell borders:** **#D99594 (shaded red)**, single, ~1pt (sz 8).
- **Vertical alignment:** every cell (header and body) is **vertically
  centered**.

Typical 3-column shapes:

- Random encounters: `D6 | Monster | See area`
- Adversary roster: `Encounter | Area | Notes`
- NPC locators: `Who | When | Where`

The builder shades and borders cells directly. When authoring by hand, set the
header fill to `920000` with white Scaly Sans Caps text, band alternating body rows
with `F2DBDB`, and give every cell a `D99594` border. (The three values were
sampled from real draft adventure tables.)

---

## 5a. Running footer

Every page carries a running footer, **right-aligned**, in **Scaly Sans Caps
10pt** black, in the form:

```
<Node number and name> -Page <n>
```

e.g. `N04: The Gralhund Villa -Page 1`. (The house original uses the adventure
title — `<Adventure Title> -Page 147`; for a single node, key it
to the node's number and name instead.) The builder derives the footer text
from the node title automatically, or from an explicit `{"type":"meta",
"running":"N04: The Gralhund Villa"}` block placed first in the block list.

---

## 6. Fixed macro-structure of a node

Author every node in this order. Section headings are **verbatim** and use the
levels shown.

```
Heading 1   N##: Node Name
Epigraph    In-character quote(s) + —Attribution        (optional)
Heading 2   Revelations            → Core Bulleted list (how PCs learn of it)
Heading 2   Overview               → run-in labels (District/Street, Purpose,
                                       Description, History, Footprints, Secret Door)
                                     + first-arrival Boxed Text
Heading 2   Main Scenario
Heading 3     <Place> Features     → run-in label paragraphs (Atmosphere, Lighting, …)
Heading 3     Random Encounters    → intro + table
Heading 3     Adversary Roster     → intro + table
Heading 2   Locations of The <Place> (S)   → intro sentence
Heading 3     S1: <Name>           → Boxed read-aloud + run-in mechanics [+ Tuning]
Heading 3     S2: <Name>           → …
              …                     (S1…Sn area keys, in order)
Heading 2   Developments           → post-dungeon consequences
Heading 3     <topic>              [Heading 4 nested options]
Heading 2   Clues
Heading 3     Evidence
Heading 3     Leads
```

Each **area key (H3)** follows the same internal rhythm:
1. **Boxed Text** read-aloud describing the room on first sight.
2. **Run-in label** paragraphs for the interactive/mechanical elements.
3. Optional **Tuning The Encounter** block if the room has a scalable fight.

---

## 7. Do / Don't

**Do**
- Apply named styles; keep the single maroon `#920000`.
- Lead mechanical paragraphs with a bold run-in `Label.`.
- Bold creature names inline; keep the four Tuning tiers in order.
- Open each area key with Boxed read-aloud text.

**Don't**
- Don't hand-format headings (size+bold) instead of using the style.
- Don't invent a second red or introduce fonts outside the six v3 families.
- Don't put read-aloud text in Core Body — it belongs in Boxed Text.
- Don't reorder or rename the fixed spine sections.
