#!/usr/bin/env python3
"""Render reviewed slide HTML fragments into the bundled standalone shell.

A deck without "shell_version": 2 renders exactly as before (v1). With "shell_version": 2 the build adds
slide IDs, cross-references ([[2-2]] / [[@key]]), an evidence panel per slide, a compact source line,
build-time KaTeX (render_math.cjs), speaker-script merging (--script) and static lint (--lint).
Fields, syntax and codes: references/deck-json.md.

exit: 0 ok · 1 error (build, E-*, lint error; with --strict also lint warnings and the build warnings
W-MATH-UNAVAILABLE (unless --no-math), W-MATH-SKIPPED, W-IMG-MISSING, W-NOTES-MISSING) · 2 usage
"""
import argparse
import ast
import base64
import hashlib
import html
import json
import math
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from html.parser import HTMLParser
from pathlib import Path


# ---------------------------------------------------------------------------
# v1 output (unchanged: a deck without "shell_version": 2 must stay byte-identical)
# ---------------------------------------------------------------------------

def render(spec, shell):
    slides = spec.get("slides", [])
    if not slides:
        raise ValueError("slides must contain at least one reviewed slide")
    sections = []
    for index, slide in enumerate(slides, 1):
        for field in ("title", "body", "visual", "sources"):
            if not slide.get(field):
                raise ValueError(f"slide {index}: missing {field}")
        sources = []
        for source in slide["sources"]:
            sources.append('<a href="{}">{}</a>'.format(
                html.escape(source["url"], quote=True), html.escape(source["label"])))
        layout = slide.get("layout", "split")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", layout):
            raise ValueError(f"slide {index}: layout must be a CSS class name")
        section = html.escape(str(slide.get("section", "1")), quote=True)
        label = html.escape(slide.get("section_label", section), quote=True)
        nav = html.escape(re.sub(r"<[^>]*>", " ", slide["title"]), quote=True)
        classes = "inner wide" if layout == "wide" else "inner"
        sections.append(f'''<section class="slide layout-{layout}" data-sec="{section}" data-section-label="{label}" data-nav="{nav}">
<div class="card"><div class="{classes}">
<div class="txt"><div class="ey"></div><h2>{slide['title']}</h2>{slide['body']}</div>
<div class="vis">{slide['visual']}</div></div>
<footer class="src"><span>근거: {' · '.join(sources)}</span><span>{html.escape(slide.get('ids', ''))}</span></footer></div>
<aside class="speaker-notes">{html.escape(slide.get('note', ''))}</aside></section>''')
    if "<!-- SLIDES -->" not in shell:
        raise ValueError("shell is missing its slide insertion point")
    return (shell.replace("{{TITLE}}", html.escape(spec.get("title", "논문 발표")))
            .replace("{{SUBTITLE}}", html.escape(spec.get("subtitle", "검토용 초안")))
            .replace("<!-- SLIDES -->", "\n".join(sections)))


def inline_images(page, base):
    """Embed local <img src="relative/path"> files as data URIs so the HTML stays standalone."""
    def embed(match):
        src = match.group(2)
        path = base / src
        if src.startswith(("data:", "http:", "https:")) or not path.is_file():
            return match.group(0)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f'{match.group(1)}data:{mime};base64,{data}{match.group(3)}'
    return re.sub(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', embed, page)


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
SHELL_PATH = SCRIPT_DIR.parent / "assets" / "deck-shell.html"
RENDER_MATH = SCRIPT_DIR / "render_math.cjs"

V2_SLIDE_FIELDS = ("evidence", "math", "key", "id", "part", "kind", "seconds", "term", "claims", "src_visible")
PARTS = ("main", "appendix", "review")
KIND_SECONDS = {"intro": 30, "result": 50, "mechanism": 80, "summary": 20}
KEY_RE = re.compile(r"[a-z0-9][a-z0-9-]*")
MATH_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
SCRIPT_ID_RE = re.compile(r"^(\d+-\d+|A-\d+|R-\d+)\b")
SCRIPT_KEY_RE = re.compile(r"^@([a-z0-9][a-z0-9-]*)(?![a-z0-9-])")
ID_TOKEN_RE = re.compile(r"(?<![0-9A-Za-z.\-])(\d+-\d+|A-\d+|R-\d+)(?![0-9.\-%])")
XREF_RE = re.compile(r"\[\[([^\[\]|]+?)(?:\|([^\[\]]*))?\]\]")
MATH_RE = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
UPPER_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])[A-Z][A-Za-z]*[A-Z][A-Za-z]*(?![A-Za-z])")
SENTENCE_END_RE = re.compile(r"[.?!。](?=\s|$)")
INVISIBLE_RE = re.compile(r"[\s\u200b-\u200d\u2060\ufeff]+")
SENTINEL_RE = re.compile("\ue000(\\d+)\ue001")
CHIP_LABELS = {"orig": "원문", "table": "표 값", "config": "config", "calc": "계산", "est": "추정",
               "assume": "가정", "nd": "미기술", "interp": "해석", "hyp": "저자 가설", "illus": "설명용",
               "cite": "인용 원전"}
CHIP_REQUIRED = ("calc", "est", "assume", "nd", "interp", "hyp", "illus", "config", "cite")
CLAIM_LAYERS = ("main", "evidence", "notes", "appendix")
TITLE_LABEL_ENDINGS = ("전체", "개요", "결과", "정리", "요약", "소개", "목록", "비교")
DECK_BYTES_LIMIT = 2 * 1024 * 1024
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source",
             "track", "wbr"}
SKIP_TAGS = {"a", "code", "pre", "script", "style", "svg", "template"}
MATH_SKIP_TAGS = SKIP_TAGS - {"a"}   # formulas inside links are rendered; svg/code/pre/template text is not
RAW_TAGS = {"script", "style"}
STRICT_BUILD_CODES = ("W-MATH-UNAVAILABLE", "W-MATH-SKIPPED", "W-IMG-MISSING", "W-NOTES-MISSING")
PAPER_URL_RE = re.compile(r"arxiv\.org/|\.pdf(?:$|[#?])|#page=|openreview\.net/|aclanthology\.org/|doi\.org/",
                          re.I)
PAGE_MARK_RE = re.compile(r"\bpp?\.\s*\d|§|\d\s*쪽")
TOKEN_RE = re.compile(r"<!--.*?-->|<![^>]*>|<\?[^>]*>|</?[A-Za-z][^\s/>]*(?:\"[^\"]*\"|'[^']*'|[^'\">])*>", re.S)
TAG_NAME_RE = re.compile(r"<(/?)([A-Za-z][^\s/>]*)")


class BuildError(Exception):
    """Collected E-* errors; printed together, exit 1."""

    def __init__(self, errors):
        super().__init__("; ".join(f"{c}: {m}" for c, m in errors))
        self.errors = errors


WARNED = []   # (code, counts_for_strict) of build warnings printed in this run


def warn(code, message, strict=True):
    """Print a build warning. strict=False keeps a warning the user asked for (e.g. --no-math) out of --strict."""
    WARNED.append((code, strict))
    print(f"WARN {code}: {message}", file=sys.stderr)


def strip_tags(text):
    return re.sub(r"<[^>]*>", "", text or "")


def normalize_title(text):
    text = re.sub(r"<\s*(?:br|wbr)\b[^>]*>", " ", text or "", flags=re.I)
    text = html.unescape(strip_tags(text))
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip()


def title_text(title):
    """Plain title text (tags removed, entities decoded, whitespace collapsed)."""
    return re.sub(r"\s+", " ", html.unescape(strip_tags(re.sub(r"<\s*(?:br|wbr)\b[^>]*>", " ", title or "",
                                                                 flags=re.I)))).strip()


def nows(text):
    return INVISIBLE_RE.sub("", text or "")


def number_text(value):
    return ("%g" % value) if isinstance(value, float) else str(value)


# ---------------------------------------------------------------------------
# slide model, validation, IDs
# ---------------------------------------------------------------------------

class Slide:
    def __init__(self, index, raw, v2):
        self.index = index
        self.pos = index + 1
        self.raw = raw
        self.v2 = v2
        self.title = raw.get("title", "")
        self.section = str(raw.get("section", "1"))
        self.label_raw = raw.get("section_label", self.section)
        self.layout = raw.get("layout", "split")
        self.note = raw.get("note", "") or ""
        self.part = (raw.get("part") or "main") if v2 else "main"
        self.key = raw.get("key") if v2 else None
        self.kind = raw.get("kind") if v2 else None
        self.term = raw.get("term") if v2 else None
        self.claims = list(raw.get("claims") or []) if v2 else []
        self.evidence = (raw.get("evidence") or "") if v2 else ""
        self.math = (raw.get("math") or {}) if v2 else {}
        self.src_visible = raw.get("src_visible", 2) if v2 else None
        seconds = raw.get("seconds") if v2 else None
        self.seconds = seconds if seconds is not None else KIND_SECONDS.get(self.kind)
        self.id = None

    @property
    def ref(self):
        return self.id or f"s{self.pos}"

    @property
    def is_main(self):
        return self.part == "main"


