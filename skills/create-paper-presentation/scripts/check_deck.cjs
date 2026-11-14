#!/usr/bin/env node
// A real-browser check of the bundled shell; it does not establish factual accuracy.
// Usage: node check_deck.cjs deck.html output-directory [--budget-min N] [--strict]
// v1 decks (no data-shell="2") get the original checks plus measurements reported as warnings;
// v2-only interaction checks (evidence panel, zoom, main end, present) run only when window.deckShell exists.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL, fileURLToPath} = require('node:url');

const LIMIT = {
  visible: 550, visibleMedian: 350, prose: 200, proseMedian: 120, sentences: 3, au: 4,
  mainVisual: 0.35, mainVisualTarget: 0.45, conditions: 2, srcIds: 2, titleLines: 3,
  scale1280: 0.8, scale1024: 0.75, presentShare: 0.9, present1024: 0.79, progress: 0.2,
  cropGlyph: 12, phoneCard: 1.3, deckBytes: 2 * 1024 * 1024,
};

function parseArgs(argv) {
  const positional = [];
  const options = {budgetMin: null, strict: false};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--strict') options.strict = true;
    else if (arg === '--budget-min' || arg.startsWith('--budget-min=')) {
      const value = arg.includes('=') ? arg.split('=')[1] : argv[++i];
      options.budgetMin = Number(value);
      if (!(options.budgetMin > 0)) throw new Error('--budget-min needs a positive number of minutes');
    } else if (arg.startsWith('--')) throw new Error('Unknown option ' + arg);
    else positional.push(arg);
  }
  return {positional, options};
}

function loadPlaywright() {
  const tried = [];
  for (const name of [process.env.PLAYWRIGHT_MODULE, 'playwright', 'playwright-core'].filter(Boolean)) {
    try { return require(name); } catch (error) { tried.push(`${name}: ${error.code || error.message}`); }
  }
  throw new Error('Playwright not found (' + tried.join('; ') + '). Set PLAYWRIGHT_MODULE.');
}

const quantile = (values, f) => {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  return sorted[Math.floor(f * (sorted.length - 1) + 0.5)];
};
const round = (value, digits = 3) => (value === null || value === undefined || !Number.isFinite(value)) ? null
  : Math.round(value * 10 ** digits) / 10 ** digits;

