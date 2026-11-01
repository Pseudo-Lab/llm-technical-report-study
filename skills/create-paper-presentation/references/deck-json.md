# 덱 JSON · 빌드 · 검사

`scripts/build_deck.py`가 덱 JSON(+ 원장 · 대본)을 셸에 넣어 독립 HTML 하나를 만들고, `scripts/check_deck.cjs`가 그 HTML을 브라우저로 렌더해 잰다. 화면 부품의 HTML은 [shell-components.md](shell-components.md), 원장은 [claim-ledger.md](claim-ledger.md).

## v1과 v2

- 덱에 `"shell_version": 2`가 **없으면** v1이다. 출력은 예전 빌드와 바이트까지 같다. 옛 덱은 그대로 다시 빌드해도 된다.
- `"shell_version": 2`이면 장 ID · 상호참조 · 출처 줄 접기 · 근거 패널 · 수식 사전 렌더 · 본편 끝 등이 켜진다. `<html>`에 `data-shell="2"`가 붙는다.
- v1 덱에 v2 장 필드(`evidence` · `math` · `key` · `id` · `part` · `kind` · `seconds` · `term` · `claims` · `src_visible`)가 있으면 경고 W-V2-FIELD-IGNORED 후 무시하고 v1 출력을 낸다.
- v1 검증(장 필드 `title` · `body` · `visual` · `sources` 필수, `layout`은 CSS 클래스 이름)은 v2에서도 그대로다.

## 덱 필드

v1 필드 `title` · `subtitle` · `slides`는 그대로다.

| 필드 | 형 | 기본 | 효과 |
| --- | --- | --- | --- |
| `shell_version` | int | 1 | `2`이면 v2 마크업 · 처리 전부. `<html data-shell="2">` |
| `budget_minutes` | number | 없음 | 발표 시간(분). `<html data-budget-min="…">`, lint · check의 시간 · 장 수 예산 |
| `compare_pair` | str | 없음 | lint: 들어가며 장 화면 글에 이 문자열이 있어야 함(L-PAIR) |
| `scope_terms` | [str] | 없음 | lint: 항목마다 `term`이 같은 본편 장이 하나 이상(L-SCOPE-MISSING) |
| `out_of_scope_terms` | [str] | 없음 | lint: 본편 화면 글에 나오면 경고(L-SCOPE-OUT) |
| `known_terms` | [str] | [] | 첫 등장 정의 검사(L-DEFINE-FIRST)의 허용 목록 |
| `claims_file` | str | 없음 | 덱 JSON 폴더 기준 상대 경로의 원장. `--claims`가 우선 |

## 장 필드

v1 필드 `title` · `body` · `visual` · `sources[{label, url}]` · `note` · `section` · `section_label` · `layout` · `ids`는 그대로다. `ids`는 출처 줄 오른쪽(`.src-ids`)에 보이므로 읽기 지도 항목(파트 · RQ 번호 · 개념 페이지 이름)을 읽을 수 있는 라벨로 쓴다(예: `지도 · KV cache 계산`. `#c-…` 같은 원시 앵커 이름을 쓰지 않는다).

| 필드 | 형 | 기본 | 효과 · 검사 |
| --- | --- | --- | --- |
| `key` | str `^[a-z0-9][a-z0-9-]*$` | 없음 | 덱 안에서 유일. `data-key`, 상호참조 `[[@key]]`, 대본 제목줄 `## @key` |
| `id` | str | 자동 | 적으면 자동 ID와 같아야 함(다르면 빌드 오류 E-ID-DRIFT) |
| `part` | `main` · `appendix` · `review` | `main` | 순서는 main → appendix → review만(E-PART-ORDER) |
| `kind` | `intro` · `result` · `mechanism` · `summary` | 없음 | `data-kind`, 기본 설명 시간 |
| `seconds` | int 5–300 | kind 기본값 | `data-seconds` |
| `term` | str | 없음 | `data-term`, 제목 첫 어구 검사(L-TITLE-TERM) |
| `claims` | [str] | [] | `data-claims`(공백 구분), 원장 lint |
| `evidence` | HTML str | 없음 | 근거 패널 본문 |
| `math` | {name: {`tex`, `tex_narrow`?, `display`? = true}} | {} | 조각 안 `<span data-math="name"></span>` 자리표시를 KaTeX로 바꿈 |
| `src_visible` | int 1–3 | 2 | 화면 출처 줄에 보일 출처 수 |
| `sources[i].detail` | str | 없음 | 근거 패널 '출처 전체'에만 보임 |

- `kind` 기본 초: `intro` 30 · `result` 50 · `mechanism` 80 · `summary` 20. `seconds`도 `kind`도 없으면 `data-seconds`를 쓰지 않는다. 열린 질문 · 토론 장은 `kind: "summary"`에 `seconds`(30–60)를 직접 적는다([screen-budget.md](screen-budget.md) 5절).
- `layout` 값은 장의 `layout-{값}` 클래스가 된다(셸에는 `cover` · `overview` · `process` · `quantitative` · `reference`가 있다. 기본은 `split`). `wide`면 `.inner`에도 `wide`가 붙어 넓은 도식을 담는다.

