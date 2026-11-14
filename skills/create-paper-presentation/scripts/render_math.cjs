#!/usr/bin/env node
// Build-time KaTeX renderer for build_deck.py.
// Request (stdin):  {"items":[{"id","tex","display"}],"embedFonts":true}
// Response (stdout): {"katex","items":[{"id","html"}|{"id","error"}],"css","fonts"}
// Only the fonts the rendered HTML actually uses are embedded (woff2 data URIs).
// Exit codes: 0 ok (per-item parse errors are reported in the response), 2 bad usage or request, 3 KaTeX not found.
'use strict';
const fs = require('node:fs');
const path = require('node:path');

function fail(code, message) {
  process.stderr.write('render_math: ' + message + '\n');
  process.exit(code);
}

function parseArgs(argv) {
  let katexDir = null;
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--katex') {
      katexDir = argv[++i];
      if (!katexDir) fail(2, '--katex needs a directory');
    } else if (arg.startsWith('--katex=')) {
      katexDir = arg.slice('--katex='.length);
    } else if (arg === '-h' || arg === '--help') {
      process.stdout.write('Usage: node render_math.cjs [--katex DIR] < request.json > response.json\n');
      process.exit(0);
    } else {
      fail(2, 'unknown argument ' + arg);
    }
  }
  return {katexDir};
}

// --katex DIR -> KATEX_MODULE -> require.resolve('katex/package.json') from this folder.
// The first location that is given is used; a wrong explicit location is an error, not a fallthrough.
function locateKatex(katexDir) {
  let dir, via;
  if (katexDir) { dir = katexDir; via = '--katex'; }
  else if (process.env.KATEX_MODULE) { dir = process.env.KATEX_MODULE; via = 'KATEX_MODULE'; }
  else {
    try {
      dir = path.dirname(require.resolve('katex/package.json', {paths: [__dirname]}));
      via = 'require.resolve';
    } catch (error) {
      fail(3, 'KaTeX not found: no --katex, no KATEX_MODULE, and require.resolve("katex/package.json") from ' +
        __dirname + ' failed (' + (error.code || error.message) + '). Run `npm install` in scripts/ or set KATEX_MODULE.');
    }
  }
  dir = path.resolve(dir);
  const pkgPath = path.join(dir, 'package.json');
  const jsPath = path.join(dir, 'dist', 'katex.js');
  const cssPath = path.join(dir, 'dist', 'katex.min.css');
  for (const file of [pkgPath, jsPath, cssPath]) {
    if (!fs.existsSync(file)) fail(3, `KaTeX not found via ${via}: missing ${file}`);
  }
  let pkg, katex;
  try { pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8')); } catch (error) { fail(3, `cannot read ${pkgPath}: ${error.message}`); }
  if (pkg.name !== 'katex') fail(3, `${pkgPath} is not the katex package (name: ${pkg.name})`);
  try { katex = require(jsPath); } catch (error) { fail(3, `cannot load ${jsPath}: ${error.message}`); }
  return {dir, katex, version: String(pkg.version || katex.version || ''), cssPath};
}

// ---------- CSS analysis ----------
const normWeight = value => {
  const v = String(value || '').trim().toLowerCase();
  if (v === 'bold' || v === 'bolder') return 700;
  if (v === '' || v === 'normal' || v === 'lighter') return 400;
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : 400;
};
const normStyle = value => (/italic|oblique/i.test(String(value || '')) ? 'italic' : 'normal');
const unquote = value => String(value || '').trim().replace(/^["']|["']$/g, '');

function parseFontFaces(css) {
  const faces = [];
  const re = /@font-face\{([^}]*)\}/g;
  let m;
  while ((m = re.exec(css))) {
    const body = m[1];
    const family = unquote((/font-family:([^;}]*)/.exec(body) || [])[1]);
    const weight = normWeight((/font-weight:([^;}]*)/.exec(body) || [])[1]);
    const style = normStyle((/font-style:([^;}]*)/.exec(body) || [])[1]);
    const woff2 = (/url\(([^)]*\.woff2)\)/.exec(body) || [])[1];
    const name = woff2 ? path.basename(unquote(woff2), '.woff2') : family;
    faces.push({family, weight, style, woff2: woff2 ? unquote(woff2) : null, name, key: `${family}|${weight}|${style}`});
  }
  return faces;
}

