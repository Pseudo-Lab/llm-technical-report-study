# 근거 원장 `claims.json`

## 왜 · 언제 · 어디에

- **왜**: 화면 · 대본 · 근거 패널 · 부록은 같은 근거를 다른 밀도로 쓴다. 숫자와 주장을 한 원장에 먼저 적어 두면 화면을 줄여도 근거가 떨어져 나가지 않고, 어느 층에 무엇이 있어야 하는지 lint가 확인할 수 있다.
- **언제**: 장을 설계하기 전, 읽기 지도와 원문을 읽은 직후. 장을 쓰면서 새 숫자가 생기면 원장에 먼저 더한다.
- **어디에**: 덱 JSON 옆. 덱 JSON의 `claims_file`(덱 JSON 폴더 기준 상대 경로)로 가리킨다. 빌드 인자 `--claims FILE`이 있으면 그쪽이 우선한다. 예시는 [example-claims.json](../assets/example-claims.json).

## 형식

```json
{
 "deck": "논문 슬라이드 예시 — LLaMA 1 → Llama 2",
 "claims": [
  {
   "id": "kv-70b",
   "statement": "Llama 2-70B 토큰당 KV cache는 320 KiB",
   "kind": "calc",
   "layer": "main",
   "scope": "KV cache",
   "value": 327680,
   "unit": "B",
   "display": "320 KiB",
   "expr": "2*80*8*128*2",
   "formula": "2 \\times L \\times n_{kv} \\times d_h \\times b",
   "conditions": ["fp16 2 B", "K+V", "80층 합산", "batch 1"],
   "inputs": ["l2-70b-config"],
   "importance": {"technical": "high", "presentation": "high"},
   "checks": ["head 차원 128 = 8,192 ÷ 64"]
  }
 ]
}
```

| 필드 | 필수 | 뜻 |
| --- | --- | --- |
| `id` | 예 | `^[a-z0-9][a-z0-9-]*$`, 덱 안에서 유일. 장 `claims`가 이 값을 가리킨다 |
| `statement` | 예 | 원자적 주장 하나(아래 '원자적 주장') |
| `kind` | 예 | 증거 종류(아래 표) |
| `layer` | 예 | 이 주장이 있어야 하는 가장 얕은 층: `main` · `evidence` · `notes` · `appendix` |
| `scope` | 권장 | 배정 블록 항목 이름. 장 `term`과 같은 어휘 |
| `value` · `unit` · `display` | 수치일 때 | 값(계산 가능한 기본 단위), 단위, 화면 표기(예: 327680 · `B` · `320 KiB`) |
| `expr` | 선택 | 산술식. 숫자 · `+ - * / ( ) .` · 공백만. lint가 다시 계산해 `value`와 비교 |
| `tol` | 선택 | 허용 오차(절대값). 기본 1e-9 × max(1, \|value\|) |
| `formula` | 선택 | TeX 식(근거 패널 · 부록에서 같은 식을 쓴다) |
| `conditions` | 수치일 때 권장 | 모델 · stage · task · metric · shot · sampling · dtype · 합산 범위 등 |
| `screen_condition` | 선택 | 결론을 바꾸는 조건 한 가지. 이 글이 참조 장 화면에 있어야 한다 |
| `inputs` | 계산 · 판정이면 | 이 값의 근거가 된 다른 claim id |
| `sources` | 원문 · 표 · config · 인용이면 | `[{"label", "url"}]`. 라벨은 판본 · 절/표 · 쪽(예: `LLaMA v1 Table 3 (p.4)`) |
| `importance` | 권장 | `{"technical": "high\|medium\|low", "presentation": "high\|medium\|low"}` |
| `checks` | 선택 | 원문 사실 · 계산 가정 대조 기록(아래 '충돌 검증') |
| `cells` | 표 값이면 권장 | `{"행\|열": "원문 셀 글"}`(예: `{"LLaMA 65B\|BoolQ": "85.3"}`). lint가 참조 장(화면 · 패널)의 HTML 표에서 그 칸을 찾아 글을 대조한다. 행은 첫 열(또는 첫 두 열을 이은 글), 열은 머리글이나 `data-label` |
| `ratio_of` | 선택 | `[A, B]`: `value` = A의 value ÷ B의 value |
| `factors` | 선택 | `[{"name", "from", "to"}]`: Π(from ÷ to) = `value`. from = 이전, to = 새것이므로 `value`는 **이전 ÷ 새것** |

## 증거 종류와 표지

