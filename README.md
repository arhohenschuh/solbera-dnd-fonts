# D&D Fonts and House Style

Fonts, Word templates, and typography references for 2014-era D&D 5e documents.
This is an independently maintained repository at
[arhohenschuh/solbera-dnd-fonts](https://github.com/arhohenschuh/solbera-dnd-fonts).
The original Solbera collection is retained and credited, but upstream
synchronization and upstream pull requests are no longer part of the workflow.

## Start Here

- Formatting standard: [docs/HOUSE-STYLE.md](docs/HOUSE-STYLE.md).
- Current Word template: [templates/5e Module_Format.docx](templates/5e%20Module_Format.docx).
- Original font specimen: open [index.html](index.html) directly in a browser.
  No build, dependency installation, or development server is required.
- Reusable web-font definitions: [stylesheet.css](stylesheet.css). Its font URLs
  are relative to this file; preserve the layout when copying it elsewhere.

For Word, install the fonts listed in the house-style guide and restart Word.
The current stack uses Nodesto Caps Condensed for titles, Baskervville Caps for
headings, Bookinsanity Remake for prose, Scaly Sans for reference material, and
Zatanna Misdirection for epigraphs. The guide specifies the exact family names,
sizes, colours, and Word styles.

## Layout

```text
fonts/
  solbera/           Original D&D font families
  custom/            Baskervville Caps and Bonum SC derivatives
  vendor/            Complete Andada and TeX Gyre packages
templates/
  archive/           Superseded Word template
docs/
  provenance/        Preserved earlier README and attribution
specimens/
  comparisons/       Word comparisons of heading fonts
  research/          Earlier comparison output and diagnostic images
index.html           Editable Solbera font specimen
stylesheet.css       Local web-font definitions
LICENSE              Solbera collection licence
```

Font filenames and vendor-package contents are preserved. Comparison document
filenames use English. The original root-level font directories now live under
the three font groups above; existing consumers must update their paths.

## Custom Builds

- [fonts/custom/Baskervville Caps/README.txt](fonts/custom/Baskervville%20Caps/README.txt)
  documents the current heading family: drawn small caps, cap-height figures,
  and corrected punctuation, without relying on Word's synthetic small caps.
- [fonts/custom/Bonum SC/README.txt](fonts/custom/Bonum%20SC/README.txt)
  documents the alternative four-style Bookman-derived small-caps family.
  It is retained for comparison, not used by the current house style.
- [docs/Solbera Font Assignments.docx](docs/Solbera%20Font%20Assignments.docx)
  retains the font-assignment reference.

## Repository Workflow

`origin` is the owner's GitHub repository above; `master` tracks `origin/master`.
Fetch, pull, and push only against that repository. There is no original-upstream
remote, and no requirement to retain its layout or branch compatibility.
Existing Git history remains intact; no orphan branch or history rewrite is
needed to maintain this project independently.

The browser specimen and stylesheet load the font files from this checkout,
not from upstream URLs or potentially different installed copies.

## Licences and Provenance

The collection contains assets under different licences:

- Solbera families: CC BY-SA 4.0, supplied in [LICENSE](LICENSE).
- Baskervville Caps: SIL OFL 1.1, as documented in its build README above.
- Andada: SIL OFL 1.1, supplied in
  [fonts/vendor/andada/SIL Open Font License.txt](fonts/vendor/andada/SIL%20Open%20Font%20License.txt).
- TeX Gyre and Bonum SC: GUST Font License, supplied in
  [fonts/vendor/tex-gyre/doc/GUST-FONT-LICENSE.txt](fonts/vendor/tex-gyre/doc/GUST-FONT-LICENSE.txt).

Independent maintenance does not remove attribution or derivative-licensing
obligations. The earlier README, including the Solbera, Ryrok, Ners, and
LUCASTUCIOUS credits and historical notes, is preserved unchanged in
[docs/provenance/README.md](docs/provenance/README.md).
