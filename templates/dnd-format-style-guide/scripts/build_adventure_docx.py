#!/usr/bin/env python3
"""
build_adventure_docx.py — Self-contained builder for the canonical
D&D House Style.

Produces a .docx using the v3 named styles from the required bundled
references/template.docx. The bundle is the current 5e Module_Format.docx;
its styles, numbering, and final section layout are preserved. Sample content
is removed before the supplied blocks are rendered. There is no legacy-font
fallback and no post-build font migration step.

USAGE
  python build_adventure_docx.py content.json out.docx
  python build_adventure_docx.py --demo out.docx     # emit a sample node

CONTENT JSON (a list of blocks). Each block: {"type": ..., ...}
  {"type":"title","text":"..."}                 -> Heading 1  (node title, e.g. "N17: ...")
  {"type":"h2","text":"..."}                     -> Heading 2  (Revelations / Overview / Main Scenario / Locations... / Developments / Clues)
  {"type":"h3","text":"..."}                     -> Heading 3  (area keys "S1: ...", feature blocks)
  {"type":"h4","text":"..."}                     -> Heading 4  (nested options)
  {"type":"epigraph","text":"...","by":"..."}    -> Epigraph (italic quote + attribution line)
  {"type":"boxed","text":"..."}                  -> Boxed Text (read-aloud, maroon border)
  {"type":"body","text":"..."}                   -> Core Body paragraph (supports **bold** inline)
  {"type":"label","label":"Atmosphere","text":"..."}  -> Core Body with bold run-in "Label." + text (supports **bold**)
  {"type":"bullet","text":"..."}                 -> Core Bulleted (supports **bold**)
  {"type":"tuning","tiers":{"Frail":"...","Baseline":"...","Strong":"...","Hard to kill":"..."}}
                                                 -> "Tuning The Encounter" headline + 4 Sidebar Bulleted tiers
  {"type":"table","header":["D6","Monster","Area"],"rows":[["1-2","...","S3"], ...]}
  {"type":"statheading","text":"Goblin"}         -> Stat Block Heading
  {"type":"statmeta","text":"Small humanoid, neutral evil"} -> Stat Block Metadata (italic)
  {"type":"meta","running":"N04: The Gralhund Villa"}  -> sets the right-aligned
      running footer '<running> -Page <n>'. If omitted, the footer is derived
      from the first `title` block.

Inline emphasis: wrap text in **double asterisks** to bold it (e.g. creature
names per 5e convention).
"""
import sys, os, json, re

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

MAROON = RGBColor(0x92, 0x00, 0x00)   # the one and only accent — #920000 (maroon)
MAROON_HEX = "920000"                 # table header fill
TABLE_BAND_HEX = "F2DBDB"             # light pink — banded body rows (alt. with white)
TABLE_BORDER_HEX = "D99594"          # shaded red — table cell borders/frames
WHITE = RGBColor(0xFF, 0xFF, 0xFF)    # table header text
BLACK  = RGBColor(0x00, 0x00, 0x00)
TABLE_FONT = "Scaly Sans Remake"
CAPTION_FONT = "Scaly Sans Caps"
TUNING_TIERS = ("Frail", "Baseline", "Strong", "Hard to kill")

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.normpath(os.path.join(HERE, "..", "references", "template.docx"))


# ----------------------------------------------------------------------------- inline
def add_runs(p, text):
    """Split on **bold** markers and add runs with correct emphasis."""
    for i, chunk in enumerate(re.split(r'\*\*(.+?)\*\*', text)):
        if not chunk:
            continue
        r = p.add_run(chunk)
        if i % 2 == 1:
            r.bold = True


def _shade_cell(cell, hex_fill):
    """Directly shade a table cell (theme-independent)."""
    tcpr = cell._tc.get_or_add_tcPr()
    shd = tcpr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd'); tcpr.append(shd)
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)


def _cell_borders(cell, hex_color=TABLE_BORDER_HEX, sz=8):
    """Apply single borders of the given color to all four sides of a cell."""
    tcpr = cell._tc.get_or_add_tcPr()
    tcb = tcpr.find(qn('w:tcBorders'))
    if tcb is None:
        tcb = OxmlElement('w:tcBorders'); tcpr.append(tcb)
    for edge in ('top', 'left', 'bottom', 'right'):
        e = tcb.find(qn('w:' + edge))
        if e is None:
            e = OxmlElement('w:' + edge); tcb.append(e)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), str(sz))
        e.set(qn('w:space'), '0')
        e.set(qn('w:color'), hex_color)


