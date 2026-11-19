# -*- coding: utf-8 -*-
"""Generates the static pages + assets/js/i18n.js from content.py.
Run:  python3 _dev/build.py   (from the repo root)"""
import json, os, re, html as H
from content import C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://hamzehabunemeh.github.io/lumora-website"
PHONE = "+962779230903"; PHONE_TXT = "+962 77 923 0903"
WA = "https://wa.me/962779230903"
EMAIL = "lumoradigitalsjo@gmail.com"
IG = "https://www.instagram.com/lumoradigitals.jo"

def en(k): return C[k][0]
def t(k, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag}{c} data-i18n="{k}"{a}>{en(k)}</{tag}>'

# ---------- icons ----------
I = {
"arrow": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"ext": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg>',
"globe": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
"mega": '<svg viewBox="0 0 24 24"><path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1Z"/><path d="M15 8.5a5 5 0 0 1 0 7M18 6a8.5 8.5 0 0 1 0 12"/></svg>',
"pen": '<svg viewBox="0 0 24 24"><path d="m12 19 7-7 3 3-7 7-3-3Z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5Z"/><path d="m2 2 7.6 7.6"/><circle cx="11" cy="11" r="2"/></svg>',
"insta": '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>',
"chart": '<svg viewBox="0 0 24 24"><path d="M4 20V14M10 20V9M16 20V12M22 20V4"/><path d="M2 20h20"/></svg>',
"bulb": '<svg viewBox="0 0 24 24"><path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2Z"/></svg>',
"spark": '<svg viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/></svg>',
"layers": '<svg viewBox="0 0 24 24"><path d="m12 2 10 5-10 5L2 7l10-5Z"/><path d="m2 12 10 5 10-5M2 17l10 5 10-5"/></svg>',
"zap": '<svg viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/></svg>',
"trend": '<svg viewBox="0 0 24 24"><path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/></svg>',
"target": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
"flag": '<svg viewBox="0 0 24 24"><path d="M4 22V4M4 4h13l-2 4 2 4H4"/></svg>',
"phone": '<svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
"mail": '<svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
"pin": '<svg viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
"chat": '<svg viewBox="0 0 24 24"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.6A8.5 8.5 0 1 1 21 11.5Z"/></svg>',
"check": '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>',
"info": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
"wa": '<svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5.3-.5v-.5c0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4ZM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4a9.8 9.8 0 0 1-1.5-5.2C2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9a9.7 9.7 0 0 1 2.9 6.9c0 5.4-4.4 9.8-9.8 9.8Zm8.4-18.2A11.8 11.8 0 0 0 .2 12c0 2.1.5 4.1 1.6 5.9L.1 24l6.3-1.7c1.7.9 3.7 1.4 5.6 1.4 6.5 0 11.8-5.3 11.8-11.8 0-3.1-1.2-6.1-3.4-8.3Z"/></svg>',
}

CHAT_BTN = I["chat"].replace("<svg ", '<svg fill="none" stroke="currentColor" stroke-width="1.6" ')
SERVICES = [("s1","globe","web"),("s2","mega","marketing"),("s3","pen","design"),("s4","insta","social"),("s5","chart","seo"),("s6","bulb","branding")]
VALUES = [("v1","spark"),("v2","layers"),("v3","zap"),("v4","trend")]
WORK = [
 ("Evo Gym","cat.fitness","evo","https://hamzehabunemeh.github.io/evo-gym-website/"),
 ("Trasimeno Coffee","cat.cafe","trasimeno","https://hamzehabunemeh.github.io/trasimeno-coffee-website/"),
 ("Dynamic Gym","cat.fitness","dynamic","https://hamzehabunemeh.github.io/dynamic-gym-website/index.html"),
 ("Fitness Factory Gym","cat.fitness","fitness-factory","https://hamzehabunemeh.github.io/fitness-factory-gym/"),
 ("My Tribe Gym","cat.fitness","my-tribe","https://hamzehabunemeh.github.io/My-tribe-gym/"),
 ("Ritual Studio","cat.yoga","ritual","https://hamzehabunemeh.github.io/Ritual-studios/"),
]
NAV = [("index.html","nav.home"),("about.html","nav.about"),("services.html","nav.services"),("work.html","nav.work"),("faq.html","nav.faq"),("contact.html","nav.contact")]