// Installed into the page (after each navigation) for the measurements below.
function installHelpers() {
  if (window.__ck) return;
  const vis = el => !!el && (el.checkVisibility
    ? el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true})
    : !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length));
  const INVIS = /[\s​-‍⁠﻿]/g;
  const EXCL = '.ey, .scroll-hint, .katex-mathml, template, script, style';
  // Prose leaves out titles, tables, figures, formulas and claim-table furniture (legend · verdict · captions);
  // all of it still counts as visible text. Mirrors PROSE_SKIP_* in build_deck.py.
  const PROSE_EXCL = 'h2, table, svg, .katex, .math-inline, .math-block, [role="img"], .ev-chip, .tag, .num, .pf-grid, .fx-bars, .fx-terms, .dv-eq, .claim-legend, .verdict, .cap, figcaption';
  const SENT = '.txt p, .txt li, .vis > p:not(.cap):not(.cond):not(.claim-legend):not(.pair-line):not(.subst), .vis .bx .d, .vis .annotation span, .vis blockquote';
  const UNIT = 'table, svg, img, canvas, [role="img"], .math-block, .bx, .annotation, .derive, .factor, .claim-table, .ba, .profile, .summary-cols, figure, .flow, .compare-panel, .diagram-panel, [data-au]';
  const AU_EXCL = '.cond, .ev-chip, .tag, .cap, figcaption, .scroll-hint';
  const KEYCELL = '.em, .cl-hi, .cl-x, [data-key-cell]';
  const ID_TOKEN = /(?<![0-9A-Za-z.\-])(\d+-\d+|A-\d+|R-\d+)(?![0-9.\-%])/g;
  const slides = () => [...document.querySelectorAll('.slide')];
  const show = index => {
    if (window.deckShell && window.deckShell.show) { window.deckShell.show(index); return; }
    const jump = document.getElementById('jump');
    jump.value = String(index);
    jump.dispatchEvent(new Event('change'));
  };
  const current = () => {
    if (window.deckShell && window.deckShell.current) return window.deckShell.current();
    const match = /^(\d+)/.exec((document.getElementById('count') || {}).textContent || '');
    return match ? Number(match[1]) - 1 : -1;
  };
  const settle = () => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const textOf = (el, extra) => {
    const parts = [];
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const p = n.parentElement;
      if (!p || p.closest('.katex-mathml, template, script, style') || (extra && p.closest(extra))) continue;
      parts.push(n.data);
    }
    return parts;
  };
  const countSentences = el => {
    const text = textOf(el).join('').replace(/\s+/g, ' ').trim();
    let n = (text.match(/[.?!。](?=\s|$)/g) || []).length;
    if (!n && text.replace(INVIS, '').length >= 25 && /[다요까]$/.test(text)) n = 1;
    return n;
  };
  const lineCount = h => {
    if (!h || !vis(h)) return 0;
    const range = document.createRange();
    range.selectNodeContents(h);
    const rects = [...range.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    if (!rects.length) return 0;
    const tol = Math.max(2, Math.min(...rects.map(r => r.height)) * 0.5);
    const tops = rects.map(r => r.top).sort((a, b) => a - b);
    let lines = 1, last = tops[0];
    for (const top of tops) if (top - last > tol) { lines++; last = top; }
    return lines;
  };
  const srcVisible = slide => {
    const src = slide.querySelector('.src,.slide-source');
    if (!src || !vis(src)) return false;
    const rect = src.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  };
  const meta = (slide, index) => ({
    slide: index + 1, id: slide.dataset.id || null, part: slide.dataset.part || 'main', kind: slide.dataset.kind || null,
  });
  // Rendered glyph height of a crop: data-glyph-px (digit height in the image's own pixels) × shown ÷ natural width.
  const glyphOf = img => {
    const rect = img.getBoundingClientRect();
    const natural = img.naturalWidth || 0;
    const scale = natural ? rect.width / natural : null;
    const given = img.hasAttribute('data-glyph-px') ? Number(img.getAttribute('data-glyph-px')) : null;
    return {glyphPx: given !== null && scale !== null ? given * scale : null, dataGlyphPx: given, renderScale: scale,
      loaded: natural > 0};
  };
  // Every <img> in the deck, hidden evidence panels included: a fresh Image() probe per source that has not
  // decoded, so lazy or hidden images are tested too. Returns the ones that do not load.
  async function brokenImages() {
    const list = slides();
    const probe = src => new Promise(resolve => {
      const img = new Image();
      const timer = setTimeout(() => resolve(false), 8000);
      img.onload = () => { clearTimeout(timer); resolve(img.naturalWidth > 0); };
      img.onerror = () => { clearTimeout(timer); resolve(false); };
      img.src = src;
    });
    const out = [];
    for (const img of document.images) {
      if (img.complete && img.naturalWidth > 0) continue;
      const attr = img.getAttribute('src') || '';
      if (attr && await probe(img.src)) continue;
      const slide = img.closest('.slide');
      const where = img.closest('.evidence') ? 'evidence' : img.closest('.inner') ? 'screen' : 'other';
      const scheme = (/^([a-z][a-z0-9+.-]*):/i.exec(img.src) || [])[1] || '';
      out.push({slide: slide ? list.indexOf(slide) + 1 : null, id: slide ? slide.dataset.id || null : null, where,
        src: attr.startsWith('data:') ? attr.slice(0, 40) + '…' : attr, remote: /^https?$/i.test(scheme)});
    }
    return out;
  }

  // Screen-mode measurements of one slide (call after show).
  function measure(index, ids) {
    const slide = slides()[index];
    const out = meta(slide, index);
    const inner = slide.querySelector('.inner');
    out.srcVisible = srcVisible(slide);
    const srcLine = slide.querySelector('.src-line');
    out.srcLine = !!srcLine;
    const srcLinks = srcLine ? [...srcLine.querySelectorAll('a')] : [...slide.querySelectorAll('.src a')];
    out.srcIds = srcLinks.length;
    out.srcIdsNamed = srcLinks.filter(a => a.textContent.replace(INVIS, '').length > 0).length;
    out.hasPanel = !!slide.querySelector('.evidence');
    out.notesChars = ((slide.querySelector('.speaker-notes') || {}).textContent || '').replace(INVIS, '').length;
    out.seconds = slide.dataset.seconds ? Number(slide.dataset.seconds) : null;
    if (!inner) return Object.assign(out, {missingInner: true, visibleChars: 0, proseChars: 0, sentences: 0, au: 0,
      mainVisualShare: null, conditions: 0, chips: {}, titleLines: 0, unlinked: [], crops: [], claimLegendMissing: 0,
      verdictMissing: false});
    const cache = new Map();
    const v = el => { if (!cache.has(el)) cache.set(el, vis(el)); return cache.get(el); };
    let visible = 0, prose = 0;
    const unlinkedParts = [];
    const walker = document.createTreeWalker(inner, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const p = n.parentElement;
      if (!p || p.closest(EXCL) || !v(p)) continue;
      const chars = n.data.replace(INVIS, '').length;
      if (!chars) continue;
      visible += chars;
      if (!p.closest(PROSE_EXCL)) prose += chars;
      if (!p.closest('a')) unlinkedParts.push(n.data);
    }
    const sentenceEls = [...inner.querySelectorAll(SENT)].filter(v);
    const sentenceSet = new Set(sentenceEls);
    const sentenceRoots = sentenceEls.filter(el => {
      for (let p = el.parentElement; p && p !== inner; p = p.parentElement) if (sentenceSet.has(p)) return false;
      return true;
    });
    const units = [...inner.querySelectorAll(UNIT)].filter(el => v(el) && !el.closest(AU_EXCL));
    const roots = units.filter(el => {
      for (let p = el.parentElement; p && p !== inner; p = p.parentElement) if (p.matches(UNIT)) return false;
      return true;
    });
    let au = 0;
    for (const el of roots) {
      au += el.hasAttribute('data-au') ? Math.max(0, Math.min(4, parseInt(el.getAttribute('data-au'), 10) || 0)) : 1;
    }
    const txt = inner.querySelector('.txt');
    if (txt && [...txt.querySelectorAll('p, ul, ol, blockquote')].some(el => v(el) &&
        !el.matches('.cond, .pair-line, .scroll-hint') && !el.closest(UNIT) && !el.closest(AU_EXCL))) au += 1;
    if ([...inner.querySelectorAll('.vis > p:not(.cap):not(.cond):not(.pair-line):not(.scroll-hint)')].some(v)) au += 1;
    // Main-visual share = [data-main] area ÷ the content area of .inner (its box minus padding). Both share the
    // card's scale, so the ratio is scale-free. Ceiling ≈ 0.60 in split (the .txt column takes the rest), ≈ 0.70
    // in wide (title · body rows above), so the 0.45 target is reachable in both layouts.
    const innerRect = inner.getBoundingClientRect();
    const innerStyle = getComputedStyle(inner);
    const cssScale = inner.offsetWidth ? innerRect.width / inner.offsetWidth : 1;
    const pad = name => (parseFloat(innerStyle[name]) || 0) * cssScale;
    const contentW = Math.max(0, innerRect.width - pad('paddingLeft') - pad('paddingRight'));
    const contentH = Math.max(0, innerRect.height - pad('paddingTop') - pad('paddingBottom'));
    const innerArea = contentW * contentH;
    const mains = [...inner.querySelectorAll('[data-main]')].filter(v);
    let best = 0;
    for (const el of (mains.length ? mains : roots)) {
      const r = el.getBoundingClientRect();
      best = Math.max(best, r.width * r.height);
    }
    const chips = {};
    for (const chip of inner.querySelectorAll('.ev-chip')) {
      if (!v(chip)) continue;
      const kind = chip.dataset.ev || 'none';
      chips[kind] = (chips[kind] || 0) + 1;
    }
    const unlinkedText = unlinkedParts.join(' ');
    const unlinked = [...new Set([...unlinkedText.matchAll(ID_TOKEN)].map(m => m[1]).filter(t => ids.includes(t)))];
    // Thumbnails (.crop-thumb, ~60px tall, opened by zoom) are not meant to be read in place: no glyph check.
    const crops = [...inner.querySelectorAll('img')].filter(img => v(img) && !img.closest('.crop-thumb')).map(glyphOf);
    const tables = [...slide.querySelectorAll('.claim-table')];
    return Object.assign(out, {
      visibleChars: visible, proseChars: prose,
      sentences: sentenceRoots.reduce((sum, el) => sum + countSentences(el), 0),
      au, mainVisualShare: innerArea ? best / innerArea : null,
      conditions: [...inner.querySelectorAll('.cond')].filter(v).length,
      chips, titleLines: lineCount(inner.querySelector('h2')), unlinked, crops,
      claimLegendMissing: tables.filter(t => !t.querySelector('.claim-legend')).length,
      verdictMissing: !!slide.querySelector('.cl-x') && !slide.querySelector('.verdict'),
    });
  }

  // Phone (read mode) measurements of the shown slide.
  function phone(index) {
    const slide = slides()[index];
    const out = meta(slide, index);
    const card = slide.querySelector('.card');
    out.cardHeight = card ? card.getBoundingClientRect().height : 0;
    out.scrollScreens = document.documentElement.scrollHeight / innerHeight;
    out.titleLines = lineCount(slide.querySelector('.inner h2'));
    out.srcVisible = srcVisible(slide);
    out.keyCellsOffscreen = 0;
    for (const region of slide.querySelectorAll('.table-wrap, .diagram-scroll, .math-block')) {
      if (!vis(region)) continue;
      const rr = region.getBoundingClientRect();
      for (const cell of region.querySelectorAll(KEYCELL)) {
        if (!vis(cell)) continue;
        const cr = cell.getBoundingClientRect();
        if (cr.right > rr.right + 1 || cr.left < rr.left - 1) out.keyCellsOffscreen++;
      }
    }
    out.mathHintMissing = 0;
    for (const block of slide.querySelectorAll('.math-block')) {
      if (!vis(block) || block.scrollWidth <= block.clientWidth + 2) continue;
      const hint = block._scrollHint || (block.nextElementSibling && block.nextElementSibling.matches('.scroll-hint')
        ? block.nextElementSibling : null);
      if (!hint || !vis(hint)) out.mathHintMissing++;
    }
    return out;
  }

  function facts() {
    const root = document.documentElement;
    const list = slides();
    const normW = w => (w === 'normal' ? '400' : w === 'bold' ? '700' : String(parseInt(w, 10) || w));
    const faces = new Set([...document.fonts].map(f => `${f.family.replace(/^["']|["']$/g, '')}|${normW(f.weight)}|${f.style}`));
    const fontsMissing = new Set();
    for (const el of document.querySelectorAll('.katex-html *')) {
      if (![...el.childNodes].some(n => n.nodeType === 3 && /\S/.test(n.data))) continue;
      const cs = getComputedStyle(el);
      const family = cs.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
      if (!family.startsWith('KaTeX_')) continue;
      const key = `${family}|${normW(cs.fontWeight)}|${cs.fontStyle}`;
      if (!faces.has(key)) fontsMissing.add(key);
    }
    let links = 0;
    const broken = [];
    list.forEach((slide, index) => {
      for (const a of slide.querySelectorAll('a[href^="#s"]')) {
        const match = /^#s(\d+)$/.exec(a.getAttribute('href'));
        if (!match) continue;
        links++;
        const target = Number(match[1]);
        if (target < 1 || target > list.length) broken.push({slide: index + 1, id: slide.dataset.id || null, href: a.getAttribute('href')});
      }
    });
    const zoomable = document.querySelector('figure.crop img, .evidence img, img[data-zoom]');
    return {
      shell: root.dataset.shell === '2' ? 2 : 1,
      hasDeckShell: !!window.deckShell,
      budgetMin: root.dataset.budgetMin ? Number(root.dataset.budgetMin) : null,
      total: list.length,
      ids: list.map(s => s.dataset.id).filter(Boolean),
      math: {
        katex: document.querySelectorAll('.katex').length,
        mathml: document.querySelectorAll('.katex-mathml').length,
        fallback: document.querySelectorAll('.math-fallback').length,
        fontsMissing: [...fontsMissing].sort(),
      },
      xref: {links, broken},
      evidenceCrops: [...document.querySelectorAll('.evidence img')].map(img => ({
        slide: list.indexOf(img.closest('.slide')) + 1, id: (img.closest('.slide') || {dataset: {}}).dataset.id || null,
        dataGlyphPx: img.hasAttribute('data-glyph-px') ? Number(img.getAttribute('data-glyph-px')) : null,
      })),
      zoomSlide: zoomable ? list.indexOf(zoomable.closest('.slide')) : -1,
      zoomInPanel: !!(zoomable && zoomable.closest('.evidence')),
      panelSlides: list.map((s, i) => (s.querySelector('.evidence') ? i : -1)).filter(i => i >= 0),
      hasBack: list.some(s => ['appendix', 'review'].includes(s.dataset.part)),
      mainEnd: (() => {
        let idx = list.findIndex(s => s.classList.contains('is-main-end'));
        if (idx < 0) list.forEach((s, i) => { if ((s.dataset.part || 'main') === 'main') idx = i; });
        return idx;
      })(),
    };
  }

  window.__ck = {vis, show, current, settle, measure, phone, facts, srcVisible, glyphOf, brokenImages,
    scale: () => {
      const root = document.documentElement;
      const fit = root.classList.contains('fit');
      const s = parseFloat(root.style.getPropertyValue('--s') || getComputedStyle(root).getPropertyValue('--s'));
      return {fit, scale: fit && Number.isFinite(s) ? Math.round(s * 10000) / 10000 : null};
    }};
}