def _set_running_footer(doc, text):
    """Put a running footer on every page in Scaly Sans Caps, 10 pt.

    Mirrors the house running line (e.g. '<Adventure Title>
    -Page 147') but keyed to this node's number and name.
    """
    doc.settings.odd_and_even_pages_header_footer = False
    for section in doc.sections:
        section.different_first_page_header_footer = False
        footer = section.footer
        footer.is_linked_to_previous = False
        for element in list(footer._element):
            footer._element.remove(element)
        p = footer.add_paragraph(style="Footer")
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        def _run(t):
            r = p.add_run(t)
            r.font.name = CAPTION_FONT
            r.font.size = Pt(10)
            r.font.color.rgb = BLACK
            return r

        _run(text + " -Page ")
        # PAGE field
        r = p.add_run()
        fb = OxmlElement('w:fldChar'); fb.set(qn('w:fldCharType'), 'begin')
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = ' PAGE '
        fe = OxmlElement('w:fldChar'); fe.set(qn('w:fldCharType'), 'end')
        r._r.append(fb); r._r.append(it); r._r.append(fe)
        r.font.name = CAPTION_FONT; r.font.size = Pt(10); r.font.color.rgb = BLACK


def _style_has_numbering(doc, name):
    """True if the named style carries its own list numbering (numPr)."""
    try:
        return 'numPr' in doc.styles[name].element.xml
    except KeyError:
        return False


