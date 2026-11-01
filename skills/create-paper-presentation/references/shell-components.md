# 셸 화면 부품과 동작 (v2)

모든 부품과 동작은 덱 JSON에 `"shell_version": 2`를 둔 덱(`<html data-shell="2">`)에서 쓴다. **v1 덱에는 아무 변화가 없다.** v2 규칙은 `html[data-shell="2"]`나 아래 새 클래스에만 걸리므로, 옛 덱은 다시 빌드해도 화면이 같다. 기존 부품(`.bx` · `.annotation` · `.flow` · `.hbar-chart` · `.norm-pair` · `.condition-panels` · `.tbl` · `.figure` · `.equation` · `.formula` 등)은 그대로 쓸 수 있다.

AU(주의 단위)는 [screen-budget.md](screen-budget.md) 4절의 규칙으로 센다. 색은 셸의 기존 토큰(`--blue` · `--green` · `--orange` · `--red` · `--gray-s` …)만 쓴다. v2 본문(`.txt p`)은 20px이다.

## 화면 부품

### 근거 표지 `.ev-chip`

- **언제**: 값 · 문장의 증거 종류를 알릴 때. 그 종류가 해당하는 모든 장에, 근거 범위(열 하나 · 카드 하나 · 조건 줄 하나 · 문단 하나)마다 한 번. 패널의 대입 줄 · 인용 옆에도 붙인다. 위계는 [design-and-evidence.md](design-and-evidence.md) '근거 표지 위계'.
- **HTML**: `<span class="ev-chip" data-ev="calc">계산</span>`
- **원문 값과 계산값이 섞인 표**: 범위를 열로 나누고 계산 열 머리에 한 번 붙인다. 셀마다 붙이지 않는다. `rowcards` 표는 휴대폰에서 `thead`가 숨으므로 그 열의 `data-label`에도 라벨 글을 넣는다(예: `data-label="토큰당 KV cache · 계산"`).

```html
<thead><tr><th>모델</th><th class="numcol">KV head <span class="ev-chip" data-ev="config">config</span></th><th class="numcol">토큰당 KV cache <span class="ev-chip" data-ev="calc">계산</span></th></tr></thead>
```

- **종류 · 라벨(글은 이 라벨 그대로)**: `orig` 원문 · `table` 표 값 · `config` config · `calc` 계산 · `est` 추정 · `assume` 가정 · `nd` 미기술 · `interp` 해석 · `hyp` 저자 가설 · `illus` 설명용 · `cite` 인용 원전.
- **주의**: 13px · 600. 원문 · 표 값 · config · 인용 원전 = 회색 테두리, 계산 = 초록, 추정 · 가정 = 주황, 미기술 = 회색 점선, 해석 · 저자 가설 = 파랑, 설명용 = 점선. 제목 안에는 넣지 않는다.
- **AU**: 0

### 조건 줄 `.cond`

- **언제**: 결론을 바꾸는 조건이 있을 때만, 장당 0–1개. 없으면 만들지 않는다.
- **HTML**: `<p class="cond"><span class="ev-chip" data-ev="calc">계산</span> 공개 config 값 · fp16 2 B · K+V · 80층 합산 · batch 1</p>`
- **주의**: 16px, 위 점선. 숨기지 않는 크기다. 표지는 조건 줄 첫머리에. 기본 자리는 `visual`이다: 어디에 두든 AU는 0이지만, `body`(`.txt`)에 두면 그 줄의 문장이 본문 문장 수에 들어간다([screen-budget.md](screen-budget.md) 2절).
- **AU**: 0

### 출처 줄 (빌드가 만듦)

- **언제**: 모든 장. 덱 JSON `sources`와 `src_visible`(기본 2)로 정한다.
- **HTML**: `.src-line`(화면 출처 1–2개 + 나머지 수 `.src-more` 버튼) · `.src-side`(`.src-ids` · `.main-end` · `.ev-btn`). 자세한 마크업은 [deck-json.md](deck-json.md) '빌드 출력'.
- **주의**: 패널이 없으면 출처 전부가 출처 줄에 보인다. `.main-end`는 작은 주황 테두리 라벨('본편 끝'), `.ev-btn`은 작은 둥근 버튼('근거 펼치기 E').

### 근거 패널 `aside.evidence`