## 최소 예 (장 하나)

덱에 이 장 하나뿐이면 자동 ID는 `1-1`이다. `claims.json`은 [claim-ledger.md](claim-ledger.md) 형식으로 `kv-65b` · `kv-70b` · `kv-ratio`를 담는다.

```json
{
 "title": "최소 예 — KV cache 한 장",
 "subtitle": "v2 필드 보기",
 "shell_version": 2,
 "budget_minutes": 1,
 "scope_terms": ["KV cache"],
 "out_of_scope_terms": ["RoPE"],
 "known_terms": ["LLaMA", "KiB"],
 "claims_file": "claims.json",
 "slides": [
  {
   "key": "kv-cache",
   "id": "1-1",
   "part": "main",
   "kind": "mechanism",
   "seconds": 60,
   "term": "KV cache",
   "section": "1",
   "section_label": "구조",
   "title": "KV cache: 토큰당 2,560 → 320 KiB, KV head 64 → 8이 전부다",
   "body": "<p><dfn>KV cache</dfn>는 생성 중 이전 토큰의 K · V를 저장해 두는 메모리입니다.</p>",
   "visual": "<figure class=\"factor\" data-main role=\"img\" aria-label=\"토큰당 KV cache 2,560 KiB에서 320 KiB. KV head 64에서 8로 8배 감소, 층과 head 차원은 동일\"><div class=\"fx-bars\"><div class=\"fx-row\"><span class=\"fx-name\">LLaMA-65B</span><span class=\"fx-track\"><i style=\"width:100%\"></i></span><b class=\"fx-val\">2,560 KiB</b></div><div class=\"fx-row fx-new\"><span class=\"fx-name\">Llama 2-70B</span><span class=\"fx-track\"><i style=\"width:12.5%\"></i></span><b class=\"fx-val\">320 KiB</b></div></div><ol class=\"fx-terms\"><li class=\"fx-chg\"><span class=\"fx-k\">KV head</span><span class=\"fx-ab\">64 → 8</span><b class=\"fx-r\">÷ 8</b></li><li class=\"fx-same\"><span class=\"fx-k\">층</span><span class=\"fx-ab\">80 → 80</span><b class=\"fx-r\">동일</b></li><li class=\"fx-same\"><span class=\"fx-k\">head 차원</span><span class=\"fx-ab\">128 → 128</span><b class=\"fx-r\">동일</b></li></ol><span data-math=\"kv\"></span><figcaption class=\"fx-sum\">합: ÷ 8</figcaption></figure><p class=\"cond\"><span class=\"ev-chip\" data-ev=\"calc\">계산</span> 공개 config 값 · fp16 2 B · K+V · 80층 합산 · batch 1</p><figure class=\"crop crop-thumb only-wide\" data-au=\"0\"><img src=\"figures/llama1-table2.png\" alt=\"LLaMA v1 Table 2 원본(눌러서 확대)\" width=\"200\" data-glyph-px=\"14\"><figcaption>원본 · 눌러서 확대</figcaption></figure>",
   "evidence": "<p><span class=\"ev-chip\" data-ev=\"calc\">계산</span> \\(L\\) 층 수 · \\(n_{kv}\\) KV head 수 · \\(d_h\\) head 차원 · \\(b\\) 값 하나의 바이트(fp16 = 2) · 맨 앞 2 = K와 V</p><p class=\"subst\">LLaMA-65B: 2 × 80 × 64 × 128 × 2 B = 2,621,440 B = 2,560 KiB</p><p class=\"subst\">Llama 2-70B: 2 × 80 × 8 × 128 × 2 B = 327,680 B = 320 KiB</p><p><span class=\"ev-chip\" data-ev=\"config\">config</span> 70B의 층 80 · KV head 8 · head 차원 128은 논문이 아니라 공개 config 값입니다.</p><figure class=\"crop\"><img src=\"figures/llama1-table2.png\" alt=\"LLaMA v1 Table 2\" data-glyph-px=\"14\" data-display-width=\"560\"><figcaption>원문 · LLaMA v1 Table 2 (p.3) · 전체 / 발표자 표시 없음</figcaption></figure>",
   "math": {
    "kv": {"tex": "\\text{KV/token} = 2 \\times L \\times n_{kv} \\times d_h \\times b", "tex_narrow": "\\begin{aligned}\\text{KV/token} &= 2 \\times L \\times n_{kv} \\\\ &\\quad \\times d_h \\times b\\end{aligned}", "display": true}
   },
   "src_visible": 1,
   "sources": [
    {"label": "LLaMA v1 Table 2 (p.3)", "url": "https://arxiv.org/pdf/2302.13971v1#page=3"},
    {"label": "Llama-2-70b-hf config", "url": "https://huggingface.co/meta-llama/Llama-2-70b-hf/blob/main/config.json", "detail": "num_hidden_layers 80 · num_key_value_heads 8"}
   ],
   "claims": ["kv-65b", "kv-70b", "kv-ratio"],
   "ids": "지도 · KV cache 계산",
   "note": "토큰 하나당 KV cache는 K와 V 두 개, 층 수, KV head 수, head 차원, 바이트 수의 곱입니다. 두 모델은 층과 head 차원이 같고 KV head만 64에서 8로 줄어 8배가 전부 거기서 나옵니다. 70B 값은 논문이 아니라 공개 config에서 왔다고 말합니다."
  }
 ]
}
```