def strip(s): return re.sub("<[^>]+>","",H.unescape(s))

# ---------- layout ----------
def head(page, title_k, desc_k, path):
    ROBOTS = '\n<meta name="robots" content="noindex">' if path in ('thanks.html','404.html') else ''
    return f'''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try{{if(localStorage.getItem("lumora-lang")==="ar"){{var d=document.documentElement;d.lang="ar";d.dir="rtl";d.classList.add("i18n-wait");setTimeout(function(){{d.classList.remove("i18n-wait")}},900)}}}}catch(e){{}}</script>
<title data-key="{title_k}">{strip(en(title_k))}</title>
<meta name="description" data-key="{desc_k}" content="{H.escape(strip(en(desc_k)))}">
<meta name="theme-color" content="#03050a">{ROBOTS}
<link rel="canonical" href="{SITE}/{'' if path=='index.html' else path}">
<link rel="alternate" hreflang="en" href="{SITE}/{'' if path=='index.html' else path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LUMORA">
<meta property="og:title" content="{H.escape(strip(en(title_k)))}">
<meta property="og:description" content="{H.escape(strip(en(desc_k)))}">
<meta property="og:image" content="{SITE}/assets/img/brand/og.jpg">
<meta property="og:url" content="{SITE}/{'' if path=='index.html' else path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="48x48" href="assets/img/brand/favicon-48.png">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/sora.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="{page}">
<a class="skip" href="#main" data-i18n="skip">{en("skip")}</a>
<div class="ambient" aria-hidden="true"></div><div class="grain" aria-hidden="true"></div>
<div class="cursor-glow" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"><span></span></div>
'''

BRAND = '''<a class="brand" href="index.html" aria-label="LUMORA — Home">
  <img src="assets/img/brand/icon-sm.webp" alt="" width="36" height="33">
  <span class="brand-text"><span class="brand-name">LUMOR<b>Λ</b></span><span class="brand-sub">DIGITAL &amp; CREATIVE</span></span>
</a>'''

def header(path):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h==path else ""} data-i18n="{k}">{en(k)}</a>' for h,k in NAV)
    return f'''<header class="header">
 <div class="wrap">
  {BRAND}
  <nav class="nav" aria-label="Main">{links}</nav>
  <div class="header-actions">
   <button class="lang-btn" type="button" aria-label="التبديل إلى العربية"><span class="ar">عربي</span></button>
   <a class="btn btn-primary btn-sm" href="contact.html#quote"><span data-i18n="cta.quote">{en("cta.quote")}</span>{I["arrow"]}</a>
   <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu" data-i18n-attr="aria-label:menu"><span></span><span></span></button>
  </div>
 </div>
</header>
<div class="mobile-menu" id="mobile-menu">
 {links}
 <a class="btn btn-primary" href="contact.html#quote"><span data-i18n="cta.quote">{en("cta.quote")}</span>{I["arrow"]}</a>
</div>
'''

def footer():
    nav = "".join(f'<li><a href="{h}" data-i18n="{k}">{en(k)}</a></li>' for h,k in NAV)
    svcs = "".join(f'<li><a href="services.html#{a}" data-i18n="{s}.t">{en(s+".t")}</a></li>' for s,_,a in SERVICES)
    return f'''<footer class="footer">
 <div class="wrap">
  <div class="footer-top">
   <div>
    {BRAND}
    {t("f.about","p")}
    <div class="socials">
     <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I["insta"]}</a>
     <a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{I["chat"]}</a>
     <a href="mailto:{EMAIL}" aria-label="Email">{I["mail"]}</a>
    </div>
   </div>
   <div>{t("f.explore","h4")}<ul>{nav}</ul></div>
   <div>{t("f.services","h4")}<ul>{svcs}</ul></div>
   <div>{t("f.contact","h4")}<ul>
     <li><a class="ltr" href="tel:{PHONE}">{PHONE_TXT}</a></li>
     <li><a class="ltr" href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li><a href="{IG}" target="_blank" rel="noopener" class="ltr">@lumoradigitals.jo</a></li>
     <li>{t("loc","span","muted")}</li>
   </ul></div>
  </div>
  <div class="footer-word" data-scroll="enter" aria-hidden="true">LUMORΛ</div>
  <div class="footer-bottom">
   <span>© <span data-year>2026</span> LUMORA. <span data-i18n="f.rights">{en("f.rights")}</span></span>
   <span data-i18n="f.slogan">{en("f.slogan")}</span>
   <a href="privacy.html" data-i18n="f.privacy">{en("f.privacy")}</a>
  </div>
 </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp" data-i18n-attr="aria-label:wa.label">{I["wa"]}</a>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/lenis.min.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

def page(path, pagekey, title_k, desc_k, main, chrome=True):
    out = head(pagekey, title_k, desc_k, path) + header(path) + f'<main id="main">\n{main}\n</main>\n' + footer()
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f: f.write(out)

def page_hero(eb, h1, lead, extra=""):
    return f'''<section class="page-hero" data-scroll="exit">
 <img class="ghost-mark" src="assets/img/brand/icon.webp" alt="" aria-hidden="true">
 <div class="wrap">
  <span class="eyebrow" data-reveal data-i18n="{eb}">{en(eb)}</span>
  <h1 class="h-xl" data-reveal style="--d:.08s" data-i18n="{h1}">{en(h1)}</h1>
  <p class="lead" data-reveal style="--d:.16s" data-i18n="{lead}">{en(lead)}</p>
  {extra}
 </div>