- **언제**: result · mechanism 장에는 기본으로 둔다(L-EVIDENCE-MISSING). 원문 인용 · 전체 크기 crop · 기호 풀이 · 대입 → 단위 · 가정 풀이 · 보조 수치. 각 항목 옆에 그 종류의 근거 표지를 붙인다.
- **HTML**: 장 JSON `evidence`에 조각을 쓰면 빌드가 `<aside class="evidence">` 안 `.ev-body`로 넣고, 그 뒤에 '출처 전체'(`.ev-sources`)를 자동으로 붙인다. 안에 권장하는 것: `blockquote.ev-quote[lang]` · `figure.crop` · `.derive` · `p.subst` · 일반 `p` · `ul` · `.table-wrap`.
- **주의**: 결론을 바꾸는 조건, 계산의 일반식, 설계 선택의 이유 한 문장, 근거가 된 원본 그림 · 표는 패널에만 두지 않는다(화면에도 둔다). 패널에는 그 원문 인용 · 대입 · 전체 크기 crop을 더한다.
- **AU**: 화면 AU에 들어가지 않는다.

### 단계 · 유도 카드 `.derive`

- **언제**: 배정 항목의 기제 · 유도를 본편에서 보일 때.
- **HTML**:

```html
<ol class="derive" data-main aria-label="SwiGLU 폭 유도 4단계">
 <li><span class="dv-eq">\(2 \cdot d \cdot 4d = 8d^2\)</span><span class="dv-why">ReLU FFN: 행렬 2개 (d×4d, 4d×d)</span></li>
 <li><span class="dv-eq">\(3 \cdot d \cdot h = 3dh\)</span><span class="dv-why">SwiGLU FFN: 행렬 3개</span></li>
 <li><span class="dv-eq">\(3dh = 8d^2\)</span><span class="dv-why">두 FFN의 파라미터 수를 같게 둔다</span></li>
 <li><span class="dv-eq">\(h = \tfrac{8}{3}d = \tfrac{2}{3} \cdot 4d\)</span><span class="dv-why">원문의 (2/3)·4d</span></li>
 <li class="dv-end">답: 행렬이 하나 늘어도 폭을 2/3로 줄이면 FFN 크기는 그대로다</li>
</ol>
```

- **주의**: 번호는 CSS 카운터(`.dv-end`는 번호 없는 강조 줄). 단계 ≤ 4(`.dv-end` 제외), 넘으면 장을 나눈다(L-DERIVE-STEPS). 한국어 이유는 TeX 밖 `.dv-why`에. 실제 숫자 대입(예: d = 4,096 → 10,922.7)은 패널의 `p.subst`.
- **AU**: 1

### 요인 분해 카드 `.factor`

- **언제**: 정량 결과가 여러 요인의 곱 · 합일 때. 최종 수치만 비교하지 않는다.
- **HTML**:

```html
<figure class="factor" data-main role="img" aria-label="토큰당 KV cache 2,560 KiB에서 320 KiB. KV head 64에서 8로 8배 감소, 층과 head 차원은 동일">
 <div class="fx-bars">
  <div class="fx-row"><span class="fx-name">LLaMA-65B</span><span class="fx-track"><i style="width:100%"></i></span><b class="fx-val">2,560 KiB</b></div>
  <div class="fx-row fx-new"><span class="fx-name">Llama 2-70B</span><span class="fx-track"><i style="width:12.5%"></i></span><b class="fx-val">320 KiB</b></div>
 </div>
 <ol class="fx-terms">
  <li class="fx-chg"><span class="fx-k">KV head</span><span class="fx-ab">64 → 8</span><b class="fx-r">÷ 8</b></li>
  <li class="fx-same"><span class="fx-k">층</span><span class="fx-ab">80 → 80</span><b class="fx-r">동일</b></li>
  <li class="fx-same"><span class="fx-k">head 차원</span><span class="fx-ab">128 → 128</span><b class="fx-r">동일</b></li>
 </ol>
 <span data-math="kv"></span>
 <figcaption class="fx-sum">합: ÷ 8 → 2,560 KiB가 320 KiB</figcaption>
</figure>
```

