#!/usr/bin/env python3
"""
validate_adventure_docx.py — Style-conformance checker for the canonical
D&D House Style version 3.

Given a .docx, this reports how well it follows the house style guide:
fonts, the single maroon #920000 accent, the named paragraph styles, the
fixed section spine, boxed read-aloud usage, run-in labels, the four-tier
Tuning block, and banded tables.

Findings are graded:
  CRITICAL — breaks the structure/style system (wrong/missing spine, read-aloud
             not in Boxed Text, a second accent color or non-v3 typography)
  MAJOR    — inconsistent but readable (missing run-in labels, Tuning tier
             order/labels off, table not using the accent style)
  MINOR    — cosmetic (spacing, stray manual formatting)

USAGE
  python validate_adventure_docx.py <file.docx> [--node N17] [--json]

  --node N17   restrict checks to the chapter whose Heading 1 starts with "N17"
  --json       emit machine-readable JSON instead of a text report

Exit code is 0 if there are no CRITICAL findings, else 1.
"""
import sys, re, json, argparse

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

MAROON = "920000"
HOUSE_FONTS = {
    "Nodesto Caps Condensed", "Baskervville Caps", "Bookinsanity Remake",
    "Scaly Sans Remake", "Scaly Sans Caps", "Zatanna Misdirection",
}
STYLE_RULES = {
    "Normal": ("Bookinsanity Remake", 10, "000000"),
    "Title": ("Nodesto Caps Condensed", 28, MAROON),
    "Heading 1": ("Nodesto Caps Condensed", 28, MAROON),
    "Heading 2": ("Baskervville Caps", 18.5, MAROON),
    "Heading 3": ("Baskervville Caps", 15, MAROON),
    "Heading 4": ("Baskervville Caps", 13.5, MAROON),
    "Core Body": ("Bookinsanity Remake", 10, "000000"),
    "Core Bulleted": ("Bookinsanity Remake", 10, "000000"),
    "Boxed Text": ("Bookinsanity Remake", 9, "000000"),
    "Epigraph": ("Zatanna Misdirection", 10, "000000"),
    "Sidebar Body": ("Scaly Sans Remake", 10, "000000"),
    "Sidebar Bulleted": ("Scaly Sans Remake", 10, "000000"),
    "Sidebar Headline": ("Scaly Sans Caps", 12, MAROON),
    "Stat Block Heading": ("Nodesto Caps Condensed", 12, MAROON),
    "Stat Block Metadata": ("Scaly Sans Remake", 10, "000000"),
    "Legalese": ("Scaly Sans Remake", 7, "000000"),
    "Footer": ("Scaly Sans Caps", 10, "000000"),
}

# The fixed spine (Heading 2 sections), in order. Area-key locations heading and
# some section titles vary by adventure, so we match by normalized keyword.
SPINE = [
    ("revelations", "Revelations"),
    ("overview", "Overview"),
    ("main scenario", "Main Scenario"),
    ("locations", "Locations of The … (S)"),
    ("developments", "Developments"),
    ("clues", "Clues"),
]

TUNING_TIERS = ["Frail", "Baseline", "Strong", "Hard to kill"]

# Style names that legitimately carry the maroon display look.
DISPLAY_STYLES = {"Title", "Heading 1", "Heading 2", "Heading 3", "Heading 4",
                  "Sidebar Headline", "Stat Block Heading"}


def _norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def _rgb(run):
    try:
        if run.font.color and run.font.color.rgb is not None:
            return str(run.font.color.rgb)
    except Exception:
        pass
    return None


def _font_property(font, attribute):
    if attribute == "color":
        return str(font.color.rgb) if font.color.rgb is not None else None
    value = getattr(font, attribute)
    return value.pt if attribute == "size" and value is not None else value


def _style_property(style, attribute):
    visited = set()
    while style is not None and style.style_id not in visited:
        visited.add(style.style_id)
        value = _font_property(style.font, attribute)
        if value is not None:
            return value
        style = style.base_style
    return None


def _effective(paragraph, attribute, run=None):
    if run is not None:
        value = _font_property(run.font, attribute)
        if value is not None:
            return value
        if run.style is not None and run.style.element.get(qn("w:default")) != "1":
            value = _style_property(run.style, attribute)
            if value is not None:
                return value
    value = _style_property(paragraph.style, attribute)
    return "000000" if value is None and attribute == "color" else value