</section>'''

def service_cards():
    out = []
    for i,(s,ic,a) in enumerate(SERVICES,1):
        out.append(f'''<a class="card service-card" href="services.html#{a}" data-reveal>
  <span class="num">0{i}</span>
  <span class="icon">{I[ic]}</span>
  {t(s+".t","h3","h-sm")}
  {t(s+".d","p")}
  <span class="link-arrow"><span data-i18n="cta.learn">{en("cta.learn")}</span>{I["arrow"]}</span>
</a>''')
    return f'<div class="services-grid" data-stagger>{"".join(out)}</div>'

def value_cards():
    return '<div class="values" data-stagger>' + "".join(f'''<div class="card value" data-reveal><span class="icon">{I[ic]}</span>{t(v+".t","h3","h-sm")}{t(v+".d","p")}</div>''' for v,ic in VALUES) + '</div>'

def work_cards(items):
    out=[]
    for name,cat,img,url in items:
        out.append(f'''<article class="card work-card" data-reveal>
  <a class="work-media" href="{url}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
   <span class="badge" data-i18n="wk.badge">{en("wk.badge")}</span>
   <img src="assets/img/work/{img}.webp" alt="{name} website preview" loading="lazy" width="1200" height="750">
  </a>
  <div class="work-body">
   <div>{t(cat,"div","cat")}<h3>{name}</h3></div>
   <a class="btn btn-ghost btn-sm" href="{url}" target="_blank" rel="noopener" aria-label="View project: {name}"><span data-i18n="cta.project">{en("cta.project")}</span>{I["ext"]}</a>
  </div>
</article>''')
    return f'<div class="work-grid" data-stagger>{"".join(out)}</div>'

def process():
    steps="".join(f'''<div class="step" data-reveal><div class="step-dot">0{i}</div>{t(f"p{i}.t","h3","h-sm")}{t(f"p{i}.d","p")}</div>''' for i in range(1,5))
    return f'''<section class="section">
 <div class="wrap">
  <div class="section-head">
   <div><span class="eyebrow" data-reveal data-i18n="p.eyebrow">{en("p.eyebrow")}</span>
   <h2 class="h-lg" data-reveal data-i18n="p.title">{en("p.title")}</h2></div>
   {t("p.lead","p","lead",'data-reveal')}
  </div>
  <div class="process" data-scroll data-stagger><div class="process-line"><i></i></div>{steps}</div>
 </div>
</section>'''

def statement():
    return f'''<section class="section" style="padding-block:clamp(70px,10vw,140px)">
 <div class="wrap"><p class="statement" data-scroll data-words data-i18n="statement">{en("statement")}</p></div>
</section>'''

def cta():
    return f'''<section class="section" style="padding-top:0">
 <div class="wrap">
  <div class="cta-band" data-reveal="scale">
   <canvas data-wave aria-hidden="true"></canvas>
   <span class="eyebrow" data-i18n="cta.eyebrow">{en("cta.eyebrow")}</span>
   <h2 class="h-lg" data-i18n="cta.title">{en("cta.title")}</h2>
   {t("cta.lead","p","lead")}
   <div class="actions">
    <a class="btn btn-primary" href="contact.html#quote"><span data-i18n="cta.quote">{en("cta.quote")}</span>{I["arrow"]}</a>
    <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener"><span data-i18n="cta.wa">{en("cta.wa")}</span>{CHAT_BTN}</a>
   </div>
  </div>
 </div>