- **주의**: 막대는 0 기준 같은 축(폭 % = 값 ÷ 큰 값). 변하지 않은 요인 `fx-same`은 작고 흐린 '동일' 표지. 일반식은 화면에 둔다: 장 `math` 필드에 넓은 판과 `tex_narrow`를 적고 카드 안에 `<span data-math="kv"></span>`로 부른다(긴 식을 인라인 `\( … \)`로 캡션에 넣으면 휴대폰에서 잘린다). 기호 풀이와 대입 계산은 패널 `p.subst`에 둔다. 원장 `factors`와 값이 같아야 한다. `fx-sum` 줄은 선택이다: 제목과 항 카드(셸이 그리는 ×)가 이미 곱을 말하면 빼고 그 자리에 일반식을 둔다. 넓은 배치에서 제목 1줄 · 본문 1줄 · 일반식 · 조건 줄 · 썸네일에 `fx-sum`까지 두면 1440×900에서 넘친다(예시 2-3).
- **`.fx-r` 쓰기**: 넓은 화면에서 셸이 항 사이에 '×'를 그린다. 첫 항은 `÷ 8`처럼 써도 되지만, 둘째 항부터는 연산 기호 없이 배율만 쓴다(`2배` · `1/5` · `동일`). 요인이 반대로 움직이는 예(Llama 2-13B → 70B, 800 → 320 KiB):

```html
<ol class="fx-terms">
 <li class="fx-chg"><span class="fx-k">층</span><span class="fx-ab">40 → 80</span><b class="fx-r">2배</b></li>
 <li class="fx-chg"><span class="fx-k">KV head</span><span class="fx-ab">40 → 8</span><b class="fx-r">1/5</b></li>
 <li class="fx-same"><span class="fx-k">head 차원</span><span class="fx-ab">128 → 128</span><b class="fx-r">동일</b></li>
</ol>
<figcaption class="fx-sum">합: 2배 × 1/5 = 0.4배 → 800 KiB가 320 KiB</figcaption>
```

  원장은 이전 ÷ 새것으로 적는다: `value` 2.5 = `ratio_of: ["kv-13b", "kv-70b"]`, `factors` (40 ÷ 80) × (40 ÷ 8) × (128 ÷ 128) = 2.5([claim-ledger.md](claim-ledger.md) '다시 계산하기').
- **AU**: 1

### 주장 주석 표 · 범례 · 판정 띠 `.claim-table`

- **언제**: 평가 절 Table마다 첫 개요 장. 본문 주장이 표와 맞는지 보일 때.
- **HTML**:

```html
<div class="claim-table" data-main>
 <div class="table-wrap"><table class="tbl ct">
  <thead><tr><th>모델</th><th class="numcol">BoolQ</th><th class="numcol">PIQA</th><th class="numcol">SIQA</th><th class="numcol">HellaSwag</th><th class="numcol">WinoGrande</th></tr></thead>
  <tbody>
   <tr class="ct-vs"><td>Chinchilla 70B</td><td class="numcol cl-vs">83.7</td><td class="numcol cl-vs">81.8</td><td class="numcol cl-vs">51.3</td><td class="numcol cl-vs">80.8</td><td class="numcol cl-vs">74.9</td></tr>
   <tr class="ct-focus"><td>LLaMA 65B</td><td class="numcol cl-x">85.3</td><td class="numcol cl-hi">82.8</td><td class="numcol cl-hi">52.3</td><td class="numcol cl-hi">84.2</td><td class="numcol cl-hi">77.0</td></tr>
  </tbody>
 </table></div>
 <p class="claim-legend"><span><i class="cl-hi"></i>본문이 강조한 우위</span><span><i class="cl-vs"></i>본문의 비교 대상</span><span><i class="cl-x"></i>본문 주장과 표 불일치</span><span>원문 굵게는 옮기지 않음</span></p>
 <div class="verdict"><span class="vd-claim">저자: “BoolQ를 뺀 모든 항목에서 Chinchilla-70B를 앞선다”</span><span class="vd-res vd-no">표: BoolQ도 앞섬 +1.6 (85.3 − 83.7) · 5개 중 5개</span></div>
</div>
<p class="cap">원문 · LLaMA v1 Table 3 (p.4) · 두 행 · Chinchilla가 보고한 5개 열 / 생략: 다른 모델 · ARC · OpenBookQA / 칠한 칸 = 발표자 표시</p>
<figure class="crop crop-thumb only-wide" data-au="0"><img src="figures/llama1-table3.png" alt="LLaMA v1 Table 3 원본(눌러서 확대)" width="134" data-glyph-px="14"></figure>
```