// Parse one compound selector (".a.b", "span", "span.a") into {tag, classes}; null if it uses features we do not model.
function parseCompound(text) {
  if (/[:\[#*]/.test(text)) return null;
  const tag = (/^[a-zA-Z][\w-]*/.exec(text) || [])[0] || null;
  const classes = [];
  const re = /\.([\w-]+)/g;
  let m;
  while ((m = re.exec(text))) classes.push(m[1]);
  return {tag: tag ? tag.toLowerCase() : null, classes};
}

function parseFontRules(css) {
  const rules = [];
  const re = /([^{}@]+)\{([^{}]*)\}/g;
  let m, order = 0;
  while ((m = re.exec(css))) {
    const body = m[2];
    const props = {};
    const shorthand = /(?:^|;)font:([^;}]*)/.exec(body);
    if (shorthand) {
      const value = shorthand[1];
      const fam = /KaTeX_[A-Za-z0-9]+/.exec(value);
      if (fam) props.family = fam[0];
      props.weight = /\b(bold|[5-9]00)\b/.test(value) ? 700 : 400;
      props.style = normStyle(value);
    }
    const family = /(?:^|;)font-family:([^;}]*)/.exec(body);
    if (family) props.family = unquote(family[1].split(',')[0]);
    const weight = /(?:^|;)font-weight:([^;}]*)/.exec(body);
    if (weight) props.weight = normWeight(weight[1]);
    const style = /(?:^|;)font-style:([^;}]*)/.exec(body);
    if (style) props.style = normStyle(style[1]);
    if (!('family' in props) && !('weight' in props) && !('style' in props)) continue;
    for (const raw of m[1].split(',')) {
      const selector = raw.trim();
      if (!selector) continue;
      // Tokenize into compounds and combinators (descendant ' ' or child '>').
      const tokens = selector.replace(/\s*>\s*/g, ' > ').split(/\s+/);
      const parts = [];
      let combinator = ' ', ok = true;
      for (const token of tokens) {
        if (token === '>') { combinator = '>'; continue; }
        if (token === '+' || token === '~') { ok = false; break; }
        const compound = parseCompound(token);
        if (!compound) { ok = false; break; }
        parts.push({combinator, compound});
        combinator = ' ';
      }
      if (!ok || !parts.length) continue;
      const classCount = parts.reduce((n, p) => n + p.compound.classes.length, 0);
      const tagCount = parts.reduce((n, p) => n + (p.compound.tag ? 1 : 0), 0);
      rules.push({selector, parts, props, specificity: classCount * 100 + tagCount, order: order++});
    }
  }
  rules.sort((a, b) => a.specificity - b.specificity || a.order - b.order);
  return rules;
}

const matchesCompound = (node, compound) =>
  (!compound.tag || compound.tag === node.tag) && compound.classes.every(c => node.classes.has(c));

// Right-to-left selector match against the element stack (stack[last] is the element).
function matchesSelector(stack, parts) {
  let i = stack.length - 1;
  let p = parts.length - 1;
  if (!matchesCompound(stack[i], parts[p].compound)) return false;
  while (p > 0) {
    const combinator = parts[p].combinator;
    p--;
    if (combinator === '>') {
      i--;
      if (i < 0 || !matchesCompound(stack[i], parts[p].compound)) return false;
    } else {
      i--;
      while (i >= 0 && !matchesCompound(stack[i], parts[p].compound)) i--;
      if (i < 0) return false;
    }
  }
  return true;
}