이 장의 화면에는 출처 1개(`src_visible: 1`)와 `+1` 버튼 · '근거 펼치기 E', 요인 분해 카드 안 일반식(`math.kv`, 휴대폰에서는 `tex_narrow` 판), 조건 줄, Table 2 원본 썸네일이 보인다(AU 2). 근거 패널에는 기호 풀이 · 대입 두 줄 · config 풀이 · Table 2 전체 crop · 출처 전체 2개가 들어간다.

## 장 ID · 상호참조

**자동 ID** (v2만)

- 본편: `section` 값이 본편 장에서 처음 나온 순서대로 1부터 번호 n, 그 섹션 안 본편 장 순서 m → `n-m`. 같은 `section` 값이 떨어져 다시 나오면 lint 경고 L-SECTION-SPLIT, 번호는 이어서 센다.
- 부록 `A-k`, 검토 기록 `R-k`(그 part 안 순서, 1부터).
- 장 위치 N(1부터, 전체 순서)은 셸 해시 `#sN`과 같다. ID는 머리 라벨(`.ey`) 맨 앞에 `<span class="sid">`로 보인다.

**상호참조** (`body` · `visual` · `evidence` 안, v2만)

| 쓰는 법 | 화면 글 | 링크 |
| --- | --- | --- |
| `[[2-2]]` | `2-2` | `<a class="xref" href="#s3" data-ref="2-2" title="{대상 제목}">` |
| `[[@kv-cache]]` | 대상 ID(`2-2`) | 같음 |
| `[[2-2\|KV cache 분해]]` · `[[@kv-cache\|KV cache 분해]]` | `KV cache 분해 (2-2)` | 같음 |

- 찾을 수 없는 대상은 빌드 오류 E-XREF(모두 모아 한 번에 출력).
- 태그 밖 글 조각만 바꾼다. `<a>` · `<code>` · `<pre>` · `<script>` · `<style>` · `<svg>` · `<template>` 안과 속성 값은 건드리지 않는다.
- 대본(`note`) 안의 `[[…]]`는 링크가 아니라 글로 바뀐다: `[[2-2]]` → `2-2`, `[[@kv-cache|KV 분해]]` → `KV 분해(2-2)`.
- 화면에 장 번호를 글로 쓰면(링크 밖 `2-2` · `A-1`) 경고 L-UNLINKED-REF · C-XREF-UNLINKED, `#c-` · `#page=` 같은 원시 앵커를 글로 쓰면 L-RAW-ANCHOR.

## 대본 병합 `--script FILE`

여러 번 줄 수 있고 v1 · v2 덱 모두에서 쓴다.

- 형식: `## ` 제목줄 아래부터 다음 `## ` 또는 `# ` 제목줄 전까지가 그 장의 대본. `# ` 제목줄과 첫 `## ` 앞 글은 무시한다.
- 제목줄 대응 순서: ① 첫 토큰이 장 ID(`2-2`, `A-1`, `R-1`. 뒤의 ` · 제목` 등은 무시) ② `@key` ③ 정규화한 제목이 같은 장(태그 제거, `<br>` · `<wbr>` → 공백, HTML 엔티티 풀기, NFC, 공백 압축). v1 덱은 자동 ID와 `key`가 없으므로 ③만 쓴다.
- 오류(exit 1, E-SCRIPT): 어느 장과도 맞지 않는 제목줄, 같은 장에 두 번 맞는 제목줄, 병합 뒤 대본이 빈 본편 장(v1 덱은 전체 장). `--allow-missing-notes`면 빈 장은 경고로 낮춘다.
- JSON `note`가 이미 있고 대본 파일과 다르면 경고 W-NOTE-OVERRIDE 후 대본 파일 값을 쓴다.
- 결과 요약이 stderr에 나온다: `script: 6 headings · 6 matched · 0 orphan · 0 missing`.

```markdown
## 2-2 · KV cache
이제 attention 쪽입니다. 토큰 하나당 KV cache는 …

## @swiglu
먼저 FFN입니다. 질문은 "행렬이 하나 늘었는데 왜 크기가 그대로인가"입니다. …
```