- **셀 상태**: `cl-hi` 본문이 강조한 우위 · `cl-vs` 본문의 비교 대상 · `cl-par` '비슷하다'고 쓴 곳 · `cl-x` 본문 주장과 표 불일치. 발표자 강조는 `.em`(파랑 칸)이다. **행**: `ct-vs` 비교 대상 행 · `ct-focus` 주인공 행. **판정**: `vd-ok` 일치 · `vd-part` 부분 · 예외 · `vd-no` 불일치.
- **판정 띠 줄**: 저자 주장 하나에 `.verdict` 하나, 3줄 이하. `vd-claim` = '저자:' 주어 + 예외는 같은 줄, `vd-res` = 비교 칸 값 · 차이값 · 판정. 주장이 둘이면 `.verdict`를 둘 쓴다. 예(LLaMA v1 Table 7): `저자: “GSM8k에서 Minerva-62B를 앞선다”` / `표: 다수결(k = 100)에서만 +1.2 (69.7 − 68.5) · 다수결 없이는 −1.5 (50.9 − 52.4)`(`vd-part`). 저자 주장은 `body`(`.txt`)가 아니라 이 줄에 둔다.
- **판정 띠를 둘 때**: 화면에 그 표에 대한 저자 주장이 있으면 늘(`vd-ok`도). 원문이 그 표에 대해 주장하지 않으면 띠 대신 캡션에 '본문 주장 없음'을 적고 `cl-*` 칸을 쓰지 않는다(필요하면 `.em`). `cl-x`가 있으면 판정 띠는 반드시(C-VERDICT).
- **범례**: 반드시 둔다(C-CLAIM-LEGEND). 실제로 쓴 상태만 적고, 원문 굵게 줄은 늘 적는다(셀 안 `<b>`로 옮겼으면 "굵게 = 원문 굵게", 아니면 "원문 굵게는 옮기지 않음"). `.em`을 썼으면 "파랑 칸 = 발표자 강조"를 더한다. 범례 · 판정 띠 · 캡션 글은 화면 글에는 들지만 산문에서는 빠진다([screen-budget.md](screen-budget.md) 3절).
- **평가표가 아닌 표**: 설정 · 사양 표(예: Llama 2 Table 1)라도 저자가 그 수치에 대해 주장하면 같은 부품을 쓴다. 예: 저자 "40% more total tokens" / 표: 1.4T → 2.0T +43%, 1.0T → 2.0T +100%(`vd-part`).
- **주의**: 칠한 칸은 발표자 표시이고 원문 강조가 아니다. 셀 값 · 머리글 · 단위 · shot은 원문 그대로, 캡션에 원문 · 쪽 · 포함 · 생략 · 발표자 표시. 원본 표는 썸네일로 화면에, 전체 크기 crop은 패널에('원문 crop').
- **AU**: 1(썸네일 0)

### 전후 비교 쌍 `.ba`

- **언제**: 구조 변경(무엇이 어디서 달라졌나).
- **HTML**: `<div class="ba" data-main><div class="ba-side ba-before"><span class="ba-tag">원 Transformer</span>…</div><div class="ba-arrow" aria-hidden="true">→</div><div class="ba-side ba-after"><span class="ba-tag">LLaMA</span>…</div></div>`. 바뀐 곳은 `.ba-diff`(강조), 같은 곳은 `.ba-same`(흐리게).
- **주의**: 좁은 폭에서 세로로 쌓이고 화살표가 90° 돈다. 같은 연산은 같은 이름 · 같은 위치로 그린다. 예: post-norm `\(\mathrm{LN}(x + F(x))\)` 대 pre-norm `\(x + F(\mathrm{RMSNorm}(x))\)`.
- **AU**: 1(안에 SVG가 둘이어도 한 묶음)

### 프로필 카드 `.profile`

- **언제**: 표지 · 소개 장에서 두 모델을 나란히.
- **HTML**: `<div class="profile pf-prev"><div class="pf-head"><strong>LLaMA 1</strong><span>arXiv 2302.13971 · 2023-02</span></div><dl class="pf-grid"><div><dt>크기</dt><dd>6.7B · 13.0B · 32.5B · 65.2B</dd></div>…</dl>[<p class="pf-note">…</p>]</div>`. 지금 논문 쪽은 `pf-cur`.
- **주의**: 두 장을 `data-au="1"` 묶음(예: `<div class="g c2" data-main data-au="1">`) 안에 나란히 둔다.
- **AU**: 묶음 1

### 유지 · 바꿈 · 미기술 표 (정리 장)