async function fresh(page, url, viewport) {
  if (viewport) await page.setViewportSize(viewport);
  await page.goto(url);
  await page.evaluate(() => { try { localStorage.clear(); } catch (_) {} });
  await page.reload();
  await page.evaluate(() => document.fonts.ready);
  // A lazy image inside a hidden panel never fires load or error; do not wait on it forever (brokenImages probes it).
  await page.evaluate(() => Promise.all([...document.images].map(img => (img.complete ? null
    : new Promise(resolve => { img.addEventListener('load', resolve); img.addEventListener('error', resolve);
      setTimeout(resolve, 8000); })))));
  await page.evaluate(installHelpers);
}

async function notesAccess(page, label, touch) {
  const index = await page.evaluate(() => [...document.querySelectorAll('.slide')]
    .findIndex(s => ((s.querySelector('.speaker-notes') || {}).textContent || '').trim()));
  if (index < 0) return {viewport: label, slide: null, button: null, ok: null, reason: 'no slide has notes'};
  await page.evaluate(i => { window.__ck.show(i); return window.__ck.settle(); }, index);
  const button = await page.evaluate(() => {
    for (const selector of ['#notes-nav', '.notes-btn']) {
      const el = document.querySelector(selector);
      if (el && window.__ck.vis(el) && el.getBoundingClientRect().width > 0) return selector;
    }
    return null;
  });
  if (!button) return {viewport: label, slide: index + 1, button: null, ok: false, reason: 'no visible notes button'};
  const locator = page.locator(button).first();
  const press = () => (touch ? locator.tap({timeout: 3000}) : locator.click({timeout: 3000}));
  try {
    await press();
    const visible = await page.evaluate(() => {
      const notes = document.querySelector('.slide.on .speaker-notes');
      if (!notes || !window.__ck.vis(notes)) return false;
      const rect = notes.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    });
    await press();
    return {viewport: label, slide: index + 1, button, ok: visible, reason: visible ? null : 'notes not visible after press'};
  } catch (error) {
    return {viewport: label, slide: index + 1, button, ok: false, reason: String(error.message).split('\n')[0]};
  }
}

