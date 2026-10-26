# Vendored copy — UI/UX Pro Max

- **Upstream:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT, `LICENSE` beside this file)
- **Version:** 2.15.0, commit `d14efff8ed1faa4187f004f79926f428c8074ec7` (2026-10-23)
- **Copied from:** upstream `.claude/skills/ui-ux-pro-max/` — the hand-authored SKILL.md plus
  `data/`, `scripts/` and `references/`. Upstream's `cli/assets/` holds the same `data/` and
  `scripts/` byte for byte.
- **Not copied:** the six sibling skills `uipro init` also installs (`banner-design`, `brand`,
  `design`, `design-system`, `slides`, `ui-styling`). They cover banners, logos, slide decks,
  brand books and Tailwind/shadcn component styling — nothing this site makes — and
  `design-system`/`brand` would compete with `page-design` for the token system.

## Local edits (re-apply after every update)

1. `SKILL.md`: every `python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py"`
   became `python3 .claude/skills/ui-ux-pro-max/scripts/search.py`, and the sentence above the
   first command says so. `CLAUDE_PLUGIN_ROOT` is only set when the skill is installed as a
   marketplace plugin; as a project skill it expands to nothing and the path breaks. The
   repo-root-relative form is the one upstream's own CLI writes for a local Claude install.
2. `SKILL.md`: the "In anirach.com (this repo)" callout under the title.

## Updating

```bash
git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill /tmp/uupm
rm -rf .claude/skills/ui-ux-pro-max/{data,scripts,references,SKILL.md}
cp -r /tmp/uupm/.claude/skills/ui-ux-pro-max/{data,scripts,references,SKILL.md} .claude/skills/ui-ux-pro-max/
cp /tmp/uupm/LICENSE .claude/skills/ui-ux-pro-max/LICENSE
# then re-apply the two local edits above and update the version line
```