- **언제**: 정리 장. 구성요소마다 이전 → 이 논문, 유지 · 바꿈 · 미기술, 원문 이유를 한 줄로.
- **HTML**: 셸의 `.tbl`을 쓴다. 열은 `구성요소 | 이전 | 이 논문 | 유지/바꿈/미기술 | 원문 이유`.

```html
<div class="table-wrap" data-main><table class="tbl rowcards">
 <thead><tr><th>구성요소</th><th>LLaMA 1</th><th>Llama 2</th><th>판정</th><th>원문 이유</th></tr></thead>
 <tbody>
  <tr><td data-label="구성요소">정규화 [[@norm]]</td><td data-label="LLaMA 1">pre-norm + RMSNorm</td><td data-label="Llama 2">같음</td><td data-label="판정">유지</td><td data-label="원문 이유">LLaMA 1 설정을 따른다고만 씀 <span class="ev-chip" data-ev="nd">미기술</span></td></tr>
  <tr><td data-label="구성요소">attention [[@kv-cache]]</td><td data-label="LLaMA 1">MHA</td><td data-label="Llama 2">34B · 70B만 GQA</td><td data-label="판정">바꿈</td><td data-label="원문 이유">큰 모델의 추론 확장성</td></tr>
 </tbody>
</table></div>
```

- **주의**: 줄마다 해당 장 상호참조를 단다. 원문이 이유를 밝히지 않으면 `미기술` 표지, 원문이 유지 · 변경 여부 자체를 적지 않았으면 판정 칸이 `미기술`. 이유 칸은 풀어 쓴 한 구절이고, 원문 인용은 패널에. 휴대폰에서는 `rowcards`로 행 카드가 된다. 행은 5개 이하(screen-budget.md 3절 높이 예산).
- **AU**: 1

### 두 열 요약 `.summary-cols`

- **언제**: 열린 질문 · 토론 장의 '관찰' · '열린 질문' 두 열, 또는 짧은 두 묶음 요약. 유지 · 바꿈 · 미기술 정리에는 위 표를 쓴다(두 열로는 미기술과 이유가 빠진다).
- **HTML**: `<div class="summary-cols" data-main><div class="sc-col"><h3>관찰</h3><ul><li>RQ1 · 70B는 GQA로 토큰당 KV cache가 65B의 1/8 [[@kv-cache]]</li></ul></div><div class="sc-col"><h3>열린 질문</h3><ul><li>RMSNorm을 고른 이유는? <span class="ev-chip" data-ev="nd">미기술</span></li></ul></div></div>`
- **주의**: 줄마다 해당 장 상호참조를 단다. 좁은 폭에서 한 열.
- **AU**: 1

### 비교 짝 줄 `.pair-line`

- **언제**: 비교 대상이 있는 덱의 표지 · 질문 목차.
- **HTML**: `<p class="pair-line"><b>비교 짝</b> LLaMA-65B ↔ Llama 2-70B · 가중치 계승 아님</p>`
- **주의**: 덱 JSON `compare_pair`와 같은 글(L-PAIR).
- **AU**: 0(어디에 두든). `body`에 두어도 되지만, 그 줄이 문장(마침표 등으로 끝나거나 25자 이상이면서 '다 · 요 · 까'로 끝남)이면 본문 문장 수에 든다. 예의 '비교 짝 … · 가중치 계승 아님'은 문장이 아니라 0이다.

### 대입 줄 `p.subst`

- **언제**: 식에 실제 숫자를 넣은 산술 사슬. 주로 근거 패널.
- **HTML**: `<p class="subst">2 × 80 × 8 × 128 × 2 B = 327,680 B = 320 KiB</p>`
- **주의**: 숫자 정렬(`tabular-nums`), 회색 바탕. 수식(KaTeX)으로 쓰지 않고 글로 쓴다.

### 원문 인용 `blockquote.ev-quote`

- **언제**: 이유 · 주장을 담은 원문 문장. 주로 근거 패널.
- **HTML**: `<blockquote class="ev-quote" lang="en">“We use a dimension of 2/3 4d instead of 4d as in PaLM.”<cite>LLaMA v1 §2.2 (p.3)</cite></blockquote>`

### 원문 crop `figure.crop` · 썸네일 `figure.crop.crop-thumb`