대본은 이전 장과의 연결 → 도입 질문 → 설명 → (있으면) 예상 질문과 답 순서로 쓴다. 화면 문장을 그대로 옮기지 않는다(L-NOTES-COPY). 제작 · 검토 메모는 쓰지 않는다.

## 수식 (KaTeX)

**쓰는 법** (v2만)

- 인라인 `\( … \)`, 디스플레이 `\[ … \]`를 `body` · `visual` · `evidence`의 태그 밖 글 안에서 쓴다. 한 수식이 태그를 가로지르면 안 된다. JSON에서는 백슬래시를 두 번 쓴다(`"\\(h\\)"`). 조각 안 TeX의 `&lt;` 등은 엔티티를 푼 뒤 렌더한다.
- 제목에는 수식을 쓰지 않는다(L-TITLE-MATH). `<p>` 안에 `\[`를 두면 경고(L-MATH-IN-P).
- 휴대폰용 줄바꿈 판이 필요한 디스플레이 수식은 장 `math` 필드에 두고 `<span data-math="이름"></span>`(또는 `<div …></div>`)으로 부른다. `tex_narrow`는 등호 단위로 줄바꿈한 판(`aligned` 권장). `display: false`면 인라인.
- 식은 조판하고, 실제 숫자를 대입한 산술 사슬은 글(`<p class="subst">`)로 쓴다. 한국어는 TeX 밖(`.dv-why` 등)에 둔다.

**빌드**

- 처리 순서: 상호참조 → 수식 자리표시 · 구분자 수집 → `scripts/render_math.cjs` 한 번 호출 → 치환 → KaTeX CSS 주입 → 이미지 내장.
- 결과는 `htmlAndMathml`이라 MathML과 TeX 원문(annotation)이 함께 남는다. 실제로 쓴 KaTeX 글꼴만 base64로 넣는다. 수식이 하나라도 있으면 `<style id="katex-css">`가 `</head>` 앞에 들어간다.
- 출력 마크업: 인라인 `<span class="math-inline">`, 디스플레이 `<span class="math-block">`, 좁은 판이 있으면 `<span class="math-block" data-math="kv" data-has-narrow><span class="math-wide">…</span><template class="math-narrow">…</template></span>`.
- KaTeX 위치: `--katex DIR` → `KATEX_MODULE` → `scripts/` 기준 `require.resolve('katex/package.json')`. DIR은 `package.json` · `dist/`가 있는 패키지 폴더. node 위치: `--node PATH` → `NODE_BIN` → PATH의 `node`.
- 설치: `scripts/`에서 `npm install`(`package.json`이 katex 0.18.11을 고정한다), 또는 이미 설치된 katex 패키지 폴더를 `KATEX_MODULE`로 준다.
- 대체 동작: node나 KaTeX가 없거나 `--no-math`면 경고 `WARN W-MATH-UNAVAILABLE: …`, TeX 원문을 `<code class="math-fallback" data-tex="…">`로 보이고 exit 0. KaTeX가 있는데 TeX 파싱 오류면 빌드 오류 E-MATH-TEX(장 ID · TeX 표시). `data-math` 자리표시에 맞는 `math` 항목이 없으면 E-MATH-REF.
- `render_math.cjs`는 stdin JSON `{"items":[{"id","tex","display"}],"embedFonts":true}` → stdout JSON `{"katex","items":[{"id","html"}|{"id","error"}],"css","fonts"}`. KaTeX를 못 찾으면 exit 3. 같은 입력이면 같은 바이트를 낸다.

## 빌드 출력 (요지)

v2 장 하나는 이 꼴이다(대괄호는 조건부).

```html
<section class="slide layout-{layout}[ has-ev][ is-main-end]" data-sec="{section}" data-section-label="{label}" data-nav="{nav}" data-id="{id}" data-part="{part}"[ data-kind="{kind}"][ data-seconds="{seconds}"][ data-term="{term}"][ data-key="{key}"][ data-claims="{c1 c2}"]>
<div class="card"><div class="{inner classes}">
<div class="txt"><div class="ey"><span class="sid">{id}</span> · {label}</div><h2>{title}</h2>{body}</div>
<div class="vis">{visual}</div></div>
<footer class="src"><span class="src-line">근거: {출처 링크 1..k}[ <button class="src-more" type="button" aria-controls="ev-s{N}">+{M}</button>]</span><span class="src-side">[<span class="src-ids">{ids}</span>][<span class="main-end">본편 끝</span>][<button class="ev-btn" type="button" aria-expanded="false" aria-controls="ev-s{N}">근거 펼치기 <kbd>E</kbd></button>]</span></footer></div>
[<aside class="evidence" id="ev-s{N}" tabindex="-1" aria-label="근거 · {id}" hidden>
<div class="ev-head"><strong>근거 · {id}</strong><button class="ev-close" type="button" aria-label="근거 닫기">닫기 <kbd>Esc</kbd></button></div>
[<div class="ev-body">{evidence}</div>]
<div class="ev-sources"><strong>출처 전체</strong><ol><li><a href="{url}">{label}</a>[ — {detail}]</li>…</ol></div></aside>]
<aside class="speaker-notes">{note}</aside></section>
```