const VOID = new Set(['area', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);

// Fonts used by rendered KaTeX HTML. Two passes, unioned (over-inclusion only costs bytes):
// (1) per element: a rule whose last compound class set is contained in the element's classes uses its font
//     (family-less weight/style rules apply on top of KaTeX_Main);
// (2) cascade with inheritance for every element that carries visible text.
function usedFontKeys(htmlList, rules) {
  const keys = new Set();
  const simpleRules = rules.filter(r => r.parts[r.parts.length - 1].compound.classes.length && r.selector !== '.katex');
  for (const html of htmlList) {
    const stack = [];
    const re = /<(\/?)([a-zA-Z][\w:-]*)((?:[^>"']|"[^"]*"|'[^']*')*?)(\/?)>|([^<]+)/g;
    let m;
    while ((m = re.exec(html))) {
      if (m[5] !== undefined) {
        const top = stack[stack.length - 1];
        if (!top || top.skip || !top.font) continue;
        const text = m[5].replace(/&[a-zA-Z#0-9]+;/g, 'x');
        if (/\S/.test(text)) keys.add(`${top.font.family}|${top.font.weight}|${top.font.style}`);
        continue;
      }
      const closing = m[1] === '/';
      const tag = m[2].toLowerCase();
      if (closing) {
        for (let i = stack.length - 1; i >= 0; i--) {
          if (stack[i].tag === tag) { stack.length = i; break; }
        }
        continue;
      }
      const attrs = m[3] || '';
      const classMatch = /\bclass\s*=\s*("([^"]*)"|'([^']*)')/.exec(attrs);
      const classes = new Set(classMatch ? (classMatch[2] !== undefined ? classMatch[2] : classMatch[3]).split(/\s+/).filter(Boolean) : []);
      const parent = stack[stack.length - 1];
      const node = {tag, classes, skip: !!(parent && parent.skip), font: parent && parent.font ? {...parent.font} : null};
      if (classes.has('katex-mathml') || tag === 'svg' || tag === 'math') node.skip = true;
      if (classes.has('katex')) node.font = {family: 'KaTeX_Main', weight: 400, style: 'normal'};
      stack.push(node);
      if (node.font && !node.skip) {
        for (const rule of rules) {
          if (rule.selector === '.katex') continue;
          if (!matchesSelector(stack, rule.parts)) continue;
          if ('family' in rule.props) node.font.family = rule.props.family;
          if ('weight' in rule.props) node.font.weight = rule.props.weight;
          if ('style' in rule.props) node.font.style = rule.props.style;
        }
        for (const rule of simpleRules) {
          const last = rule.parts[rule.parts.length - 1].compound;
          if (!last.classes.every(c => classes.has(c))) continue;
          const family = rule.props.family || 'KaTeX_Main';
          const weight = 'weight' in rule.props ? rule.props.weight : 400;
          const style = 'style' in rule.props ? rule.props.style : 'normal';
          keys.add(`${family}|${weight}|${style}`);
        }
      }
      if (VOID.has(tag) || m[4] === '/') stack.pop();
    }
  }
  return keys;
}

// Map a wanted (family, weight, style) to an existing face: exact, else nearest in the same family.
function resolveFace(key, faces) {
  const exact = faces.find(f => f.key === key);
  if (exact) return exact;
  const [family, weightText, style] = key.split('|');
  const weight = Number(weightText);
  const same = faces.filter(f => f.family === family);
  if (!same.length) return null;
  const score = f => (f.style === style ? 0 : 1000) + Math.abs(f.weight - weight);
  return same.slice().sort((a, b) => score(a) - score(b) || a.name.localeCompare(b.name))[0];
}

function buildCss(css, faces, wantedKeys, version, distDir, embedFonts) {
  const used = new Set();
  const main = faces.find(f => f.key === 'KaTeX_Main|400|normal');
  if (main) used.add(main.name);
  for (const key of [...wantedKeys].sort()) {
    const face = resolveFace(key, faces);
    if (face) used.add(face.name);
  }
  const names = [...used].sort();
  let index = 0;
  const body = css.replace(/@font-face\{([^}]*)\}/g, (whole, inner) => {
    const face = faces[index++];
    if (!face || !used.has(face.name)) return '';
    if (!embedFonts || !face.woff2) return whole;
    const file = path.join(distDir, face.woff2);
    let data;
    try { data = fs.readFileSync(file).toString('base64'); } catch (error) { fail(3, `missing KaTeX font ${file}: ${error.message}`); }
    return '@font-face{' + inner.replace(/src:[^;}]*/, `src:url(data:font/woff2;base64,${data}) format("woff2")`) + '}';
  });
  return {css: `/* KaTeX ${version} · fonts: ${names.join(', ')} */\n` + body, fonts: names};
}

function main() {
  const {katexDir} = parseArgs(process.argv.slice(2));
  const {dir, katex, version, cssPath} = locateKatex(katexDir);
  let request;
  try { request = JSON.parse(fs.readFileSync(0, 'utf8') || '{}'); } catch (error) { fail(2, 'request is not JSON: ' + error.message); }
  const items = Array.isArray(request.items) ? request.items : null;
  if (!items) fail(2, 'request needs an "items" array');
  const embedFonts = request.embedFonts !== false;
  const out = [];
  const htmlList = [];
  for (const item of items) {
    const id = String(item && item.id);
    if (!item || typeof item.tex !== 'string') { out.push({id, error: 'tex must be a string'}); continue; }
    try {
      const html = katex.renderToString(item.tex, {
        displayMode: !!item.display,
        output: 'htmlAndMathml',
        throwOnError: true,
        trust: false,
        strict: code => (code === 'unicodeTextInMathMode' ? 'ignore' : 'warn'),
      });
      out.push({id, html});
      htmlList.push(html);
    } catch (error) {
      out.push({id, error: String(error && error.message || error)});
    }
  }
  const sourceCss = fs.readFileSync(cssPath, 'utf8');
  const faces = parseFontFaces(sourceCss);
  const rules = parseFontRules(sourceCss.replace(/@font-face\{[^}]*\}/g, ''));
  const wanted = usedFontKeys(htmlList, rules);
  const {css, fonts} = buildCss(sourceCss, faces, wanted, version, path.join(dir, 'dist'), embedFonts);
  process.stdout.write(JSON.stringify({katex: version, items: out, css, fonts}));
}

// KaTeX strict-mode warnings use console.warn; keep stdout for the JSON response only.
console.log = (...args) => process.stderr.write(args.join(' ') + '\n');
main();