- **언제**: 주장이 원문 Figure · Table에 기대는 장. 원본은 화면에 있다. 자리는 셋이다.
  - **화면 주 시각**: 장의 주제가 원문 자체(예시 그림 따라가기, 모양이 곧 주장인 그래프)이거나, 필요한 칸만 잘라 렌더 글자 12px 이상으로 읽힐 때. `data-main`을 붙인다.
  - **화면 썸네일**: HTML로 다시 그린 표 · 도식이 주 시각일 때, 캡션 아래에 작게. '원본이 여기 있다'는 표시이고 눌러서 확대해 읽는다.
  - **근거 패널**: 전체 크기 crop과 정식 캡션. 화면이 주 시각이든 썸네일이든 늘 둔다.
- **HTML**(주 시각 · 패널): `<figure class="crop"><img src="figures/llama1-table2.png" alt="LLaMA v1 Table 2" data-glyph-px="14" data-display-width="560"><figcaption>원문 · LLaMA v1 Table 2 (p.3) · 전체 / 발표자 표시 없음</figcaption></figure>`
- **HTML**(썸네일): `<figure class="crop crop-thumb only-wide" data-au="0"><img src="figures/llama1-table2.png" alt="LLaMA v1 Table 2 원본(눌러서 확대)" width="200" data-glyph-px="14"></figure>`. 바로 위 캡션이 원문 · 쪽을 말하지 않거나 자리가 넉넉하면 `<figcaption>원본 · 눌러서 확대</figcaption>`을 더한다.
- **주의**: 클릭 · Enter · Space로 확대된다. 화면(`visual`)의 crop은 `data-glyph-px`(원본 PNG의 숫자 높이 px) 필수(L-CROP-MAIN). 주 시각 crop은 렌더 글자 높이 12px 이상(C-CROP-GLYPH), 썸네일(`.crop-thumb`)은 이 검사에서 뺀다. 썸네일 크기는 **높이 약 60px**로 맞춘다: `width` = 60 × 원본 폭 ÷ 원본 높이(셸이 `height:auto`라 `height` 속성은 듣지 않는다). 예: Table 2(724×214) 200 · Table 3(845×380) 134 · Table 7(442×523) 51. 정식 캡션은 패널 crop에 두고, 썸네일이 쓰는 약 60px + 간격 14px를 높이 예산([screen-budget.md](screen-budget.md) 3절)에 넣는다. `only-wide`로 휴대폰(≤ 520px)에서는 숨긴다(카드 높이만 늘리므로, 휴대폰은 패널의 전체 크기 crop으로 본다). 정식 캡션은 '원문 · {자료} {표/그림} (p.N) · {포함} / 생략: {…} / {발표자 표시}'. `data-display-width`와 `--resize-images`로 덱 크기를 줄인다. 썸네일에는 `data-display-width`를 두지 않는다(눌러서 확대했을 때 읽히도록 원본 해상도로 내장). 같은 파일이 패널에도 있으면 두 번 내장되므로 crop은 필요한 칸만 자른다.
- **같은 원본이 여러 장에**: 그 원본이 주장의 근거인 첫 장의 화면에 두고, 값만 빌리는 다른 장은 패널에서 그 장으로 링크(`[[@key]]`)한다. 출처 라벨이 Table · Figure를 가리키는데 그 장에 crop도 crop이 있는 장으로 가는 링크도 없으면 lint가 알린다(L-CROP-MISSING).
- **HTML판만 읽었을 때**: HTML 렌더 캡처를 쓰고 캡션에 'HTML판 렌더, PDF crop 아님'(design-and-evidence.md '출처 라벨').
- **AU**: 주 시각 1, 썸네일 0(`data-au="0"`, 주 시각 면적에도 넣지 않음). 패널 crop은 화면 AU 밖.

### 정의 `dfn`

- **언제**: 약어 · 기호 · 모델 이름을 처음 쓰는 장.
- **HTML**: `<dfn>KV cache</dfn>는 생성 중 이전 토큰의 K · V를 저장해 두는 메모리입니다.`
- **주의**: v2에서 기울이지 않고 굵게. lint 첫 등장 정의로 인정된다(L-DEFINE-FIRST).

### 주 시각 표지 `data-main` · AU 직접 지정 `data-au`

- `data-main`: 아무 요소에 붙여 그 장의 주 시각을 알린다. 주 시각 면적(콘텐츠 영역 대비, 목표는 [screen-budget.md](screen-budget.md) 3절)의 기준이다. 장마다 하나.
- `data-au="n"`(0–4): 묶음 하나를 n으로 세고 안쪽은 세지 않는다. 여러 상자가 한 시각 묶음일 때, 그리고 원문 썸네일(`data-au="0"`)에 쓴다.