| `kind` | 뜻 | 화면 · 패널 표시 |
| --- | --- | --- |
| `orig` | 원문 문장 | 출처 줄로 충분(표지 없어도 됨) |
| `table` | 원문 표 값 | 출처 줄로 충분(표지 없어도 됨) |
| `config` | 공개 설정 파일 값 | `config` 표지 |
| `calc` | 발표자 계산 | `계산` 표지 |
| `est` | 추정 | `추정` 표지 |
| `assume` | 계산 가정 | `가정` 표지 |
| `nd` | 원문 미기술 | `미기술` 표지 |
| `interp` | 발표자 해석 | `해석` 표지 |
| `hyp` | 저자 가설 | `저자 가설` 표지 |
| `illus` | 설명용 예 | `설명용` 표지 |
| `cite` | 인용 원전 | `인용 원전` 표지 |
| `verdict` | 본문 주장 대 표 판정 | 표지 대신 장에 `.verdict` 요소 |

표지 HTML과 위계는 [design-and-evidence.md](design-and-evidence.md)의 '근거 표지 위계'.

## 층 배정: 두 가지 중요도

기술적 중요도(정확히 이해하는 데 필요한가)와 발표 중요도(청중이 이 장에서 가져가야 하나)를 따로 매긴다.

| 경우 | `layer` |
| --- | --- |
| 결론을 바꾸는 조건(dtype · shot · 다수결 여부 · 합산 범위 등) | 중요도와 상관없이 화면: 그 조건이 붙는 수치 claim의 `screen_condition`에 적어 조건 줄에 남긴다(조건을 따로 claim으로 두면 `main`) |
| 발표 중요도 high | `main` (화면) |
| 기술 중요도 high · 발표 중요도 낮음 | `evidence` (근거 패널) |
| 설명 방법 · 예시 · 이전 장 연결 | `notes` (대본) |
| 재현 · 다른 크기 · 다른 조건 계산 | `appendix` (부록) |

**주장 성립에 필수인 정보는 `appendix`에 두지 않는다.** 예: Llama 2-70B config 값(층 80 · KV head 8 · head 차원 128)은 기술 high · 발표 low라 `evidence`, 토큰당 320 KiB와 8배 감소는 `main`, 2,048 토큰 환산 640 MiB는 `appendix`.

## 원자적 주장

- `statement` 하나에 숫자 하나, 주장 하나. 접속사로 두 사실을 잇지 않는다.
  - 나쁨: "65B는 토큰당 2,560 KiB이고 70B는 320 KiB라 8배 줄었다"
  - 좋음: `kv-65b` "LLaMA-65B 토큰당 KV cache는 2,560 KiB" · `kv-70b` "Llama 2-70B 토큰당 KV cache는 320 KiB" · `kv-ratio` "토큰당 KV cache 감소 8배는 KV head 64 → 8에서 모두 나온다"
- 저자의 문장은 '저자:' 주어로 적는다(예: `t3-claim-chinchilla` "저자: LLaMA-65B는 BoolQ를 뺀 모든 보고 항목에서 Chinchilla-70B를 앞선다"). 표 값은 별도 `table` claim, 둘의 대조는 `verdict` claim으로 나눈다.
- 한 장에 `main` claim이 서로 독립인 둘 이상이면 장을 나눌지 먼저 검토한다.

## 충돌 검증

표지를 붙였다고 계산이 맞아지지 않는다. 계산 claim마다 아래를 원문 · config와 대조하고 `checks`에 적는다.

- 층 수 · head 수 · KV head 수 · head 차원(= hidden ÷ head 수인지)
- dtype 바이트(fp16 · bf16 = 2 B)와 단위(KiB = 1,024 B, KB = 1,000 B)
- cache 정의: K+V 둘 다인가, 층 전체 합산인가, batch · 문맥 길이는 얼마인가
- 비교 조건: 총 · 활성 파라미터, hidden 크기, 학습 토큰, shot · decoding
- 원문 문장 대 같은 논문의 표 값: 다르면 둘 다 적고 `verdict` claim을 만든다

## 다시 계산하기

