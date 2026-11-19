# LUMORA — Digital & Creative

Official website of **LUMORA**, a digital & creative agency in Amman, Jordan.
*Clarity. Creativity. Growth.*

## Pages
Home · About (with Meet the Founder) · Services · Our Work · FAQ · Contact / Request a Quote · Privacy Policy · 404 · Thank-you page

## Features
- English by default, Arabic with full RTL, switched by the language button (the choice is remembered)
- Smooth scrolling (Lenis), short scroll-driven animations, cursor spotlight on cards, icons that grow with the mouse, magnetic buttons
- Animated dotted-wave background taken from the brand identity
- Quote form handled by **Netlify Forms** (submissions arrive by email)
- Self-hosted fonts (Sora, Manrope, Alexandria), no external requests
- Respects "reduce motion" accessibility settings

## Editing content
All English and Arabic text lives in `_dev/content.py`.
After editing it, regenerate the pages:

```bash
cd _dev && python3 build.py
```

This rewrites the `.html` files and `assets/js/i18n.js`. Styles are in `assets/css/style.css`, interactions in `assets/js/main.js`.

## Deploy (Netlify)
1. Netlify → **Add new site → Import an existing project → GitHub** → choose `lumora-website`.
2. Leave the build command empty, publish directory `.`, then deploy.
3. **Forms:** Netlify detects the `quote` form automatically. Under *Site configuration → Forms → Form notifications*, add an email notification to `lumoradigitalsjo@gmail.com`.
4. When the domain is ready, add it under *Domain management*, then replace `https://lumoradigitals.netlify.app` in `_dev/build.py`, `robots.txt` and `sitemap.xml` and rebuild.