### 수식 마크업 (빌드가 만듦)

- `\( … \)` → `<span class="math-inline">`, `\[ … \]` → `<span class="math-block">`, `math` 자리표시 + `tex_narrow` → `.math-block[data-has-narrow]` 안 `.math-wide`와 `<template class="math-narrow">`. KaTeX가 없을 때는 `<code class="math-fallback">`.
- 휴대폰(≤ 520px, 읽기 모드)에서는 좁은 판이 `.math-narrow-live`로 바뀌어 보인다. 좁은 판이 없는 긴 식은 가로 스크롤 + 안내 "↔ 수식을 좌우로 밀어 끝까지 보세요."

### 휴대폰 표 · 도식

- `table.tbl.sticky1`: `.table-wrap`이 가로로 넘칠 때 첫 열을 고정한다. 주인공 열(예: Llama 2-70B)은 둘째 열에 둔다.
- `table.tbl.rowcards` + 모든 `td[data-label]`: ≤ 520px 읽기 모드에서 행을 카드로 바꾼다(`thead` 숨김, 칸마다 `data-label` 표시).
- `.only-wide` · `.only-narrow`: ≤ 520px에서는 `.only-narrow`만, 그 밖에서는 `.only-wide`만 보인다. 세로로 다시 배치한 도식에 쓴다.
- 강조 셀(`.em` · `.cl-hi` · `.cl-x` · `[data-key-cell]`)이 390px 첫 화면 밖이면 경고(C-PHONE-KEYCELL), 카드 높이가 화면의 1.3배를 넘으면 경고(C-PHONE-CARD).
- **고르는 순서**: 강조 셀이 한 열에만 있으면 `sticky1`(그 열을 둘째 열로). 두 열 이상에 있으면(예: `cl-x` 열과 `.em` 열) `sticky1`로는 한 열만 첫 화면에 들어오므로 `rowcards`를 쓴다. `rowcards` 카드가 1.3배를 넘으면 ① 비교 짝을 한 행으로 합쳐 행 수를 줄이고 ② 범례를 실제로 쓴 상태만 남기고 ③ 그래도 넘으면 장을 나눈다. 캡션의 원문 · 쪽 · 포함 · 생략 · 발표자 표시는 줄이지 않는다.

## 동작

### 키 지도

| 키 | 동작 |
| --- | --- |
| ← → PageUp PageDown Home End Space | 장 이동(본편 끝 규칙 적용) |
| N | 대본 켜기 · 끄기 |
| E | 현재 장 근거 패널 열기 · 닫기(한글 자판에서도 동작) |
| F | 전체화면 |
| Esc | 확대 → 근거 패널 순으로 닫기(전체화면 해제는 브라우저) |

입력칸 · select · contenteditable에서는 키를 무시한다. 가로로 넘치는 표 · 도식 · 수식(`.table-wrap` · `.diagram-scroll` · `.math-block`)에 포커스가 있으면 방향키는 그 영역의 스크롤에 쓰인다.

### 근거 패널

- `.ev-btn` · `.src-more` 클릭이나 E 키로 연다. 열면 패널에 포커스가 가고(`.src-more`로 열면 '출처 전체'로 스크롤), 장에 `ev-open`이 붙는다. Esc나 '닫기'로 닫으면 포커스가 `.ev-btn`으로 돌아간다. 장을 옮기면 닫힌다.
- 패널이 없는 장에서 E를 누르면 "이 장은 근거 패널이 없습니다"가 2초 보인다.
- 슬라이드 모드: 장 오른쪽 62%를 덮는 흰 패널(자체 세로 스크롤). 포커스가 패널 안이고 패널이 넘치면 ↑ ↓ PageUp PageDown Space는 패널 스크롤에 쓰이고, ← →는 장 이동이다.
- 읽기 모드: 카드 아래 블록으로 펼쳐진다.
- 인쇄: 기본 인쇄는 장마다 1쪽(패널 · 대본 · 버튼 숨김). `?print=evidence` URL이나 `deckShell.printWith({evidence:true})`이면 패널이 있는 장은 카드 1쪽 + 패널 1쪽으로 인쇄한다.

### 대본