</section>'''

# ================= pages =================
def home():
    marquee_items = "".join(f"<span>{strip(en(s+'.t'))}</span>" for s,_,_ in SERVICES)
    main = f'''<section class="hero" data-scroll="exit">
 <div class="hero-wave" aria-hidden="true"><canvas data-wave></canvas></div>
 <div class="wrap hero-inner">
  <div>
   <span class="eyebrow" data-reveal data-i18n="h.eyebrow">{en("h.eyebrow")}</span>
   <h1 class="h-xl split-lines">
    <span class="line"><span data-i18n="h.l1">{en("h.l1")}</span></span>
    <span class="line"><span style="--d:.1s" data-i18n="h.l2">{en("h.l2")}</span></span>
    <span class="line"><span style="--d:.2s" data-i18n="h.l3">{en("h.l3")}</span></span>
   </h1>
   <p class="lead" data-reveal style="--d:.35s" data-i18n="h.lead">{en("h.lead")}</p>
   <div class="hero-ctas" data-reveal style="--d:.45s">
    <a class="btn btn-primary" href="contact.html#quote"><span data-i18n="cta.quote">{en("cta.quote")}</span>{I["arrow"]}</a>
    <a class="btn btn-ghost" href="work.html"><span data-i18n="cta.work">{en("cta.work")}</span>{I["arrow"]}</a>
   </div>
  </div>
  <div class="hero-mark" data-reveal="scale" style="--d:.2s" aria-hidden="true">
   <div class="halo"></div><div class="ring"></div><div class="ring r2"></div>
   <div class="mark"><img src="assets/img/brand/icon.webp" alt="" width="600" height="580" fetchpriority="high"></div>
  </div>
 </div>
 <div class="scroll-cue" aria-hidden="true"><span data-i18n="scroll">{en("scroll")}</span><i></i></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee_items*2}{marquee_items*2}</div></div>

<section class="section">
 <div class="wrap split">
  <div>
   <span class="eyebrow" data-reveal data-i18n="hi.eyebrow">{en("hi.eyebrow")}</span>
   <h2 class="h-lg" style="margin:18px 0 26px" data-reveal data-i18n="hi.title">{en("hi.title")}</h2>
   {t("hi.p1","p","",'data-reveal')}
   {t("hi.p2","p","",'data-reveal')}
   <div class="stat-row" data-reveal>
    <span class="chip"><i></i><span data-i18n="chip.1">{en("chip.1")}</span></span>
    <span class="chip"><i></i><span data-i18n="chip.2">{en("chip.2")}</span></span>
    <span class="chip"><i></i><span data-i18n="chip.3">{en("chip.3")}</span></span>
   </div>
   <div style="margin-top:36px" data-reveal><a class="link-arrow" href="about.html"><span data-i18n="cta.learn">{en("cta.learn")}</span>{I["arrow"]}</a></div>
  </div>
  <div class="visual-card" data-scroll data-reveal="scale">
   <img src="assets/img/brand/icon.webp" alt="" loading="lazy" aria-hidden="true">
   <span class="tag"><span class="chip" style="padding:0;border:0;background:none"><i></i></span><span data-i18n="vis.tag">{en("vis.tag")}</span></span>
  </div>
 </div>
</section>

<section class="section" style="padding-top:0">
 <div class="wrap">
  <div class="section-head">
   <div><span class="eyebrow" data-reveal data-i18n="hs.eyebrow">{en("hs.eyebrow")}</span>
   <h2 class="h-lg" data-reveal data-i18n="hs.title">{en("hs.title")}</h2></div>
   {t("hs.lead","p","lead",'data-reveal')}
  </div>
  {service_cards()}
 </div>
</section>

{statement()}