# ----------------------------------------------------------------------------- blocks
def render(doc, blocks):
    running_title = None
    for b in blocks:
        t = b.get("type")
        if t == "title":
            doc.add_paragraph(b["text"], style="Heading 1")
            if running_title is None:
                running_title = b["text"]
        elif t == "meta":
            # explicit running-footer override
            running_title = b.get("running") or b.get("text") or running_title
        elif t == "h2":
            doc.add_paragraph(b["text"], style="Heading 2")
        elif t == "h3":
            doc.add_paragraph(b["text"], style="Heading 3")
        elif t == "h4":
            doc.add_paragraph(b["text"], style="Heading 4")
        elif t == "epigraph":
            p = doc.add_paragraph(style="Epigraph"); add_runs(p, b["text"])
            if b.get("by"):
                p2 = doc.add_paragraph(style="Epigraph"); p2.add_run("\u2014" + b["by"])
        elif t == "boxed":
            p = doc.add_paragraph(style="Boxed Text"); add_runs(p, b["text"])
        elif t == "body":
            p = doc.add_paragraph(style="Core Body"); add_runs(p, b["text"])
        elif t == "label":
            p = doc.add_paragraph(style="Core Body")
            r = p.add_run(b["label"].rstrip(".") + ". "); r.bold = True
            add_runs(p, b.get("text", ""))
        elif t == "bullet":
            if _style_has_numbering(doc, "Core Bulleted"):
                p = doc.add_paragraph(style="Core Bulleted")
                add_runs(p, b["text"])
            else:
                try:
                    p = doc.add_paragraph(style="List Bullet")
                except KeyError:
                    p = doc.add_paragraph(style="Core Bulleted"); p.add_run("\u2022 ")
                add_runs(p, b["text"])
        elif t == "tuning":
            tiers = b.get("tiers", {})
            if set(tiers) != set(TUNING_TIERS):
                raise ValueError("Tuning requires exactly Frail, Baseline, Strong, and Hard to kill.")
            headline = doc.add_paragraph("Tuning The Encounter", style="Sidebar Headline")
            headline.paragraph_format.keep_with_next = True
            numbered = _style_has_numbering(doc, "Sidebar Bulleted")
            for name in TUNING_TIERS:
                p = doc.add_paragraph(style="Sidebar Bulleted")
                p.paragraph_format.keep_with_next = name != TUNING_TIERS[-1]
                p.paragraph_format.keep_together = True
                if not numbered:
                    p.add_run("\u2022 ")
                r = p.add_run(name + ": "); r.bold = True; r.font.color.rgb = MAROON
                add_runs(p, tiers[name])
        elif t == "statheading":
            doc.add_paragraph(b["text"], style="Stat Block Heading")
        elif t == "statmeta":
            doc.add_paragraph(b["text"], style="Stat Block Metadata")
        elif t == "table":
            header = b["header"]; rows = b["rows"]
            tbl = doc.add_table(rows=1, cols=len(header))
            # No theme table style: house colors are applied by direct shading
            # and direct cell borders so the look never depends on the theme.
            hdr = tbl.rows[0].cells
            for i, h in enumerate(header):
                hdr[i].text = ""
                hp = hdr[i].paragraphs[0]
                hp.paragraph_format.space_before = Pt(0)
                hp.paragraph_format.space_after = Pt(0)
                rp = hp.add_run(h)
                rp.bold = True
                rp.font.color.rgb = WHITE
                rp.font.name = CAPTION_FONT
                rp.font.size = Pt(9)
                _shade_cell(hdr[i], MAROON_HEX)          # maroon header fill
                _cell_borders(hdr[i])                    # #D99594 frame
                hdr[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for ri, row in enumerate(rows):
                cells = tbl.add_row().cells
                for i, val in enumerate(row):
                    cells[i].text = ""
                    add_runs(cells[i].paragraphs[0], str(val))
                    for run in cells[i].paragraphs[0].runs:
                        run.font.name = TABLE_FONT
                        run.font.size = Pt(9)
                        run.font.color.rgb = BLACK
                    # light-pink banding on alternating rows (match the draft:
                    # first data row white, second shaded, …)
                    if ri % 2 == 1:
                        _shade_cell(cells[i], TABLE_BAND_HEX)
                    else:
                        _shade_cell(cells[i], "FFFFFF")
                    _cell_borders(cells[i])              # #D99594 frame
                    cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        else:
            raise ValueError(f"Unknown block type: {t!r}")

    if running_title:
        _set_running_footer(doc, running_title)


def new_document():
    if not os.path.isfile(TEMPLATE):
        raise FileNotFoundError(f"The bundled v3 template is required: {TEMPLATE}")
    doc = Document(TEMPLATE)
    for element in list(doc.element.body):
        if element.tag != qn("w:sectPr"):
            doc.element.body.remove(element)
    return doc


DEMO = [
    {"type": "title", "text": "N00: Sample Node"},
    {"type": "epigraph", "text": "\u201cA quiet room is a room that hasn\u2019t finished waiting.\u201d", "by": "Anonymous"},

    {"type": "h2", "text": "Revelations"},
    {"type": "bullet", "text": "A faded map on the wall shows this building and a route to the cellar."},

    {"type": "h2", "text": "Overview"},
    {"type": "body", "text": "**City District.** \u201cOld Quarter\u201d, **Street Name.** \u201cLantern Row\u201d"},
    {"type": "boxed", "text": "Dust hangs in the shafts of light that fall through shuttered windows onto bare, warped floorboards."},
    {"type": "label", "label": "Purpose", "text": "A quiet sample location used to demonstrate every block type."},

    {"type": "h2", "text": "Main Scenario"},
    {"type": "h3", "text": "Sample Node Features"},
    {"type": "label", "label": "Atmosphere", "text": "Cold, still air; the faint smell of old smoke."},

    {"type": "h3", "text": "Random Encounters"},
    {"type": "table", "header": ["D6", "Monster", "See area"],
      "rows": [["1-3", "Giant rat", "S1"], ["4-6", "Stirge", "S2"]]},

    {"type": "h3", "text": "Adversary Roster"},
    {"type": "table", "header": ["Encounter", "Area", "Notes"],
      "rows": [["2 giant rats", "S1", "Nest in the wall cavity"], ["1 stirge", "S2", "Roosts on the rafters"]]},

    {"type": "h2", "text": "Locations of The Sample Node (S)"},
    {"type": "body", "text": "The following locations are keyed to the map of the Sample Node (S)."},

    {"type": "h3", "text": "S1: Entry Hall"},
    {"type": "boxed", "text": "A narrow hall runs the length of the building, its plaster peeling in long, curling strips."},
    {"type": "label", "label": "Denizens", "text": "A **giant rat** nest is hidden behind a loose skirting board."},
    {"type": "tuning", "tiers": {
        "Frail": "A single **giant rat** darts out.",
        "Baseline": "2 **giant rats** with maximum hit points (14 total) dart out.",
        "Strong": "2 **giant rats** (max HP) plus a third joining after one round.",
        "Hard to kill": "4 **giant rats** (max HP), fighting as a coordinated pack."}},

    {"type": "h2", "text": "Developments"},
    {"type": "h3", "text": "If the Rats Are Cleared"},
    {"type": "body", "text": "The building's owner offers a modest reward and safer passage through the district."},

    {"type": "h2", "text": "Clues"},
    {"type": "h3", "text": "Evidence"},
    {"type": "bullet", "text": "Gnawed crates in S1 show the rats have been here for months, not days."},
    {"type": "h3", "text": "Leads"},
    {"type": "bullet", "text": "A merchant's ledger names a second, larger warehouse across town."},
]


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    if argv[1] == "--demo":
        blocks = DEMO
        out_path = argv[2]
    else:
        in_path, out_path = argv[1], argv[2]
        with open(in_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        blocks = data["_blocks"] if isinstance(data, dict) else data

    doc = new_document()
    render(doc, blocks)
    doc.save(out_path)
    print(f"Wrote {out_path} ({len(blocks)} blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))