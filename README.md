# LUMORA — Digital & Creative

Official website of **LUMORA**, a digital & creative agency in Amman, Jordan.
*Clarity. Creativity. Growth.*

## Pages
Home · About (with Meet the Founder) · Services · Our Work · FAQ · Contact / Request a Quote · Privacy Policy · 404 · Thank-you page

## Features
- English by default, Arabic with full RTL, switched by the language button (the choice is remembered)
- Smooth scrolling (Lenis), short scroll-driven animations, cursor spotlight on cards, icons that grow with the mouse, magnetic buttons
- Animated dotted-wave background taken from the brand identity
- Quote form handled by **FormSubmit** (submissions arrive by email)
- Self-hosted fonts (Sora, Manrope, Alexandria), no external requests
- Respects "reduce motion" accessibility settings

## Editing content
All English and Arabic text lives in `_dev/content.py`.
After editing it, regenerate the pages:

```bash
cd _dev && python3 build.py
```

This rewrites the `.html` files and `assets/js/i18n.js`. Styles are in `assets/css/style.css`, interactions in `assets/js/main.js`.

## Hosting & form
- Live on **GitHub Pages**: https://hamzehabunemeh.github.io/lumora-website/ (Settings → Pages → branch `main`).
- The quote form is sent through **FormSubmit** to `lumoradigitalsjo@gmail.com`. The very first submission triggers an activation email from FormSubmit — click **Activate Form** once, and every request after that lands in the inbox.
- After a submission the visitor lands on `thanks.html` (the redirect is set automatically, so it keeps working if the domain changes).
- When a custom domain is ready, replace the site URL in `_dev/build.py`, `robots.txt` and `sitemap.xml` and rebuild.