<section class="section" style="padding-top:0">
 <div class="wrap">
  <div class="section-head">
   <div><span class="eyebrow" data-reveal data-i18n="hw.eyebrow">{en("hw.eyebrow")}</span>
   <h2 class="h-lg" data-reveal data-i18n="hw.title">{en("hw.title")}</h2></div>
   <div data-reveal>{t("hw.lead","p","lead")}<a class="link-arrow" style="margin-top:18px" href="work.html"><span data-i18n="hw.all">{en("hw.all")}</span>{I["arrow"]}</a></div>
  </div>
  {work_cards(WORK[:4])}
 </div>
</section>

{process()}

<section class="section" style="padding-top:0">
 <div class="wrap">
  <div class="section-head">
   <div><span class="eyebrow" data-reveal data-i18n="hv.eyebrow">{en("hv.eyebrow")}</span>
   <h2 class="h-lg" data-reveal data-i18n="hv.title">{en("hv.title")}</h2></div>
  </div>
  {value_cards()}
 </div>
</section>

{cta()}'''
    page("index.html","home","home.title","home.desc",main)

def about():
    main = page_hero("ab.eyebrow","ab.h1","ab.lead") + f'''
<section class="section">
 <div class="wrap">
  <div class="mv-grid" data-stagger>
   <div class="card mv" data-reveal><span class="icon">{I["target"]}</span>{t("mi.t","h3","h-md")}{t("mi.d","p")}</div>
   <div class="card mv" data-reveal><span class="icon">{I["flag"]}</span>{t("vi.t","h3","h-md")}{t("vi.d","p")}</div>
  </div>
 </div>
</section>
<section class="section" style="padding-top:0">
 <div class="wrap">
  <div class="section-head"><div><span class="eyebrow" data-reveal data-i18n="hv.eyebrow">{en("hv.eyebrow")}</span>
  <h2 class="h-lg" data-reveal data-i18n="hv.title">{en("hv.title")}</h2></div></div>
  {value_cards()}
 </div>
</section>
<section class="section" style="padding-top:0">
 <div class="wrap">
  <span class="eyebrow" data-reveal data-i18n="ph.eyebrow">{en("ph.eyebrow")}</span>
  <p class="h-md" style="margin:26px 0 0;max-width:1000px;font-family:var(--font-display);font-weight:400;line-height:1.35;color:var(--muted)" data-reveal data-i18n="ph.text">{en("ph.text")}</p>
 </div>
</section>
{statement()}
<section class="section" id="founder" style="padding-top:0">
 <div class="wrap founder">
  <div class="founder-wrap" data-reveal="scale">
   <div class="founder-photo"><img src="assets/img/brand/founder.webp" alt="Hamzeh Abunemeh, Founder of LUMORA" width="900" height="900" loading="lazy"></div>
  </div>
  <div>
   <span class="eyebrow" data-reveal data-i18n="fo.eyebrow">{en("fo.eyebrow")}</span>
   <div class="founder-name" data-reveal data-i18n="fo.name">{en("fo.name")}</div>
   <div class="founder-role" data-reveal data-i18n="fo.role">{en("fo.role")}</div>
   <blockquote data-reveal data-i18n="fo.quote">{en("fo.quote")}</blockquote>
   {t("fo.p","p","",'data-reveal')}
   <div class="signature" data-reveal>
    <a class="btn btn-primary" href="contact.html#quote"><span data-i18n="fo.cta">{en("fo.cta")}</span>{I["arrow"]}</a>
    <div class="socials" style="margin:0"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I["insta"]}</a><a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{I["chat"]}</a></div>
   </div>
  </div>
 </div>
</section>
{cta()}'''
    page("about.html","about","about.title","about.desc",main)

def services():
    blocks=[]
    for i,(s,ic,a) in enumerate(SERVICES,1):
        items="".join(f'<li>{I["check"]}<span data-i18n="{s}.i{j}">{en(f"{s}.i{j}")}</span></li>' for j in range(1,7))
        blocks.append(f'''<div class="svc-detail" id="{a}">
  <div class="svc-head" data-reveal>
   <div class="card" style="display:inline-block;border-radius:18px;padding:0;background:none;border:0"><span class="icon">{I[ic]}</span></div>
   <div class="idx">0{i} / 06</div>
   {t(s+".t","h2","h-md")}
  </div>
  <div>
   {t(s+".l","p","",'data-reveal')}
   <ul class="inc" data-stagger>{items.replace("<li>","<li data-reveal>")}</ul>
  </div>
