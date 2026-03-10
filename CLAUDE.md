# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio and blog website for Dr. Anirach Mingkhwan, hosted on GitHub Pages at anirach.com. Static HTML/CSS/JS site with no build system.

## Development

No build step required. Open HTML files directly in browser or use any local server:

```bash
python -m http.server 8000
# or
npx serve .
```

Deploy by pushing to `main` branch — GitHub Pages auto-deploys.

## Architecture

```
/
├── index.html          # Portfolio landing page
├── style.css           # Main stylesheet (Inter font, CSS variables)
├── script.js           # Nav effects, scroll reveal, smooth scrolling
├── blog/
│   ├── index.html      # Blog listing with category filters (embedded CSS)
│   └── *.html          # Individual articles (each self-contained with embedded styles)
├── images/             # Profile photo, blog cover images
└── CNAME               # Custom domain config
```

## Conventions

- **Blog posts**: Standalone HTML files in `blog/` with all styles embedded in `<style>` tags
- **Language**: Bilingual content (English headers, Thai explanatory text)
- **CSS variables**: Use `--navy`, `--blue`, `--slate`, `--bg` etc. from `:root` (see blog/index.html or style.css)
- **Design system**: Inter font, rounded corners (`--radius: 14px`), indigo accent (`#6366f1`)
- **Cards**: Use `.card` pattern with hover lift effect and gradient backgrounds
- **Reveal animations**: Add `data-reveal` attribute for scroll-triggered fade-in

## Adding a New Blog Post

1. Create `blog/new-post.html` using existing post as template
2. Update `blog/index.html` — add card to `.blog-grid` and update category counts
3. Add cover image to `images/` if needed