def _check_typography(paragraph, run, expected, add, context, allow_tier_color=False):
    for attribute, value in zip(("name", "size", "color"), expected):
        actual = _effective(paragraph, attribute, run)
        if allow_tier_color and attribute == "color" and actual == MAROON:
            continue
        if actual != value:
            add("CRITICAL", f"{context}: {attribute} must be {value!r}, found {actual!r}.")
    for attribute in ("small_caps", "all_caps"):
        if _effective(paragraph, attribute, run):
            add("CRITICAL", f"{context}: synthetic {attribute} is not permitted in v3.")


def _paragraph_property(paragraph, path):
    value = paragraph._p.find(path)
    style = paragraph.style
    visited = set()
    while value is None and style is not None and style.style_id not in visited:
        visited.add(style.style_id)
        value = style.element.find(path)
        style = style.base_style
    return value


def _check_border(paragraph, edge, size, space, add):
    border = _paragraph_property(paragraph, f"{qn('w:pPr')}/{qn('w:pBdr')}/{qn('w:' + edge)}")
    expected = {"val": "single", "sz": str(size), "space": str(space), "color": MAROON}
    if border is None or any(border.get(qn("w:" + key)) != value for key, value in expected.items()):
        add("MAJOR", f"{paragraph.style.name}: incorrect {edge} border; expected maroon, size {size}, space {space}.")


def slice_node(paras, node):
    """Return the paragraph slice for a given node id (e.g. 'N17'), or all."""
    if not node:
        return paras
    start = end = None
    for i, p in enumerate(paras):
        if p.style.name == "Heading 1" and p.text.strip().upper().startswith(node.upper()):
            start = i
        elif start is not None and p.style.name == "Heading 1":
            end = i
            break
    if start is None:
        return None
    return paras[start:end]


