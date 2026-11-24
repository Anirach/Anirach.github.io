# Catalog series navigation

Redesigned 24 November 2026 after the owner reported that the full-width row of outlined pills looked crowded and clipped its final choices.

## Design

The series index follows the catalog's 1200px container and content gutters. Desktop presents ten tutorial courses in five columns and two rows. Names use regular 14px text; article counts are separate, quiet numerals. Hover adds a light surface. The destination selected through a URL fragment has a stronger label, light background and blue underline. RSS occupies a separate header position.

At 1024px and below, a 44px “Browse series” label opens a two-column list. It uses a labeled native checkbox, which announces its checked state, controls the list by ID and supports Space. Focus is visible on the label and links. The expanded index is in normal flow, so selecting a destination scrolls it away rather than covering the content. No JavaScript, horizontal menu scrolling, clipped labels, extra image assets or dependencies are involved.

The Thoughts catalog uses the same component with three desktop columns. Article and essay counts remain generated from the current catalog data. All post cards, dates, ordering, covers and article prose remain intact.

## Maintenance

`scripts/reindex_blog.py` owns markup, CSS and responsive behavior. Run the Tutorials generator before Thoughts because Thoughts lifts its house styles from Tutorials:

```bash
python3 scripts/reindex_blog.py --repo . --out blog/index.html
python3 scripts/reindex_blog.py --repo . --out thoughts/index.html --catalog thoughts
```

The count separator stays in markup inside a visually hidden span so INV-02f can normalize the name and count. The anchor's accessible label names the series and number of articles/essays. Do not remove the linter's protection when changing presentation.

## Verification

- All 62 site checks and the independent wiring verifier pass.
- In-memory negative checks confirm INV-02f rejects an incorrect count, a missing link and a duplicate link with the new nested markup.
- All catalog card blocks compare byte-for-byte with their pre-redesign versions; regeneration is idempotent for both catalogs.
- Browser checks at 320, 375, 768, 1024, 1025, 1440 and 1920px verify disclosure state, complete labels, reachable links and no document-level horizontal overflow.
- All ten mobile destinations were activated and their headings cleared the fixed site header. Desktop target clearance and fragment selection were checked at the narrow sticky breakpoint and normal desktop width.
- Keyboard testing verifies Space toggles the disclosure, Tab reaches RSS then the series links, Enter jumps to a destination, and focus remains visible.

Screenshots are saved outside the software checkout in the Codex visualization folder. The owner's unrelated untracked `docs/screenshots/` folder is untouched.
