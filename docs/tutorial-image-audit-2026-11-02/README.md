# Tutorial image audit — 2 November 2026

The user's Contracts screenshot showed a drawing defect: connectors floated
between nodes and crossed node bodies. Image files themselves loaded.

## Audit coverage

- All 121 Tutorial posts and their catalog.
- 422 distinct image assets: 121 covers, 121 thumbnails, 121 post share cards,
  one catalog share card and 58 article figures.
- All referenced files exist and decode. All 422 public URLs returned HTTP 200
  (a transient 503 on one figure passed the bounded retry).
- Visual contact-sheet review of all 121 cover motifs and 58 article figures.
  Full-size review of the repaired Contracts cover and its landscape share card,
  the bounded-recovery loop and the response-validation share card.

## Repairs

19 cover drawings across Engineering, Functional Workflows and Jev needed
connector corrections. `changed.json` records their slugs. Each cover's 800px
image, 144px thumbnail and 1200×630 share card was regenerated: 57 files.

`scripts/diagram_geometry.py` attaches connections to named ports derived from
node bounds. It supports actual node borders and routed return paths. The
renderers no longer guess detached line endpoints. Deliberate chart bars,
policy separators, document rules and independent panels remain recognizable
as those forms rather than being forced into a flowchart.

`scripts/image_assets.py` and `scripts/image-versions.json` version only these
repaired URLs by their content hashes, so cached artwork gets a fresh request.
The post/catalog generators retain versioning on future regeneration. Existing
integrity checkers normalize URL queries when resolving physical image files.
The cover generator now refreshes thumbnails with the source cover and updates
content hashes for tracked repaired assets.

## Verification

```sh
python3 docs/tutorial-image-audit-2026-11-02/audit.py --sheets --remote
python3 docs/tutorial-image-audit-2026-11-02/check_repairs.py
python3 scripts/make_cover.py --check
python3 .claude/skills/blog-post/assets/verify-wiring.py
python3 .claude/skills/site-check/scripts/check_site.py
python3 scripts/check_visibility.py --strict
```

The geometry regression exercises 37 motifs in square and landscape layouts
(74 renders) and validates 98 connections: endpoints on borders, no connector
interior crossing its source/target body, finite coordinates and no clipping.
The asset regression verifies 57 content hashes and 115 versioned image
references, including srcset candidates, social metadata and JSON-LD.

The local browser confirmed the Contracts cover loads at 800×800 from its
versioned URL. `contracts-before-after.png` shows the reported drawing repair.
`inventory.json`, `remote.json`, contact sheets and the integrity report retain
the audit evidence. Generated working files in this folder are excluded from
the public site by the existing Jekyll `docs/` rule.