- `expr`: lint가 안전한 산술 평가기로 계산해 `value`와 비교한다(허용 오차 `tol`). 다르면 오류 L-CLAIM-EXPR. 예: `"expr": "2*80*8*128*2"` → 327,680.
- `ratio_of`: `value` = 앞 claim value ÷ 뒤 claim value. 예: `kv-ratio`의 `["kv-65b", "kv-70b"]` → 2,621,440 ÷ 327,680 = 8.
- `factors`: Π(from ÷ to) = `value`. 예: KV head 64 → 8, 층 80 → 80, head 차원 128 → 128 → 8 × 1 × 1 = 8. 상대 오차 1e-6 밖이면 오류 L-CLAIM-FACTOR.
- **방향**: `value`는 이전 ÷ 새것이다. `ratio_of`도 `[이전, 새것]` 순서로 적어 둘이 같은 방향이 되게 한다. 화면은 새것 기준 배율(2배 · 1/5 · 0.4배)로 써도 되지만, 원장 값은 바꾸지 않는다. 요인이 반대로 움직이는 예:

```json
{"id": "kv-13b-70b-ratio", "statement": "Llama 2-13B → 70B 토큰당 KV cache는 2.5배 줄었다(층은 2배, KV head는 1/5)",
 "kind": "calc", "layer": "main", "value": 2.5, "ratio_of": ["kv-13b", "kv-70b"],
 "factors": [{"name": "층", "from": 40, "to": 80}, {"name": "KV head", "from": 40, "to": 8}, {"name": "head 차원", "from": 128, "to": 128}],
 "inputs": ["kv-13b", "kv-70b"]}
```

  (40 ÷ 80) × (40 ÷ 8) × (128 ÷ 128) = 0.5 × 5 × 1 = 2.5, `kv-13b` 819,200 B(800 KiB) ÷ `kv-70b` 327,680 B(320 KiB) = 2.5. 화면에는 '층 2배 × KV head 1/5 = 0.4배'로 쓴다([screen-budget.md](screen-budget.md) 8절).
- 본보기: 예시 원장의 KV cache 항목(`expr` · `ratio_of` · `factors`), SwiGLU 8/3 항목(`formula`와 설명용 값의 `expr`), Table 3 항목(`table` · `orig` · `verdict` 나누기).

## 장과 잇기

- 장 JSON `claims`에 그 장이 쓰는 claim id를 적는다. 원장에 없는 id는 오류(L-CLAIM-UNKNOWN).
- 표지 의무(L-CHIP-MISSING): 표지가 필요한 `kind`인데 `layer: "main"`이면 화면 글에, `layer: "evidence"`이면 근거 패널이나 화면에 그 라벨이 있어야 한다. `verdict`는 `.verdict` 요소.
- `screen_condition`이 참조 본편 장 화면에 없으면 경고(L-COND-SCREEN).
- 화면 대조: `display`가 있으면 `layer: "main"`은 참조 장 화면 글에, `evidence`는 화면이나 패널에 그 글이 있어야 한다(L-CLAIM-DISPLAY). `cells`의 칸 글이 표와 다르면 오류(L-CLAIM-CELL), 그 칸이 없으면 경고(L-CLAIM-CELL-MISSING). `main`인데 `display` · `value` · `cells` · `screen_condition` 어느 글도 화면에 없으면 알림(L-MAIN-OFFSCREEN): 패널에만 있다면 layer를 `evidence`로 고치거나 화면에 올린다.
- 그 밖의 경고: `sources`도 `inputs`도 없음(L-CLAIM-NOSOURCE), `main`인데 어느 본편 장도 참조하지 않음(L-CLAIM-UNUSED), `main`인데 부록 장만 참조(L-CLAIM-APPX-ONLY), `evidence`인데 참조 장에 근거 패널이 없음(L-CLAIM-NOEVID).

## 근거 손실 확인

기준선과 비교하고, 떨어진 항목은 되살린다. 기준선은 이렇게 정한다.

- **새로 만드는 덱**: '이전 판'이 없으므로 원장 전체와 읽기 지도의 '계산해 보면' 항목(배정 항목별 식 · 대입 · 값)을 기준선으로 삼는다. 이 항목마다 원장 claim이 있고, 그 claim이 맞는 층에 실렸는지 본다.
- **고치는 덱**: 이전 빌드의 `--lint` coverage 보고를 기준선으로 삼고, 고친 뒤 같은 것을 다시 잰다.

1. **출처 연결률**: `main` claim 중 본편 장이 참조하는 비율. 목표 100%.
2. **재계산 성공**: `expr` · `ratio_of` · `factors`가 모두 통과.
3. **조건 유지**: `screen_condition`이 화면에 남아 있는 수.

①–③은 `build_deck.py --lint`의 coverage 보고(전체 수 · 층별 수 · 참조된 main 비율 · expr · factors 재계산 성공 수 · screen_condition 유지 수 · display 일치 수 · 셀 대조 수)로 본다.