</div>''')
    main = page_hero("sv.eyebrow","sv.h1","sv.lead", f'<div class="hero-ctas" style="margin-top:36px" data-reveal><a class="btn btn-primary" href="contact.html#quote"><span data-i18n="cta.quote">{en("cta.quote")}</span>{I["arrow"]}</a></div>') + f'''
<section class="section" style="padding-top:clamp(40px,6vw,70px)">
 <div class="wrap">{"".join(blocks)}</div>
</section>
{process()}
{cta()}'''
    page("services.html","services","svc.title","svc.desc",main)

def work():
    main = page_hero("wk.eyebrow","wk.h1","wk.lead") + f'''
<section class="section">
 <div class="wrap">
  {work_cards(WORK)}
  <p class="work-note" data-reveal>{I["info"]}<span data-i18n="wk.note">{en("wk.note")}</span></p>
 </div>
</section>
{cta()}'''
    page("work.html","work","work.title","work.desc",main)

def faq():
    items="".join(f'''<div class="faq-item" data-reveal>
  <button class="faq-q" type="button" aria-expanded="false" aria-controls="fa{i}" id="fq{i}"><span data-i18n="q{i}">{en(f"q{i}")}</span><span class="pm" aria-hidden="true"></span></button>
  <div class="faq-a" id="fa{i}" role="region" aria-labelledby="fq{i}"><div>{t(f"a{i}","p")}</div></div>
</div>''' for i in range(1,9))
    main = page_hero("fq.eyebrow","fq.h1","fq.lead") + f'''
<section class="section">
 <div class="wrap"><div class="faq" data-stagger>{items}</div>
  <div class="card" style="max-width:900px;margin:60px auto 0;padding:32px;display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:space-between" data-reveal>
   <div>{t("fq.more","h3","h-sm")}{t("fq.more.d","p","muted",'style="margin:8px 0 0"')}</div>
   <a class="btn btn-primary" href="contact.html#quote"><span data-i18n="nav.contact">{en("nav.contact")}</span>{I["arrow"]}</a>
  </div>
 </div>
</section>'''
    page("faq.html","faq","faq.title","faq.desc",main)

def contact():
    def item(href, ic, lk, val, ext=False):
        tg = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a class="card contact-item" href="{href}"{tg} data-reveal><span class="icon">{I[ic]}</span><span><small data-i18n="{lk}">{en(lk)}</small><strong>{val}</strong></span></a>'
    checks="".join(f'<label class="check"><input type="checkbox" data-service value="{strip(en(s+".t"))}"><span data-i18n="opt.{s}">{en("opt."+s)}</span></label>' for s,_,_ in SERVICES)
    main = page_hero("ct.eyebrow","ct.h1","ct.lead") + f'''
<section class="section" id="quote">
 <div class="wrap contact-grid">
  <div class="contact-list" data-stagger>
   {item(WA,"chat","ct.wa",PHONE_TXT,True)}
   {item("tel:"+PHONE,"phone","ct.call",PHONE_TXT)}
   {item("mailto:"+EMAIL,"mail","ct.email",EMAIL)}
   {item(IG,"insta","ct.ig","@lumoradigitals.jo",True)}
   <div class="card contact-item" data-reveal><span class="icon">{I["pin"]}</span><span><small data-i18n="ct.loc">{en("ct.loc")}</small><strong data-i18n="loc" style="direction:inherit">{en("loc")}</strong></span></div>
  </div>
  <div class="card form-card" data-reveal>
   {t("fm.title","h2","h-md")}
   {t("fm.lead","p")}
   <form id="quote-form" method="POST" action="https://formsubmit.co/{EMAIL}">
    <input type="hidden" name="_subject" value="New quote request — LUMORA website">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="{SITE}/thanks.html">
    <input type="hidden" name="Services" value="">
    <p class="hp"><label>Don't fill this out: <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></p>
    <div class="form-grid">
     <div class="field"><label for="f-name" data-i18n="fm.name">{en("fm.name")}</label><input id="f-name" name="Name" type="text" autocomplete="name" required placeholder="{en("fm.name.ph")}" data-i18n-attr="placeholder:fm.name.ph"></div>
     <div class="field"><label for="f-email" data-i18n="fm.email">{en("fm.email")}</label><input id="f-email" name="email" type="email" autocomplete="email" required placeholder="{en("fm.email.ph")}"></div>
     <div class="field"><label for="f-phone" data-i18n="fm.phone">{en("fm.phone")}</label><input id="f-phone" name="Phone" type="tel" autocomplete="tel" placeholder="{en("fm.phone.ph")}"></div>
     <div class="field"><label for="f-biz" data-i18n="fm.biz">{en("fm.biz")}</label><input id="f-biz" name="Business" type="text" autocomplete="organization" placeholder="{en("fm.biz.ph")}" data-i18n-attr="placeholder:fm.biz.ph"></div>
     <fieldset class="field full"><legend data-i18n="fm.services">{en("fm.services")}</legend><div class="checks">{checks}</div></fieldset>
     <div class="field full"><label for="f-msg" data-i18n="fm.msg">{en("fm.msg")}</label><textarea id="f-msg" name="Message" required placeholder="{en("fm.msg.ph")}" data-i18n-attr="placeholder:fm.msg.ph"></textarea></div>
    </div>
    <div class="form-foot">
     <small data-i18n="fm.note">{en("fm.note")}</small>
     <button class="btn btn-primary" type="submit"><span data-i18n="fm.send">{en("fm.send")}</span>{I["arrow"]}</button>
    </div>
   </form>
  </div>
 </div>