- 화면 출처 수 k = min(`src_visible`, 출처 수), 나머지 M = 출처 수 − k.
- **근거 패널은 `evidence`가 있거나 M > 0일 때** 생긴다. 패널이 없으면 출처 줄에 출처 전부를 보인다(어디에도 안 보이는 출처가 없다). `.ev-sources`에는 화면에 보인 것까지 모든 출처가 순서대로 들어간다.
- `is-main-end` · `.main-end`는 마지막 본편 장에, 덱에 부록 · 검토 장이 있을 때만 붙는다.
- `<html lang="ko">`는 `<html lang="ko" data-shell="2"[ data-budget-min="{n}"]>`가 된다.

## 이미지

- 로컬 `<img src="상대 경로">`는 data URI로 내장한다(v1과 같음).
- `--resize-images`(기본 꺼짐): `<img … data-display-width="W">`이고 원본 폭이 2W보다 큰 PNG/JPEG를 폭 2W로 줄여 내장한다(Pillow, 없으면 macOS `sips`, 둘 다 없으면 경고 W-IMG-RESIZE 후 원본).
- 같은 이미지 파일을 여러 장에서 쓰면 알림 L-IMG-DUP. 같은 crop은 한 장에 두고 다른 장에서는 링크한다.
- 빌드 끝 요약: `{out}: {n} slides · {bytes} B · math {r}/{t} rendered`. 2 MB를 넘으면 경고 W-DECK-BYTES.

## lint 코드 (`build_deck.py --lint`)

덱 JSON · 원장 · 병합된 대본만 보는 정적 검사다. `error`는 exit 1, `warn`은 `--strict`일 때만 exit 1, `info`는 보고만. 출력은 stderr 한 줄씩 `LINT {sev} {code} {id or -} {메시지}`, `--lint-json FILE`이면 `[{"severity","code","slide","id","message","value","limit"}]`. 화면 글 정적 추정 = `title` + `body` + `visual`에서 태그 · `<script>` · `<style>` · `<template>`를 뺀 글(공백 제외, `[[…]]` 표기는 지운 뒤). 산문 정적 추정 = 그중 `<table>` · `<svg>` · `role="img"` 요소 · `.ev-chip` · `.tag` · 숫자 묶음 · 수식 · 제목 · 캡션(`.cap` · `figcaption`) · 범례 · 판정 띠를 뺀 것(check의 산문 정의와 같은 목록). 렌더 값은 check가 권위다. B = `budget_minutes`(없으면 예산 코드 생략).

