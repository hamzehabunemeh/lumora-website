/* LUMORA — interactions */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- language ---------- */
  const DICT = window.LUMORA_I18N || {};
  function applyLang(lang) {
    const d = DICT[lang] || DICT.en;
    root.lang = lang;
    root.dir = lang === "ar" ? "rtl" : "ltr";
    $$("[data-i18n]").forEach(el => { const v = d[el.dataset.i18n]; if (v != null) el.innerHTML = v; });
    $$("[data-i18n-attr]").forEach(el => {
      el.dataset.i18nAttr.split(";").forEach(pair => {
        const [attr, key] = pair.split(":"); if (d[key] != null) el.setAttribute(attr, d[key]);
      });
    });
    const t = $("title[data-key]"); if (t && d[t.dataset.key]) document.title = d[t.dataset.key];
    const m = $('meta[name="description"]'); if (m && m.dataset.key && d[m.dataset.key]) m.content = d[m.dataset.key];
    $$(".lang-btn").forEach(b => b.innerHTML = lang === "ar" ? '<span>EN</span>' : '<span class="ar">عربي</span>');
    $$(".lang-btn").forEach(b => b.setAttribute("aria-label", lang === "ar" ? "Switch to English" : "التبديل إلى العربية"));
    try { localStorage.setItem("lumora-lang", lang); } catch (e) {}
    splitStatements();
  }
  let lang = "en";
  try { lang = localStorage.getItem("lumora-lang") || "en"; } catch (e) {}
  applyLang(lang);
  root.classList.remove("i18n-wait");
  $$(".lang-btn").forEach(b => b.addEventListener("click", () => {
    lang = root.lang === "ar" ? "en" : "ar";
    document.body.style.opacity = 0;
    setTimeout(() => { applyLang(lang); document.body.style.opacity = ""; onScroll(); }, 220);
  }));

  /* ---------- statement: split into words ---------- */
  function splitStatements() {
    $$("[data-words]").forEach(el => {
      const out = [];
      el.childNodes.forEach(n => {
        const hl = n.nodeType === 1;
        (n.textContent || "").split(/(\s+)/).forEach(w => {
          if (!w) return;
          out.push(/^\s+$/.test(w) ? w : `<span class="w${hl ? " hl" : ""}">${w}</span>`);
        });
      });
      el.innerHTML = out.join("");
    });
  }

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  $$('a[href^="#"]').forEach(a => a.addEventListener("click", e => {
    const id = a.getAttribute("href"); if (id.length < 2) return;
    const target = $(id); if (!target) return;
    e.preventDefault();
    lenis ? lenis.scrollTo(target, { offset: -90 }) : target.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
  }));

  /* ---------- header + progress + scroll-driven values ---------- */
  const header = $(".header");
  const bar = $(".progress span");
  const wa = $(".wa-float");
  const driven = $$("[data-scroll]");
  let lastY = 0;
  function onScroll() {
    const y = window.scrollY, vh = innerHeight;
    const max = document.documentElement.scrollHeight - vh;
    if (bar) bar.style.setProperty("--p", max > 0 ? (y / max).toFixed(4) : 0);
    if (header) {
      header.classList.toggle("scrolled", y > 30);
      if (!root.classList.contains("menu-open")) header.classList.toggle("hidden", y > lastY && y > 400);
    }
    if (wa) wa.classList.toggle("show", y > 300);
    lastY = y;
    driven.forEach(el => {
      const r = el.getBoundingClientRect();
      const mode = el.dataset.scroll;
      let p;
      if (mode === "exit") p = Math.min(1, Math.max(0, -r.top / (r.height * .8)));          // 0 → 1 as element scrolls out
      else if (mode === "enter") p = Math.min(1, Math.max(0, (vh - r.top) / (vh * .9)));     // 0 → 1 as element enters
      else p = Math.min(1, Math.max(0, (vh * .85 - r.top) / (r.height * .9)));              // progress through element
      el.style.setProperty("--p", p.toFixed(4));
      if (el.hasAttribute("data-words")) {
        const ws = $$(".w", el), n = reduce ? ws.length : Math.round(p * ws.length * 1.05);
        ws.forEach((w, i) => w.classList.toggle("on", i < n));
      }
      if (el.classList.contains("process")) {
        const steps = $$(".step", el);
        steps.forEach((s, i) => s.classList.toggle("lit", reduce || p >= i / Math.max(1, steps.length - 1) - .02));
      }
    });
  }
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll);
  onScroll();

  /* ---------- reveal on enter ---------- */
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { rootMargin: "0px 0px -8% 0px", threshold: .12 });
  $$("[data-reveal], .split-lines").forEach(el => io.observe(el));
  $$("[data-stagger]").forEach(group => {
    $$("[data-reveal]", group).forEach((el, i) => el.style.setProperty("--d", (i * .08) + "s"));
  });

  /* ---------- mobile menu ---------- */
  const menuBtn = $(".menu-btn");
  if (menuBtn) menuBtn.addEventListener("click", () => {
    const open = root.classList.toggle("menu-open");
    menuBtn.setAttribute("aria-expanded", open);
    open ? lenis?.stop() : lenis?.start();
  });
  $$(".mobile-menu a").forEach(a => a.addEventListener("click", () => { root.classList.remove("menu-open"); lenis?.start(); }));

  /* ---------- page transitions ---------- */
  $$("a[href]").forEach(a => {
    const href = a.getAttribute("href");
    if (!href || href.startsWith("#") || a.target === "_blank" || /^(mailto|tel|https?):/.test(href)) return;
    a.addEventListener("click", e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault(); root.classList.add("leaving");
      setTimeout(() => location.href = href, 180);
    });
  });
  addEventListener("pageshow", () => root.classList.remove("leaving"));

  /* ---------- FAQ ---------- */
  $$(".faq-q").forEach(q => q.addEventListener("click", () => {
    const item = q.closest(".faq-item"); const open = item.classList.toggle("open");
    q.setAttribute("aria-expanded", open);
  }));

  /* ---------- pointer effects (desktop only) ---------- */
  if (finePointer && !reduce) {
    document.body.classList.add("has-pointer");
    const glow = $(".cursor-glow");
    let gx = innerWidth / 2, gy = innerHeight / 2, tx = gx, ty = gy;
    addEventListener("pointermove", e => { tx = e.clientX; ty = e.clientY; }, { passive: true });
    (function loop() {
      gx += (tx - gx) * .12; gy += (ty - gy) * .12;
      if (glow) glow.style.transform = `translate3d(${gx}px,${gy}px,0)`;
      requestAnimationFrame(loop);
    })();

    // spotlight cards
    $$(".card").forEach(c => c.addEventListener("pointermove", e => {
      const r = c.getBoundingClientRect();
      c.style.setProperty("--mx", (e.clientX - r.left) + "px");
      c.style.setProperty("--my", (e.clientY - r.top) + "px");
    }));

    // icons drift toward the cursor while scaled up
    $$(".card").forEach(c => {
      const icon = $(".icon", c); if (!icon) return;
      c.addEventListener("pointermove", e => {
        const r = icon.getBoundingClientRect();
        const dx = (e.clientX - (r.left + r.width / 2)) / 18, dy = (e.clientY - (r.top + r.height / 2)) / 18;
        icon.style.setProperty("--ix", Math.max(-6, Math.min(6, dx)) + "px");
        icon.style.setProperty("--iy", Math.max(-6, Math.min(6, dy)) + "px");
      });
      c.addEventListener("pointerleave", () => { icon.style.setProperty("--ix", "0px"); icon.style.setProperty("--iy", "0px"); });
    });

    // magnetic buttons & social icons
    $$(".btn, .socials a, .lang-btn").forEach(b => {
      b.addEventListener("pointermove", e => {
        const r = b.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * .22, y = (e.clientY - r.top - r.height / 2) * .3;
        b.style.transform = `translate(${x}px,${y}px)`;
      });
      b.addEventListener("pointerleave", () => b.style.transform = "");
    });

    // hero mark tilt
    const mark = $(".hero-mark .mark");
    if (mark) addEventListener("pointermove", e => {
      const x = (e.clientX / innerWidth - .5) * 22, y = (e.clientY / innerHeight - .5) * -18;
      mark.style.setProperty("--rx", x + "deg"); mark.style.setProperty("--ry", y + "deg");
    }, { passive: true });
  }

  /* ---------- dotted wave canvas (brand motif) ---------- */
  $$("canvas[data-wave]").forEach(cv => {
    const ctx = cv.getContext("2d");
    let w, h, dpr, visible = true, t = 0;
    const size = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    size(); addEventListener("resize", size);
    new IntersectionObserver(([e]) => visible = e.isIntersecting).observe(cv);
    const draw = () => {
      if (visible) {
        ctx.clearRect(0, 0, w, h);
        const cols = Math.floor(w / 14), rows = 26;
        for (let r = 0; r < rows; r++) {
          const depth = r / rows;
          for (let c = 0; c <= cols; c++) {
            const x = (c / cols) * w;
            const base = h * (.25 + depth * .8);
            const y = base
              - Math.sin(c * .045 + t + r * .22) * (22 + depth * 30)
              - Math.cos(c * .021 - t * .6) * 28 * (1 - depth * .5);
            const a = (.12 + depth * .55) * (.5 + .5 * Math.sin(c * .08 + t * 2 + r));
            ctx.fillStyle = `rgba(${60 + depth * 40},${150 + depth * 40},255,${a.toFixed(3)})`;
            ctx.fillRect(x, y, 1.6 + depth * .8, 1.6 + depth * .8);
          }
        }
        t += reduce ? 0 : .008;
      }
      if (!reduce) requestAnimationFrame(draw);
    };
    draw();
  });

  /* ---------- year ---------- */
  $$("[data-year]").forEach(el => el.textContent = new Date().getFullYear());
})();
