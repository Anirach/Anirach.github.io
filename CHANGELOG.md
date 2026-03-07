# Changelog

## 2.0.0 — 2025-03-07: Complete Redesign

### Overview
Full redesign of anirach.com from the old HTML5 UP "Dimension" modal-based template to a modern, scrolling academic portfolio.

### Changes

**Design**
- Replaced modal-based navigation with a clean, scrolling single-page layout
- New color palette: professional navy/blue (#0a1628, #2563eb) with white accents
- Typography switched to Inter (Google Fonts) for clean, modern readability
- Fully responsive mobile-first design with hamburger menu on small screens

**Structure**
- **Hero section**: Name, title, university affiliation, professional tagline, CTA buttons
- **Research Interests**: 6 visual cards with SVG icons (Agentic AI, Networks, Big Data, Wireless, Security, Cloud)
- **Publications**: Stats, research themes list, prominent Google Scholar CTA
- **Projects**: Cards linking to n8n server, Doctor Chatty Bot, and Agentic AI research
- **About Me**: Photo + bio layout with education/position details grid
- **Contact**: Social link cards (Google Scholar, GitHub, Facebook, Instagram)

**Technical**
- Pure HTML/CSS/JS — no build step, GitHub Pages compatible
- Custom CSS with CSS variables, grid/flexbox layouts
- Scroll-triggered reveal animations via Intersection Observer pattern
- Fixed navbar with scroll state, backdrop blur
- All SVG icons inline — no external icon library dependency
- Removed all HTML5 UP template files (jQuery, old CSS/JS/SASS)
- Removed generic "Elements" demo section

**Kept**
- CNAME file (anirach.com)
- Original images (pic01.jpg, pic02.jpg, pic03.jpg)