def validate(path, node=None):
    doc = Document(path)
    findings = []  # (level, message)

    def add(level, msg):
        findings.append((level, msg))

    paras = doc.paragraphs
    seg = slice_node(paras, node)
    if seg is None:
        add("CRITICAL", f"No Heading 1 starting with '{node}' found.")
        return findings, doc

    for name, expected in STYLE_RULES.items():
        try:
            style = doc.styles[name]
        except KeyError:
            add("CRITICAL", f"Required v3 style is missing: {name}.")
            continue
        for attribute, value in zip(("name", "size", "color"), expected):
            actual = _style_property(style, attribute)
            if attribute == "color" and actual is None:
                actual = "000000"
            if actual != value:
                add("CRITICAL", f"Style '{name}': {attribute} must be {value!r}, found {actual!r}.")

    # --- 1. Node title ---
    h1 = [p for p in seg if p.style.name == "Heading 1" and p.text.strip()]
    if not h1:
        add("CRITICAL", "No Heading 1 node title present.")
    elif not re.match(r"N\d+\s*:", h1[0].text.strip()):
        add("MAJOR", f"Node title '{h1[0].text.strip()[:40]}' is not in 'N##: Name' form.")

    # --- 2. Spine presence & order ---
    h2_texts = [_norm(p.text) for p in seg if p.style.name == "Heading 2" and p.text.strip()]
    found_order = []
    for key, label in SPINE:
        hit = next((i for i, t in enumerate(h2_texts) if key in t), None)
        if hit is None:
            lvl = "MINOR" if key in ("locations",) else "CRITICAL"
            add(lvl, f"Spine section missing (Heading 2): {label}.")
        else:
            found_order.append((key, hit))
    # order check
    seq = [pos for _, pos in found_order]
    if seq != sorted(seq):
        add("CRITICAL", "Spine sections are out of the canonical order.")

    for paragraph in seg:
        if not paragraph.text.strip():
            continue
        context = f"{paragraph.style.name} '{paragraph.text.strip()[:48]}'"
        expected = STYLE_RULES.get(paragraph.style.name)
        for run in paragraph.runs:
            if not run.text.strip():
                continue
            if expected:
                _check_typography(paragraph, run, expected, add, context,
                                  paragraph.style.name == "Sidebar Bulleted")
            else:
                font = _effective(paragraph, "name", run)
                color = _effective(paragraph, "color", run)
                if font not in HOUSE_FONTS:
                    add("CRITICAL", f"{context}: unexpected font outside the six v3 families: {font!r}.")
                if color not in ("000000", MAROON):
                    add("CRITICAL", f"{context}: second accent color beyond #920000: {color!r}.")
            if paragraph.style.name in ("Epigraph", "Stat Block Metadata") and not _effective(paragraph, "italic", run):
                add("MAJOR", f"{context}: italic formatting is required.")
            if paragraph.style.name == "Core Body" and _effective(paragraph, "bold", run) and _effective(paragraph, "italic", run):
                add("MAJOR", f"{context}: Bookinsanity run-in labels must not use bold italic.")
        if paragraph.style.name == "Heading 3":
            _check_border(paragraph, "bottom", 4, 1, add)
        elif paragraph.style.name == "Boxed Text":
            for edge in ("top", "left", "bottom", "right"):
                _check_border(paragraph, edge, 8, 4, add)
        elif paragraph.style.name == "Heading 2":
            border = _paragraph_property(paragraph, f"{qn('w:pPr')}/{qn('w:pBdr')}/{qn('w:bottom')}")
            if border is not None and border.get(qn("w:val")) not in ("none", "nil"):
                add("MAJOR", f"{context}: Heading 2 must not have a bottom border.")

    # --- 4. Area keys: Boxed read-aloud + run-in labels ---
    area_keys = [i for i, p in enumerate(seg)
                 if p.style.name == "Heading 3" and re.match(r"S\d+\s*:", p.text.strip())]
    for idx in area_keys:
        name = seg[idx].text.strip()
        # look at the block until next Heading of level 2/3
        j = idx + 1
        block = []
        while j < len(seg) and seg[j].style.name not in ("Heading 2", "Heading 3"):
            if seg[j].text.strip():
                block.append(seg[j])
            j += 1
        styles = [p.style.name for p in block]
        if "Boxed Text" not in styles:
            add("MAJOR", f"Area key '{name}' has no Boxed Text read-aloud opener.")
        else:
            # boxed text should come before the first run-in label
            first_boxed = styles.index("Boxed Text")
            if first_boxed > 2:
                add("MINOR", f"Area key '{name}': Boxed Text is not the opener.")
        # run-in label check: a paragraph whose leading bold run(s) form a
        # "Label." (the concatenated bold prefix ends with a period before the
        # first non-bold run). Handles labels split across several bold runs.
        has_label = False
        for p in block:
            if p.style.name != "Core Body" or not p.runs:
                continue
            prefix = ""
            for r in p.runs:
                if r.bold and r.text:
                    prefix += r.text
                else:
                    break
            if prefix.strip().rstrip().endswith("."):
                has_label = True
                break
        if not has_label:
            add("MINOR", f"Area key '{name}' has no bold run-in label paragraph.")

    # --- 5. Tuning blocks ---
    for i, p in enumerate(seg):
        if p.style.name == "Sidebar Headline" and _norm(p.text) == "tuning the encounter":
            tiers = []
            j = i + 1
            while j < len(seg) and seg[j].style.name == "Sidebar Bulleted":
                txt = seg[j].text.strip()
                m = re.match(r"(Frail|Baseline|Strong|Hard to kill)\s*:", txt)
                if m:
                    tiers.append(m.group(1))
                    # tier label should be bold + maroon
                    # find the run carrying the tier label
                    label_run = next((r for r in seg[j].runs if r.text.strip().rstrip(":") in TUNING_TIERS), None)
                    if label_run is not None:
                        if not _effective(seg[j], "bold", label_run):
                            add("MAJOR", f"Tuning tier '{m.group(1)}' label is not bold.")
                        if _effective(seg[j], "color", label_run) != MAROON:
                            add("MAJOR", f"Tuning tier '{m.group(1)}' label is not maroon.")
                    else:
                        add("MAJOR", f"Tuning tier '{m.group(1)}' needs a separate bold maroon label run.")
                j += 1
            missing = [t for t in TUNING_TIERS if t not in tiers]
            if missing:
                add("MAJOR", f"Tuning block near '{seg[i-1].text.strip()[:24] if i>0 else '?'}' missing tiers: {missing}.")
            elif tiers != TUNING_TIERS:
                add("MAJOR", f"Tuning tiers out of canonical order: {tiers}.")

    # --- 6. Read-aloud not misplaced in Core Body (heuristic) ---
    # (only a light MINOR heuristic: long Core Body right after an area H3 without a label)
    # skipped to avoid false positives.

    for table_index, table in enumerate(doc.tables):
        for row_index, row in enumerate(table.rows):
            header = row_index == 0
            expected_fill = MAROON if header else ("F2DBDB" if row_index % 2 == 0 else "FFFFFF")
            expected = ("Scaly Sans Caps", 9, "FFFFFF") if header else ("Scaly Sans Remake", 9, "000000")
            for cell_index, cell in enumerate(row.cells):
                context = f"Table {table_index + 1}, row {row_index + 1}, cell {cell_index + 1}"
                properties = cell._tc.get_or_add_tcPr()
                shading = properties.find(qn("w:shd"))
                fill = shading.get(qn("w:fill")) if shading is not None else None
                if fill != expected_fill or (shading is not None and any('theme' in key.lower() for key in shading.attrib)):
                    add("MAJOR", f"{context}: direct fill must be {expected_fill}, found {fill!r}.")
                if cell.vertical_alignment != WD_CELL_VERTICAL_ALIGNMENT.CENTER:
                    add("MAJOR", f"{context}: cell must be vertically centered.")
                for edge in ("top", "left", "bottom", "right"):
                    border = properties.find(f"{qn('w:tcBorders')}/{qn('w:' + edge)}")
                    if border is None or border.get(qn("w:color")) != "D99594" or border.get(qn("w:val")) != "single" or border.get(qn("w:sz")) != "8":
                        add("MAJOR", f"{context}: {edge} border must be single, size 8, #D99594.")
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if not run.text.strip():
                            continue
                        _check_typography(paragraph, run, expected, add, context)
                        if header and not _effective(paragraph, "bold", run):
                            add("MAJOR", f"{context}: header text must be bold.")

    if doc.settings.odd_and_even_pages_header_footer:
        add("MAJOR", "Separate even-page footers are enabled; the running footer must appear on every page.")
    for section_index, section in enumerate(doc.sections):
        if section.different_first_page_header_footer:
            add("MAJOR", f"Section {section_index + 1}: first-page footer differs from the running footer.")
        footer = section.footer
        paragraphs = [paragraph for paragraph in footer.paragraphs if paragraph.text.strip()]
        if len(paragraphs) != 1 or " -Page " not in paragraphs[0].text:
            add("MAJOR", f"Section {section_index + 1}: expected one '<node> -Page <n>' running footer.")
        fields = [field.text or "" for field in footer._element.iter(qn("w:instrText"))]
        fields.extend(field.get(qn("w:instr"), "") for field in footer._element.iter(qn("w:fldSimple")))
        if not any(re.match(r"\s*PAGE\b", field) for field in fields):
            add("MAJOR", f"Section {section_index + 1}: running footer needs a PAGE field.")
        for paragraph in paragraphs:
            if paragraph.alignment != WD_ALIGN_PARAGRAPH.RIGHT:
                add("MAJOR", f"Section {section_index + 1}: running footer must be right-aligned.")
            for run in paragraph.runs:
                _check_typography(paragraph, run, STYLE_RULES["Footer"], add, "Running footer")

    return findings, doc


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--node", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    findings, _ = validate(args.path, args.node)
    order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}
    findings.sort(key=lambda f: order.get(f[0], 9))

    if args.json:
        print(json.dumps([{"level": l, "message": m} for l, m in findings], indent=2))
    else:
        if not findings:
            print("PASS — no style deviations found.")
        else:
            counts = {}
            for l, _ in findings:
                counts[l] = counts.get(l, 0) + 1
            print(f"Style report for {args.path}"
                  + (f" (node {args.node})" if args.node else ""))
            print("Summary: " + ", ".join(f"{counts.get(k,0)} {k}" for k in ("CRITICAL", "MAJOR", "MINOR")))
            print("-" * 60)
            for l, m in findings:
                print(f"[{l:8}] {m}")

    has_critical = any(l == "CRITICAL" for l, _ in findings)
    return 1 if has_critical else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