</section>'''
    page("contact.html","contact","contact.title","contact.desc",main)

def privacy():
    secs="".join(f'{t("pv.h."+k,"h2")}{t("pv."+k,"p")}' for k in ["collect","use","store","rights","contact"])
    main = page_hero("pv.eyebrow","pv.h1","pv.intro") + f'''
<section class="section" style="padding-top:clamp(40px,6vw,70px)">
 <div class="wrap"><div class="prose" data-reveal>{t("pv.updated","p","muted")}{secs}</div></div>
</section>'''
    page("privacy.html","privacy","pv.title","pv.desc",main)

def status_page(path, key, title_k, inner):
    main = f'''<section class="status">
 <div class="hero-wave" aria-hidden="true" style="height:55%"><canvas data-wave></canvas></div>
 <div style="position:relative;z-index:2">{inner}</div>
</section>'''
    page(path, key, title_k, "home.desc", main)

def notfound():
    status_page("404.html","404","nf.title", f'''<div class="big" data-reveal="scale">404</div>
  <h1 class="h-lg" data-reveal data-i18n="nf.h1">{en("nf.h1")}</h1>
  {t("nf.lead","p","lead",'data-reveal')}
  <div class="actions" data-reveal><a class="btn btn-primary" href="index.html"><span data-i18n="cta.home">{en("cta.home")}</span>{I["arrow"]}</a>
  <a class="btn btn-ghost" href="contact.html"><span data-i18n="nav.contact">{en("nav.contact")}</span></a></div>''')

def thanks():
    status_page("thanks.html","thanks","thanks.title", f'''<div class="check-mark" data-reveal="scale">{I["check"]}</div>
  <h1 class="h-lg" data-reveal data-i18n="th.h1">{en("th.h1")}</h1>
  {t("th.lead","p","lead",'data-reveal')}
  <div class="actions" data-reveal><a class="btn btn-primary" href="index.html"><span data-i18n="cta.home">{en("cta.home")}</span>{I["arrow"]}</a>
  <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener"><span data-i18n="cta.wa">{en("cta.wa")}</span></a></div>''')

PLAIN = {"home.title","home.desc","work.title","work.desc","about.title","about.desc","svc.title","svc.desc","faq.title","faq.desc","contact.title","contact.desc","thanks.title","nf.title","pv.title","pv.desc"}
def i18n():
    d = {"en":{k:v[0] for k,v in C.items()}, "ar":{k:v[1] for k,v in C.items()}}
    for k in list(d["en"]):  # titles/meta are plain text
        if k in PLAIN:
            d["en"][k]=strip(d["en"][k]); d["ar"][k]=strip(d["ar"][k])
    js = "/* generated by _dev/build.py — edit _dev/content.py instead */\nwindow.LUMORA_I18N=" + json.dumps(d, ensure_ascii=False, separators=(",",":")) + ";\n"
    with open(os.path.join(ROOT,"assets/js/i18n.js"),"w",encoding="utf-8") as f: f.write(js)

if __name__ == "__main__":
    for fn in (home, about, services, work, faq, contact, privacy, notfound, thanks, i18n): fn()
    print("built")