| 코드 | 심각도 | 조건 |
| --- | --- | --- |
| L-BUDGET-SLIDES | warn | 본편 장 수가 round(0.8B)–floor(1.05B) 밖(floor(1.2B) 초과면 메시지에 '상한 초과') |
| L-BUDGET-INTRO | warn | 들어가며 > 3장(`kind: intro` 본편 장. 어느 장에도 kind가 없으면 첫 본편 섹션) |
| L-BUDGET-TIME | warn | 본편 `seconds` 합 > B × 60 |
| L-NOTES-MINUTES | warn | 본편 대본 공백 제외 글자 ÷ 300 > B |
| L-NOTES-LONG | info | 장 대본 글자 ÷ 300 × 60 > 1.5 × 그 장 seconds |
| L-NOTES-MISSING | warn | v2 본편 장에 대본 없음 |
| L-NOTES-COPY | warn | 화면 글 8글자 조각 중 대본에도 있는 비율 > 0.6 |
| L-DENSITY-VISIBLE | info | 장 화면 글 추정 > 550 |
| L-DENSITY-PROSE | info | 장 산문 추정 > 200 |
| L-SENTENCES | warn | `body`의 `p` · `li` 문장 수 > 3 |
| L-TITLE-BR | warn | 제목에 `<br>` |
| L-TITLE-TERM | warn | `term`이 제목 첫 콜론 앞 또는 첫 12자 안에 없음 |
| L-TITLE-LABEL | warn | 3어절 이하 제목, 또는 '전체 · 개요 · 결과 · 정리 · 요약 · 소개 · 목록 · 비교'로 끝나고 콜론 뒤 주장이 없는 제목 |
| L-TITLE-MATH | warn | 제목에 수식 구분자 |
| L-EVIDENCE-MISSING | warn | v2 본편 result · mechanism 장에 `evidence` 없음 |
| L-CHIP-MISSING | warn | 참조 claim이 표지 필요 종류인데 층에 맞는 자리에 라벨 없음 |
| L-CHIP-REPEAT | warn | 한 장 화면에 같은 `.ev-chip` 라벨 3번 이상(근거 범위 둘까지는 같은 라벨 2번이 정상) |
| L-REPEAT-TEXT | warn | 공백 · 문장부호를 뺀 화면 글에서 20자 이상 같은 조각이 본편 3장 이상 |
| L-RAW-ANCHOR | warn | 화면 글에 `#c-` · `#page=` 같은 원시 앵커 |
| L-SRC-PAGE | warn | 화면 출처 줄에 보이는 논문 출처(arXiv · PDF · `#page=` 링크, config 제외)의 라벨에 쪽(`p.N`) · 절(`§`) 표시가 없음. HTML판만 읽었으면 `§X (HTML판, 쪽 미확인)` |
| L-UNLINKED-REF | warn | 화면 글(링크 밖)에 실제 장 ID와 같은 토큰 |
| L-DEFINE-FIRST | warn | 대문자 2개 이상 영문 토큰이 본편에서 처음 나온 장까지 정의되지 않음 |
| L-PAIR | warn | `compare_pair`가 들어가며 장 화면 글에 없음 |
| L-SCOPE-MISSING | warn | `scope_terms` 항목에 `term`이 같은 본편 장이 없음 |
| L-SCOPE-DEF | info | 그 장에 `<dfn>`도 '용어:' 제목도 없음 |
| L-SCOPE-OUT | warn | `out_of_scope_terms`가 본편 화면 글에 나옴 |
| L-CALC-SUBST | warn | 화면에 `.factor`나 `data-ev="calc"`가 있는데 화면 · 패널에 `.subst` · `.derive`가 없고 대본에도 '=' 없음 |
| L-DERIVE-STEPS | warn | `.derive`의 `li:not(.dv-end)` > 4 |
| L-COND-MANY | warn | 화면에 `.cond` 2개 이상 |
| L-CROP-MAIN | warn | `visual` 안 `<img>`에 `data-glyph-px`가 없거나 `figure.crop` 밖 |
| L-CROP-MISSING | warn | 장 `sources` 라벨이 `Table` · `Figure` · `Fig.` · `표` · `그림`을 가리키는데, 그 장(화면 · 패널)에 `figure.crop`도 없고 crop이 있는 장으로 가는 `[[…]]` 링크도 없음 |
| L-IMG-DUP | info | 같은 이미지 파일을 여러 장에서 씀 |
| L-MATH-IN-P | warn | `<p>` 안에 `\[` |
| L-SECTION-SPLIT | warn | 같은 `section`이 떨어져 다시 나옴 |
| L-CLAIM-UNKNOWN | error | 장 `claims`에 원장에 없는 id |
| L-CLAIM-EXPR | error | `expr` 계산값 ≠ `value`(허용 오차 밖) |
| L-CLAIM-FACTOR | error | `factors`의 Π(from/to) 또는 `ratio_of` 비 ≠ `value`(상대 오차 1e-6) |
| L-CLAIM-NOSOURCE | warn | `sources`도 `inputs`도 없음 |
| L-CLAIM-UNUSED | warn | layer main인데 어느 본편 장도 참조하지 않음 |
| L-CLAIM-APPX-ONLY | warn | layer main인데 부록 장만 참조 |
| L-CLAIM-NOEVID | warn | layer evidence인데 참조 장에 근거 패널이 없음 |
| L-COND-SCREEN | warn | `screen_condition` 글이 참조 본편 장 화면 글에 없음 |
| L-CLAIM-DISPLAY | warn | `display` 글이 참조 장 화면(layer main) · 화면이나 패널(layer evidence)에 없음 |
| L-CLAIM-CELL | error | `cells` 형식 오류, 또는 참조 장 표의 그 행 · 열 셀 글 ≠ 원장 값 |
| L-CLAIM-CELL-MISSING | warn | `cells`의 행 · 열이 참조 장(화면 · 패널)의 어느 표에도 없음 |
| L-MAIN-OFFSCREEN | info | layer main인데 `display` · `value` · `cells` · `screen_condition` 어느 글도 참조 장 화면에 없음(패널에만 있으면 layer를 고친다) |
| coverage | info | 원장 요약: 전체 수 · layer별 · 참조된 main 비율(출처 연결률) · expr 재계산 성공 수 · factors · ratio 통과 수 · screen_condition 유지 수 · display 일치 수 · 셀 대조 수 · 화면 대조 불가 main |

빌드 오류(exit 1): E-FIELD(장 필수 필드 · `layout` · `sources` 형식) · E-ID-DRIFT · E-PART-ORDER · E-XREF · E-SCRIPT · E-MATH-TEX · E-MATH-REF · E-MATH-RENDER(`render_math.cjs`가 실패하거나 잘못된 JSON을 냄) · E-CLAIMS(원장을 읽을 수 없음 · `claims` 목록 없음 · id 형식 오류나 중복). 경고: W-V2-FIELD-IGNORED · W-NOTE-OVERRIDE · W-MATH-UNAVAILABLE · W-MATH-SKIPPED(`<svg>` · `<code>` · `<pre>` · `<template>` 안의 수식은 TeX 그대로 남음) · W-IMG-MISSING(`<img src>` 파일 없음) · W-IMG-RESIZE · W-DECK-BYTES · W-NOTES-MISSING(v2인데 `--script` 없이 대본 빈 본편 장) · W-SCRIPT-MISSING(`--allow-missing-notes`로 낮춘 빈 대본). `--strict`면 lint 경고에 더해 빌드 경고 W-MATH-UNAVAILABLE(`--no-math`로 끈 경우 제외) · W-MATH-SKIPPED · W-IMG-MISSING · W-NOTES-MISSING도 exit 1이다.