- 이동줄의 '대본' 버튼(`#notes-nav`)과 N 키. 모든 폭 · 터치 기기에서 열 수 있다(C-NOTES-ACCESS). 떠 있는 옛 대본 버튼은 v2에서 숨긴다.
- 켜짐 상태를 저장하지 않는다(새로 열면 꺼진 상태).
- 슬라이드 모드에서는 덮개로, 읽기 모드에서는 현재 장 아래 블록으로 보인다.

### 전체화면

- 이동줄 '전체화면'(`#fs`) 버튼이나 F 키. 머리줄을 숨기고 배율 상한을 4로 올린다. 이동줄은 카드 아래 얇은 띠로 자리를 따로 차지하고(카드를 덮지 않음), 2초 움직임이 없으면 투명해진다. 커서도 2초 뒤 숨는다. 포커스는 무대로 간다.
- 목표: 1920×1080에서 카드 폭 ≥ 화면 폭의 90%(C-PRESENT). 휴대폰 폭(≤ 520px)에서는 버튼을 숨긴다.
- 일반 배율은 v1 식 그대로다(1280×800 ≈ 0.87, 1024×768 ≈ 0.77). 프로젝터에서 더 크게 보려면 전체화면을 쓴다.

### 진행 표시 · 장 선택 · 본편 끝 · 상호참조

- **진행 표시 접기**: 현재 장이 있는 섹션만 라벨 + 점으로, 나머지 섹션은 '라벨 n' 접힌 버튼(누르면 그 섹션 첫 장)으로 보인다. 부록 섹션들은 '부록 n' 버튼 하나로 합친다. 휴대폰에서는 한 줄 가로 스크롤(목표: 390×844에서 머리줄 ≤ 20%, C-PROGRESS).
- **장 선택 목록**: '본편' · '부록' · '검토 기록' 묶음으로 나뉘고, 항목 글은 `{ID} · {제목}`.
- **본편 끝**: 마지막 본편 장에서 → · PageDown · Space를 처음 누르면 넘어가지 않고 "본편 끝 — 한 번 더 누르면 부록"을 4초 보인다. 4초 안에 다시 누르면 부록으로 간다. 그 장의 '다음' 버튼은 '부록 →'이고 바로 넘어간다. End · 장 선택 · 점은 그대로(C-MAIN-END).
- **상호참조 되돌아가기**: `a.xref`를 누르면 대상 장으로 가고, 이동줄에 '← {이전 ID}' 버튼(`#xref-back`)이 생긴다. 누르면 돌아가고, 다른 방법으로 이동하면 사라진다.

### crop 확대

`figure.crop img` · `.evidence img` · `img[data-zoom]`은 클릭 · Enter · Space로 확대 대화상자(`#zoom-dlg`)를 연다. 대화상자 안을 누르면 '화면에 맞춤 ↔ 원본 크기'가 바뀐다. Esc · 닫기로 닫으면 포커스가 이미지로 돌아간다. 열린 동안 장 이동 키는 막힌다(C-ZOOM).

### 시험 고리

`window.deckShell = {version: 2, current(), show(i), present(on), toggleEvidence(open?), toggleNotes(on?), printWith(opts)}`. 기존 `window.deckCheck()`는 그대로이고, v2에서는 항목마다 `id` · `part` · `hasEvidence` · `srcVisible`이 덧붙는다. `check_deck.cjs`가 이 고리로 패널 · 대본 · 전체화면 · 본편 끝을 시험한다.

## 휴대폰 규칙 요약

- 휴대폰과 높이가 낮은 화면은 한 장씩 세로로 읽는 읽기 모드다. 다음 장은 맨 위에서 시작한다.
- 표: 강조 셀이 한 열이면 첫 열 고정(`sticky1`) + 주인공 열은 둘째 열, 두 열 이상이면 행 카드(`rowcards`). 강조 셀이 첫 화면 안에 보이게 한다.
- 도식: 세로 변형(`.only-narrow`)을 따로 두거나 HTML 도식을 쓴다. SVG를 줄여서 해결하지 않는다.
- 수식: `tex_narrow`(등호 단위 줄바꿈), 안 되면 가로 스크롤 + 안내.
- 카드 높이 ≤ 화면의 1.3배. 넘으면 행을 짝 행으로 합치고 범례를 쓴 상태만 남기고, 그래도 넘으면 장을 나누거나 층을 옮긴다(캡션 규율은 줄이지 않는다).
- 대본 · 근거 패널은 카드 아래 블록으로 펼쳐진다.