def validate_and_model(spec, v2):
    """Return Slide objects; raise BuildError for invalid input (v1 checks keep the v1 messages)."""
    slides = spec.get("slides")
    if not isinstance(slides, list) or not slides:
        raise BuildError([("E-FIELD", "slides must contain at least one reviewed slide")])
    errors = []
    model = []
    for index, raw in enumerate(slides):
        if not isinstance(raw, dict):
            errors.append(("E-FIELD", f"slide {index + 1}: must be an object"))
            raw = {}
        for field in ("title", "body", "visual", "sources"):
            if not raw.get(field):
                errors.append(("E-FIELD", f"slide {index + 1}: missing {field}"))
        layout = raw.get("layout", "split")
        if not isinstance(layout, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", layout):
            errors.append(("E-FIELD", f"slide {index + 1}: layout must be a CSS class name"))
        sources = raw.get("sources") or []
        if not isinstance(sources, list) or any(not isinstance(s, dict) or not isinstance(s.get("url"), str)
                                                or not isinstance(s.get("label"), str) for s in sources):
            errors.append(("E-FIELD", f"slide {index + 1}: sources must be [{{label, url}}]"))
        model.append(Slide(index, raw, v2))
    if errors:
        raise BuildError(errors)
    if not v2:
        return model

    keys = {}
    rank_prev = 0
    for s in model:
        raw, where = s.raw, f"slide {s.pos}"
        if s.key is not None:
            if not isinstance(s.key, str) or not KEY_RE.fullmatch(s.key):
                errors.append(("E-FIELD", f"{where}: key must match ^[a-z0-9][a-z0-9-]*$ ({s.key!r})"))
            elif s.key in keys:
                errors.append(("E-FIELD", f"{where}: key '{s.key}' already used by slide {keys[s.key]}"))
            else:
                keys[s.key] = s.pos
        if s.part not in PARTS:
            errors.append(("E-FIELD", f"{where}: part must be one of {', '.join(PARTS)} ({s.part!r})"))
        else:
            rank = PARTS.index(s.part)
            if rank < rank_prev:
                errors.append(("E-PART-ORDER", f"{where}: part '{s.part}' after '{PARTS[rank_prev]}' "
                                               "(order must be main → appendix → review)"))
            rank_prev = max(rank_prev, rank)
        if s.kind is not None and s.kind not in KIND_SECONDS:
            errors.append(("E-FIELD", f"{where}: kind must be one of {', '.join(KIND_SECONDS)} ({s.kind!r})"))
        seconds = raw.get("seconds")
        if seconds is not None and (isinstance(seconds, bool) or not isinstance(seconds, int)
                                    or not 5 <= seconds <= 300):
            errors.append(("E-FIELD", f"{where}: seconds must be an integer 5–300 ({seconds!r})"))
        if s.term is not None and not isinstance(s.term, str):
            errors.append(("E-FIELD", f"{where}: term must be a string"))
        if not isinstance(raw.get("claims", []), list) or any(not isinstance(c, str) for c in s.claims):
            errors.append(("E-FIELD", f"{where}: claims must be a list of strings"))
        if not isinstance(s.evidence, str):
            errors.append(("E-FIELD", f"{where}: evidence must be an HTML string"))
        sv = s.src_visible
        if isinstance(sv, bool) or not isinstance(sv, int) or not 1 <= sv <= 2:
            errors.append(("E-FIELD", f"{where}: src_visible must be 1 or 2 ({sv!r})"))
        if not isinstance(s.math, dict):
            errors.append(("E-FIELD", f"{where}: math must be an object"))
        else:
            for name, entry in s.math.items():
                if not MATH_NAME_RE.fullmatch(str(name)):
                    errors.append(("E-MATH-REF", f"{where}: math name '{name}' must match [A-Za-z0-9][A-Za-z0-9_-]*"))
                elif not isinstance(entry, dict) or not isinstance(entry.get("tex"), str):
                    errors.append(("E-MATH-REF", f"{where}: math '{name}' needs a string tex"))
                elif ("tex_narrow" in entry and not isinstance(entry["tex_narrow"], str)) or \
                        ("display" in entry and not isinstance(entry["display"], bool)):
                    errors.append(("E-MATH-REF", f"{where}: math '{name}': tex_narrow must be a string, display a boolean"))
        for i, source in enumerate(raw.get("sources") or []):
            if "detail" in source and not isinstance(source["detail"], str):
                errors.append(("E-FIELD", f"{where}: sources[{i}].detail must be a string"))
            if not nows(source["label"]) or not source["url"].strip():
                errors.append(("E-FIELD", f"{where}: sources[{i}] needs a non-empty label and url "
                                          "(an empty label leaves the visible source line blank)"))
    budget = spec.get("budget_minutes")
    if budget is not None and (isinstance(budget, bool) or not isinstance(budget, (int, float)) or budget <= 0):
        errors.append(("E-FIELD", f"budget_minutes must be a positive number ({budget!r})"))
    for field in ("compare_pair", "claims_file"):
        if spec.get(field) is not None and not isinstance(spec[field], str):
            errors.append(("E-FIELD", f"{field} must be a string"))
    for field in ("scope_terms", "out_of_scope_terms", "known_terms"):
        value = spec.get(field)
        if value is not None and (not isinstance(value, list) or any(not isinstance(v, str) for v in value)):
            errors.append(("E-FIELD", f"{field} must be a list of strings"))
    if errors:
        raise BuildError(errors)

    assign_ids(model)
    for s in model:
        given = s.raw.get("id")
        if given is not None and given != s.id:
            errors.append(("E-ID-DRIFT", f"slide {s.pos}: id '{given}' but the automatic id is '{s.id}'"))
    if errors:
        raise BuildError(errors)
    return model


def assign_ids(model):
    order, counts, appendix, review = {}, {}, 0, 0
    for s in model:
        if s.part == "main":
            if s.section not in order:
                order[s.section] = len(order) + 1
            counts[s.section] = counts.get(s.section, 0) + 1
            s.id = f"{order[s.section]}-{counts[s.section]}"
        elif s.part == "appendix":
            appendix += 1
            s.id = f"A-{appendix}"
        else:
            review += 1
            s.id = f"R-{review}"


def ignored_v2_fields(spec):
    found = []
    for index, raw in enumerate(spec.get("slides") or [], 1):
        if isinstance(raw, dict):
            names = [f for f in V2_SLIDE_FIELDS if f in raw]
            if names:
                found.append(f"slide {index} ({', '.join(names)})")
    return found


# ---------------------------------------------------------------------------
# speaker script merge (--script)
# ---------------------------------------------------------------------------

def parse_script(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise BuildError([("E-SCRIPT", f"cannot read script {path}: {error}")])
    entries, current = [], None
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            if current:
                entries.append(current)
            current = [line[3:].strip(), number, []]
        elif line.startswith("# "):
            if current:
                entries.append(current)
            current = None
        elif current is not None:
            current[2].append(line)
    if current:
        entries.append(current)
    return [(heading, number, "\n".join(lines).strip()) for heading, number, lines in entries]


def merge_scripts(model, paths, v2, allow_missing):
    by_id = {s.id: s for s in model if s.id}
    by_key = {s.key: s for s in model if s.key}
    by_title = {}
    for s in model:
        by_title.setdefault(normalize_title(s.title), []).append(s)
    errors, matched = [], {}
    headings = orphans = 0
    for path in paths:
        for heading, number, body in parse_script(path):
            headings += 1
            where = f"{path}:{number} '## {heading}'"
            target = None
            if v2:
                id_match = SCRIPT_ID_RE.match(heading)
                key_match = SCRIPT_KEY_RE.match(heading)
                if id_match and id_match.group(1) in by_id:
                    target = by_id[id_match.group(1)]
                elif key_match and key_match.group(1) in by_key:
                    target = by_key[key_match.group(1)]
            if target is None:
                candidates = by_title.get(normalize_title(heading), [])
                if len(candidates) > 1:
                    errors.append(("E-SCRIPT", f"{where}: title matches {len(candidates)} slides "
                                               f"({', '.join(c.ref for c in candidates)}); use the slide ID"))
                    orphans += 1
                    continue
                target = candidates[0] if candidates else None
            if target is None:
                errors.append(("E-SCRIPT", f"{where}: no slide matches (ID, @key or title)"))
                orphans += 1
                continue
            if target.pos in matched:
                errors.append(("E-SCRIPT", f"{where}: slide {target.ref} already matched by {matched[target.pos][0]}"))
                continue
            matched[target.pos] = (where, body)
    for s in model:
        if s.pos in matched:
            body = matched[s.pos][1]
            if s.note and s.note != body:
                warn("W-NOTE-OVERRIDE", f"{s.ref}: JSON note differs from the script; using the script")
            s.note = body
    missing = [s for s in model if (s.is_main if v2 else True) and not s.note.strip()]
    for s in missing:
        if allow_missing:
            warn("W-SCRIPT-MISSING", f"{s.ref}: no speaker script (--allow-missing-notes)")
        else:
            errors.append(("E-SCRIPT", f"{s.ref}: no speaker script after merge "
                                       "(add a heading or pass --allow-missing-notes)"))
    print(f"script: {headings} headings · {len(matched)} matched · {orphans} orphan · {len(missing)} missing",
          file=sys.stderr)
    if errors:
        raise BuildError(errors)


# ---------------------------------------------------------------------------
# fragment transforms (text outside tags; cross-references skip a/code/pre/script/style/svg/template,
# formulas skip the same set except a)
# ---------------------------------------------------------------------------

def transform(fragment, on_text, on_tag=None, skip=SKIP_TAGS, on_skipped=None):
    """Copy tags verbatim and pass text runs to on_text. Text under a `skip` tag is copied unchanged
    (on_skipped(text, outermost skipped tag) sees it). on_tag(tag, name, fragment, end) may return
    (replacement, new_end) to replace a start tag (and what it consumes) at the top level."""
    out, pos, stack, n = [], 0, [], len(fragment)
    while pos < n:
        match = TOKEN_RE.search(fragment, pos)
        start = match.start() if match else n
        if start > pos:
            text = fragment[pos:start]
            if stack and on_skipped is not None:
                on_skipped(text, stack[0])
            out.append(text if stack else on_text(text))
        if not match:
            break
        tag, pos = match.group(0), match.end()
        name_match = TAG_NAME_RE.match(tag)
        if not name_match:
            out.append(tag)
            continue
        closing, name = name_match.group(1) == "/", name_match.group(2).lower()
        self_closing = tag.endswith("/>")
        if not closing and not stack and on_tag is not None:
            replaced = on_tag(tag, name, fragment, pos)
            if replaced is not None:
                out.append(replaced[0])
                pos = replaced[1]
                continue
        out.append(tag)
        if name in RAW_TAGS and not closing and not self_closing:
            end = re.compile(r"</%s\s*>" % name, re.I).search(fragment, pos)
            stop = end.end() if end else n
            out.append(fragment[pos:stop])
            pos = stop
            continue
        if closing:
            if stack and stack[-1] == name:
                stack.pop()
        elif self_closing or name in VOID_TAGS:
            continue
        elif stack:
            if name == stack[-1]:
                stack.append(name)
        elif name in skip:
            stack.append(name)
    return "".join(out)


def resolve_ref(target, by_id, by_key):
    target = target.strip()
    if target.startswith("@"):
        return by_key.get(target[1:])
    return by_id.get(target)


def xref_html(fragment, owner, by_id, by_key, errors):
    def on_text(text):
        def repl(match):
            target = resolve_ref(match.group(1), by_id, by_key)
            if target is None:
                errors.append(("E-XREF", f"{owner.ref}: [[{match.group(0)[2:-2]}]] has no target"))
                return match.group(0)
            nav = html.escape(re.sub(r"<[^>]*>", " ", target.title), quote=True)
            label = (match.group(2) or "").strip()
            text_out = f"{label} ({target.id})" if label else target.id
            return (f'<a class="xref" href="#s{target.pos}" data-ref="{target.id}" '
                    f'title="{nav}">{text_out}</a>')
        return XREF_RE.sub(repl, text)
    return transform(fragment, on_text)


def xref_note(note, owner, by_id, by_key, errors):
    def repl(match):
        target = resolve_ref(match.group(1), by_id, by_key)
        if target is None:
            errors.append(("E-XREF", f"{owner.ref} (note): [[{match.group(0)[2:-2]}]] has no target"))
            return match.group(0)
        label = (match.group(2) or "").strip()
        return f"{label}({target.id})" if label else target.id
    return XREF_RE.sub(repl, note)


# ---------------------------------------------------------------------------
# math (KaTeX via render_math.cjs)
# ---------------------------------------------------------------------------

class MathJob:
    """Collects delimiters and placeholders as sentinels, renders once, then substitutes markup."""

    def __init__(self):
        self.occurrences = []   # dicts: kind, slide, name, tex, ids
        self.requests = []      # render_math items (unique ids)
        self.request_ids = set()
        self.owners = {}        # request id -> slide ref (for E-MATH-TEX)
        self.errors = []
        self.skipped = {}       # (slide ref, tag) -> first snippet of TeX left unrendered (W-MATH-SKIPPED)

    def _request(self, item_id, tex, display, slide):
        if item_id not in self.request_ids:
            self.request_ids.add(item_id)
            self.owners[item_id] = slide.ref
            self.requests.append({"id": item_id, "tex": tex, "display": display})

    def collect(self, fragment, slide, counters):
        if "\ue000" in fragment or "\ue001" in fragment:
            self.errors.append(("E-MATH-TEX", f"{slide.ref}: private-use characters U+E000/U+E001 are reserved"))
            return fragment

        def on_text(text):
            def repl(match):
                display = match.group(2) is not None
                tex = html.unescape(match.group(2) if display else match.group(1))
                key = "d" if display else "i"
                item_id = f"s{slide.pos}:{key}{counters[key]}"
                counters[key] += 1
                self._request(item_id, tex, display, slide)
                self.occurrences.append({"kind": "block" if display else "inline", "slide": slide,
                                         "tex": tex, "id": item_id})
                return f"\ue000{len(self.occurrences) - 1}\ue001"
            result = MATH_RE.sub(repl, text)
            leftover = re.sub("\ue000\\d+\ue001", "", result)
            if re.search(r"\\[\(\)\[\]]", leftover):
                snippet = re.search(r"\\[\(\)\[\]].{0,30}", leftover, re.S).group(0)
                self.errors.append(("E-MATH-TEX", f"{slide.ref}: unmatched math delimiter near '{snippet}' "
                                                  "(a formula must not cross a tag)"))
            return result

        def on_tag(tag, name, frag, end):
            if name not in ("span", "div"):
                return None
            attr = re.search(r'\sdata-math\s*=\s*("([^"]*)"|\'([^\']*)\')', tag)
            if not attr:
                return None
            close = re.compile(r"\s*</%s\s*>" % name, re.I).match(frag, end)
            mname = html.unescape(attr.group(2) if attr.group(2) is not None else attr.group(3))
            if not close:
                self.errors.append(("E-MATH-REF", f"{slide.ref}: placeholder data-math=\"{mname}\" must be empty"))
                return None
            entry = slide.math.get(mname) if isinstance(slide.math, dict) else None
            if entry is None:
                self.errors.append(("E-MATH-REF", f"{slide.ref}: data-math=\"{mname}\" has no entry in the slide's math"))
                return tag + frag[end:close.end()], close.end()
            display = entry.get("display", True)
            item_id = f"s{slide.pos}:m:{mname}"
            self._request(item_id, entry["tex"], display, slide)
            narrow_id = None
            if display and entry.get("tex_narrow"):
                narrow_id = item_id + ":narrow"
                self._request(narrow_id, entry["tex_narrow"], True, slide)
            self.occurrences.append({"kind": "placeholder", "slide": slide, "name": mname, "tex": entry["tex"],
                                     "display": display, "id": item_id, "narrow": narrow_id})
            return f"\ue000{len(self.occurrences) - 1}\ue001", close.end()

        def on_skipped(text, tag):
            found = MATH_RE.search(text) or re.search(r"\\[\(\[]", text)
            if found and (slide.ref, tag) not in self.skipped:
                self.skipped[(slide.ref, tag)] = re.sub(r"\s+", " ", text[found.start():found.start() + 40])

        return transform(fragment, on_text, on_tag, skip=MATH_SKIP_TAGS, on_skipped=on_skipped)

    def render(self, args):
        """Return (results by id or None if unavailable, css or None).
        Falls back to TeX source (W-MATH-UNAVAILABLE) only when math is off or not available: --no-math, no node,
        node cannot be started (OSError), or render_math exit 3 (KaTeX not found). Any other failure of the
        renderer (crash, bad request, wrong binary, invalid JSON) is the build error E-MATH-RENDER."""
        if not self.requests:
            return {}, None
        fallback = "formulas are shown as TeX source"
        if args.no_math:
            warn("W-MATH-UNAVAILABLE", f"--no-math: {fallback}", strict=False)
            return None, None
        node = args.node or os.environ.get("NODE_BIN") or shutil.which("node")
        if not node:
            warn("W-MATH-UNAVAILABLE", f"node not found (--node, NODE_BIN, PATH); {fallback}")
            return None, None
        command = [node, str(RENDER_MATH)]
        if args.katex:
            command += ["--katex", str(Path(args.katex).resolve())]
        request = json.dumps({"items": self.requests, "embedFonts": True}, ensure_ascii=False)
        try:
            proc = subprocess.run(command, input=request.encode("utf-8"), stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        except OSError as error:
            warn("W-MATH-UNAVAILABLE", f"cannot run {node}: {error}; {fallback}")
            return None, None
        stderr = proc.stderr.decode("utf-8", "replace").strip()
        last = stderr.splitlines()[-1] if stderr else "no stderr"
        if proc.returncode == 3:
            warn("W-MATH-UNAVAILABLE", f"{last}; {fallback}")
            return None, None
        if proc.returncode != 0:
            raise BuildError([("E-MATH-RENDER", f"{node} {RENDER_MATH.name} exited {proc.returncode}: {last}")])
        if stderr:
            print(stderr, file=sys.stderr)
        try:
            response = json.loads(proc.stdout.decode("utf-8"))
            results = {item["id"]: item for item in response["items"]}
        except (ValueError, KeyError, TypeError) as error:
            raise BuildError([("E-MATH-RENDER", f"{node} {RENDER_MATH.name} returned invalid JSON ({error}); "
                                                f"stderr: {last}")])
        for request_item in self.requests:
            result = results.get(request_item["id"])
            if result is None or "error" in result or "html" not in result:
                message = (result or {}).get("error", "no result")
                self.errors.append(("E-MATH-TEX", f"{self.owners[request_item['id']]} [{request_item['id']}] "
                                                  f"{message} — TeX: {request_item['tex']}"))
        return results, response.get("css")

    def markup(self, results):
        """Markup for every occurrence; results None means KaTeX unavailable (fallback)."""
        out, rendered = [], 0
        for occ in self.occurrences:
            if results is None:
                esc = html.escape(occ["tex"], quote=True)
                code = f'<code class="math-fallback" data-tex="{esc}">{esc}</code>'
                if occ["kind"] == "inline":
                    out.append(code)
                elif occ["kind"] == "block":
                    out.append(f'<span class="math-block">{code}</span>')
                elif occ["display"]:
                    out.append(f'<span class="math-block" data-math="{html.escape(occ["name"], quote=True)}">{code}</span>')
                else:
                    out.append(code)
                continue
            body = results[occ["id"]]["html"]
            rendered += 1
            if occ["kind"] == "inline":
                out.append(f'<span class="math-inline">{body}</span>')
            elif occ["kind"] == "block":
                out.append(f'<span class="math-block">{body}</span>')
            else:
                name = html.escape(occ["name"], quote=True)
                if not occ["display"]:
                    out.append(f'<span class="math-inline" data-math="{name}">{body}</span>')
                elif occ["narrow"]:
                    narrow = results[occ["narrow"]]["html"]
                    out.append(f'<span class="math-block" data-math="{name}" data-has-narrow><span class="math-wide">'
                               f'{body}</span><template class="math-narrow">{narrow}</template></span>')
                else:
                    out.append(f'<span class="math-block" data-math="{name}">{body}</span>')
        return out, rendered


# ---------------------------------------------------------------------------
# v2 render
# ---------------------------------------------------------------------------

def source_link(source):
    return '<a href="{}">{}</a>'.format(html.escape(source["url"], quote=True), html.escape(source["label"]))


def render_slide_v2(s, frags, main_end):
    sources = s.raw["sources"]
    visible = min(s.src_visible, len(sources))
    more = len(sources) - visible
    has_panel = bool(frags["evidence"]) or more > 0
    if not has_panel:
        visible, more = len(sources), 0
    section = html.escape(s.section, quote=True)
    label = html.escape(str(s.label_raw), quote=True)
    nav = html.escape(re.sub(r"<[^>]*>", " ", s.title), quote=True)
    sid = html.escape(s.id, quote=True)
    inner = "inner wide" if s.layout == "wide" else "inner"
    classes = (" has-ev" if has_panel else "") + (" is-main-end" if main_end else "")
    extra = ""
    if s.kind:
        extra += f' data-kind="{html.escape(s.kind, quote=True)}"'
    if s.seconds is not None:
        extra += f' data-seconds="{s.seconds}"'
    if s.term:
        extra += f' data-term="{html.escape(s.term, quote=True)}"'
    if s.key:
        extra += f' data-key="{html.escape(s.key, quote=True)}"'
    if s.claims:
        extra += f' data-claims="{html.escape(" ".join(s.claims), quote=True)}"'
    links = " · ".join(source_link(src) for src in sources[:visible])
    more_btn = (f' <button class="src-more" type="button" aria-expanded="false" aria-controls="ev-s{s.pos}">'
                f'+{more}</button>'
                if more > 0 else "")
    ids = s.raw.get("ids", "")
    side = ((f'<span class="src-ids">{html.escape(ids)}</span>' if ids else "")
            + ('<span class="main-end">본편 끝</span>' if main_end else "")
            + (f'<button class="ev-btn" type="button" aria-expanded="false" aria-controls="ev-s{s.pos}">'
               '근거 펼치기 <kbd>E</kbd></button>' if has_panel else ""))
    panel = ""
    if has_panel:
        items = []
        for src in sources:
            detail = src.get("detail")
            items.append(f'<li>{source_link(src)}{" — " + html.escape(detail) if detail else ""}</li>')
        ev_body = f'<div class="ev-body">{frags["evidence"]}</div>\n' if frags["evidence"] else ""
        panel = (f'<aside class="evidence" id="ev-s{s.pos}" tabindex="-1" aria-label="근거 · {sid}" hidden>\n'
                 f'<div class="ev-head"><strong>근거 · {sid}</strong><button class="ev-close" type="button" '
                 f'aria-label="근거 닫기">닫기 <kbd>Esc</kbd></button></div>\n'
                 f'{ev_body}'
                 f'<div class="ev-sources"><strong>출처 전체</strong><ol>{"".join(items)}</ol></div></aside>\n')
    return (f'<section class="slide layout-{s.layout}{classes}" data-sec="{section}" data-section-label="{label}" '
            f'data-nav="{nav}" data-id="{sid}" data-part="{html.escape(s.part, quote=True)}"{extra}>\n'
            f'<div class="card"><div class="{inner}">\n'
            f'<div class="txt"><div class="ey"><span class="sid">{sid}</span> · {label}</div>'
            f'<h2>{s.title}</h2>{frags["body"]}</div>\n'
            f'<div class="vis">{frags["visual"]}</div></div>\n'
            f'<footer class="src"><span class="src-line">근거: {links}{more_btn}</span>'
            f'<span class="src-side">{side}</span></footer></div>\n'
            f'{panel}<aside class="speaker-notes">{html.escape(s.note)}</aside></section>')


def prepare_v2(model):
    """Resolve cross-references and collect formulas (no Node needed). Returns (fragments, MathJob);
    raises BuildError for E-XREF / E-MATH-REF / unmatched delimiters. Notes get plain-text references."""
    by_id = {s.id: s for s in model}
    by_key = {s.key: s for s in model if s.key}
    errors = []
    frags = {}
    for s in model:
        frags[s.pos] = {field: xref_html(field_value, s, by_id, by_key, errors)
                        for field, field_value in (("body", s.raw["body"]), ("visual", s.raw["visual"]),
                                                   ("evidence", s.evidence))}
        s.note = xref_note(s.note, s, by_id, by_key, errors)
    if errors:
        raise BuildError(errors)
    job = MathJob()
    for s in model:
        counters = {"i": 0, "d": 0}
        for field in ("body", "visual", "evidence"):
            frags[s.pos][field] = job.collect(frags[s.pos][field], s, counters)
    if job.errors:
        raise BuildError(job.errors)
    for (ref, tag), snippet in job.skipped.items():
        hint = ("SVG text cannot hold KaTeX: put the formula next to the SVG or write the label as plain text"
                if tag == "svg" else "move the formula out of the element if it should be typeset")
        warn("W-MATH-SKIPPED", f"{ref}: math inside <{tag}> stays TeX source near '{snippet}' ({hint})")
    return frags, job


def render_v2(spec, model, prepared, shell, args):
    """Return (page, math_rendered, math_total). Raises BuildError for E-MATH-TEX."""
    frags, job = prepared
    results, css = job.render(args)
    if job.errors:
        raise BuildError(job.errors)
    markup, rendered = job.markup(results)
    for s in model:
        for field in ("body", "visual", "evidence"):
            frags[s.pos][field] = SENTINEL_RE.sub(lambda m: markup[int(m.group(1))], frags[s.pos][field])
    has_back = any(not s.is_main for s in model)
    mains = [s for s in model if s.is_main]
    last_main = mains[-1].pos if (mains and has_back) else None
    sections = [render_slide_v2(s, frags[s.pos], s.pos == last_main) for s in model]
    if "<!-- SLIDES -->" not in shell:
        raise ValueError("shell is missing its slide insertion point")
    if '<html lang="ko">' not in shell:
        raise ValueError('shell is missing <html lang="ko">')
    page = (shell.replace("{{TITLE}}", html.escape(spec.get("title", "논문 발표")))
            .replace("{{SUBTITLE}}", html.escape(spec.get("subtitle", "검토용 초안")))
            .replace("<!-- SLIDES -->", "\n".join(sections)))
    budget = spec.get("budget_minutes")
    html_attrs = ' data-shell="2"' + (f' data-budget-min="{number_text(budget)}"' if budget is not None else "")
    page = page.replace('<html lang="ko">', f'<html lang="ko"{html_attrs}>', 1)
    if rendered and css:
        page = page.replace("</head>", f'<style id="katex-css">{css}</style>\n</head>', 1)
    return page, rendered, len(job.occurrences)


# ---------------------------------------------------------------------------
# images (missing files, --resize-images)
# ---------------------------------------------------------------------------

IMG_SRC_RE = re.compile(r'<img\b[^>]*?\bsrc\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.I)


def report_missing_images(model, base):
    """W-IMG-MISSING for every local <img src> (body · visual · evidence) whose file does not exist.
    Output is unchanged: such an <img> stays a broken relative link (inline_images cannot embed it)."""
    seen = set()
    for s in model:
        for field in ("body", "visual", "evidence"):
            fragment = s.evidence if field == "evidence" else s.raw.get(field, "")
            for match in IMG_SRC_RE.finditer(fragment or ""):
                src = html.unescape(match.group(1) if match.group(1) is not None else match.group(2)).strip()
                if not src or re.match(r"(?i)^(?:[a-z][a-z0-9+.-]*:|//)", src):
                    continue
                path = base / re.split(r"[?#]", src, 1)[0]
                if (s.ref, src) not in seen and not path.is_file():
                    seen.add((s.ref, src))
                    warn("W-IMG-MISSING", f"{s.ref} ({field}): <img src=\"{src}\"> — no file {path}")


def image_width(data):
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return int.from_bytes(data[16:20], "big")
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = int.from_bytes(data[i + 2:i + 4], "big")
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                return int.from_bytes(data[i + 7:i + 9], "big")
            i += 2 + length
    return None


def resize_image(path, width):
    """Return resized bytes, or None (with W-IMG-RESIZE) when no resizer is available."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / ("resized" + path.suffix.lower())
        try:
            from PIL import Image  # optional
            with Image.open(path) as image:
                height = max(1, round(image.height * width / image.width))
                image.resize((width, height), Image.LANCZOS).save(target)
            return target.read_bytes()
        except ImportError:
            pass
        sips = shutil.which("sips")
        if sips:
            proc = subprocess.run([sips, "--resampleWidth", str(width), str(path), "--out", str(target)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0 and target.is_file():
                return target.read_bytes()
        warn("W-IMG-RESIZE", f"{path}: no Pillow or sips; embedding the original")
        return None


def resize_images(page, base):
    def embed(match):
        tag = match.group(0)
        src_match = re.search(r'\bsrc="([^"]+)"', tag)
        width_match = re.search(r'\bdata-display-width="(\d+)"', tag)
        if not src_match or not width_match:
            return tag
        src = src_match.group(1)
        path = base / src
        if src.startswith(("data:", "http:", "https:")) or not path.is_file():
            return tag
        mime = mimetypes.guess_type(path.name)[0]
        if mime not in ("image/png", "image/jpeg"):
            return tag
        target = 2 * int(width_match.group(1))
        width = image_width(path.read_bytes())
        if not width or width <= target:
            return tag
        data = resize_image(path, target)
        if data is None:
            return tag
        uri = f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
        tag = tag[:src_match.start(1)] + uri + tag[src_match.end(1):]
        # data-glyph-px describes the embedded PNG; keep it true after downscaling.
        glyph = re.search(r'\bdata-glyph-px="([0-9.]+)"', tag)
        if glyph:
            scaled = "%g" % round(float(glyph.group(1)) * target / width, 1)
            tag = tag[:glyph.start(1)] + scaled + tag[glyph.end(1):]
        return tag
    return re.sub(r"<img\b[^>]*>", embed, page)


# ---------------------------------------------------------------------------
# static lint (--lint)
# ---------------------------------------------------------------------------

class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.children, self.parent = tag, attrs, [], parent

    @property
    def classes(self):
        return set(self.attrs.get("class", "").split())

    def iter(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.iter()

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur)
        self.cur.children.append(node)
        if tag not in VOID_TAGS:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur))

    def handle_endtag(self, tag):
        node = self.cur
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.cur = node.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse_fragment(text):
    builder = TreeBuilder()
    builder.feed(text or "")
    builder.close()
    return builder.root


def simplify_tex(tex):
    text = re.sub(r"\\(?:text|mathrm|mathbf|operatorname|mathit)\s*\{([^{}]*)\}", r"\1", tex)
    text = re.sub(r"\\[A-Za-z]+", "", text)
    return re.sub(r"[{}^_&\\$~]", "", text)


ALWAYS_SKIP = {"script", "style", "template"}
# Prose leaves out titles, tables, figures, formulas and the claim-table furniture (legend, verdict, captions);
# all of it still counts as visible text. Mirrors PROSE_EXCL in check_deck.cjs.
PROSE_SKIP_TAGS = {"table", "svg", "h2", "figcaption"}
PROSE_SKIP_CLASSES = {"ev-chip", "tag", "num", "pf-grid", "fx-bars", "fx-terms", "dv-eq", "katex", "math-inline",
                      "math-block", "claim-legend", "verdict", "cap"}


def is_caption(node):
    return node.tag == "figcaption" or "cap" in node.classes


def drop_omission(text):
    """Caption segments ('원문 · … / 생략: … / …') without the '생략' part: omitted source columns keep their
    original names and are not terms the talk uses (L-DEFINE-FIRST)."""
    return " / ".join(seg for seg in text.split("/") if not seg.strip().startswith("생략"))


def is_prose_excluded(node):
    return (node.tag in PROSE_SKIP_TAGS or node.attrs.get("role") == "img"
            or bool(node.classes & PROSE_SKIP_CLASSES) or "data-math" in node.attrs)


def collect_text(node, math_entries, mode, exclude=None, sep=" "):
    """mode: 'visible' (math simplified), 'prose' (math and non-prose elements dropped),
    'plain' (math dropped, for token scans)."""
    parts = []

    def walk(current):
        for child in current.children:
            if isinstance(child, Node):
                if child.tag in ALWAYS_SKIP or (exclude and exclude(child)):
                    continue
                if mode == "prose" and is_prose_excluded(child):
                    continue
                name = child.attrs.get("data-math")
                if name is not None and mode == "visible":
                    entry = math_entries.get(name) if isinstance(math_entries, dict) else None
                    if isinstance(entry, dict) and isinstance(entry.get("tex"), str):
                        parts.append(simplify_tex(entry["tex"]))
                walk(child)
            else:
                pieces, last = [], 0
                for match in MATH_RE.finditer(child):
                    pieces.append(child[last:match.start()])
                    if mode == "visible":
                        pieces.append(simplify_tex(match.group(1) if match.group(1) is not None else match.group(2)))
                    last = match.end()
                pieces.append(child[last:])
                parts.append("".join(pieces))
    walk(node)
    return sep.join(parts)


def find_all(roots, predicate):
    for root in roots:
        for node in root.iter():
            if predicate(node):
                yield node


def has_class(name):
    return lambda node: name in node.classes


def count_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    count = len(SENTENCE_END_RE.findall(text))
    if not count and len(nows(text)) >= 25 and re.search(r"[다요까]$", text):
        count = 1
    return count


def outermost(nodes):
    chosen = set(id(n) for n in nodes)
    return [n for n in nodes if not any(id(a) in chosen for a in n.ancestors())]


class LintSlide:
    def __init__(self, s):
        self.s = s
        strip = lambda text: XREF_RE.sub("", text or "")
        self.title_plain = title_text(XREF_RE.sub("", s.title))
        self.body = parse_fragment(strip(s.raw.get("body", "")))
        self.visual = parse_fragment(strip(s.raw.get("visual", "")))
        self.evidence = parse_fragment(strip(s.evidence))
        self.screen = [self.body, self.visual]
        math_entries = s.math
        self.visible_text = " ".join([self.title_plain] + [collect_text(r, math_entries, "visible")
                                                           for r in self.screen])
        self.visible_chars = len(nows(self.visible_text))
        self.prose_chars = len(nows(" ".join(collect_text(r, math_entries, "prose") for r in self.screen)))
        captions = outermost(list(find_all(self.screen, is_caption)))
        self.define_text = " ".join([self.title_plain] + [
            collect_text(r, math_entries, "plain", exclude=is_caption) for r in self.screen] + [
            drop_omission(collect_text(c, math_entries, "plain", sep="")) for c in captions])
        self.evidence_text = collect_text(self.evidence, math_entries, "visible")
        self.unlinked_text = " ".join([self.title_plain] + [
            collect_text(r, math_entries, "visible", exclude=lambda n: n.tag == "a") for r in self.screen])
        self.chips = [(n.attrs.get("data-ev", ""), re.sub(r"\s+", " ", collect_text(n, {}, "plain", sep="")).strip())
                      for n in find_all(self.screen, has_class("ev-chip"))]
        self.ev_chips = [(n.attrs.get("data-ev", ""), re.sub(r"\s+", " ", collect_text(n, {}, "plain", sep="")).strip())
                         for n in find_all([self.evidence], has_class("ev-chip"))]
        self.dfns = [re.sub(r"\s+", " ", collect_text(n, {}, "plain", sep="")).strip()
                     for n in find_all(self.screen, lambda n: n.tag == "dfn")]

    def any_screen(self, predicate):
        return any(True for _ in find_all(self.screen, predicate))

    def any_evidence(self, predicate):
        return any(True for _ in find_all([self.evidence], predicate))

    def has_chip(self, kind, where):
        label = CHIP_LABELS.get(kind)
        chips = self.chips if where == "screen" else self.ev_chips
        return any(ev == kind or text == label for ev, text in chips)

    def term_title(self):
        term = self.s.term
        return bool(term) and re.match(re.escape(term) + r"\s*:", self.title_plain) is not None


def budget_numbers(minutes):
    lo = int(math.floor(0.8 * minutes + 0.5 + 1e-9))
    hi = int(math.floor(1.05 * minutes + 1e-9))
    cap = int(math.floor(1.2 * minutes + 1e-9))
    return lo, hi, cap


class Lint:
    def __init__(self):
        self.findings = []

    def add(self, severity, code, slide, message, value=None, limit=None):
        self.findings.append({"severity": severity, "code": code, "slide": slide.pos if slide else None,
                              "id": slide.id if slide else None, "message": message, "value": value,
                              "limit": limit, "_ref": slide.ref if slide else "-"})

    def emit(self, json_path):
        for f in self.findings:
            print(f"LINT {f['severity']} {f['code']} {f['_ref']} {f['message']}", file=sys.stderr)
        if json_path:
            rows = [{k: f[k] for k in ("severity", "code", "slide", "id", "message", "value", "limit")}
                    for f in self.findings]
            Path(json_path).parent.mkdir(parents=True, exist_ok=True)
            Path(json_path).write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        counts = {sev: sum(1 for f in self.findings if f["severity"] == sev) for sev in ("error", "warn", "info")}
        print(f"lint: {counts['error']} error · {counts['warn']} warn · {counts['info']} info", file=sys.stderr)
        return counts


def eval_expr(expr):
    if not isinstance(expr, str) or not expr.strip() or not re.fullmatch(r"[0-9+\-*/(). \t]+", expr):
        raise ValueError("only digits, + - * / ( ) . and spaces are allowed")
    tree = ast.parse(expr, mode="eval")

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            return left / right
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = ev(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("unsupported expression")
    return ev(tree)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def load_claims(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise BuildError([("E-CLAIMS", f"cannot read claim ledger {path}: {error}")])
    claims = data.get("claims") if isinstance(data, dict) else None
    if not isinstance(claims, list):
        raise BuildError([("E-CLAIMS", f"{path}: needs a \"claims\" list")])
    errors, seen = [], set()
    for i, claim in enumerate(claims):
        cid = claim.get("id") if isinstance(claim, dict) else None
        if not isinstance(cid, str) or not KEY_RE.fullmatch(cid):
            errors.append(("E-CLAIMS", f"{path}: claims[{i}].id must match ^[a-z0-9][a-z0-9-]*$"))
        elif cid in seen:
            errors.append(("E-CLAIMS", f"{path}: duplicate claim id '{cid}'"))
        else:
            seen.add(cid)
    if errors:
        raise BuildError(errors)
    return claims


def run_lint(spec, model, v2, claims, deck_dir):
    lint = Lint()
    slides = [LintSlide(s) for s in model]
    mains = [ls for ls in slides if ls.s.is_main]
    budget = spec.get("budget_minutes")
    has_panel = {ls.s.pos: bool(ls.s.evidence) or len(ls.s.raw["sources"]) > (ls.s.src_visible or 99)
                 for ls in slides}

    # deck budget
    if is_number(budget) and budget > 0:
        lo, hi, cap = budget_numbers(budget)
        n = len(mains)
        if not lo <= n <= hi:
            extra = " · 상한 초과" if n > cap else ""
            lint.add("warn", "L-BUDGET-SLIDES", None, f"본편 {n}장, 목표 {lo}–{hi}장 · 상한 {cap}장 "
                                                       f"({number_text(budget)}분){extra}", n, [lo, hi])
        if any(ls.s.kind for ls in mains):
            intro = [ls for ls in mains if ls.s.kind == "intro"]
        else:
            first = mains[0].s.section if mains else None
            intro = [ls for ls in mains if ls.s.section == first]
        if len(intro) > 3:
            lint.add("warn", "L-BUDGET-INTRO", None, f"들어가며 {len(intro)}장 > 3장", len(intro), 3)
        planned = sum(ls.s.seconds or 0 for ls in mains)
        if planned > budget * 60:
            lint.add("warn", "L-BUDGET-TIME", None, f"본편 설명 시간 합 {planned}초 > {number_text(budget)}분",
                     planned, budget * 60)
        notes_chars = sum(len(nows(ls.s.note)) for ls in mains)
        if notes_chars / 300 > budget:
            lint.add("warn", "L-NOTES-MINUTES", None, f"본편 대본 {notes_chars}자 ÷ 300 = "
                                                       f"{notes_chars / 300:.1f}분 > {number_text(budget)}분",
                     round(notes_chars / 300, 2), budget)

    ids = {s.id for s in model if s.id}
    for ls in slides:
        s = ls.s
        if s.is_main:
            if ls.visible_chars > 550:
                lint.add("info", "L-DENSITY-VISIBLE", s, f"화면 글 추정 {ls.visible_chars}자 > 550",
                         ls.visible_chars, 550)
            if ls.prose_chars > 200:
                lint.add("info", "L-DENSITY-PROSE", s, f"산문 추정 {ls.prose_chars}자 > 200", ls.prose_chars, 200)
            sentences = sum(count_sentences(collect_text(n, s.math, "visible", sep=""))
                            for n in outermost(list(find_all([ls.body], lambda n: n.tag in ("p", "li")))))
            if sentences > 3:
                lint.add("warn", "L-SENTENCES", s, f"본문 문장 {sentences}개 > 3", sentences, 3)
            if v2 and not s.note.strip():
                lint.add("warn", "L-NOTES-MISSING", s, "본편 장에 대본이 없음")
            if v2 and s.kind in ("result", "mechanism") and not s.evidence:
                lint.add("warn", "L-EVIDENCE-MISSING", s, f"kind {s.kind} 장에 evidence 없음")
        screen = nows(ls.visible_text)
        note = nows(s.note)
        if note and len(screen) >= 8:
            grams = {screen[i:i + 8] for i in range(len(screen) - 7)}
            ratio = sum(1 for g in grams if g in note) / len(grams)
            if ratio > 0.6:
                lint.add("warn", "L-NOTES-COPY", s, f"화면 글 8글자 조각의 {ratio:.0%}가 대본에도 있음",
                         round(ratio, 3), 0.6)
        if s.seconds and note:
            spoken = len(note) / 300 * 60
            if spoken > 1.5 * s.seconds:
                lint.add("info", "L-NOTES-LONG", s, f"대본 {len(note)}자 ≈ {spoken:.0f}초 > 1.5 × {s.seconds}초",
                         round(spoken), 1.5 * s.seconds)
        if re.search(r"<\s*br\b", s.title, re.I):
            lint.add("warn", "L-TITLE-BR", s, "제목에 <br> — <wbr>이나 자연 줄바꿈을 쓴다")
        if s.term:
            head = ls.title_plain.split(":", 1)[0] if ":" in ls.title_plain else ""
            position = ls.title_plain.casefold().find(s.term.casefold())
            if not (s.term.casefold() in head.casefold() or 0 <= position < 12):
                lint.add("warn", "L-TITLE-TERM", s, f"term '{s.term}'이 제목 첫 콜론 앞 · 첫 12자 안에 없음")
        claim_part = ls.title_plain.split(":", 1)[1].strip() if ":" in ls.title_plain else ""
        bare = re.sub(r"[\s.!?…·]+$", "", ls.title_plain)
        if not claim_part and (len(ls.title_plain.split()) <= 3 or bare.endswith(TITLE_LABEL_ENDINGS)):
            lint.add("warn", "L-TITLE-LABEL", s, f"라벨형 제목 '{ls.title_plain}' — 콜론 뒤에 주장을 쓴다")
        if re.search(r"\\[\(\[]", s.title):
            lint.add("warn", "L-TITLE-MATH", s, "제목에 수식 구분자")
        repeated = {}
        for ev, text in ls.chips:
            label = text or CHIP_LABELS.get(ev, ev)
            repeated[label] = repeated.get(label, 0) + 1
        for label, count in sorted(repeated.items()):
            if count >= 3:
                lint.add("warn", "L-CHIP-REPEAT", s, f"표지 '{label}' {count}번", count, 2)
        if "#c-" in ls.visible_text or "#page=" in ls.visible_text:
            lint.add("warn", "L-RAW-ANCHOR", s, "화면 글에 원시 앵커(#c- · #page=)")
        sources = s.raw["sources"]
        shown = min(s.src_visible, len(sources)) if (v2 and has_panel[s.pos]) else len(sources)
        for src in sources[:shown]:
            if (PAPER_URL_RE.search(src["url"]) and "config" not in src["label"].casefold()
                    and not PAGE_MARK_RE.search(src["label"])):
                lint.add("warn", "L-SRC-PAGE", s, f"화면 출처 '{src['label']}'에 쪽(p.N) · 절(§) 표시가 없음")
        if v2:
            tokens = sorted({t for t in ID_TOKEN_RE.findall(ls.unlinked_text) if t in ids})
            if tokens:
                lint.add("warn", "L-UNLINKED-REF", s, f"링크 없는 장 번호 {', '.join(tokens)} — [[…]]로 쓴다")
        calc_screen = ls.any_screen(has_class("factor")) or ls.any_screen(lambda n: n.attrs.get("data-ev") == "calc")
        if calc_screen:
            shown = (ls.any_screen(has_class("subst")) or ls.any_screen(has_class("derive"))
                     or ls.any_evidence(has_class("subst")) or ls.any_evidence(has_class("derive")))
            if not shown and "=" not in s.note:
                lint.add("warn", "L-CALC-SUBST", s, "계산 표지 · 요인 분해가 있는데 대입(.subst · .derive · 대본 '=')이 없음")
        for derive in find_all(ls.screen + [ls.evidence], lambda n: n.tag == "ol" and "derive" in n.classes):
            steps = sum(1 for c in derive.children if isinstance(c, Node) and c.tag == "li" and "dv-end" not in c.classes)
            if steps > 4:
                lint.add("warn", "L-DERIVE-STEPS", s, f".derive {steps}단계 > 4 — 장을 나눈다", steps, 4)
        conds = sum(1 for _ in find_all(ls.screen, has_class("cond")))
        if conds >= 2:
            lint.add("warn", "L-COND-MANY", s, f"조건 줄 {conds}개 ≥ 2", conds, 1)
        for img in find_all([ls.visual], lambda n: n.tag == "img"):
            in_crop = any(a.tag == "figure" and "crop" in a.classes for a in img.ancestors())
            if "data-glyph-px" not in img.attrs or not in_crop:
                lint.add("warn", "L-CROP-MAIN", s, f"화면 이미지 {img.attrs.get('src', '')[:60]!r}: "
                                                   "figure.crop 안 · data-glyph-px 필요")
        for p in find_all(ls.screen + [ls.evidence], lambda n: n.tag == "p"):
            if "\\[" in raw_text(p):
                lint.add("warn", "L-MATH-IN-P", s, "<p> 안에 \\[ … \\] — 디스플레이 수식은 p 밖에 둔다")
                break

    # cross-slide checks
    mains_text = [(ls, nows(ls.visible_text)) for ls in mains]
    check_repeats(lint, mains)
    check_define_first(lint, mains, spec.get("known_terms") or [])
    pair = spec.get("compare_pair")
    if pair:
        if any(ls.s.kind for ls in mains):
            intro = [ls for ls in mains if ls.s.kind == "intro"]
        else:
            first = mains[0].s.section if mains else None
            intro = [ls for ls in mains if ls.s.section == first]
        if not any(nows(pair) in nows(ls.visible_text) for ls in intro):
            lint.add("warn", "L-PAIR", None, f"compare_pair '{pair}'가 들어가며 장 화면 글에 없음")
    for term in spec.get("scope_terms") or []:
        owners = [ls for ls in mains if ls.s.term == term]
        if not owners:
            lint.add("warn", "L-SCOPE-MISSING", None, f"scope_terms '{term}'의 term을 가진 본편 장이 없음")
        elif not any(ls.dfns or ls.term_title() for ls in owners):
            lint.add("info", "L-SCOPE-DEF", owners[0].s, f"'{term}' 장에 <dfn>도 '{term}:' 제목도 없음")
    for term in spec.get("out_of_scope_terms") or []:
        for ls, text in mains_text:
            if nows(term) and nows(term) in text:
                lint.add("warn", "L-SCOPE-OUT", ls.s, f"범위 밖 용어 '{term}'가 본편 화면에 나옴")
    check_images(lint, slides, deck_dir)
    last, seen = None, set()
    for s in model:
        if s.section != last and s.section in seen:
            lint.add("warn", "L-SECTION-SPLIT", s, f"section '{s.section}'이 떨어져 다시 나옴")
        seen.add(s.section)
        last = s.section

    if claims is not None:
        check_claims(lint, slides, claims, has_panel)
    return lint


def raw_text(node):
    parts = []
    for child in node.children:
        parts.append(raw_text(child) if isinstance(child, Node) else child)
    return "".join(parts)


def check_repeats(lint, mains):
    size = 20
    owners = {}
    texts = {}
    for ls in mains:
        text = "".join(ch for ch in ls.visible_text
                       if not ch.isspace() and not unicodedata.category(ch).startswith(("P", "Z", "C")))
        texts[ls.s.pos] = text
        for gram in {text[i:i + size] for i in range(len(text) - size + 1)}:
            owners.setdefault(gram, set()).add(ls.s.pos)
    by_set = {}
    for gram, positions in owners.items():
        if len(positions) >= 3:
            by_set.setdefault(tuple(sorted(positions)), set()).add(gram)
    pos_to_slide = {ls.s.pos: ls.s for ls in mains}
    for positions in sorted(by_set):
        grams = by_set[positions]
        text = texts[positions[0]]
        fragments, i = [], 0
        while i <= len(text) - size:
            if text[i:i + size] in grams:
                j = i
                while j + 1 <= len(text) - size and text[j + 1:j + 1 + size] in grams:
                    j += 1
                fragments.append(text[i:j + size])
                i = j + size
            else:
                i += 1
        refs = ", ".join(pos_to_slide[p].ref for p in positions)
        for fragment in dict.fromkeys(fragments):
            lint.add("warn", "L-REPEAT-TEXT", pos_to_slide[positions[0]],
                     f"'{fragment[:40]}{'…' if len(fragment) > 40 else ''}' ({len(fragment)}자)가 본편 "
                     f"{len(positions)}장에 반복: {refs}", len(positions), 2)


def check_define_first(lint, mains, known_terms):
    defined = list(known_terms)

    def is_defined(token):
        for term in defined:
            if token == term or token in re.split(r"[^A-Za-z0-9]+", term):
                return True
        return False
    seen = set()
    for ls in mains:
        defined.extend(ls.dfns)
        if ls.term_title():
            defined.append(ls.s.term)
        for token in UPPER_TOKEN_RE.findall(ls.define_text):
            if token in seen:
                continue
            seen.add(token)
            if not is_defined(token):
                lint.add("warn", "L-DEFINE-FIRST", ls.s, f"'{token}'이 처음 나온 장까지 정의되지 않음 "
                                                         "(<dfn>, 'term:' 제목, known_terms)")


def check_images(lint, slides, deck_dir):
    uses = {}
    for ls in slides:
        for img in find_all(ls.screen + [ls.evidence], lambda n: n.tag == "img"):
            src = img.attrs.get("src", "")
            if not src or src.startswith(("data:", "http:", "https:")):
                continue
            path = (deck_dir / src).resolve()
            if not path.is_file():
                continue
            key = hashlib.sha256(str(path).encode("utf-8")).hexdigest()
            entry = uses.setdefault(key, {"src": src, "size": path.stat().st_size, "slides": []})
            if ls.s not in entry["slides"]:
                entry["slides"].append(ls.s)
    for key in sorted(uses, key=lambda k: uses[k]["slides"][0].pos):
        entry = uses[key]
        if len(entry["slides"]) >= 2:
            refs = ", ".join(s.ref for s in entry["slides"])
            lint.add("info", "L-IMG-DUP", entry["slides"][0], f"같은 이미지 {entry['src']} ({entry['size']:,} B)를 "
                                                             f"{len(entry['slides'])}장에서 씀: {refs} — 한 장에 두고 링크",
                     len(entry["slides"]), 1)


def cell_text(node):
    """Cell text for value comparison: footnote <sup> and evidence chips left out, whitespace removed."""
    skip = lambda n: n.tag == "sup" or "ev-chip" in n.classes
    return unicodedata.normalize("NFC", nows(collect_text(node, {}, "visible", exclude=skip, sep="")))


def table_cells(table):
    """[(row labels, column labels, cell text)] for the body cells of one <table> (rowspan · colspan expanded).
    Column labels: header-row text at that column (every header row) and the cell's data-label.
    Row labels: the first column's text and the first two columns joined (model | size split tables)."""
    rows = []

    def walk(node, section):
        for child in node.children:
            if not isinstance(child, Node) or child.tag == "table":
                continue
            if child.tag == "tr":
                rows.append((section, child))
            else:
                walk(child, child.tag if child.tag in ("thead", "tbody", "tfoot") else section)
    walk(table, None)
    grid, pending = [], {}
    for section, tr in rows:
        cells = [c for c in tr.children if isinstance(c, Node) and c.tag in ("td", "th")]
        row, col, index = [], 0, 0
        while index < len(cells) or (pending and col <= max(pending)):
            if col in pending:
                remaining, cell = pending[col]
                row.append(cell)
                if remaining <= 1:
                    del pending[col]
                else:
                    pending[col] = (remaining - 1, cell)
                col += 1
                continue
            if index >= len(cells):
                row.append(None)
                col += 1
                continue
            cell = cells[index]
            index += 1
            span = int(cell.attrs.get("colspan") or 1) if str(cell.attrs.get("colspan") or 1).isdigit() else 1
            rspan = int(cell.attrs.get("rowspan") or 1) if str(cell.attrs.get("rowspan") or 1).isdigit() else 1
            for _ in range(max(1, span)):
                row.append(cell)
                if rspan > 1:
                    pending[col] = (rspan - 1, cell)
                col += 1
        grid.append((section, row))
    head = [row for section, row in grid if section == "thead"]
    body = [row for section, row in grid if section != "thead"]
    if not head:
        while body and all(c is None or c.tag == "th" for c in body[0]):
            head.append(body.pop(0))
    out = []
    for row in body:
        first = [cell_text(c) if c is not None else "" for c in row[:2]]
        row_labels = {first[0], "".join(first)} - {""}
        for j, cell in enumerate(row):
            if cell is None or j == 0:
                continue
            col_labels = {cell_text(h[j]) for h in head if j < len(h) and h[j] is not None}
            if cell.attrs.get("data-label"):
                col_labels.add(unicodedata.normalize("NFC", nows(cell.attrs["data-label"])))
            out.append((row_labels, col_labels - {""}, cell_text(cell)))
    return out


def check_display_and_cells(lint, claim, users, main_users, counts):
    """L-CLAIM-DISPLAY · L-CLAIM-CELL · L-CLAIM-CELL-MISSING · L-MAIN-OFFSCREEN for one claim."""
    cid, layer = claim["id"], claim.get("layer")
    display = claim.get("display")
    if isinstance(display, str) and nows(display) and layer in ("main", "evidence"):
        targets = main_users if layer == "main" else users
        for ls in targets:
            counts["display_total"] += 1
            text = nows(ls.visible_text) + ("" if layer == "main" else nows(ls.evidence_text))
            if nows(display) in text:
                counts["display_ok"] += 1
            else:
                where = "화면" if layer == "main" else "화면 · 패널"
                lint.add("warn", "L-CLAIM-DISPLAY", ls.s, f"claim '{cid}' display '{display}'가 {where} 글에 없음")
    cells = claim.get("cells")
    if cells is not None:
        if not isinstance(cells, dict) or any(not isinstance(v, str) for v in cells.values()):
            lint.add("error", "L-CLAIM-CELL", None, f"claim '{cid}': cells는 {{\"행|열\": \"원문 셀 글\"}} (값은 문자열)")
            cells = {}
        tables = [(ls, cell) for ls in users
                  for table in find_all(ls.screen + [ls.evidence], lambda n: n.tag == "table")
                  for cell in table_cells(table)]
        for key, expected in cells.items():
            parts = key.split("|")
            if len(parts) != 2 or not all(nows(p) for p in parts):
                lint.add("error", "L-CLAIM-CELL", None, f"claim '{cid}': cells 키 '{key}'는 '행|열' 꼴")
                continue
            a, b = (unicodedata.normalize("NFC", nows(p)) for p in parts)
            want = unicodedata.normalize("NFC", nows(expected))
            found = [(ls, text) for ls, (rows, cols, text) in tables
                     if (a in rows and b in cols) or (b in rows and a in cols)]
            counts["cell_total"] += 1
            if not found:
                lint.add("warn", "L-CLAIM-CELL-MISSING", users[0].s if users else None,
                         f"claim '{cid}' cells '{key}': 참조 장의 표에 그 행 · 열이 없음")
                continue
            wrong = [(ls, text) for ls, text in found if text != want]
            for ls, text in wrong:
                lint.add("error", "L-CLAIM-CELL", ls.s, f"claim '{cid}' cells '{key}': 표 '{text}' ≠ 원장 '{expected}'",
                         text, expected)
            if not wrong:
                counts["cell_ok"] += 1
    if layer == "main" and claim.get("kind") != "verdict" and not (isinstance(display, str) and nows(display)):
        candidates = [claim.get("screen_condition")] + list((cells or {}).values())
        value = claim.get("value")
        if is_number(value):
            candidates += [number_text(value)] + ([f"{value:,}"] if isinstance(value, int) else [])
        candidates = [nows(c) for c in candidates if isinstance(c, str) and nows(c)]
        if not candidates:
            if main_users:
                counts["unchecked"].append(cid)
            return
        for ls in main_users:
            if not any(c in nows(ls.visible_text) for c in candidates):
                lint.add("info", "L-MAIN-OFFSCREEN", ls.s, f"claim '{cid}' (layer main): display · value · cells · "
                                                           "screen_condition 어느 글도 화면에 없음 — 패널에만 있으면 layer를 고친다")


def check_claims(lint, slides, claims, has_panel):
    by_id = {c["id"]: c for c in claims}
    refs = {cid: [] for cid in by_id}
    for ls in slides:
        for cid in ls.s.claims:
            if cid not in by_id:
                lint.add("error", "L-CLAIM-UNKNOWN", ls.s, f"claim '{cid}'가 원장에 없음")
            else:
                refs[cid].append(ls)
    expr_total = expr_ok = factor_total = factor_ok = cond_total = cond_ok = 0
    counts = {"display_total": 0, "display_ok": 0, "cell_total": 0, "cell_ok": 0, "unchecked": []}
    for claim in claims:
        cid = claim["id"]
        value = claim.get("value")
        if "expr" in claim:
            expr_total += 1
            try:
                result = eval_expr(claim["expr"])
                if not is_number(value):
                    raise ValueError("value is missing or not a number")
                tol = claim.get("tol")
                tol = tol if is_number(tol) else 1e-9 * max(1, abs(value))
                if abs(result - value) > tol:
                    lint.add("error", "L-CLAIM-EXPR", None, f"claim '{cid}': {claim['expr']} = {result:g} ≠ value "
                                                           f"{value:g} (tol {tol:g})", result, value)
                else:
                    expr_ok += 1
            except (ValueError, SyntaxError, ZeroDivisionError, TypeError) as error:
                lint.add("error", "L-CLAIM-EXPR", None, f"claim '{cid}': expr를 계산할 수 없음 ({error})")
        for field in ("factors", "ratio_of"):
            if field not in claim:
                continue
            factor_total += 1
            try:
                if not is_number(value):
                    raise ValueError("value is missing or not a number")
                if field == "factors":
                    product = 1.0
                    for factor in claim["factors"]:
                        if not is_number(factor.get("from")) or not is_number(factor.get("to")) or factor["to"] == 0:
                            raise ValueError(f"factor {factor.get('name')!r} needs numeric from/to (to ≠ 0)")
                        product *= factor["from"] / factor["to"]
                    got = product
                    expr = " × ".join(f"{f['from']:g}/{f['to']:g}" for f in claim["factors"])
                else:
                    a, b = claim["ratio_of"]
                    va, vb = by_id.get(a, {}).get("value"), by_id.get(b, {}).get("value")
                    if not is_number(va) or not is_number(vb) or vb == 0:
                        raise ValueError(f"ratio_of claims {a!r}, {b!r} need numeric values")
                    got = va / vb
                    expr = f"{a} ÷ {b}"
                if abs(got - value) > 1e-6 * max(abs(value), 1e-12):
                    lint.add("error", "L-CLAIM-FACTOR", None, f"claim '{cid}' {field}: {expr} = {got:g} ≠ value {value:g}",
                             got, value)
                else:
                    factor_ok += 1
            except (ValueError, TypeError, KeyError, AttributeError) as error:
                lint.add("error", "L-CLAIM-FACTOR", None, f"claim '{cid}' {field}: {error}")
        if not claim.get("sources") and not claim.get("inputs"):
            lint.add("warn", "L-CLAIM-NOSOURCE", None, f"claim '{cid}': sources도 inputs도 없음")
        layer = claim.get("layer")
        users = refs.get(cid, [])
        main_users = [ls for ls in users if ls.s.is_main]
        if layer == "main":
            if not users:
                lint.add("warn", "L-CLAIM-UNUSED", None, f"claim '{cid}' (layer main)을 참조하는 본편 장이 없음")
            elif not main_users:
                lint.add("warn", "L-CLAIM-APPX-ONLY", users[0].s, f"claim '{cid}' (layer main)을 부록 장만 참조")
        if layer == "evidence":
            for ls in users:
                if not has_panel[ls.s.pos]:
                    lint.add("warn", "L-CLAIM-NOEVID", ls.s, f"claim '{cid}' (layer evidence)인데 근거 패널이 없음")
        kind = claim.get("kind")
        for ls in users:
            if kind == "verdict":
                ok_screen = ls.any_screen(has_class("verdict"))
                ok = ok_screen if layer == "main" else (ok_screen or ls.any_evidence(has_class("verdict")))
                if layer in ("main", "evidence") and not ok:
                    lint.add("warn", "L-CHIP-MISSING", ls.s, f"claim '{cid}' (verdict): .verdict 요소가 없음")
            elif kind in CHIP_REQUIRED:
                label = CHIP_LABELS[kind]
                if layer == "main" and not ls.has_chip(kind, "screen"):
                    lint.add("warn", "L-CHIP-MISSING", ls.s, f"claim '{cid}' ({kind}): 화면에 '{label}' 표지 없음")
                elif layer == "evidence" and not (ls.has_chip(kind, "screen") or ls.has_chip(kind, "evidence")):
                    lint.add("warn", "L-CHIP-MISSING", ls.s, f"claim '{cid}' ({kind}): 패널 · 화면에 '{label}' 표지 없음")
        condition = claim.get("screen_condition")
        if condition and main_users:
            cond_total += 1
            missing = [ls for ls in main_users if nows(condition) not in nows(ls.visible_text)]
            for ls in missing:
                lint.add("warn", "L-COND-SCREEN", ls.s, f"claim '{cid}' screen_condition '{condition}'이 화면에 없음")
            if not missing:
                cond_ok += 1
        check_display_and_cells(lint, claim, users, main_users, counts)
    layers = {}
    for claim in claims:
        layers[claim.get("layer", "?")] = layers.get(claim.get("layer", "?"), 0) + 1
    main_claims = [c for c in claims if c.get("layer") == "main"]
    linked = sum(1 for c in main_claims if any(ls.s.is_main for ls in refs.get(c["id"], [])))
    share = linked / len(main_claims) if main_claims else 1.0
    layer_text = " · ".join(f"{k} {layers[k]}" for k in sorted(layers, key=lambda k: (CLAIM_LAYERS + (k,)).index(k)))
    lint.add("info", "coverage", None, f"원장 {len(claims)}개 ({layer_text}) · 출처 연결률 {linked}/{len(main_claims)}"
                                       f" = {share:.0%} · expr 재계산 {expr_ok}/{expr_total} · factors · ratio "
                                       f"{factor_ok}/{factor_total} · screen_condition 유지 {cond_ok}/{cond_total}"
                                       f" · display 일치 {counts['display_ok']}/{counts['display_total']}"
                                       f" · 셀 대조 {counts['cell_ok']}/{counts['cell_total']}"
                                       f" · 화면 대조 불가 main {len(counts['unchecked'])}"
                                       + (f" ({', '.join(counts['unchecked'])})" if counts["unchecked"] else ""),
             round(share, 4), 1.0)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="Reviewed slide JSON")
    parser.add_argument("output", type=Path, nargs="?", help="Standalone HTML output (omit with --lint to lint only)")
    parser.add_argument("--script", action="append", type=Path, default=[], metavar="FILE",
                        help="Speaker script Markdown (## ID · ## @key · ## title); repeatable")
    parser.add_argument("--allow-missing-notes", action="store_true",
                        help="Missing scripts warn instead of fail (and do not count for --strict)")
    parser.add_argument("--lint", action="store_true", help="Static checks (stderr: LINT sev code id message)")
    parser.add_argument("--lint-json", type=Path, metavar="FILE", help="Also write lint findings as JSON")
    parser.add_argument("--claims", type=Path, metavar="FILE", help="Claim ledger (overrides claims_file)")
    parser.add_argument("--strict", action="store_true",
                        help="Lint warnings and the build warnings " + ", ".join(STRICT_BUILD_CODES) + " also exit 1")
    parser.add_argument("--katex", metavar="DIR", help="KaTeX package folder (else KATEX_MODULE)")
    parser.add_argument("--node", metavar="PATH", help="Node.js binary (else NODE_BIN, else PATH)")
    parser.add_argument("--no-math", action="store_true", help="Do not render formulas; show TeX source")
    parser.add_argument("--resize-images", action="store_true",
                        help="Downscale PNG/JPEG wider than 2 × data-display-width before embedding")
    args = parser.parse_intermixed_args()
    lint_requested = args.lint or args.lint_json is not None
    if args.output is None and not lint_requested:
        parser.error("OUTPUT is required unless --lint is given")
    try:
        spec = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"ERROR: cannot read {args.input}: {error}", file=sys.stderr)
        return 1
    if not isinstance(spec, dict):
        print("ERROR: deck JSON must be an object", file=sys.stderr)
        return 1
    version = spec.get("shell_version", 1)
    if version not in (1, 2) or isinstance(version, bool):
        print(f"ERROR E-FIELD: shell_version must be 1 or 2 ({version!r})", file=sys.stderr)
        return 1
    v2 = version == 2
    deck_dir = args.input.resolve().parent
    status = 0
    try:
        if not v2:
            ignored = ignored_v2_fields(spec)
            if ignored:
                warn("W-V2-FIELD-IGNORED", "shell_version is not 2; ignored v2 fields in " + "; ".join(ignored))
        model = validate_and_model(spec, v2)
        if args.script:
            merge_scripts(model, args.script, v2, args.allow_missing_notes)
        report_missing_images(model, deck_dir)
        prepared = prepare_v2(model) if v2 else None   # E-XREF / E-MATH-REF also stop a lint-only run
        if lint_requested:
            claims = None
            claims_path = args.claims or ((deck_dir / spec["claims_file"]) if v2 and spec.get("claims_file") else None)
            if v2 and claims_path is not None:
                claims = load_claims(claims_path)
            counts = run_lint(spec, model, v2, claims, deck_dir).emit(args.lint_json)
            if counts["error"] or (args.strict and counts["warn"]):
                status = 1
        if args.output is None:
            return strict_status(args, status)
        if v2 and not args.script:
            silent = [s.ref for s in model if s.is_main and not s.note.strip()]
            if silent:
                warn("W-NOTES-MISSING", f"{len(silent)} main slides have no speaker script ({', '.join(silent)}); "
                                        "add note fields or --script", strict=not args.allow_missing_notes)
        shell = SHELL_PATH.read_text(encoding="utf-8")
        if v2:
            page, rendered, total = render_v2(spec, model, prepared, shell, args)
        else:
            merged = dict(spec)
            merged["slides"] = [dict(raw, note=s.note) if (args.script and s.note != (raw.get("note", "") or ""))
                                else raw for raw, s in zip(spec["slides"], model)]
            page, rendered, total = render(merged, shell), 0, 0
        base = args.input.resolve().parent
        if args.resize_images:
            page = resize_images(page, base)
        result = inline_images(page, base)
    except BuildError as error:
        for code, message in error.errors:
            print(f"ERROR {code}: {message}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    size = len(result.encode("utf-8"))
    print(f"{args.output}: {len(model)} slides · {size} B · math {rendered}/{total} rendered", flush=True)
    if size > DECK_BYTES_LIMIT:
        warn("W-DECK-BYTES", f"{args.output}: {size:,} B > 2 MB ({DECK_BYTES_LIMIT:,} B) — "
                             "shrink or reuse images (--resize-images, link instead of repeating)")
    return strict_status(args, status)


def strict_status(args, status):
    """--strict: the build warnings in STRICT_BUILD_CODES (not ones the user asked for) also exit 1."""
    hits = sorted({code for code, strict in WARNED if strict and code in STRICT_BUILD_CODES})
    if args.strict and hits:
        print(f"STRICT: build warnings {', '.join(hits)} → exit 1", file=sys.stderr)
        return 1
    return status


if __name__ == "__main__":
    sys.exit(main())