## 검사 코드 (`check_deck.cjs`)

기존 동작은 그대로다: 위치 인자 `deck.html outdir`, 뷰포트 1440×900 · 860×760 · 390×844, 스크린샷 `{w}-sNN.png`, `review.pdf`, `checks.json`의 `views` · `navigation` · `links` · `brokenLocal` · `errors` · `failures` · `note`. 기존 실패 `{w}: slide N overflow or missing source`는 넘침과 출처 줄 문제를 함께 알린다. 어느 쪽인지는 `views[].slides[]`의 `innerOverflow` · `cardOverflow` · `hasSource`로 보고(출처 줄 문제는 C-SRC-HIDDEN으로도 나온다), 넘침이면 [screen-budget.md](screen-budget.md) 3절 '높이 예산'으로 고친다. Playwright는 `PLAYWRIGHT_MODULE` → `playwright` → `playwright-core` 순서로 찾는다. v1 덱(`window.deckShell` 없음)에서는 v2 전용 검사를 건너뛰고 보고만 한다.

**측정 정의** (1440×900 슬라이드 모드, 장마다 `show` 뒤. 본편 = `data-part="main"`, v1 덱은 전체)

- 보이는 요소: `el.checkVisibility({checkOpacity:true, checkVisibilityCSS:true})`.
- **화면 글**: `.inner` 안 글 노드의 공백 제외 글자 합. `.ey, .scroll-hint, .katex-mathml, template, script, style` 아래는 뺀다(출처 줄 · 근거 패널 · 대본은 `.inner` 밖이라 빠진다). 제목 · 표 · SVG 글 · KaTeX 글 · 캡션은 들어간다.
- **산문**: 화면 글에서 `h2, table, svg, .katex, .math-inline, .math-block, [role="img"], .ev-chip, .tag, .num, .pf-grid, .fx-bars, .fx-terms, .dv-eq, .claim-legend, .verdict, .cap, figcaption` 아래 글을 뺀 것(캡션 · 범례 · 판정 띠는 화면 글에는 든다).
- **문장 수**: `.txt p, .txt li, .vis > p:not(.cap):not(.cond):not(.claim-legend):not(.pair-line):not(.subst), .vis .bx .d, .vis .annotation span, .vis blockquote` 중 서로 조상 관계가 아닌 요소마다 `[.?!。]` 뒤 공백 · 끝 개수. 0개인데 25자 이상이고 다/요/까로 끝나면 1.
- **AU**: [screen-budget.md](screen-budget.md) 4절.
- **주 시각 면적**: `[data-main]`(없으면 가장 큰 AU 뿌리)의 넓이 ÷ 콘텐츠 영역 넓이. 콘텐츠 영역 = `.inner`의 padding 안쪽 넓이(제목 · 본문 칸 포함, 그래서 상한은 split ≈ 0.60 · wide ≈ 0.70). 원문 썸네일(`.crop-thumb`)은 주 시각이 아니다.
- **조건 수** = 보이는 `.cond`, **화면 출처 수** = `.src-line a`(v1은 `.src a`), **표지** = 보이는 `.ev-chip`의 `data-ev`별 수, **제목 줄 수** = `h2` 글의 줄 수(1440 · 390).
- 중앙값 · p90: 정렬 후 index `floor(f·(n−1)+0.5)`.