async function main() {
  const {positional, options} = parseArgs(process.argv.slice(2));
  const [input, output] = positional;
  if (!input || !output) throw new Error('Usage: node check_deck.cjs deck.html output-directory [--budget-min N] [--strict]');
  const {chromium} = loadPlaywright();
  const out = path.resolve(output);
  fs.mkdirSync(out, {recursive: true});
  const browser = await chromium.launch({headless: true,
    ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
  const errors = [], views = [], failures = [], warnings = [];
  const warn = (code, item, value, limit, msg) => warnings.push({code, slide: item ? item.slide : null,
    id: item ? item.id : null, value: value === undefined ? null : value, limit: limit === undefined ? null : limit, msg});
  try {
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    const url = /^https?:\/\//.test(input) ? input : pathToFileURL(path.resolve(input)).href;
    for (const vp of [{width:1440,height:900},{width:860,height:760},{width:390,height:844}]) {
      await page.setViewportSize(vp);
      await page.goto(url);
      await page.evaluate(() => localStorage.clear());
      await page.reload();
      await page.evaluate(() => document.fonts.ready);
      const audit = await page.evaluate(() => window.deckCheck());
      if (!audit.length) failures.push(`${vp.width}: no slides`);
      const horizontalOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 2);
      if (horizontalOverflow) failures.push(`${vp.width}: page horizontal overflow`);
      if (vp.width < 820) {
        const mobileMode = await page.evaluate(() => ({fit:document.documentElement.classList.contains('fit'),toggleHidden:document.querySelector('#mode').hidden}));
        if (mobileMode.fit || !mobileMode.toggleHidden) failures.push(`${vp.width}: unsupported mobile fit mode available`);
        await page.selectOption('#jump','0');
        await page.evaluate(() => window.scrollTo(0,document.documentElement.scrollHeight));
        if (audit.length > 1) {
          await page.locator('#next').click();
          if (await page.evaluate(() => window.scrollY > 2)) failures.push(`${vp.width}: next slide retained previous scroll position`);
        }
        // A saved desktop preference must not clip the mobile layout on reload.
        await page.evaluate(() => localStorage.setItem('paper-study-' + document.title + '-mode','slide'));
        await page.reload();
        if (await page.evaluate(() => document.documentElement.classList.contains('fit'))) failures.push(`${vp.width}: saved slide mode bypassed mobile layout`);
        await page.evaluate(() => localStorage.clear());
      }
      for (const item of audit) {
        if (item.innerOverflow || item.cardOverflow || !item.hasSource)
          failures.push(`${vp.width}: slide ${item.slide} overflow or missing source`);
        await page.selectOption('#jump', String(item.slide - 1));
        await page.screenshot({path:path.join(out,`${vp.width}-s${String(item.slide).padStart(2,'0')}.png`),fullPage:vp.width < 820});
      }
      views.push({viewport:vp, horizontalOverflow, slides:audit});
    }
    await page.setViewportSize({width:1440,height:900});
    await page.reload();
    await page.locator('body').click({position:{x:5,y:5}});
    await page.keyboard.press('Home');
    const first = await page.locator('#count').innerText();
    const total = await page.locator('.slide').count();
    if (total > 1) await page.locator('#next').click();
    const next = await page.locator('#count').innerText();
    if (total > 1) await page.locator('#prev').click();
    const previous = await page.locator('#count').innerText();
    await page.locator('body').click({position:{x:5,y:5}});
    await page.keyboard.press('End');
    const end = await page.locator('#count').innerText();
    await page.keyboard.press('ArrowLeft');
    const left = await page.locator('#count').innerText();
    await page.locator('#mode').click();
    const read = await page.evaluate(() => !document.documentElement.classList.contains('fit'));
    await page.locator('#mode').click();
    const fit = await page.evaluate(() => document.documentElement.classList.contains('fit'));
    const navigation = {first,next,previous,end,left,read,fit};
    if (first !== `1 / ${total}` || previous !== first || next !== `${Math.min(2,total)} / ${total}` ||
        end !== `${total} / ${total}` || left !== `${Math.max(1,total-1)} / ${total}` || !read || !fit)
      failures.push('navigation or mode toggle mismatch');
    const links = await page.locator('.slide a').evaluateAll(nodes => nodes.map(a => ({label:a.textContent,href:a.href})));
    const brokenLocal = links.filter(link => link.href.startsWith('file:') && !fs.existsSync(fileURLToPath(new URL(link.href))));
    if (brokenLocal.length) failures.push(`${brokenLocal.length} missing local link targets`);
    await page.emulateMedia({media:'print'});
    await page.pdf({path:path.join(out,'review.pdf'),preferCSSPageSize:true,printBackground:true});
    await page.emulateMedia({media:'screen'});

    // ---------- v2 measurements (reported for every deck; v2-only checks need window.deckShell) ----------
    await fresh(page, url, {width:1440,height:900});
    const facts = await page.evaluate(() => window.__ck.facts());
    const v2 = facts.shell === 2;
    const interactive = v2 && facts.hasDeckShell;
    if (v2 && !facts.hasDeckShell) failures.push('C-SHELL: data-shell="2" but window.deckShell is missing');
    // images that do not load (all decks; local · data URI = v2 fail / v1 warn, remote = warn)
    const images = {broken: await page.evaluate(() => window.__ck.brokenImages())};
    for (const b of images.broken) {
      const where = `slide ${b.slide === null ? '-' : b.slide}${b.id ? ' (' + b.id + ')' : ''} ${b.where} ${b.src || '(no src)'}`;
      if (v2 && !b.remote) failures.push(`C-IMG-BROKEN: ${where}`);
      else warn('C-IMG-BROKEN', b, null, null, `이미지가 열리지 않음: ${where}${b.remote ? ' (원격, 네트워크 확인)' : ' (v1 덱 보고)'}`);
    }
    const perSlide = [];
    for (let i = 0; i < facts.total; i++) {
      perSlide.push(await page.evaluate(async ([index, ids]) => {
        window.__ck.show(index);
        await document.fonts.ready;
        await window.__ck.settle();
        return window.__ck.measure(index, ids);
      }, [i, facts.ids]));
    }
    const mains = perSlide.filter(s => s.part === 'main');
    for (const s of perSlide) {
      if (!s.srcVisible) failures.push(`C-SRC-HIDDEN: 1440: slide ${s.slide}${s.id ? ' (' + s.id + ')' : ''} source line missing or hidden`);
      if (v2 && (!s.srcLine || s.srcIdsNamed === 0))
        failures.push(`C-SRC-EMPTY: slide ${s.slide}${s.id ? ' (' + s.id + ')' : ''} has no named source link in .src-line`);
      if (v2 && s.part === 'main' && s.notesChars === 0) warn('C-NOTES-MISSING', s, 0, null, '본편 장에 대본이 없음');
      if (s.part === 'main') {
        if (s.visibleChars > LIMIT.visible) warn('C-VISIBLE', s, s.visibleChars, LIMIT.visible, `화면 글 ${s.visibleChars}자 > ${LIMIT.visible}`);
        if (s.proseChars > LIMIT.prose) warn('C-PROSE', s, s.proseChars, LIMIT.prose, `산문 ${s.proseChars}자 > ${LIMIT.prose}`);
        if (s.sentences > LIMIT.sentences) warn('C-SENTENCES', s, s.sentences, LIMIT.sentences, `문장 ${s.sentences}개 > ${LIMIT.sentences}`);
        if (s.au > LIMIT.au) warn('C-AU', s, s.au, LIMIT.au, `주의 단위 ${s.au} > ${LIMIT.au}`);
        if (['result', 'mechanism'].includes(s.kind) && s.mainVisualShare !== null && s.mainVisualShare < LIMIT.mainVisual)
          warn('C-MAINVIS', s, round(s.mainVisualShare), LIMIT.mainVisual, `주 시각 면적 ${Math.round(s.mainVisualShare * 100)}% < ${Math.round(LIMIT.mainVisual * 100)}% (.inner 콘텐츠 영역 대비, 목표 ${Math.round(LIMIT.mainVisualTarget * 100)}%)`);
      }
      if (s.conditions >= LIMIT.conditions) warn('C-COND', s, s.conditions, 1, `조건 줄 ${s.conditions}개`);
      if (v2 && s.srcIds > LIMIT.srcIds) warn('C-SRC-IDS', s, s.srcIds, LIMIT.srcIds, `화면 출처 링크 ${s.srcIds}개 > ${LIMIT.srcIds}`);
      if (s.titleLines >= LIMIT.titleLines) warn('C-TITLE-LINES', s, s.titleLines, 2, `1440 제목 ${s.titleLines}줄`);
      if (s.unlinked.length) warn('C-XREF-UNLINKED', s, s.unlinked.length, 0, `링크 없는 장 번호 ${s.unlinked.join(', ')}`);
      for (const crop of s.crops) {
        if (crop.glyphPx !== null && crop.glyphPx < LIMIT.cropGlyph)
          warn('C-CROP-GLYPH', s, round(crop.glyphPx, 1), LIMIT.cropGlyph, `원문 crop 글자 높이 ${crop.glyphPx.toFixed(1)}px < ${LIMIT.cropGlyph}px`);
        else if (crop.glyphPx === null && crop.renderScale !== null && crop.renderScale < 0.5)
          warn('C-CROP-GLYPH', s, round(crop.renderScale), 0.5, `글자 크기 모름: data-glyph-px 없음 · 표시 배율 ${crop.renderScale.toFixed(2)}`);
      }
      if (s.claimLegendMissing) warn('C-CLAIM-LEGEND', s, s.claimLegendMissing, 0, '.claim-table에 .claim-legend 없음');
      if (s.verdictMissing) warn('C-VERDICT', s, null, null, '.cl-x 셀이 있는데 .verdict 없음');
      if (v2 && s.part === 'main' && ['result', 'mechanism'].includes(s.kind) && !s.hasPanel)
        warn('C-EVIDENCE-MISSING', s, null, null, `kind ${s.kind} 장에 근거 패널 없음`);
    }
    const stat = key => mains.map(s => s[key]).filter(Number.isFinite);
    const summary = {
      visible: {median: quantile(stat('visibleChars'), 0.5), p90: quantile(stat('visibleChars'), 0.9)},
      prose: {median: quantile(stat('proseChars'), 0.5), p90: quantile(stat('proseChars'), 0.9)},
      au: {median: quantile(stat('au'), 0.5), max: stat('au').length ? Math.max(...stat('au')) : null},
      titleLines3plusShare: mains.length ? round(mains.filter(s => s.titleLines >= 3).length / mains.length) : null,
      mainVisual: {basis: '[data-main] ÷ .inner content box (padding excluded)', target: LIMIT.mainVisualTarget,
        warnBelow: LIMIT.mainVisual,
        belowTarget: mains.filter(s => ['result', 'mechanism'].includes(s.kind) && s.mainVisualShare !== null &&
          s.mainVisualShare < LIMIT.mainVisualTarget).map(s => s.id || s.slide)},
    };
    if (summary.visible.median > LIMIT.visibleMedian) warn('C-VISIBLE-MEDIAN', null, summary.visible.median, LIMIT.visibleMedian, `본편 화면 글 중앙값 ${summary.visible.median} > ${LIMIT.visibleMedian}`);
    if (summary.visible.p90 > LIMIT.visible) warn('C-VISIBLE-P90', null, summary.visible.p90, LIMIT.visible, `본편 화면 글 p90 ${summary.visible.p90} > ${LIMIT.visible}`);
    if (summary.prose.median > LIMIT.proseMedian) warn('C-PROSE-MEDIAN', null, summary.prose.median, LIMIT.proseMedian, `본편 산문 중앙값 ${summary.prose.median} > ${LIMIT.proseMedian}`);
    if (summary.prose.p90 > LIMIT.prose) warn('C-PROSE-P90', null, summary.prose.p90, LIMIT.prose, `본편 산문 p90 ${summary.prose.p90} > ${LIMIT.prose}`);
    const density = {perSlide: perSlide.map(s => ({slide: s.slide, id: s.id, part: s.part, kind: s.kind,
      visibleChars: s.visibleChars, proseChars: s.proseChars, sentences: s.sentences, au: s.au,
      mainVisualShare: round(s.mainVisualShare), conditions: s.conditions, srcIds: s.srcIds, chips: s.chips,
      titleLines1440: s.titleLines, titleLines390: null})), summary};

    // budget (DOM)
    const minutes = options.budgetMin || facts.budgetMin || null;
    const anyKind = mains.some(s => s.kind);
    const firstSection = await page.evaluate(() => {
      const s = [...document.querySelectorAll('.slide')].find(x => (x.dataset.part || 'main') === 'main');
      return s ? s.dataset.sec || '1' : null;
    });
    const sections = await page.evaluate(() => [...document.querySelectorAll('.slide')].map(x => x.dataset.sec || '1'));
    const introSlides = anyKind ? mains.filter(s => s.kind === 'intro').length
      : mains.filter(s => sections[s.slide - 1] === firstSection).length;
    const plannedSeconds = mains.reduce((sum, s) => sum + (s.seconds || 0), 0);
    const notesChars = mains.reduce((sum, s) => sum + s.notesChars, 0);
    const budget = {minutes, mainSlides: mains.length, target: null, cap: null, introSlides, plannedSeconds, notesChars,
      notesMinutes: round(notesChars / 300, 2)};
    if (minutes) {
      const lo = Math.floor(0.8 * minutes + 0.5 + 1e-9), hi = Math.floor(1.05 * minutes + 1e-9), cap = Math.floor(1.2 * minutes + 1e-9);
      budget.target = [lo, hi];
      budget.cap = cap;
      if (mains.length < lo || mains.length > hi)
        warn('C-BUDGET-SLIDES', null, mains.length, [lo, hi], `본편 ${mains.length}장, 목표 ${lo}–${hi}장 · 상한 ${cap}장${mains.length > cap ? ' · 상한 초과' : ''}`);
      if (introSlides > 3) warn('C-BUDGET-INTRO', null, introSlides, 3, `들어가며 ${introSlides}장 > 3장`);
      if (plannedSeconds > minutes * 60) warn('C-BUDGET-TIME', null, plannedSeconds, minutes * 60, `본편 설명 시간 ${plannedSeconds}초 > ${minutes}분`);
      if (notesChars / 300 > minutes) warn('C-NOTES-MINUTES', null, round(notesChars / 300, 2), minutes, `본편 대본 ${notesChars}자 ≈ ${(notesChars / 300).toFixed(1)}분 > ${minutes}분`);
    }

    // math, xref, crops (page facts)
    const math = {katex: facts.math.katex, mathml: facts.math.mathml, fallback: facts.math.fallback, hintMissing: [],
      fontsMissing: facts.math.fontsMissing};
    if (math.fallback) warn('C-MATH-FALLBACK', null, math.fallback, 0, `.math-fallback ${math.fallback}개 (KaTeX 미렌더)`);
    if (math.katex !== math.mathml) warn('C-MATH-MATHML', null, math.mathml, math.katex, `.katex ${math.katex}개 ≠ .katex-mathml ${math.mathml}개`);
    if (math.fontsMissing.length) warn('C-MATH-FONT', null, math.fontsMissing.length, 0, `내장되지 않은 KaTeX 글꼴: ${math.fontsMissing.join(', ')}`);
    const xref = {links: facts.xref.links, broken: facts.xref.broken,
      unlinked: perSlide.filter(s => s.unlinked.length).map(s => ({slide: s.slide, id: s.id, tokens: s.unlinked}))};
    for (const b of xref.broken) failures.push(`C-XREF-BROKEN: slide ${b.slide}${b.id ? ' (' + b.id + ')' : ''} links ${b.href} but the deck has ${facts.total} slides`);
    const crops = [];
    for (const s of perSlide) for (const crop of s.crops) crops.push({slide: s.slide, id: s.id, glyphPx: round(crop.glyphPx, 1), where: 'screen'});
    const panelCrops = new Map();   // slide number -> [glyphOf] measured with the panel open (1440, below)

    // evidence panel toggle, zoom, main end (v2)
    const evidence = {slidesWithPanel: facts.panelSlides.length,
      mainWithoutPanel: perSlide.filter(s => s.part === 'main' && ['result', 'mechanism'].includes(s.kind) && !s.hasPanel).map(s => s.id || s.slide),
      toggleFailures: [], toggles: []};
    let zoom = null, mainEnd = null;
    if (interactive) {
      for (const index of facts.panelSlides) {
        const record = {slide: index + 1, id: perSlide[index].id};
        try {
          await page.evaluate(i => { window.__ck.show(i); return window.__ck.settle(); }, index);
          await page.locator('.slide.on .ev-btn').click({timeout: 3000});
          Object.assign(record, await page.evaluate(async () => {
            const slide = document.querySelector('.slide.on');
            const panel = slide.querySelector('.evidence');
            await window.__ck.settle();
            const imgs = [...panel.querySelectorAll('img')].map(img => (window.__ck.vis(img) ? window.__ck.glyphOf(img)
              : {glyphPx: null, renderScale: null}));
            return {opened: !panel.hidden && window.__ck.vis(panel), focusInside: panel.contains(document.activeElement),
              evOpen: slide.classList.contains('ev-open'), expanded: slide.querySelector('.ev-btn').getAttribute('aria-expanded'),
              panelImgs: imgs};
          }));
          panelCrops.set(record.slide, record.panelImgs);
          delete record.panelImgs;
          await page.keyboard.press('Escape');
          Object.assign(record, await page.evaluate(() => {
            const slide = document.querySelector('.slide.on');
            const panel = slide.querySelector('.evidence');
            return {closed: panel.hidden || !window.__ck.vis(panel), focusOnButton: document.activeElement === slide.querySelector('.ev-btn')};
          }));
        } catch (error) { record.error = String(error.message).split('\n')[0]; }
        record.ok = !record.error && record.opened && record.focusInside && record.evOpen && record.closed && record.focusOnButton;
        evidence.toggles.push(record);
        if (!record.ok) {
          evidence.toggleFailures.push(record);
          const what = record.error || ['opened', 'focusInside', 'evOpen', 'closed', 'focusOnButton'].filter(k => !record[k]).join(', ');
          failures.push(`C-EVIDENCE-TOGGLE: slide ${record.slide}${record.id ? ' (' + record.id + ')' : ''}: ${what}`);
        }
      }
      if (facts.zoomSlide >= 0) {
        zoom = {slide: facts.zoomSlide + 1, inPanel: facts.zoomInPanel};
        try {
          await page.evaluate(i => { window.__ck.show(i); return window.__ck.settle(); }, facts.zoomSlide);
          if (facts.zoomInPanel) await page.locator('.slide.on .ev-btn').click({timeout: 3000});
          zoom.loaded = await page.evaluate(() => {
            const img = document.querySelector('figure.crop img, .evidence img, img[data-zoom]');
            img.setAttribute('data-check-zoom', '');
            return img.complete && img.naturalWidth > 0;
          });
          if (!zoom.loaded) throw new Error('zoom image did not load (naturalWidth 0)');
          await page.locator('img[data-check-zoom]').click({timeout: 3000});
          zoom.opened = await page.evaluate(() => { const d = document.getElementById('zoom-dlg'); return !!d && (d.open || d.hasAttribute('open')); });
          await page.keyboard.press('Escape');
          zoom.closed = await page.evaluate(() => { const d = document.getElementById('zoom-dlg'); return !d || !(d.open || d.hasAttribute('open')); });
          if (facts.zoomInPanel) await page.keyboard.press('Escape');
        } catch (error) { zoom.error = String(error.message).split('\n')[0]; }
        await page.evaluate(() => { const img = document.querySelector('img[data-check-zoom]'); if (img) img.removeAttribute('data-check-zoom'); });
        zoom.ok = !zoom.error && zoom.opened && zoom.closed;
        if (!zoom.ok) failures.push(`C-ZOOM: slide ${zoom.slide}: ${zoom.error || (!zoom.opened ? '#zoom-dlg did not open' : 'Esc did not close #zoom-dlg')}`);
      }
      if (facts.hasBack && facts.mainEnd >= 0 && facts.mainEnd < facts.total - 1) {
        mainEnd = {slide: facts.mainEnd + 1};
        try {
          await page.evaluate(i => { window.__ck.show(i); if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); return window.__ck.settle(); }, facts.mainEnd);
          await page.keyboard.press('ArrowRight');
          mainEnd.afterFirst = (await page.evaluate(() => window.__ck.current())) + 1;
          await page.keyboard.press('ArrowRight');
          mainEnd.afterSecond = (await page.evaluate(() => window.__ck.current())) + 1;
        } catch (error) { mainEnd.error = String(error.message).split('\n')[0]; }
        mainEnd.ok = !mainEnd.error && mainEnd.afterFirst === mainEnd.slide && mainEnd.afterSecond === mainEnd.slide + 1;
        if (!mainEnd.ok) failures.push(`C-MAIN-END: slide ${mainEnd.slide}: ${mainEnd.error || `→ went to ${mainEnd.afterFirst}, then ${mainEnd.afterSecond}`}`);
      }
    }

    // evidence-panel crops: rendered glyph height with the panel open at 1440 (reported; the panel crop is
    // read through zoom, so no threshold). Panels that were not opened report glyphPx null.
    for (const crop of facts.evidenceCrops) {
      const measured = panelCrops.get(crop.slide);
      const m = measured && measured.length ? measured.shift() : null;
      crops.push({slide: crop.slide, id: crop.id, glyphPx: m ? round(m.glyphPx, 1) : null, where: 'evidence',
        dataGlyphPx: crop.dataGlyphPx, renderScale: m ? round(m.renderScale) : null});
    }

    // scale (all decks report; v2 warns)
    const scale = {};
    for (const vp of [{width:1440,height:900},{width:1280,height:800},{width:1024,height:768},{width:860,height:760}]) {
      await fresh(page, url, vp);
      scale[`${vp.width}x${vp.height}`] = (await page.evaluate(() => window.__ck.scale())).scale;
    }
    if (v2) {
      if (!(scale['1280x800'] >= LIMIT.scale1280)) warn('C-SCALE', null, scale['1280x800'], LIMIT.scale1280, `1280×800 배율 ${scale['1280x800']} < ${LIMIT.scale1280}`);
      if (!(scale['1024x768'] >= LIMIT.scale1024)) warn('C-SCALE', null, scale['1024x768'], LIMIT.scale1024, `1024×768 배율 ${scale['1024x768']} < ${LIMIT.scale1024}`);
    }
    if (interactive) {
      for (const vp of [{width:1920,height:1080},{width:1024,height:768}]) {
        await fresh(page, url, vp);
        const measured = await page.evaluate(async () => {
          window.deckShell.present(true);
          await window.__ck.settle();
          const card = document.querySelector('.slide.on .card');
          const result = {scale: window.__ck.scale().scale, cardWidthShare: card ? card.getBoundingClientRect().width / innerWidth : null};
          window.deckShell.present(false);
          return result;
        });
        const key = `present${vp.width}x${vp.height}`;
        scale[key] = {scale: measured.scale, cardWidthShare: round(measured.cardWidthShare)};
      }
      const p1920 = scale.present1920x1080, p1024 = scale.present1024x768;
      if (!(p1920.cardWidthShare >= LIMIT.presentShare)) warn('C-PRESENT', null, p1920.cardWidthShare, LIMIT.presentShare, `1920×1080 전체화면 카드 폭 ${p1920.cardWidthShare} < ${LIMIT.presentShare}`);
      if (!(p1024.scale >= LIMIT.present1024)) warn('C-PRESENT', null, p1024.scale, LIMIT.present1024, `1024×768 전체화면 배율 ${p1024.scale} < ${LIMIT.present1024}`);
    }

    // notes access: 860×760 (mouse) and 390×844 (touch)
    const notes = [];
    await fresh(page, url, {width:860,height:760});
    notes.push(await notesAccess(page, '860x760', false));
    const touch = await browser.newContext({viewport:{width:390,height:844}, isMobile:true, hasTouch:true});
    const phonePage = await touch.newPage();
    phonePage.on('pageerror', error => errors.push(error.message));
    const phone = {scrollLengthMedian: null, cardsOver: [], keyCellsOffscreen: []};
    let progress = null;
    try {
      await fresh(phonePage, url);
      notes.push(await notesAccess(phonePage, '390x844 touch', true));
      await fresh(phonePage, url);
      const header = await phonePage.evaluate(() => {
        const top = document.querySelector('header.top');
        return top ? top.getBoundingClientRect().height : null;
      });
      progress = {viewport: '390x844', headerHeight: round(header, 1), share: header === null ? null : round(header / 844)};
      if (progress.share !== null && progress.share > LIMIT.progress) warn('C-PROGRESS', null, progress.share, LIMIT.progress, `390×844 머리줄 높이 ${Math.round(progress.share * 100)}% > 20%`);
      const screens = [];
      for (let i = 0; i < facts.total; i++) {
        const p = await phonePage.evaluate(async index => {
          window.__ck.show(index);
          await document.fonts.ready;
          await window.__ck.settle();
          return window.__ck.phone(index);
        }, i);
        screens.push(p.scrollScreens);
        density.perSlide[i].titleLines390 = p.titleLines;
        if (!p.srcVisible) failures.push(`C-SRC-HIDDEN: 390: slide ${p.slide}${p.id ? ' (' + p.id + ')' : ''} source line missing or hidden`);
        if (p.cardHeight > LIMIT.phoneCard * 844) {
          phone.cardsOver.push({slide: p.slide, id: p.id, screens: round(p.cardHeight / 844, 2)});
          warn('C-PHONE-CARD', p, round(p.cardHeight / 844, 2), LIMIT.phoneCard, `390 카드 높이 ${(p.cardHeight / 844).toFixed(2)}화면 > ${LIMIT.phoneCard}`);
        }
        if (p.keyCellsOffscreen) {
          phone.keyCellsOffscreen.push({slide: p.slide, id: p.id, count: p.keyCellsOffscreen});
          warn('C-PHONE-KEYCELL', p, p.keyCellsOffscreen, 0, `390 첫 화면 밖 핵심 칸 ${p.keyCellsOffscreen}개`);
        }
        if (p.mathHintMissing) {
          math.hintMissing.push({slide: p.slide, id: p.id, count: p.mathHintMissing});
          warn('C-MATH-HINT', p, p.mathHintMissing, 0, '390에서 넘치는 수식에 가로 스크롤 안내가 없음');
        }
      }
      phone.scrollLengthMedian = round(quantile(screens, 0.5), 2);
    } finally { await touch.close(); }
    for (const n of notes) {
      if (n.ok === false) {
        if (v2) failures.push(`C-NOTES-ACCESS: ${n.viewport}: ${n.reason}`);
        else warn('C-NOTES-ACCESS', null, null, null, `${n.viewport}: ${n.reason} (v1 덱 보고)`);
      }
    }
    // A v2 deck without any speaker script cannot pass the notes check (대본은 본편 100%).
    if (v2 && notes.length && notes.every(n => n.ok === null))
      failures.push('C-NOTES-ACCESS: no slide has speaker notes (build with --script or note fields)');

    if (v2) {
      const evidenceUrl = new URL(url);
      evidenceUrl.searchParams.set('print', 'evidence');
      evidenceUrl.hash = '';
      await page.setViewportSize({width:1440,height:900});
      await page.goto(evidenceUrl.href);
      await page.evaluate(() => document.fonts.ready);
      await page.emulateMedia({media:'print'});
      await page.pdf({path:path.join(out,'review-evidence.pdf'),preferCSSPageSize:true,printBackground:true});
      await page.emulateMedia({media:'screen'});
    }

    let deckBytes = null;
    if (!/^https?:\/\//.test(input)) {
      deckBytes = fs.statSync(path.resolve(input)).size;
      if (deckBytes > LIMIT.deckBytes) warn('C-DECK-BYTES', null, deckBytes, LIMIT.deckBytes, `파일 ${deckBytes.toLocaleString('en-US')} B > 2 MB`);
    }
    if (errors.length) failures.push(`${errors.length} browser errors`);
    const report = {views,navigation,links,brokenLocal,errors,failures,
      note:'External URLs were collected, not HTTP-validated. Screenshots require visual review.',
      shell: facts.shell, warnings, budget, density, scale, notesAccess: notes, progress, math, evidence, xref, crops,
      images, phone, deckBytes, zoom, mainEnd};
    fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify({slides:total,viewports:views.length,navigation,brokenLocal,errors,failures,
      warnings: warnings.length, density: summary, budget, scale},null,2));
    process.exitCode = failures.length || (options.strict && warnings.length) ? 1 : 0;
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