| 코드 | 종류 | 조건 |
| --- | --- | --- |
| C-VISIBLE | warn | 장 화면 글 > 550 |
| C-VISIBLE-MEDIAN · C-VISIBLE-P90 | warn | 본편 중앙값 > 350 · p90 > 550 |
| C-PROSE | warn | 장 산문 > 200 |
| C-PROSE-MEDIAN · C-PROSE-P90 | warn | 본편 중앙값 > 120 · p90 > 200 |
| C-SENTENCES | warn | 장 문장 > 3 |
| C-AU | warn | AU > 4 |
| C-MAINVIS | warn | result · mechanism 장의 주 시각 면적 < 0.35(목표 ≥ 0.45는 보고) |
| C-COND | warn | `.cond` ≥ 2 |
| C-SRC-IDS | warn | v2 장 화면 출처 링크 > 2 |
| C-TITLE-LINES | warn | 1440 제목 ≥ 3줄 |
| C-SHELL | **fail** | `data-shell="2"`인데 `window.deckShell`이 없음 |
| C-IMG-BROKEN | v2 **fail** / 원격 · v1 warn | 이미지가 열리지 않음(로컬 · data URI는 v2 실패, 원격은 경고) |
| C-SRC-HIDDEN | **fail** | 출처 줄이 없거나 보이지 않음(모든 덱) |
| C-SRC-EMPTY | v2 **fail** | `.src-line`에 이름 있는 출처 링크가 하나도 없음 |
| C-NOTES-MISSING | warn | v2 본편 장에 대본이 없음 |
| C-XREF-BROKEN | **fail** | `href="#sN"`인데 N번째 장이 없음 |
| C-XREF-UNLINKED | warn | 화면 글(링크 밖)에 실제 `data-id`와 같은 토큰 |
| C-SCALE | warn | v2: 1280×800 배율 < 0.8, 1024×768 < 0.75 |
| C-PRESENT | warn | v2: 1920×1080 전체화면 카드 폭 ÷ 화면 폭 < 0.9, 또는 1024×768 전체화면 배율 < 0.79 |
| C-NOTES-ACCESS | v2 **fail** / v1 보고 | 860×760 · 390×844(터치)에서 대본 버튼으로 대본이 보이지 않음 |
| C-PROGRESS | warn | 390×844에서 머리줄 높이 > 20% |
| C-EVIDENCE-TOGGLE | v2 **fail** | `.ev-btn` → 보임 · 포커스 · `ev-open`, Esc → 숨김 · 포커스 복귀 중 하나라도 어긋남 |
| C-EVIDENCE-MISSING | warn | v2 본편 result · mechanism 장에 패널 없음 |
| C-ZOOM | v2 **fail** | 첫 확대 가능 이미지 클릭 → 확대 대화상자, Esc → 닫힘이 안 됨 |
| C-MAIN-END | v2 **fail** | 부록이 있는데 마지막 본편 장에서 → 한 번에 넘어가거나 두 번에도 안 넘어감 |
| C-MATH-FALLBACK | warn | `.math-fallback` 있음(KaTeX 없이 빌드) |
| C-MATH-MATHML | warn | `.katex` 수 ≠ `.katex-mathml` 수 |
| C-MATH-HINT | warn | 390에서 넘치는 `.math-block`인데 안내가 숨겨짐 |
| C-MATH-FONT | warn | 렌더된 KaTeX 글꼴 · 굵기 · 기울기 조합이 내장 글꼴에 없음 |
| C-CROP-GLYPH | warn | `.inner` 안 이미지(썸네일 `.crop-thumb` 제외)의 렌더 글자 높이 < 12px(1440). `data-glyph-px`가 없고 축소율 < 0.5면 '글자 크기 모름' |
| C-CLAIM-LEGEND | warn | `.claim-table`에 `.claim-legend` 없음 |
| C-VERDICT | warn | `.cl-x` 셀이 있는데 같은 장에 `.verdict` 없음 |
| C-PHONE-CARD | warn | 390에서 카드 높이 > 1.3 × 844 |
| C-PHONE-KEYCELL | warn | 390에서 `.em, .cl-hi, .cl-x, [data-key-cell]`이 가로 스크롤 영역 첫 화면 밖 |
| C-BUDGET-SLIDES · C-BUDGET-INTRO · C-BUDGET-TIME · C-NOTES-MINUTES | warn | lint와 같은 식을 DOM으로 계산 |
| C-DECK-BYTES | warn | 파일 > 2 MB |

실패는 `checks.json`의 `failures`에 `CODE: …` 꼴로, 경고는 `warnings: [{code, slide, id, value, limit, msg}]`로 들어간다. 새 키: `shell` · `warnings` · `budget` · `density`(`perSlide` · `summary`) · `scale` · `notesAccess` · `progress` · `math` · `evidence` · `xref` · `crops` · `phone` · `deckBytes`. v2 덱이면 근거 패널을 장마다 한 쪽씩 붙인 `review-evidence.pdf`도 만든다.

## CLI 한눈에

```sh
python3 scripts/build_deck.py IN.json [OUT.html] [--script F]... [--allow-missing-notes] \
  [--lint] [--lint-json F] [--claims F] [--strict] [--katex DIR] [--node PATH] [--no-math] [--resize-images]
#   OUT 없이 --lint만 주면 쓰지 않고 lint만. exit: 0 정상 · 1 오류(빌드 · E-*(E-CLAIMS 포함) · lint error · --strict 경고) · 2 사용법
node scripts/render_math.cjs [--katex DIR] < req.json > res.json      # exit 3 = KaTeX 없음
node scripts/check_deck.cjs DECK.html OUTDIR [--budget-min N] [--strict]
```

환경 변수: `NODE_BIN`, `KATEX_MODULE`, `PLAYWRIGHT_MODULE`, `CHROME_PATH`. 같은 입력이면 빌드 출력은 바이트까지 같다(재현성). 고친 뒤 두 번 빌드해 `cmp`로 확인한다.
