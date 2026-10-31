# Llama 2 (arXiv:2307.09288v2) — 다섯 파트 읽기 지도

<!-- 원문 링크는 arXiv v2 PDF의 파일 페이지 기준이다(본문에서 확인한 페이지는 인쇄 쪽수와 같다). H3 하나가 HTML 한 페이지다. 파트별 범위는 2026-10-24 스터디 배정을 따른다. -->

<!-- part: overview -->
## 한눈에 보기

### 다섯 파트가 다루는 내용

Llama 2는 **LLaMA 1의 사전학습 recipe를 거의 그대로 두고, 그 위에 사람 선호로 학습한 reward model과 반복 RLHF를 얹어 공개 chat 모델을 만들 수 있는가**를 묻습니다. 이번 주에는 사전학습의 바뀐 점(§2.2 · A.2.1 · §2.3), 후학습 데이터와 GAtt · 평가(§3.1 · §3.2.1 · §3.3 · §3.4), RM과 RS · PPO(§3.2.2 · §3.2.3)를 읽고, W01에서 넘긴 tokenizer · RoPE · 품질 분류기를 Background와 Data에서 깊게 봅니다.

| 파트 | 이번 주에 다루는 내용 | 필수 원문 | 개념 | 분량 |
| --- | --- | --- | --- | --- |
| Architecture & Pre-training (이경민) | LLaMA 1에서 **유지한 것과 바꾼 것**, 하이퍼파라미터의 출처, 2K → 4K context 실험, GQA가 KV cache를 얼마나 줄이는지, 기반 모델 평가(범주 · 새 벤치마크 · 비공개 모델 비교) | §2.2(Tokenizer 제외) · Table 1 · Fig. 5 · App. A.2.1 · Table 16–18 · Fig. 24 · §2.3 · Table 3–4 | 19개 | ■■■■■ 높음 |
| Data & Synthesis (정호찬) | W01에서 넘긴 **웹 품질 필터**: CCNet의 fastText 언어 식별 · KenLM perplexity 필터 · Wikipedia 참조 분류기가 어떻게 작동하는지, Llama 2가 데이터 정제에 대해 말한 것과 말하지 않은 것 | LLaMA 1 §2.1 · CCNet §3 · fastText · KenLM 원전 · Llama 2 §2.1 · §4.1 Table 10 | 12개 | ■■■■□ 중간–높음 |
| Post-training (송용우 · 임병극) | **데이터 & 후학습**: SFT 27,540개와 답 토큰 loss, 선호 데이터 수집 절차와 단위, 여러 턴 지시를 지키게 하는 GAtt, RLHF 결과를 RM · GPT-4 · 사람으로 잰 방법과 그 한계 | §3 도입 · §3.1 · §3.2.1 · Table 5–6 · §3.3 · Fig. 9–10 · §3.4 · Fig. 11–12 | 15개 | ■■■■□ 중간–높음 |
| Alignment & RL (김민제 · 강민우) | 선호 쌍 → ranking loss · margin → 두 개의 RM과 그 scaling, RLHF V1–V5에서 rejection sampling과 PPO의 결합, 조건부 reward · whitening · KL | §3.2.2 · Eq. (1)–(2) · Table 7–8 · Fig. 6 · §3.2.3 · Eq. (3)–(4) · Fig. 7–8 | 20개 | ■■■■■ 높음 |
| Background (이정민 · 김민선) | W01에서 넘긴 **tokenizer**(BPE 학습 · SentencePiece · byte fallback)와 **위치 인코딩의 계보**(사인파 → 학습형 절대 위치 → 상대 위치 → RoPE) | Llama 2 §2.2 Tokenizer(p.6) · RoPE 한 줄(p.5) + BPE · SentencePiece · Transformer · RoFormer 원전 | 15개 | ■■■■□ 중간–높음 |

분량 = 개념 수 + 필수 원문 분량. Architecture는 본문 4쪽에 부록 표 8개, Alignment는 본문 약 6쪽(p.10–16)에 수식 4개가 몰려 있습니다. Post-training은 본문 약 7쪽(p.8–10 · 16–19), Data · Background는 Llama 2 본문이 한두 줄이라 원전(CCNet · BPE · RoFormer 등)이 분량의 대부분입니다. 개념 수에는 `(선택)` 페이지도 포함합니다.

<a id="overview-collab"></a>

### 분량과 함께 할 파트

- **분량 차이:** Architecture는 **1명**이 개념 19개(평가 6개 포함)를 맡아 가장 무겁습니다. 필수만 하면 12개이고, §2.2.1 하드웨어 · 탄소와 A.6 오염 분석은 `(선택)`으로 표시했습니다. Alignment는 2명이 수식 4개와 개념 20개를 맡습니다. Data는 1명이 원전(CCNet · fastText · KenLM)과 공개 코드 위주로 읽고, Background는 두 주제(tokenizer · 위치 인코딩)에 로드맵이 하나씩 있습니다.
- **배정 범위에서 확인할 것:** Architecture 범위 “Tokenizer 제외 Hyperparameters까지”가 §2.2.1(하드웨어 · 탄소, p.6–7)을 포함하는지 정해지지 않아 선택으로 두었습니다. §2.1 사전학습 데이터는 Data 파트의 맥락 페이지로만 넣었습니다.
- **배정되지 않은 원문:** §4 Safety 전체(p.20–32)와 §5 Discussion(p.32–35)은 이번 배정에 없습니다. [배정 밖 원문](#unassigned-scope) 페이지에 목록을 두었습니다.
- **같이 보는 원문:** 같은 선호 데이터와 같은 RM이 여러 단계에 쓰입니다. Post-training이 모은 선호 데이터가 Alignment의 RM이 되고, 그 RM이 rejection sampling과 PPO의 보상, 그리고 Post-training이 다루는 모델 기반 평가의 판정자가 됩니다.

| 함께 준비 | 왜 같이 하나 | 공유하는 원문 |
| --- | --- | --- |
| Post RQ2 + Alignment RQ1 | 4단계 선호 강도가 margin m(r)이 되고, “비교 1개 = 응답 2개 = RM 입력 2행”이라는 단위가 RM batch(512 pairs = 1,024 rows)로 이어집니다. | §3.2.1–§3.2.2 · Table 6 · 27–28 |
| Post RQ4 + Alignment RQ1 | Post-training이 맡은 §3.4.1 모델 기반 평가는 Alignment의 RM 점수를 지표로 씁니다. RM 정확도(Table 7–8)와 RM 점수의 사람 평가 일치(Fig. 29)를 한 번에 정리하면 겹치지 않습니다. | §3.2.2 Results · §3.4.1 · Fig. 11 · 29 |
| Post RQ3 + Alignment RQ2 | GAtt는 RLHF V3 이후에 적용됐고, 학습 데이터를 최신 RLHF 모델로 sampling합니다. V1–V5 타임라인 한 장을 같이 쓰면 둘 다 설명하기 쉽습니다. | §3.2.3 · §3.3 · Fig. 11 |
| Background RQ2 + Architecture RQ2 | 2K → 4K context 확장은 RoPE를 그대로 두고 학습 길이만 늘린 것입니다. 위치 인코딩 계보 끝에 4K 실험(Table 16–17)을 붙이면 Architecture의 부담이 줄어듭니다. | §2.2 · App. A.2.1 · Table 16–17 · RoFormer §3 |
| Background RQ1 + Data RQ1 | CCNet의 KenLM은 **SentencePiece로 토큰화한 문단**에 perplexity를 계산합니다. 같은 SentencePiece를 Background가 설명하면 Data는 필터 쪽에 집중할 수 있습니다. | CCNet §3 · SentencePiece |
| Architecture RQ4 + Post RQ4 | 기반 모델 평가(자동 벤치마크)와 chat 모델 평가(RM · GPT-4 · 사람)가 무엇을 재는지 대비하면 “평가” 한 장으로 묶을 수 있습니다. | §2.3 · §3.4 |

제안 조합: **(Post RQ2 + Alignment RQ1: 선호 데이터 → RM)** · **(Background RQ2 + Architecture RQ2: RoPE와 4K context)** · **(Background RQ1 + Data RQ1: SentencePiece와 KenLM)**. 최종 담당과 분량은 사람이 정합니다.

<!-- part: architecture -->
## Architecture & Pre-training

### 이 파트의 질문

- **담당:** 이경민
- **범위:** [§2.2 Training Details](https://arxiv.org/pdf/2307.09288v2#page=5)(Tokenizer 제외) · Hyperparameters · [App. A.2.1 Architecture Changes Compared to Llama 1](https://arxiv.org/pdf/2307.09288v2#page=47) · [§2.3 Llama 2 Pretrained Model Evaluation](https://arxiv.org/pdf/2307.09288v2#page=7). Tokenizer는 Background가 맡습니다.
- **RQ1. LLaMA 1에서 무엇을 그대로 가져왔고, 무엇이 실제로 바뀌었나?**
  - 필수 원문: [§2 도입 · §2.2 · Table 1](https://arxiv.org/pdf/2307.09288v2#page=5) · [Fig. 5](https://arxiv.org/pdf/2307.09288v2#page=6)
  - 개념: [유지한 것과 바꾼 것](#c-recipe-delta) · [optimizer 설정값의 출처](#c-opt-values) · [2T 토큰에서도 포화되지 않은 loss](#c-loss-curve)
- **RQ2. context를 2K → 4K로 늘린 효과는 어떻게 확인했나?**
  - 필수 원문: [App. A.2.1 Context Length · Table 16–17](https://arxiv.org/pdf/2307.09288v2#page=47)
  - 개념: [2K → 4K context와 그 통제 실험](#c-context-4k) · (선택) [긴 문맥 벤치마크(SCROLLS)](#c-long-context-bench) · (선택) [F1 · ROUGE · EM 채점](#c-f1-rouge)
  - 위치 인코딩 자체는 Background의 [RoPE](#c-pos-rope)에서 봅니다.
- **RQ3. GQA는 KV cache와 추론 확장성을 어떻게 바꾸나?**
  - 필수 원문: [App. A.2.1 Grouped-Query Attention · Table 18 · Fig. 24](https://arxiv.org/pdf/2307.09288v2#page=47) · [Table 1](https://arxiv.org/pdf/2307.09288v2#page=6)
  - 개념: [KV cache](#c-kv-cache) · [MHA · MQA · GQA](#c-mha-mqa-gqa) · [GQA ablation과 FFN 보정](#c-gqa-ablation) · [70B의 KV cache 계산](#c-kv-math) · [8-GPU tensor parallel 배포와 Fig. 24](#c-tp-serving) · (선택, 논문 밖) [GQA 이후: Llama 3 · Mistral · MLA](#c-arch-followup)
- **RQ4. 기반 모델은 무엇을, 어떻게 채점했나?**
  - 필수 원문: [§2.3 · Table 3–4](https://arxiv.org/pdf/2307.09288v2#page=7) · 개별 결과 [App. A.2.2 · Table 19–25](https://arxiv.org/pdf/2307.09288v2#page=48)
  - 개념: [벤치마크 묶음과 평균의 재계산](#c-bench-groups) · [W01에 없던 벤치마크](#c-bench-new) · [비공개 모델과의 비교](#c-closed-compare) · (선택) [데이터 오염 분석](#c-contamination)
  - W01에서 다룬 채점 방식(likelihood · 길이 정규화 · exact match · pass@k · maj1@k)은 [W01 읽기 지도](../w01/llama1-reading-map.html#c-likelihood-eval)를 다시 씁니다.
- **(선택) §2.2.1. 2T 토큰 학습은 어떤 하드웨어와 비용으로 실행됐나?** 배정 범위에 들어가는지 정해지지 않았습니다.
  - 원문: [§2.2.1 · Table 2](https://arxiv.org/pdf/2307.09288v2#page=6)
  - 개념: [두 클러스터: InfiniBand와 RoCE](#c-clusters) · [GPU 시간으로 처리량과 MFU 계산](#c-compute-math) · [탄소 발자국과 그 가정](#c-carbon)

<a id="c-recipe-delta"></a>

### 유지한 것과 바꾼 것

- **무엇인가:** Llama 2의 사전학습은 새 구조가 아니라 **LLaMA 1 recipe + 다섯 가지 변경**입니다. 저자는 “더 강한 데이터 정제, 새 데이터 혼합, 40% 더 많은 토큰, 두 배 context, 큰 모델의 GQA”를 변경으로 듭니다.
- **원문:** [§2 도입 · §2.2](https://arxiv.org/pdf/2307.09288v2#page=5) — “We adopt most of the pretraining setting and model architecture from Llama 1.” 구조 차이(primary architectural differences)는 context 길이와 GQA 두 가지라고 명시합니다. [Table 1](https://arxiv.org/pdf/2307.09288v2#page=6) · [Tokenizer](https://arxiv.org/pdf/2307.09288v2#page=6)

| 항목 | LLaMA 1 (W01) | Llama 2 | 구분 |
| --- | --- | --- | --- |
| 블록 | pre-norm RMSNorm · SwiGLU · RoPE | 같음 | 유지 |
| Tokenizer | SentencePiece BPE · 숫자 분리 · byte fallback | “same tokenizer as Llama 1”, 어휘 32k | 유지 |
| Optimizer | AdamW β₁ 0.9 · β₂ 0.95 · wd 0.1 · clip 1.0 · cosine → 10% · warmup 2,000 | 같음 + eps 10⁻⁵ 명시 | 유지 |
| Batch | 4M 토큰 | 4M 토큰 | 유지 |
| Context | 2,048 | **4,096** | 구조 변경 |
| Attention | MHA | 7B · 13B MHA, **34B · 70B GQA** | 구조 변경 (일부 크기) |
| 데이터 | 공개 7개 소스 · 비율 공개 | “a new mix of publicly available data”, 비율 미공개 | 데이터 변경 |
| 토큰 | 1.0T (7B · 13B) / 1.4T (33B · 65B) | 2.0T (모든 크기) | 데이터 변경 |

- **설명할 수 있어야 하는 것:**
  - [ ] 구조 변경(context · GQA)과 데이터 변경(혼합 · 2T)을 다른 칸으로 나눠 말한다.
  - [ ] “40% 더 많은 토큰”은 1.4T → 2.0T 기준이고, 7B · 13B는 1.0T → 2.0T로 두 배라는 점을 말한다(추출자 계산).
  - [ ] Llama 2가 LLaMA 1 **가중치에서 이어 학습한 것이 아니라** 같은 recipe로 새로 학습했다는 점을 말한다. 원문은 “pretraining approach”를 따랐다고만 적습니다.
  - [ ] 34B는 논문에 보고했지만 red teaming 시간이 부족해 공개를 미뤘다는 점을 말한다([p.4 각주](https://arxiv.org/pdf/2307.09288v2#page=4)).
- **함께 볼 개념:** [2K → 4K context](#c-context-4k) · [MHA · MQA · GQA](#c-mha-mqa-gqa) · [사전학습 데이터](#c-pretrain-corpus) · W01: [RMSNorm](../w01/llama1-reading-map.html#c-rmsnorm) · [SwiGLU](../w01/llama1-reading-map.html#c-swiglu) · [RoPE](../w01/llama1-reading-map.html#c-rope)

<a id="c-opt-values"></a>

### optimizer 설정값의 출처

- **무엇인가:** Llama 2의 사전학습 하이퍼파라미터는 LLaMA 1과 같고, LLaMA 1의 값은 GPT-3와 거의 같습니다. 원문은 선택 이유를 적지 않습니다.
- **원문:** [§2.2 Hyperparameters](https://arxiv.org/pdf/2307.09288v2#page=5) · [Table 1](https://arxiv.org/pdf/2307.09288v2#page=6)

| 설정 | PyTorch AdamW 기본값 | GPT-3 (2020) | LLaMA 1 | Llama 2 |
| --- | --- | --- | --- | --- |
| β₁ / β₂ | 0.9 / 0.999 | 0.9 / 0.95 | 0.9 / 0.95 | 0.9 / 0.95 |
| eps | 1e-8 | 1e-8 | 원문 미기술 | **1e-5** |
| weight decay | 0.01 | 0.1 | 0.1 | 0.1 |
| gradient clipping | 없음 | 1.0 | 1.0 | 1.0 |
| schedule | – | cosine → 10% | cosine → 10% | cosine → 10% |
| warmup | – | 375M 토큰 | 2,000 step | 2,000 step |
| 최대 LR | 1e-3 | 크기별 | 3.0e-4 / 1.5e-4 | 7B · 13B 3.0e-4, 34B · 70B 1.5e-4 |
| batch | – | 크기별 | 4M 토큰 | 4M 토큰 |

- **계산해 보면 (추출자 계산):** 2.0T ÷ 4M = **500,000 step**. warmup 2,000 step = 8B 토큰 = 전체의 0.4%로, LLaMA 1(1.4T, 약 35만 step의 0.6%)보다 비중이 더 작습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Llama 2가 새로 적은 eps = 10⁻⁵가 기본값(10⁻⁸)보다 크다는 점과, 이 값이 2차 모멘트가 매우 작은 파라미터에서 update가 튀는 것을 막는 역할을 한다는 일반적 설명을 구분한다(원문은 이유 미기술).
  - [ ] 큰 모델(34B · 70B)의 최대 LR이 절반이라는 점이 LLaMA 1과 같다는 것을 말한다.
  - [ ] 같은 AdamW 설정이 RM · PPO 학습에도 다시 쓰인다는 점을 연결한다([후학습 설정 비교](#c-sft-settings)).
- **함께 볼 개념:** W01: [β₂ = 0.95와 나머지 설정값의 출처](../w01/llama1-reading-map.html#c-opt-values) · [Warmup 2,000 step](../w01/llama1-reading-map.html#c-warmup)

<a id="c-loss-curve"></a>

### 2T 토큰에서도 포화되지 않은 loss

- **무엇인가:** Fig. 5는 네 크기의 학습 perplexity가 2T 토큰까지 계속 내려가고, 같은 토큰 수에서는 큰 모델이 항상 아래에 있음을 보입니다.
- **원문:** [Fig. 5](https://arxiv.org/pdf/2307.09288v2#page=6) — “after pretraining on 2T Tokens, the models still did not show any sign of saturation.” [§2.1](https://arxiv.org/pdf/2307.09288v2#page=5) — 2T를 고른 이유는 “good performance–cost trade-off”라는 한 문장뿐입니다.
- **왜 그런가 (배경 설명):** Chinchilla 손실 식 `L = E + A/N^α + B/D^β`에서 D를 늘리면 데이터 항이 계속 줄어듭니다. 7B 기준 Chinchilla 권장치는 약 140B 토큰이고, 2T는 그 약 14배입니다(추출자 계산). 줄어드는 폭은 점점 작아지지만 0이 되지 않습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] “포화되지 않았다”는 그림의 관찰이며, 몇 토큰에서 멈추는 것이 최적인지에 대한 실험은 원문에 없다는 점을 말한다.
  - [ ] 그래프의 y축이 loss가 아니라 train PPL로 표시되어 있다는 점을 확인한다.
  - [ ] LLaMA 1의 “작은 모델을 오래” 논리가 2T로 한 번 더 확장됐다는 연결을 말한다.
- **함께 볼 개념:** W01: [스케일링 법칙 ②](../w01/llama1-reading-map.html#c-chinchilla-loss) · [큰 모델일수록 loss가 낮은 이유](../w01/llama1-reading-map.html#c-size-loss)

<a id="c-context-4k"></a>

### 2K → 4K context와 그 통제 실험

- **무엇인가:** 학습 시퀀스 길이를 2,048에서 4,096 토큰으로 늘린 변경입니다. 저자가 든 이유는 긴 chat 기록 · 요약 · 긴 문서 이해입니다.
- **원문:** [App. A.2.1 · Table 16–17](https://arxiv.org/pdf/2307.09288v2#page=47) — 두 모델 모두 **150B 토큰**, 같은 구조 · 하이퍼파라미터, context만 다르게 학습한 비교입니다. SCROLLS(평균 입력 3.5k)에서 좋아지고 SQuAD에서 떨어지지 않았다고 적습니다.

| 과제 | 지표 | 2k | 4k |
| --- | --- | --- | --- |
| NarrativeQA | F1 | 0.21 | 17.26 |
| Qasper | F1 | 0.71 | 18.52 |
| QuALITY | acc | 26.1 | 29.6 |
| QMSum | ROUGE-1/2/L | 0.13 / 0.01 / 0.12 | 15.08 / 3.55 / 12.16 |
| ContractNLI | EM | 11.76 | 16.33 |
| SQuAD | EM / F1 | 57.23 / 62.89 | 57.99 / 64.46 |
| HellaSwag (0-shot) | acc | 75.1 | 74.8 |
| TriviaQA (64-shot) | EM | 53.7 | 52.2 |
| GSM8K (8-shot) | acc | 4.9 | 6.5 |

- **설명할 수 있어야 하는 것:**
  - [ ] 이 비교가 최종 2T 모델이 아니라 150B 토큰 ablation이라는 조건을 말한다.
  - [ ] 2k 모델의 NarrativeQA · Qasper가 거의 0인 이유를 추정한다: 입력이 2k를 넘으면 잘리거나 문맥 밖으로 밀려 답의 근거를 못 보기 때문으로 보입니다(추출자 해석, 원문은 입력 처리 방식을 적지 않음).
  - [ ] 일반 과제는 “유지”이지 모두 오르지는 않는다는 점을 HellaSwag · TriviaQA로 보인다.
  - [ ] RoPE를 그대로 쓰면서 학습 길이만 늘렸고, 위치 보간 같은 별도 기법은 원문에 없다는 점을 말한다.
- **함께 볼 개념:** [긴 문맥 벤치마크](#c-long-context-bench) · [KV cache](#c-kv-cache)

<a id="c-long-context-bench"></a>

### 긴 문맥 벤치마크(SCROLLS)

- **무엇인가:** 4K context의 효과를 보려고 쓴 긴 입력 과제 묶음입니다. SCROLLS의 평균 입력 길이는 3.5k 토큰입니다.
- **원문:** [App. A.2.1 · Table 16](https://arxiv.org/pdf/2307.09288v2#page=47)

| 과제 | 무엇을 평가하나 | 형식 · 지표 |
| --- | --- | --- |
| NarrativeQA | 책 · 영화 대본 전체를 읽고 줄거리 질문에 답하기 | 자유 생성 · F1 |
| Qasper | NLP 논문 전문을 읽고 질문에 답하기 | 자유 생성 · F1 |
| QuALITY | 긴 기사 · 소설을 읽고 객관식 질문 | 보기 4개 · 정확도 |
| QMSum | 회의록에서 질문에 맞는 부분 요약 | 요약 생성 · ROUGE-1/2/L |
| ContractNLI | 계약서가 주어진 가설을 함의 · 모순 · 언급 없음 중 무엇인지 | 분류 · EM |

- **설명할 수 있어야 하는 것:**
  - [ ] 다섯 과제가 각각 QA · 객관식 · 요약 · 분류라는 점과 그래서 지표가 다르다는 점을 말한다.
  - [ ] 2K 모델은 입력의 상당 부분을 볼 수 없어서 점수가 낮다는 해석과, 이것이 4K의 효과를 크게 보이게 한다는 점을 말한다(추출자 해석).
- **원전:** [SCROLLS](https://arxiv.org/abs/2201.03533)

<a id="c-f1-rouge"></a>

### F1 · ROUGE · EM 채점

- **무엇인가:** 생성한 답을 정답과 비교하는 세 가지 방법입니다. EM은 정규화 후 완전히 같아야 1점, F1은 단어 단위로 겹친 비율, ROUGE는 n-gram이 겹친 비율(요약에 주로 씀)입니다.
- **원문:** [Table 16 · 22 · 23](https://arxiv.org/pdf/2307.09288v2#page=47) — 지표 이름만 적고 정규화 세부는 적지 않습니다.
- **계산해 보면 (설명용):** 정답 `Charles Darwin`, 생성 `Darwin`
  - EM: 같지 않음 → **0**
  - F1: 겹친 단어 1개. precision = 1/1, recall = 1/2 → F1 = 2 × 1 × 0.5 ÷ 1.5 = **0.67**
  - 생성 `the naturalist Charles Darwin`: precision = 2/4(관사 제거 시 2/3), recall = 2/2 → F1 = 0.67(0.8)
- **설명할 수 있어야 하는 것:**
  - [ ] 같은 답이 EM 0점, F1 0.67점이 되는 예를 계산한다.
  - [ ] 정답이 길고 표현이 다양한 과제(QuAC · Qasper · 요약)에 F1 · ROUGE를 쓰는 이유를 말한다.
- **함께 볼 개념:** W01: [Greedy 생성과 exact match](../w01/llama1-reading-map.html#c-greedy-em)

<a id="c-kv-cache"></a>

### KV cache

- **무엇인가:** 자기회귀 생성에서 이전 토큰들의 key · value를 저장해 두고, 새 토큰마다 그 토큰의 query만 계산해 저장된 K · V와 attention을 하는 방식입니다. 이전 토큰의 K · V를 매번 다시 계산하지 않아 빨라지는 대신 메모리를 씁니다.
- **원문:** [App. A.2.1](https://arxiv.org/pdf/2307.09288v2#page=47) — “A standard practice for autoregressive decoding is to cache the key (K) and value (V) pairs…” context 창이나 batch가 커지면 MHA 모델의 KV cache 메모리가 크게 늘고, 큰 모델에서는 이것이 병목이 된다고 적습니다.
- **크기 식 (일반식):** `KV cache = 2(K·V) × layer 수 × KV head 수 × head 차원 × 시퀀스 길이 × batch × 바이트`
- **설명할 수 있어야 하는 것:**
  - [ ] 학습(모든 토큰을 한 번에 계산)에는 KV cache가 없고, **생성할 때만** 필요하다는 점을 말한다.
  - [ ] 식에서 context 길이와 batch에 정비례한다는 점, 그래서 4K context 확장과 GQA가 같은 문제의 양면이라는 점을 말한다.
  - [ ] 줄일 수 있는 항이 “KV head 수”라는 점을 다음 페이지의 MQA · GQA와 연결한다.
- **함께 볼 개념:** [MHA · MQA · GQA](#c-mha-mqa-gqa) · [70B의 KV cache 계산](#c-kv-math)

<a id="c-mha-mqa-gqa"></a>

### MHA · MQA · GQA

- **무엇인가:** query head 수는 그대로 두고 **key · value head 수**를 줄이는 세 가지 배치입니다.
  - **MHA:** query head마다 자기 K · V를 가짐 (KV head = H).
  - **MQA:** 모든 query head가 K · V 하나를 공유 (KV head = 1, Shazeer 2019).
  - **GQA:** query head를 G개 묶음으로 나눠 묶음마다 K · V를 공유 (KV head = G, Ainslie et al. 2023). G = 1이면 MQA, G = H이면 MHA입니다.
- **원문:** [App. A.2.1](https://arxiv.org/pdf/2307.09288v2#page=47) — 큰 모델에서는 K · V projection을 여러 head가 공유해도 성능이 크게 떨어지지 않는다(Chowdhery et al. 2022)고 적고, MQA(KV projection 1개)와 GQA(**8개**)를 비교합니다. [Table 1](https://arxiv.org/pdf/2307.09288v2#page=6): GQA는 34B · 70B에만, 7B · 13B는 MHA.
- **그림 (설명용, query 8 head 기준):**

  ```
  MHA  Q: 1 2 3 4 5 6 7 8   KV: 1 2 3 4 5 6 7 8
  GQA  Q: 1 2 | 3 4 | 5 6 | 7 8   KV: A | B | C | D   (G = 4)
  MQA  Q: 1 2 3 4 5 6 7 8   KV: A
  ```

- **설명할 수 있어야 하는 것:**
  - [ ] 세 방식에서 query 수는 같고 KV head 수만 다르다는 점을 그림으로 말한다.
  - [ ] GQA는 “어떤 토큰을 볼지 고르는” sparse attention이 아니라 **K · V를 head 사이에 공유**하는 방식이라는 점을 구분한다.
  - [ ] 7B · 13B에는 GQA를 쓰지 않았다는 적용 범위를 말한다.
  - [ ] GQA 원 논문의 uptraining(MHA checkpoint의 head를 평균해 GQA로 바꾸고 원 사전학습 compute의 5%로 추가 학습)은 원전의 방법이며, Llama 2가 그렇게 초기화했다는 기술은 없다는 점을 말한다(원문 미기술).
- **함께 볼 개념:** [GQA ablation](#c-gqa-ablation) · 원전: GQA [arXiv:2305.13245](https://arxiv.org/abs/2305.13245v3) §2.1–§2.2 · MQA [arXiv:1911.02150](https://arxiv.org/abs/1911.02150)

<a id="c-gqa-ablation"></a>

### GQA ablation과 FFN 보정

- **무엇인가:** 30B 모델을 150B 토큰으로 MHA · MQA · GQA 세 가지로 학습해 비교한 실험입니다.
- **원문:** [App. A.2.1 · Table 18](https://arxiv.org/pdf/2307.09288v2#page=48) — 전체 파라미터 수를 맞추려고 attention이 줄어든 만큼 **FFN 차원을 MQA는 1.33배, GQA는 1.3배** 늘렸습니다. 0-shot(MMLU 5-shot, GSM8K 8-shot).

| | BoolQ | PIQA | SIQA | HellaSwag | ARC-e | ARC-c | NQ | TQA | MMLU | GSM8K | HumanEval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MHA | 71.0 | 79.3 | 48.2 | 75.1 | 71.2 | 43.0 | 12.4 | 44.7 | 28.0 | 4.9 | 7.9 |
| MQA | 70.6 | 79.0 | 47.9 | 74.5 | 71.6 | 41.9 | 14.5 | 42.8 | 26.5 | 4.8 | 7.3 |
| GQA | 69.4 | 78.8 | 48.6 | 75.4 | 72.1 | 42.5 | 14.0 | 46.2 | 26.9 | 5.3 | 7.9 |

- **계산해 보면 (추출자 계산, 11개 단순 평균):** MHA 44.2 · MQA 43.8 · GQA 44.3. 저자 결론 “GQA는 대부분 MHA와 비슷하고 평균적으로 MQA보다 낫다”와 맞습니다. 세 방식의 차이는 0.5점 안쪽이고, 항목별로는 GQA가 MHA보다 낮은 곳(BoolQ −1.6 · MMLU −1.1)도 있습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 이 실험이 attention만 바꾼 것이 아니라 FFN 크기도 함께 바꾼 비교라는 점을 말한다.
  - [ ] 저자가 GQA를 고른 근거가 **품질(MQA보다 평균 우위)과 배포 편의(다음 페이지)** 두 가지라는 점을 말한다.
  - [ ] 30B · 150B 토큰 실험이고, 실제 34B · 70B 체크포인트의 비교가 아니라는 조건을 말한다.
- **함께 볼 개념:** [8-GPU tensor parallel 배포](#c-tp-serving)

<a id="c-kv-math"></a>

### 70B의 KV cache 계산

- **무엇인가:** GQA가 실제로 얼마나 줄이는지 숫자로 보는 페이지입니다. 원문은 layer 수 · head 수를 적지 않으므로, 공개된 모델 설정값(70B: 80 layer, query 64 head, KV 8 head, head 차원 128 / 7B: 32 layer, 32 head MHA, head 차원 128)을 씁니다(**논문 밖** · 추출자 계산, fp16 2바이트).

| 모델 · 방식 | 토큰당 KV cache | 4,096 토큰 1개 | 4,096 토큰 × batch 64 |
| --- | --- | --- | --- |
| 70B · GQA (KV 8) | 2 × 80 × 8 × 128 × 2 B = **320 KiB** | 1.25 GiB | 80 GiB |
| 70B · MHA였다면 (KV 64) | 2.5 MiB | 10 GiB | 640 GiB |
| 70B · MQA였다면 (KV 1) | 40 KiB | 0.16 GiB | 10 GiB |
| 7B · MHA (실제) | 2 × 32 × 32 × 128 × 2 B = 512 KiB | 2 GiB | 128 GiB |

- **읽는 법:** 70B 가중치만 fp16으로 약 138 GB입니다. MHA였다면 4K × 64개 대화의 KV cache(640 GiB)가 8×80GB 노드 전체를 넘습니다. GQA는 이를 1/8로 줄여 **70B의 토큰당 cache가 7B(MHA)보다 작아집니다.**
- **설명할 수 있어야 하는 것:**
  - [ ] 식에 숫자를 넣어 70B GQA의 토큰당 320 KiB를 계산한다.
  - [ ] context를 2K → 4K로 늘리면 cache도 2배가 된다는 점을 말하고, GQA가 그 증가분을 상쇄하고도 남는다는 점을 보인다.
  - [ ] 이 계산의 설정값은 논문이 아니라 공개 config에서 왔다는 점을 밝힌다.
- **함께 볼 개념:** [KV cache](#c-kv-cache) · [8-GPU tensor parallel 배포](#c-tp-serving)

<a id="c-tp-serving"></a>

### 8-GPU tensor parallel 배포와 Fig. 24

- **무엇인가:** tensor parallelism은 한 layer의 행렬을 여러 GPU에 나눠(attention은 head 단위로) 계산하는 병렬화입니다(Megatron-LM, Shoeybi et al. 2019). Llama 2는 지연 시간을 줄이려고 가장 큰 모델을 **A100 8장 한 노드**에 tensor parallel로 올립니다.
- **원문:** [App. A.2.1](https://arxiv.org/pdf/2307.09288v2#page=47) — MQA는 KV head가 GPU 수(8)보다 적어 head 단위로 나눌 수 없습니다. 모든 GPU에 KV를 복제하거나(그러면 cache 크기가 GQA와 같아짐), batch 차원으로 나눠야 하는데 후자는 서비스가 복잡해집니다. [Fig. 24](https://arxiv.org/pdf/2307.09288v2#page=48) — 30B ablation 모델, 8×80GiB A100, 출력 128 토큰, batch를 1부터 두 배씩. MHA는 context 256에서 batch 1024, context 2k에서 batch 128일 때 메모리 부족(OOM), MQA · GQA는 통과.
- **계산해 보면 (추출자 계산):** MHA가 멈춘 두 지점의 저장 토큰 수는 1024 × (256 + 128) ≈ 39만, 128 × (2,048 + 128) ≈ 28만으로 비슷한 크기입니다. 즉 batch × 길이가 일정량을 넘으면 KV cache가 메모리를 채운다는 해석과 맞습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] GQA의 8 KV head가 8 GPU에 정확히 하나씩 나뉜다는 점이 선택 이유의 하나라는 것을 말한다.
  - [ ] Fig. 24에서 MQA와 GQA가 비슷한 것은 MQA의 KV를 모든 GPU에 복제해 cache 크기가 같아졌기 때문이라는 조건을 말한다.
  - [ ] 작은 batch에서는 세 방식의 지연 시간이 비슷하고, 차이는 큰 batch(처리량)에서 난다는 점을 말한다.
- **원전:** Megatron-LM [arXiv:1909.08053](https://arxiv.org/abs/1909.08053) · Pope et al., Efficiently Scaling Transformer Inference [arXiv:2211.05102](https://arxiv.org/abs/2211.05102)

<a id="c-arch-followup"></a>

### GQA 이후: Llama 3 · Mistral · MLA

- **무엇인가 (논문 밖):** Llama 2에서 큰 모델에만 쓴 GQA가 이후 어떻게 기본값이 됐는지입니다.

| 모델 | attention | KV head | context | 기타 |
| --- | --- | --- | --- | --- |
| Llama 2 (2023.07) | 7B · 13B MHA, 34B · 70B GQA | 8 (GQA) | 4K | 어휘 32k |
| Mistral 7B (2023.10) | GQA + sliding window attention | 8 | 8K | 7B부터 GQA |
| Llama 3 (2024.07) | **8B · 70B · 405B 모두 GQA** | 8 | 8K → 128K | 어휘 128K, RoPE θ 500,000 |
| DeepSeek-V2 (2024.05) | MLA: K · V를 저차원 latent로 압축해 cache | – | 128K | W05에서 다룸 |

- **설명할 수 있어야 하는 것:**
  - [ ] Llama 3가 8B부터 GQA를 쓴 사실로, 작은 모델에도 KV cache 절약이 중요해졌다는 흐름을 말한다.
  - [ ] GQA(head 공유)와 MLA(차원 압축)는 KV cache를 줄이는 다른 방법이라는 점을 말하고, W03(Qwen2의 7B MHA→GQA) · W05(MLA)로 연결한다.
- **출처:** [Llama 3 Table 3](https://arxiv.org/abs/2407.21783) (2026-10-17 확인) · [Mistral 7B](https://arxiv.org/abs/2310.06825) · [DeepSeek-V2](https://arxiv.org/abs/2405.04434). Mistral · DeepSeek-V2 항목은 이번에 원문을 다시 열지 않았습니다.

<a id="c-bench-groups"></a>

### 벤치마크 묶음과 평균의 재계산

- **무엇인가:** §2.3은 개별 벤치마크 대신 **범주 평균**(Table 3)을 먼저 보여줍니다. 모든 평가는 Meta 내부 평가 라이브러리로 했고, MPT · Falcon은 내부 재현값과 공개값 중 **높은 쪽**을 씁니다.
- **원문:** [§2.3 · Table 3](https://arxiv.org/pdf/2307.09288v2#page=7) · 개별 결과 [App. A.2.2 · Table 19–25](https://arxiv.org/pdf/2307.09288v2#page=48)

| 범주 | 들어가는 벤치마크 | shot | 지표 | 70B 평균 (재계산) |
| --- | --- | --- | --- | --- |
| Code | HumanEval · MBPP | 0 · 3 | pass@1 평균 | (29.9 + 45.0) ÷ 2 = 37.5 |
| Commonsense | PIQA · SIQA · HellaSwag · WinoGrande · ARC-e · ARC-c · OBQA · CommonsenseQA | 0 (CSQA 7) | 정확도 | 575.3 ÷ 8 = 71.9 |
| World Knowledge | NaturalQuestions · TriviaQA | 5 | EM | (39.5 + 87.6) ÷ 2 = 63.6 |
| Reading Comp. | SQuAD · QuAC · BoolQ | 0 | EM · F1 · 정확도 | (80.7 + 42.4 + 85.0) ÷ 3 = 69.4 |
| Math | GSM8K · MATH | 8 · 4 | top-1 (maj1@1) | (56.8 + 13.5) ÷ 2 = 35.2 |
| MMLU | 57과목 | 5 | 정확도 | 68.9 |
| BBH | BIG-Bench Hard | 3 | 정확도 | 51.2 |
| AGIEval | 영어 과제만 | 3–5 | 정확도 | 54.2 |

- **결과:** Llama 2 70B는 LLaMA 1 65B보다 MMLU +5.5(63.4 → 68.9), BBH +7.7(43.5 → 51.2). 다만 Llama 2 34B의 Math(24.2)는 13B(28.7)보다 낮습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Table 3의 평균을 Table 20–25의 개별 값으로 다시 계산할 수 있다는 점을 하나 이상 보인다(추출자 계산, 모두 일치).
  - [ ] 범주 구성이 LLaMA 1과 다르다는 점을 말한다: BoolQ가 상식 추론에서 독해로 옮겨졌고, CommonsenseQA · SQuAD · QuAC · BBH · AGIEval이 새로 들어왔습니다.
  - [ ] 서로 다른 지표(EM · F1 · 정확도)를 한 범주에서 그대로 평균했다는 점을 말한다.
  - [ ] 비교 모델 점수를 “내부 평가와 공개값 중 높은 쪽”으로 잡은 규칙이 비교 모델에 유리한 쪽이라는 점을 말한다.
- **함께 볼 개념:** [W01에 없던 벤치마크](#c-bench-new) · W01: [벤치마크 목록과 ‘20개’](../w01/llama1-reading-map.html#c-bench-list)

<a id="c-bench-new"></a>

### W01에 없던 벤치마크

- **무엇인가:** 이번 범주에 새로 들어간 벤치마크가 무엇을 묻고 어떻게 채점되는지입니다. 원문은 이 벤치마크들의 프롬프트 형식을 적지 않습니다. 아래 예시는 형식을 보이기 위한 **설명용 문항**입니다.
- **원문:** [§2.3](https://arxiv.org/pdf/2307.09288v2#page=7) · [Table 20 · 23 · 24](https://arxiv.org/pdf/2307.09288v2#page=49)

| 벤치마크 | 무엇을 평가하나 | 형식 · 채점 | 설명용 예시 | 70B |
| --- | --- | --- | --- | --- |
| CommonsenseQA | 개념 사이의 상식 관계(ConceptNet 기반) | 질문 + 보기 5개 · 7-shot · 정확도 | “우산을 쓰는 이유는?” (비 · 햇빛 · …) | 78.5 |
| SQuAD (2.0) | Wikipedia 지문에서 답이 되는 구간 찾기, 답이 없는 질문 포함 | 지문 + 질문 → 구간 생성 · EM | 지문의 한 구절을 그대로 답 | 0-shot 80.7 |
| QuAC | 지문을 보지 못한 학생이 묻고 교사가 지문에서 답하는 대화형 QA | 대화 기록 + 질문 → 구간 · F1 | “그 뒤에 그는 무엇을 했나?” | 0-shot 42.4 · 1-shot 49.3 |
| BoolQ | 지문 + 예/아니오 질문 | 정확도 | W01 참고 | 85.0 |
| BBH | BIG-Bench에서 이전 모델이 사람 평가자보다 못했던 23개 어려운 과제(논리 추론 · 날짜 계산 등) | 3-shot · 정확도 | “오늘이 3월 1일이면 10일 전은?” | 51.2 |
| AGIEval (영어) | 사람용 표준 시험: SAT · LSAT · LogiQA · AQuA-RAT | 3–5-shot · 정확도 | LSAT 논리 추론 문항 | 54.2 (SAT-en 86.9 · LSAT-AR 25.7) |

- **설명할 수 있어야 하는 것:**
  - [ ] 각 벤치마크가 “보기 고르기 / 구간 찾기 / 대화형 / 시험” 중 어디에 속하는지 말한다.
  - [ ] SQuAD는 EM, QuAC는 F1로 채점하는 이유(대화형 답은 경계가 모호해 부분 점수가 필요)를 말한다.
  - [ ] AGIEval 안에서도 SAT-en 86.9와 LSAT-AR 25.7처럼 편차가 크다는 점을 말한다.
- **원전:** [CommonsenseQA](https://arxiv.org/abs/1811.00937) · [SQuAD 2.0](https://arxiv.org/abs/1806.03822) · [QuAC](https://arxiv.org/abs/1808.07036) · [BBH](https://arxiv.org/abs/2210.09261) · [AGIEval](https://arxiv.org/abs/2304.06364)

<a id="c-closed-compare"></a>

### 비공개 모델과의 비교

- **무엇인가:** Llama 2 70B를 GPT-3.5 · GPT-4 · PaLM · PaLM-2-L과 비교한 표입니다. 비교 모델 점수는 각 기술 보고서에서 가져왔습니다.
- **원문:** [Table 4](https://arxiv.org/pdf/2307.09288v2#page=8)

| 벤치마크 (shot) | GPT-3.5 | GPT-4 | PaLM | PaLM-2-L | Llama 2 70B |
| --- | --- | --- | --- | --- | --- |
| MMLU (5) | 70.0 | 86.4 | 69.3 | 78.3 | 68.9 |
| TriviaQA (1) | – | – | 81.4 | 86.1 | 85.0 |
| Natural Questions (1) | – | – | 29.3 | 37.5 | 33.0 |
| GSM8K (8) | 57.1 | 92.0 | 56.5 | 80.7 | 56.8 |
| HumanEval (0) | 48.1 | 67.0 | 26.2 | – | 29.9 |
| BBH (3) | – | – | 52.3 | 65.7 | 51.2 |

- **설명할 수 있어야 하는 것:**
  - [ ] MMLU · GSM8K는 GPT-3.5에 가깝고 코드(HumanEval 29.9 vs 48.1)는 차이가 크다는 저자 요약을 표로 말한다.
  - [ ] 직접 잰 값이 아니라 다른 보고서에서 옮긴 값이라 평가 설정이 같다는 보장이 없다는 점을 말한다.

<a id="c-contamination"></a>

### 데이터 오염 분석

- **무엇인가:** 평가 문항이 사전학습 데이터에 이미 들어 있어서 점수가 부풀었는지 확인하는 분석입니다.
- **원문:** [App. A.6 · Table 51](https://arxiv.org/pdf/2307.09288v2#page=75)
  - **이전 방법:** GPT-3 등은 13-gram이 하나라도 겹치면 오염, PaLM은 8-gram의 70% 이상이 학습 데이터에 있으면 오염으로 봤습니다.
  - **Llama 2 방법:** 토큰화한 입력에서, 평가 문항과 학습 데이터에 함께 나오는 **10토큰 넘는 n-gram**에 속한 토큰을 “오염 토큰”으로 셉니다(최대 4개 위치 불일치 허용). 문항의 오염도 = 오염 토큰 비율. 1,500 코어로 약 7시간, suffix array 사용.
  - **판정:** clean(< 20%) · not clean(≥ 20%) · not dirty(< 80%) · dirty(≥ 80%) 네 부분집합. **가장 깨끗한 쪽이 평균보다 낮고, 가장 더러운 쪽이 평균보다 높을 때만** 오염이 점수에 영향을 줬다고 봅니다. 최소 일치 길이 L을 10–50으로 바꿔 반복합니다.

| 데이터셋 (70B) | 부분집합 | 문항 수 | 점수 | 전체 평균 |
| --- | --- | --- | --- | --- |
| HellaSwag (L = 40) | Clean | 7,391 | 80.0 | 82.5 |
| | Dirty | 848 | 92.2 | 82.5 |
| MMLU-Humanities (L = 50) | Clean | 3,996 | 62.2 | 65.3 |
| | Dirty | 520 | 85.8 | 65.3 |

- **설명할 수 있어야 하는 것:**
  - [ ] 두 조건을 모두 요구하는 이유(한쪽만 성립하면 문항 난이도 차이일 수 있음)를 말한다.
  - [ ] 영향이 있다고 판정된 것은 HellaSwag와 MMLU(Humanities · Overall)뿐이고, 나머지 데이터셋은 근거가 부족했다는 결론을 말한다.
  - [ ] 오염 판정이 점수를 다시 계산해 보고하는 데까지는 가지 않았다는 점(Table 3 수치는 그대로)을 말한다.
- **원전:** PaLM [arXiv:2204.02311](https://arxiv.org/abs/2204.02311) §8 · GPT-3 [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) App. C

<a id="c-clusters"></a>

### 두 클러스터: InfiniBand와 RoCE

- **무엇인가:** 사전학습을 Meta의 Research SuperCluster(RSC)와 내부 production 클러스터 두 곳에서 했고, 둘의 네트워크와 전력 상한이 다릅니다.
- **원문:** [§2.2.1](https://arxiv.org/pdf/2307.09288v2#page=6)

| | RSC | Production 클러스터 |
| --- | --- | --- |
| GPU | A100 | A100 |
| 연결 | NVIDIA Quantum InfiniBand | RoCE (일반 ethernet 스위치 기반 RDMA) |
| 대역폭 | 200 Gbps 엔드포인트 | 200 Gbps 엔드포인트 |
| GPU당 전력 상한 | 400W | 350W |

  저자는 더 저렴한 RoCE가 **2,000 GPU까지** InfiniBand에 거의 맞먹게 확장된다고 적습니다. [Table 2](https://arxiv.org/pdf/2307.09288v2#page=7)의 전력 열로 보면 34B만 350W(production)에서 학습했습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 두 클러스터의 차이 두 가지(연결 방식 · 전력 상한)를 말한다.
  - [ ] RoCE 비교는 저자의 정성적 진술이고 처리량 수치는 공개되지 않았다는 점을 말한다.
  - [ ] 학습 병렬화 방식(FSDP · tensor · pipeline 차수)은 사전학습에 대해서는 원문에 없다는 점을 말한다.

<a id="c-compute-math"></a>

### GPU 시간으로 처리량과 MFU 계산

- **무엇인가:** Table 2의 GPU 시간과 2T 토큰으로 GPU당 처리량과 하드웨어 활용률을 역산하는 페이지입니다. 원문은 GPU 수 · 기간 · 정밀도를 적지 않으므로 아래는 모두 **추출자 계산**입니다(학습 compute ≈ 6ND, 크기는 7 · 13 · 34 · 70B 명목값, A100 BF16 피크 312 TFLOP/s).
- **원문:** [Table 2](https://arxiv.org/pdf/2307.09288v2#page=7) — 7B 184,320 · 13B 368,640 · 34B 1,038,336 · 70B 1,720,320 GPU-hours, 합계 3,311,616.

| 모델 | 학습 compute | tokens/s/GPU | GPU당 실효 연산 | MFU(어림) |
| --- | --- | --- | --- | --- |
| 7B | 8.4 × 10²² | 3,014 | 127 TFLOP/s | 약 41% |
| 13B | 1.6 × 10²³ | 1,507 | 118 TFLOP/s | 약 38% |
| 34B (350W) | 4.1 × 10²³ | 535 | 109 TFLOP/s | 약 35% |
| 70B | 8.4 × 10²³ | 323 | 136 TFLOP/s | 약 43% |
| 비교: LLaMA 1 65B | 5.5 × 10²³ | 380 | 149 TFLOP/s | 약 48% |

- **설명할 수 있어야 하는 것:**
  - [ ] GPU-hours → 초 → tokens/s/GPU → `6N × tokens/s ÷ 피크` 순서로 MFU를 구한다.
  - [ ] 70B를 2,048장으로 돌렸다면 1,720,320 ÷ 2,048 = 840시간 ≈ 35일이라는 계산을 하고, GPU 수는 가정이라는 점을 밝힌다.
  - [ ] GQA는 학습 compute를 거의 줄이지 않고(attention projection 일부만 작아짐) 주로 **추론**을 위한 선택이라는 점을 말한다.
- **함께 볼 개념:** W01: [65B 학습의 메모리와 처리량 계산](../w01/llama1-reading-map.html#c-memory-math)

<a id="c-carbon"></a>

### 탄소 발자국과 그 가정

- **무엇인가:** GPU 시간 × GPU 전력(TDP)에 탄소 집약도를 곱해 사전학습 배출량을 추정한 값입니다.
- **원문:** [§2.2.1 · Table 2](https://arxiv.org/pdf/2307.09288v2#page=7) — 총 3.3M GPU-hours, **539 tCO₂eq**, 전량 Meta가 상쇄. 실제 사용 전력 대신 TDP를 쓰고, interconnect · 서버 · 냉각 전력과 GPU 생산 배출은 넣지 않았다고 적습니다.
- **계산해 보면 (추출자 계산):** 7B 184,320 h × 0.4 kW = 73.7 MWh → 31.22 t ÷ 73.7 MWh = 0.4235 t/MWh. 34B(350W)도 같은 0.4235가 나옵니다. 이는 **LLaMA 1이 쓴 0.385 kg/kWh × PUE 1.1 = 0.4235**와 정확히 같아, 같은 가정을 쓴 것으로 보입니다. 전체 전력은 약 1,273 MWh입니다(LLaMA 1 65B 449 MWh).
- **설명할 수 있어야 하는 것:**
  - [ ] Table 2의 열(GPU 시간 · 전력 · 배출)로 계수를 역산해 LLaMA 1과 같은 가정임을 보인다.
  - [ ] 원문이 빠뜨렸다고 스스로 밝힌 전력 항목을 말한다.
  - [ ] 후학습(SFT · RLHF · 사람 평가)의 compute와 배출은 이 표에 없다는 점을 말한다.
- **함께 볼 개념:** W01: [탄소 발자국 추정](../w01/llama1-reading-map.html#c-carbon)

<!-- part: data -->
## Data & Synthesis

### 이 파트의 질문

- **담당:** 정호찬 (Data & Synthesis)
- **출발점:** W01에서는 [CommonCrawl — 67%, 네 단계 필터](../w01/llama1-reading-map.html#c-src-cc)와 [웹 품질 필터의 계보](../w01/llama1-reading-map.html#c-quality-lineage)를 한 장씩만 봤습니다. 이번에는 각 단계가 **무슨 모델로, 어떤 수식과 기준값으로** 돌아가는지 원전과 코드까지 내려가 봅니다.
- **범위:** W01에서 넘긴 품질 분류기(fastText + KenLM). Llama 2 원문은 [§2.1](https://arxiv.org/pdf/2307.09288v2#page=5)의 “more robust data cleaning” 한 구절뿐이라, LLaMA 1 §2.1과 CCNet · fastText · KenLM 원전이 분량의 대부분입니다. §2.1의 나머지 내용은 RQ1의 맥락 페이지로 둡니다.
- **RQ1. Llama 2는 데이터 정제에 대해 무엇을 적었고 무엇을 적지 않았나?**
  - 필수 원문: [Llama 2 §2 · §2.1](https://arxiv.org/pdf/2307.09288v2#page=5) · [§4.1](https://arxiv.org/pdf/2307.09288v2#page=20) · [Table 10](https://arxiv.org/pdf/2307.09288v2#page=22)
  - 개념: [Llama 2 원문이 말한 것과 말하지 않은 것](#c-q-llama2-said) · [로드맵](#c-q-roadmap)
  - 맥락(선택): [사전학습 데이터: 적힌 것과 빠진 것](#c-pretrain-corpus) · [언어 분포](#c-language-dist) · [추가 독성 필터링을 하지 않은 결정](#c-no-scrub)
- **RQ2. LLaMA 1이 쓴 CCNet은 어떤 순서로, 무엇을 거르나?**
  - 필수 원문: [LLaMA 1 §2.1](https://arxiv.org/pdf/2302.13971v1#page=2) · [CCNet §3–§5](https://arxiv.org/pdf/1911.00359v2#page=2)
  - 개념: [CCNet 파이프라인](#c-q-ccnet-pipeline) · [fastText 언어 식별](#c-q-langid)
- **RQ3. fastText 분류기와 KenLM perplexity는 각각 무엇을 계산하나?**
  - 필수 원문: [fastText §2](https://arxiv.org/pdf/1607.01759v3#page=1) · [CCNet §3.4](https://arxiv.org/pdf/1911.00359v2#page=2) · [KenLM (Heafield 2011)](https://aclanthology.org/W11-2123.pdf)
  - 개념: [fastText 분류기의 구조](#c-q-fasttext) · [KenLM과 perplexity](#c-q-kenlm-ppl) · [head · middle · tail](#c-q-ppl-buckets)
- **RQ4. “Wikipedia 참조 페이지 분류기”는 어떻게 재현됐고, 그 뒤 기준은 어떻게 바뀌었나?**
  - 필수 원문: [LLaMA 1 §2.1](https://arxiv.org/pdf/2302.13971v1#page=2) · [GPT-3 App. A](https://arxiv.org/pdf/2005.14165v4#page=43) · [Llama 3 §3.1.1](https://arxiv.org/pdf/2407.21783v3#page=5)
  - 개념: [참조 페이지 분류기](#c-q-ref-classifier) · [그 뒤의 품질 분류기](#c-q-followup)

<a id="c-q-llama2-said"></a>

### Llama 2 원문이 데이터 정제에 대해 말한 것과 말하지 않은 것

- **무엇인가:** Llama 2 본문에서 사전학습 데이터 정제와 관련된 문장을 모두 모아, 기술됨 / 미기술 / 하지 않았다고 명시로 나눈 표입니다.
- **원문:** [§2](https://arxiv.org/pdf/2307.09288v2#page=5) · [§2.1](https://arxiv.org/pdf/2307.09288v2#page=5) · [§4.1 Steps Taken to Pretrain Responsibly](https://arxiv.org/pdf/2307.09288v2#page=20) · [§4.1 Language Identification](https://arxiv.org/pdf/2307.09288v2#page=21) · [Table 10](https://arxiv.org/pdf/2307.09288v2#page=22)

| 항목 | 구분 | 원문 근거 |
| --- | --- | --- |
| 정제를 강화했다 | **기술됨 (한 구절)** | §2: “we performed more robust data cleaning”. 무엇을 어떻게 바꿨는지는 없음 |
| 새 데이터 혼합 | 기술됨 | §2.1: “a new mix of data from publicly available sources”, Meta 제품 · 서비스 데이터 미포함 |
| 개인정보 많은 사이트 제거 | 기술됨 | §2.1 · §4.1: “certain sites known to contain a high volume of personal information about private individuals” |
| 사실적 소스 up-sampling | 기술됨 (의도만) | §2.1: “up-sampling the most factual sources in an effort to increase knowledge and dampen hallucinations”. 어느 소스를 몇 배로 올렸는지는 없음 |
| 중복 제거 단위 · 언어 필터 · LM 필터 · 참조 페이지 분류기 | **미기술** | Llama 2 본문 어디에도 CCNet · KenLM · 참조 페이지 분류기가 나오지 않음. §2가 “LLaMA 1의 사전학습 방식에서 출발했다”고만 적음 |
| 추가 필터링 | **하지 않았다고 명시** | §4.1: “No additional filtering was conducted on the datasets”. 맥락은 독성 · 인구 집단 삭제(over-scrubbing) 회피입니다 |
| fastText 언어 식별 | 기술됨 (**분석용**) | §4.1: “fastText (Bojanowski et al., 2016) language identification tool and a threshold of 0.5”. Table 10의 언어 분포를 **측정**하는 데 쓴 것이고, 이것으로 데이터를 걸렀다는 문장은 없음 |

- **왜 조심해야 하나:** “No additional filtering”을 “품질 필터가 없었다”로 읽으면 미기술을 미수행으로 바꾸는 셈입니다. 같은 문단이 개인정보 사이트 제거와 법무 검토를 함께 적고, 이유도 독성 분류나 인구 집단 삭제 같은 안전 쪽 맥락에서 댑니다. 그래서 이 문장은 “안전 목적의 추가 scrub을 하지 않았다”로 읽는 쪽이 원문에 가깝습니다(추출자 해석).
- **LLaMA 1과 이어지는 고리:** Llama 2가 LLaMA 1의 방식을 출발점으로 삼았다고 적었으므로 CCNet류 정제를 이어 썼을 가능성은 있습니다. 하지만 원문이 그렇다고 말하지는 않습니다. 발표에서는 “LLaMA 1에서 기술됨 → Llama 2에서는 미기술”로 구분해 말합니다.
- **계산해 보면:** Table 10에 나열된 28개 항목의 합은 **99.99%** 입니다. 영어 89.70%와 unknown 8.38%를 더하면 98.08%이고, 나머지 26개 언어를 다 합쳐도 1.91%입니다(`scripts/table10_sum.py`). unknown에 대해 원문은 “partially made up of programming code data”라고 적었습니다. 아래 [언어 식별](#c-q-langid)에서 실제 lid.176 모델에 코드를 넣으면 점수가 0.5를 넘지 못하는 것을 확인합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Llama 2의 정제 관련 문장을 기술됨 / 미기술 / 하지 않았다고 명시로 나눠 말한다.
  - [ ] fastText 언어 식별이 Llama 2에서는 **필터가 아니라 분석 도구**로 등장한다는 점을 말한다(임계값 0.5).
  - [ ] “No additional filtering”의 범위를 원문 맥락(독성 · over-scrubbing)과 함께 말한다.
- **함께 볼 개념:** [로드맵](#c-q-roadmap) · W02: [사전학습 데이터: 적힌 것과 빠진 것](#c-pretrain-corpus) · [추가 독성 필터링을 하지 않은 결정](#c-no-scrub) · [언어 분포](#c-language-dist)

<a id="c-q-roadmap"></a>

### 품질 필터 로드맵: GPT-3 → CCNet → LLaMA 1 → Llama 2 → Llama 3 · DCLM · FineWeb-Edu

- **무엇인가:** “좋은 웹 글”을 고르는 기준(양성 예시)과 채점 모델이 세대마다 어떻게 바뀌었는지 한 장으로 본 표입니다. 기준값은 원문에 있는 것만 적었습니다.

| 시점 | 작업 | 채점 모델 | “좋은 글”의 기준 | 남기는 규칙 | 근거 |
| --- | --- | --- | --- | --- | --- |
| 2019.11 | CCNet | KenLM 5-gram (SentencePiece 위) | 언어별 **Wikipedia**에서 학습한 LM의 낮은 perplexity | 거르지 않고 head · middle · tail로 **나누기만** 함 | [§3.4 · §5.2](https://arxiv.org/pdf/1911.00359v2#page=3) |
| 2020.05 | GPT-3 | 로지스틱 회귀 (Spark tokenizer + HashingTF) | WebText · Wikipedia · 웹 책 말뭉치 vs 원시 CC | `np.random.pareto(9) > 1 − score`인 문서만 확률적으로 유지 | [App. A](https://arxiv.org/pdf/2005.14165v4#page=43) |
| 2023.02 | LLaMA 1 | CCNet + “linear model” | Wikipedia가 **참고문헌으로 인용한 페이지** vs 무작위 페이지 | 참조로 분류되지 않은 페이지 버림 (기준값 미기술) | [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) |
| 2023.04 | RedPajama v1 (재현, 논문 밖) | CCNet head+middle + fastText 이진 분류기 | Wikipedia 참조 URL 약 30만 페이지 vs 같은 수의 CC 페이지 | `wiki_prob ≥ 0.25` | [rp_v1 README](https://github.com/togethercomputer/RedPajama-Data/blob/rp_v1/data_prep/cc/README.md) |
| 2023.07 | **Llama 2** | **미기술** | 미기술 (“more robust data cleaning”, factual up-sampling) | 미기술 | [§2 · §2.1](https://arxiv.org/pdf/2307.09288v2#page=5) |
| 2024.06 | DCLM | fastText (unigram+bigram) | **OpenHermes 2.5 + ELI5** (지시문 형식 데이터) vs RefinedWeb 재현본 | 점수 상위 **10%** | [§4.4 · Table 5](https://arxiv.org/pdf/2406.11794v4#page=9) |
| 2024.06 | FineWeb-Edu | Snowflake-arctic-embed-m + 선형 회귀 | Llama-3-70B-Instruct가 매긴 **교육적 가치 0–5점** | 반올림 점수 **≥ 3** | [§4](https://arxiv.org/pdf/2406.17557v2#page=8) |
| 2024.07 | Llama 3 | fastText + DistilRoBERTa | “Wikipedia가 인용할 만한가” + **Llama 2가 판정한** 품질 요구 | 여러 설정을 실험했다고만 적음 (최종 기준값 미기술) | [§3.1.1](https://arxiv.org/pdf/2407.21783v3#page=5) |

- **표에서 읽을 것:** 기준이 “고품질 말뭉치와 닮았나”(CCNet · GPT-3) → “편집자가 인용할 만한가”(LLaMA 1) → “LLM이 좋다고 판정하나”(Llama 3 · FineWeb-Edu) → “지시문 데이터와 닮았나”(DCLM)로 옮겨 갑니다. 채점 모델은 n-gram LM과 선형 분류기에서 임베딩 모델 위의 회귀로 커졌지만, DCLM의 최선 방법은 여전히 fastText였습니다.
- **분류의 반례 먼저:** “모델 기반 필터가 규칙 필터보다 낫다”로 정리하고 싶어지지만, DCLM Table 4(1B-1x)에서 PageRank 상위 20%는 CORE 26.1로 필터를 안 건 RefinedWeb 재현본(27.5)보다 낮았습니다. 반대로 Llama 3는 모델 필터와 함께 규칙(중복 n-gram 비율, dirty word, KL divergence)도 계속 썼습니다. 모델이냐 규칙이냐보다 **무엇을 양성으로 두나**가 결과를 더 크게 갈랐다는 것이 DCLM Table 5의 결과입니다(아래 [후속](#c-q-followup)).
- **설명할 수 있어야 하는 것:**
  - [ ] 세대별 “좋은 글”의 기준을 한 줄씩 말하고, Llama 2 칸이 비어 있는 이유(원문 미기술)를 말한다.
  - [ ] CCNet은 LM 점수로 **나누기만** 했고, 실제로 버린 것은 그 위에서 bucket을 고른 사용자(예: RedPajama의 head+middle)라는 점을 말한다.
  - [ ] 기준값(GPT-3의 α=9, RedPajama의 0.25, DCLM의 상위 10%, FineWeb-Edu의 3점)이 각각 어디서 나왔는지 말한다.
- **함께 볼 개념:** W01 [웹 품질 필터의 계보](../w01/llama1-reading-map.html#c-quality-lineage) · [CCNet 파이프라인](#c-q-ccnet-pipeline) · [그 뒤의 품질 분류기](#c-q-followup)

<a id="c-pretrain-corpus"></a>

### 사전학습 데이터: 적힌 것과 빠진 것

- **무엇인가:** Llama 2의 사전학습 데이터는 “공개 출처의 새 혼합”이라는 것 외에 소스 목록과 비율이 공개되지 않았습니다. LLaMA 1(W01)과 가장 크게 달라진 점입니다.
- **원문:** [§2 · §2.1](https://arxiv.org/pdf/2307.09288v2#page=5) · [§4.1 Steps Taken to Pretrain Responsibly](https://arxiv.org/pdf/2307.09288v2#page=20) · [Table 52](https://arxiv.org/pdf/2307.09288v2#page=77)

| 항목 | 원문에 적힌 것 | 원문에 없는 것 |
| --- | --- | --- |
| 출처 | 공개된 온라인 출처의 새 혼합, Meta 제품 · 서비스 · 사용자 데이터 미포함 | 소스 이름 · 비율 · epochs (LLaMA 1 Table 1에 해당하는 표) |
| 정제 | “more robust data cleaning”, 개인정보가 많은 일부 사이트 제거, 데이터셋마다 Meta의 개인정보 · 법무 검토 | 정제 단계 · 필터 · 중복 제거 단위 |
| 혼합 | 가장 사실적인(factual) 소스를 **up-sampling** — 지식을 늘리고 환각을 줄이려는 의도 | 어느 소스를 몇 배로 올렸는지 |
| 규모 | 2T 토큰, “좋은 성능–비용 trade-off” | 고유 토큰 수 · 반복량 |
| 시점 | 사전학습 데이터 cutoff 2022년 9월, 일부 tuning 데이터 2023년 7월까지, 학습 기간 2023년 1–7월 | – |

- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA 1이 공개한 것(7개 소스 · 비율 · 소스별 전처리)과 Llama 2가 공개한 것을 표로 비교한다.
  - [ ] factual up-sampling의 효과(환각 감소)는 의도로 적혀 있을 뿐 따로 측정한 실험이 없다는 점을 말한다.
  - [ ] 비율 대신 공개한 것이 “분석”(언어 · 인구 표현 · 독성, §4.1)이라는 점을 다음 페이지들과 연결한다.
- **함께 볼 개념:** [추가 독성 필터링을 하지 않은 결정](#c-no-scrub) · W01: [Llama 2 · Llama 3의 데이터](../w01/llama1-reading-map.html#c-llama-data) · [Books3와 ‘공개 데이터’의 경계](../w01/llama1-reading-map.html#c-books3)

<a id="c-language-dist"></a>

### 언어 분포

- **무엇인가:** 사전학습 데이터의 언어 구성입니다. 언어별 비율을 정해서 섞은 것이 아니라, 섞인 결과를 fastText 언어 식별(임계값 0.5)로 측정한 값입니다.
- **원문:** [§4.1 Language Identification · Table 10](https://arxiv.org/pdf/2307.09288v2#page=22) — 문서의 0.005% 넘게 나오는 언어만 표에 적었습니다.

| 언어 | 비율 | 언어 | 비율 |
| --- | --- | --- | --- |
| 영어 | 89.70% | 일본어 | 0.10% |
| unknown (코드 일부 포함) | 8.38% | 폴란드어 · 포르투갈어 | 각 0.09% |
| 독일어 | 0.17% | 베트남어 | 0.08% |
| 프랑스어 | 0.16% | 우크라이나어 | 0.07% |
| 스웨덴어 | 0.15% | **한국어** | **0.06%** |
| 중국어 · 스페인어 · 러시아어 | 각 0.13% | 카탈루냐어 · 세르비아어 | 각 0.04% |
| 네덜란드어 | 0.12% | 그 외 9개 언어 | 0.01–0.03% |
| 이탈리아어 | 0.11% | | |

- **계산해 보면 (추출자 계산):** 영어와 unknown을 뺀 26개 언어의 합은 **1.91%**입니다. 표의 단위가 문서인지 토큰인지 원문이 밝히지 않으므로, 토큰 비율로 가정하면 한국어는 2T × 0.06% ≈ **12억 토큰**입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA 1의 다국어는 Wikipedia 20개 라틴 · 키릴 언어였고, Llama 2 표에는 중국어 · 일본어 · 한국어 · 베트남어 · 인도네시아어가 나타난다는 차이를 말한다.
  - [ ] unknown 8.38%의 일부가 코드라는 원문 설명을 말한다.
  - [ ] 저자가 이 분포를 근거로 영어 외 언어 사용을 권하지 않는다는 점(§5.2 · 모델 카드의 out-of-scope)을 말한다.
- **함께 볼 개념:** W01: [다국어 구성](../w01/llama1-reading-map.html#c-multilingual)

<a id="c-no-scrub"></a>

### 추가 독성 필터링을 하지 않은 결정

- **무엇인가:** 독성 문서를 사전학습 데이터에서 걸러내지(scrub) 않기로 한 선택과, 대신 독성 비율을 측정해 공개한 것입니다.
- **원문:** [§4.1](https://arxiv.org/pdf/2307.09288v2#page=20) — “No additional filtering was conducted on the datasets”. 저자가 든 이유는 세 가지입니다.
  1. 혐오 표현 분류 같은 과제에도 쓸 수 있도록 범용성을 유지.
  2. 과도한 정제가 특정 인구 집단을 우연히 지우는 문제(demographic erasure)를 피함.
  3. 덜 거른 데이터로 학습한 모델이 **더 적은 예시로 안전 튜닝**된다는 관찰.
- **측정 방법:** [Fig. 13](https://arxiv.org/pdf/2307.09288v2#page=21) — ToxiGen으로 학습한 HateBERT 분류기로 문서의 각 줄을 점수 매겨 평균한 값을 문서 점수로 씁니다. 전체 말뭉치의 10% 무작위 표본에서 독성 확률 0.5 이상인 문서는 약 **0.2%**입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] “추가 필터링 없음”이 “정제 없음”이 아니라는 점을 말한다. 개인정보 사이트 제거와 데이터 정제는 따로 했습니다.
  - [ ] 그 결과로 사전학습 13B · 70B의 ToxiGen 점수가 LLaMA 1보다 높아졌고, 저자가 이를 필터링을 덜 한 탓으로 추정한다는 연결을 말한다(§4.1 [Table 11](https://arxiv.org/pdf/2307.09288v2#page=22), 배정 밖).
  - [ ] 그래서 저자가 기반 모델을 “상당한 안전 튜닝 뒤에만 배포하라”고 적은 이유를 말한다.
- **원전:** HateBERT [arXiv:2010.12472](https://arxiv.org/abs/2010.12472) · ToxiGen [arXiv:2203.09509](https://arxiv.org/abs/2203.09509)

<a id="c-q-ccnet-pipeline"></a>

### CCNet 파이프라인 — 중복 제거 → 언어 식별 → LM 점수

- **무엇인가:** Facebook AI가 2019년에 공개한 CommonCrawl 정제 파이프라인입니다. 스냅숏 하나를 받아 문단 해시로 중복을 지우고, fastText로 언어를 정하고, 언어별 Wikipedia LM으로 perplexity를 매겨 언어 × {head, middle, tail} 파일로 나눕니다. LLaMA 1 저자 중 Marie-Anne Lachaux · Armand Joulin · Edouard Grave는 CCNet 저자이기도 합니다(두 논문의 저자 목록으로 확인).
- **원문:** [LLaMA 1 §2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — “deduplicates the data at the line level, performs language identification with a fastText linear classifier … and filters low quality content with an n-gram language model.” 원전은 [CCNet arXiv:1911.00359v2](https://arxiv.org/abs/1911.00359) (LLaMA 1은 LREC 2020판을 인용).

| 단계 | CCNet 원문에 적힌 것 | 절 |
| --- | --- | --- |
| 0. 샤딩 | 스냅숏 하나는 압축 해제 기준 20–30TB, 약 30억 페이지(2019년 2월판 24TB). WET 파일을 5GB 샤드로 묶어 **1,600개 샤드** | [§3.1](https://arxiv.org/pdf/1911.00359v2#page=2) |
| 1. 중복 제거 | 문단을 정규화(소문자, 숫자 → 0, 유니코드 구두점 · 악센트 제거)한 뒤 **SHA-1의 앞 64비트**를 키로 씀. 중복 문단이 텍스트의 **70%**. 메뉴 · 쿠키 경고 · 연락처 같은 boilerplate가 함께 빠짐 | [§3.2](https://arxiv.org/pdf/1911.00359v2#page=2) |
| 2. 언어 식별 | fastText 분류기, 최고 점수가 **0.5 초과**면 그 언어, 아니면 버림 | [§3.3](https://arxiv.org/pdf/1911.00359v2#page=2) |
| 3. LM 점수 | 언어별 SentencePiece + KenLM **5-gram Kneser-Ney**를 Wikipedia로 학습, 문단마다 perplexity. 언어마다 perplexity로 **같은 크기 세 덩어리** head · middle · tail | [§3.4](https://arxiv.org/pdf/1911.00359v2#page=3) |

- **왜 이 순서인가 (저자 설명 + 실험):** 다른 언어 페이지에도 영어 쿠키 경고 같은 boilerplate가 많아서, 중복을 먼저 지워야 언어 판정이 정확해진다고 적었습니다([§4.1](https://arxiv.org/pdf/1911.00359v2#page=3), Fig. 3). 기존 Grave et al. (2018)과 순서를 바꾼 것이고, 순서를 바꾸기 전에는 저자원 언어 문서가 영어로 잘못 분류되거나 언어 미확정으로 버려졌다고 보고합니다. 아래 [언어 식별](#c-q-langid)에서 이 효과를 lid.176으로 재현합니다.
- **중복 제거의 범위 (실험):** 몇 개 샤드의 해시와 비교하느냐에 따라 남는 양이 다릅니다. 샤드 하나 안에서만 비교하면 문자 기준 **42%**가, 100개 샤드와 비교하면 **28%**가 남습니다. 50개 샤드의 해시는 15억 개, 디스크 13.5GB, RAM 40GB였고, 저자들은 50개 샤드(코퍼스의 약 3%)를 절충점으로 골랐습니다([§4.2](https://arxiv.org/pdf/1911.00359v2#page=3)).
- **비용 (원문 수치):** 해시 계산은 CPU 코어 하나에서 초당 약 600문서, 1,600 CPU로 45분. 두 번째 단계에서는 CPU 시간 중 언어 식별이 12.5%, SentencePiece가 33%, LM이 13%를 차지합니다. 전체는 서론에서 “5,000 CPU 코어로 스냅숏당 8.5시간”, §4.3에서 “약 9시간”이라고 적어 **두 곳의 값이 조금 다릅니다**.
- **결과 규모:** 2019년 2월 스냅숏 하나에서 174개 언어 3.2TB(압축). 영어는 문서 706M, 토큰 532B입니다([§5.1](https://arxiv.org/pdf/1911.00359v2#page=4), Table 6).
- **코드에서 확인한 것 (논문 밖, [cc_net main](https://github.com/facebookresearch/cc_net) 마지막 커밋 2020-12-09):** `dedup.py`는 문서를 `"\n"`으로 잘라 줄마다 해시합니다. CCNet 논문이 “paragraph”라 부르고 LLaMA 1이 “line level”이라 부르는 것이 WET 텍스트의 같은 줄 단위라는 뜻입니다. `mine.py` 기본값은 `lang_threshold=0.5`, `hash_in_mem=50`, `min_len=300`(300자 미만 문서 제거)입니다. LLaMA 1이 이 기본값을 그대로 썼는지는 **미기술**입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 세 단계의 순서와, 중복 제거를 언어 식별보다 먼저 하는 이유를 Fig. 3의 결과와 함께 말한다.
  - [ ] 중복 제거가 페이지가 아니라 **줄(문단) 단위**라서 페이지 본문은 남고 반복 줄만 빠진다는 점을 말한다.
  - [ ] 중복 비교 범위(1 샤드 42% → 100 샤드 28%)와 RAM 사이의 trade-off를 말한다.
- **함께 볼 개념:** [fastText 언어 식별](#c-q-langid) · [KenLM과 perplexity](#c-q-kenlm-ppl) · [head · middle · tail](#c-q-ppl-buckets) · W01 [CommonCrawl — 67%](../w01/llama1-reading-map.html#c-src-cc)

<a id="c-q-langid"></a>

### fastText 언어 식별 — lid.176과 임계값 0.5

- **무엇인가:** 텍스트 한 덩어리를 176개 언어 중 하나로 분류하는 fastText 모델입니다. 공개 모델 이름이 `lid.176.bin`(126MB)과 압축판 `lid.176.ftz`(917kB)입니다.
- **원문:**
  - [CCNet §3.3](https://arxiv.org/pdf/1911.00359v2#page=2) — Wikipedia · Tatoeba · SETimes로 학습, **문자 n-gram** 특징, hierarchical softmax, 176개 언어, 언어마다 [0, 1] 점수. CPU 코어 하나에서 **초당 1,000문서**. 최고 점수가 0.5보다 높으면 그 언어로 분류하고, 아니면 버림.
  - [fastText 언어 식별 문서](https://fasttext.cc/docs/en/language-identification.html) — 학습 데이터(Wikipedia · Tatoeba · SETimes, CC-BY-SA), 두 파일 크기, “bin이 조금 더 빠르고 정확하다”는 설명. 정확도 수치는 이 페이지에 없음. 모델 라이선스는 CC BY-SA 3.0.
  - [Llama 2 §4.1](https://arxiv.org/pdf/2307.09288v2#page=21) — 같은 계열 도구를 임계값 0.5로 **분석**에 썼습니다. 인용은 Bojanowski et al. (2016, “Enriching Word Vectors with Subword Information”)이고, fastText 문서가 인용하라고 하는 논문(Joulin et al. 2016 두 편)과는 다릅니다. 어느 모델 파일을 썼는지는 미기술입니다.
- **왜 문자 n-gram인가:** 언어 판별의 단서는 단어보다 철자 패턴(예: `ção`, `sch`, 한글 음절)에 많고, 처음 보는 단어도 조각은 아는 경우가 많기 때문입니다. 단어 기반 분류기를 다룬 Bag of Tricks 논문 자체에는 문자 n-gram이 없고, 하위 단어 특징은 Bojanowski et al. (2016)에서 들어왔습니다. Llama 2가 Bojanowski를 인용한 것도 이 점과 맞습니다(추출자 해석).
- **돌려 보면 (설명용, 실제 `lid.176.ftz`, sha256 `8f3472cf…`, fasttext-wheel 0.9.2):** 직접 쓴 문장 10개를 넣고 CCNet 규칙(최고 점수 > 0.5)을 적용했습니다. `scripts/lid_demo.py`

| 입력 | 1순위 | 점수 | CCNet 규칙 |
| --- | --- | --- | --- |
| 영어 문장 | en | 0.978 | en |
| 한국어 문장 | ko | 1.000 | ko |
| 한영 혼합 (“오늘 meeting 에서 deadline 을…”) | ko | 0.998 | ko |
| 파이썬 코드 한 줄 | en | 0.425 | **버림** |
| HTML/CSS 조각 | ru | 0.105 | **버림** |
| 메뉴 한 줄 `Home \| About \| Contact \| Login` | en | 0.146 | **버림** |
| `OK` | en | 0.125 | **버림** |
| 숫자만 있는 줄 | en | 0.125 | **버림** |
| 프랑스어 문장 + 영어 쿠키 문구 | fr | 0.663 (en 0.244) | fr |
| 같은 문장에서 쿠키 문구를 지움 | fr | 0.962 (en 0.019) | fr |

  - 마지막 두 줄이 CCNet §4.1의 주장(boilerplate를 먼저 지우면 언어 판정이 정확해진다)을 작은 규모로 보여 줍니다. 영어 쿠키 문구 하나 때문에 프랑스어 점수가 0.962에서 0.663으로 떨어졌습니다. 문서가 더 짧거나 영어 문구가 더 길었다면 0.5 아래로 내려가 버려졌을 것입니다(추출자 해석).
  - 코드와 HTML은 0.5를 넘지 못했습니다. Llama 2 Table 10의 unknown 8.38%를 원문이 “부분적으로 코드”라고 설명한 것과 맞는 결과입니다. 다만 Llama 2가 이 모델 파일과 이 입력 단위를 썼는지는 미기술이라서, 이 실행은 메커니즘을 보여 줄 뿐 Table 10을 재현한 것은 아닙니다.
  - `OK`와 숫자 줄의 분포가 en 0.125, ca 0.086으로 똑같았습니다. 쓸 만한 특징이 거의 없을 때 모델이 내는 기본 분포로 보입니다(추출자 해석).
  - 실행 메모: fasttext-wheel 0.9.2의 `predict()`는 NumPy 2에서 `copy=False` 오류가 나서, 내부 `m.f.predict()`를 직접 불렀습니다. 확률 값은 같은 함수에서 나옵니다.
- **기준값은 작업마다 다릅니다:** CCNet과 Llama 2는 0.5, FineWeb은 영어 점수 **≥ 0.65**를 썼습니다([FineWeb §3.3](https://arxiv.org/pdf/2406.17557v2#page=4)).
- **설명할 수 있어야 하는 것:**
  - [ ] lid.176의 학습 데이터 · 언어 수 · 특징(문자 n-gram) · 기준값 0.5를 말한다.
  - [ ] Llama 2에서는 이 도구가 필터가 아니라 Table 10을 만든 측정 도구라는 점을 말한다.
  - [ ] 혼합 언어 페이지에서 boilerplate가 점수를 끌어내리는 예를 들어, 중복 제거를 먼저 하는 이유를 설명한다.
- **함께 볼 개념:** [fastText 분류기의 구조](#c-q-fasttext) · [CCNet 파이프라인](#c-q-ccnet-pipeline) · W02 [언어 분포](#c-language-dist) · 원전: [Joulin et al. 2016 arXiv:1607.01759](https://arxiv.org/abs/1607.01759) · [Bojanowski et al. 2016 arXiv:1607.04606](https://arxiv.org/abs/1607.04606) · [Grave et al. 2018 arXiv:1802.06893](https://arxiv.org/abs/1802.06893)

<a id="c-q-fasttext"></a>

### fastText 분류기의 구조 — 임베딩 평균 위의 선형층

- **무엇인가:** 문서를 단어(와 n-gram) 조각으로 쪼개 조각마다 벡터를 찾고, 그 벡터들을 **평균**해 문서 벡터 하나를 만든 뒤 선형층과 softmax로 라벨 확률을 내는 분류기입니다. 은닉층에 비선형이 없어서 “rank 제약이 걸린 선형 모델”이라고 부릅니다.
- **원문:** [Joulin et al. 2016 §2](https://arxiv.org/pdf/1607.01759v3#page=1) — 목표 함수는 $-\frac{1}{N}\sum_{n=1}^{N} y_n \log f(BAx_n)$ 입니다. 여기서 $x_n$은 n번째 문서의 정규화된 특징 가방(bag of features), $A$는 단어 · n-gram 임베딩 표(look-up table), $B$는 출력 선형층, $f$는 softmax입니다. CPU 여러 개에서 비동기 SGD로, 학습률을 선형으로 줄이며 학습합니다.

| 장치 | 원문 내용 | 왜 필요한가 |
| --- | --- | --- |
| 임베딩 평균 | word2vec의 CBOW 구조에서 가운데 단어 자리에 라벨을 둔 형태 | 특징과 클래스 사이에 파라미터를 공유해, 예시가 적은 클래스도 일반화 |
| hierarchical softmax (§2.1) | Huffman 트리, 학습 계산량 $O(kh) → O(h \log_2 k)$ ($k$ = 클래스 수, $h$ = 은닉 차원) | 클래스가 많을 때(언어 176개, 태그 31만 개) 속도 |
| n-gram 특징 (§2.2) | bag of n-grams로 국소 어순을 일부 반영 | 순서를 모델링하지 않고도 정확도 1–4%p 상승(감성 분류, bigram 추가 시) |
| hashing trick (§2.2) | bigram만 쓰면 1,000만 bin, 그 이상이면 1억 bin | n-gram 사전을 저장하지 않고 고정 메모리 |

- **속도 주장 (원문 수치):** 표준 멀티코어 CPU로 10억 단어 이상을 10분 안에 학습하고, 50만 문장을 31만 2천 개 클래스 중에서 1분 안에 분류합니다(초록). 감성 분류 8개 데이터셋에서 fastText(h=10, bigram)는 한 epoch에 1–10초, char-CNN · VDCNN은 수십 분에서 며칠이었고(Table 2, CNN은 Tesla K40 GPU, fastText는 CPU 20 스레드), 정확도는 VDCNN보다 약간 낮고 char-CNN보다 약간 높았습니다(Table 1).
- **왜 데이터 필터에 쓰이나:** 수십억 문서에 점수를 매겨야 하므로 문서 하나의 비용이 거의 조회 + 평균 + 내적 한 번이어야 합니다. 같은 구조가 CCNet의 언어 식별(라벨 176개)에도, RedPajama · DCLM의 품질 분류기(라벨 2개)에도 쓰였습니다.
- **기본값을 같이 기억할 것:** `fasttext supervised`의 기본값은 lr 0.1, dim 100, epoch 5, wordNgrams 1(unigram만), minn · maxn 0(문자 n-gram 없음), loss softmax, bucket 200만입니다([옵션 문서](https://fasttext.cc/docs/en/options.html)). RedPajama는 옵션 없이 기본값으로 학습했고, DCLM은 wordNgrams만 2로 바꿨습니다.
- **돌려 보면 (설명용):** `scripts/toy_classifier.py` — 위 구조를 순수 파이썬으로 짰습니다. 단어 + 해시 bigram(4,096 bucket), 임베딩 8차원, 평균 → 선형 → sigmoid. 양성은 “기관 보고서 · 학술 · 법원” 문체를 흉내 낸 직접 쓴 문장 12개, 음성은 광고 · 메뉴 · 잡담 12개, 60 epoch(평균 loss 0.724 → 0.003).

| 처음 보는 입력 | P(참조 페이지) |
| --- | --- |
| 기관 보도문 | 0.999 |
| 백과사전 본문형 | 0.999 |
| 광고 | 0.025 |
| 쿠키 배너 | 0.003 |
| 전문 포럼 문장 (GPU 드라이버 질문, 정상 글) | 0.993 |
| 기관 어휘를 섞은 스팸 (“the report said buy now…”) | 0.213 |

  - 전문 포럼 글이 0.993인 것은 내용이 아니라 `the … the …` 같은 기능어 분포가 양성과 닮았기 때문으로 보입니다. 기관 어휘를 섞은 스팸이 0.213으로 RedPajama 기준 0.25와 가깝다는 점도 같은 성질을 보여 줍니다. 분류기는 “좋은 글”이 아니라 “양성 예시와 표면 통계가 닮은 글”을 고릅니다(추출자 해석).
  - 같은 24문장을 실제 fastText로 학습하면(`scripts/ft_supervised.py`) 기본값(epoch 5)에서는 모든 입력이 **0.500**으로 전혀 학습되지 않았고, epoch 50에서 기관 보도문 0.806 · 광고 0.361 · 전문 포럼 0.959가 나왔습니다. epoch 50 + wordNgrams 2에서는 다시 0.50 근처로 모였습니다. 기본값은 수십만 예시(RedPajama 약 60만, DCLM 40만)를 전제로 한 값이고, 24문장은 그 전제를 벗어납니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 목표 함수의 $A$(임베딩 표) · 평균 · $B$(선형층)가 각각 무엇인지 그림 없이 말한다.
  - [ ] hierarchical softmax와 hashing trick이 각각 어느 비용(클래스 수, n-gram 사전 크기)을 줄이는지 말한다.
  - [ ] 분류기가 표면 통계로 판단하기 때문에 생기는 오판(정상 전문 글 통과, 섞인 스팸의 경계 점수)을 예로 든다.
- **함께 볼 개념:** [fastText 언어 식별](#c-q-langid) · [참조 페이지 분류기](#c-q-ref-classifier) · 원전: [arXiv:1607.01759 §2](https://arxiv.org/abs/1607.01759) · [FastText.zip arXiv:1612.03651](https://arxiv.org/abs/1612.03651)

<a id="c-q-kenlm-ppl"></a>

### KenLM과 perplexity — Wikipedia LM이 매기는 “놀람”

- **무엇인가:** KenLM은 n-gram 언어모델을 **빠르게 조회**하는 C++ 라이브러리이고(Heafield 2011), 2013년부터는 modified Kneser-Ney 모델을 **추정**하는 `lmplz`도 들어 있습니다(Heafield et al. 2013). CCNet은 이것으로 언어별 Wikipedia 5-gram 모델을 만들고 웹 문서의 perplexity를 쟀습니다.
- **원문:**
  - [Heafield 2011](https://aclanthology.org/W11-2123.pdf) (WMT 2011) — PROBING(선형 탐사 해시 테이블, 속도용)과 TRIE(비트 패킹 · 정렬 · 보간 탐색 · 선택적 양자화, 메모리용) 두 자료구조. PROBING은 SRILM보다 **2.4배 빠르고 메모리는 57%**. 당시에는 모델 추정을 다른 도구에 의존했다(“we are currently dependent on them to generate an ARPA file”)고 적었습니다.
  - [Heafield et al. 2013](https://aclanthology.org/P13-2121.pdf) (ACL 2013) — 보간 포함 modified Kneser-Ney 추정을 스트리밍 + 정렬로 구현. RAM 140GB 머신 한 대로 2.8일에 1,260억 토큰의 가지치기 없는 모델. 3억 200만 토큰 모델에서는 SRILM 대비 RAM 7.7%, 벽시계 시간 14.0%.
  - [CCNet §3.4](https://arxiv.org/pdf/1911.00359v2#page=3) — “a 5-gram Kneser-Ney model as implemented in the KenLM library … because of its efficiency”. 논문은 “modified”라고 적지 않았습니다. 공개 Makefile은 `lmplz -o 5 … --discount_fallback`으로 모델을 만들고, SentencePiece는 unigram 모델 · 어휘 65,536, 학습 입력은 Wikipedia 문서 100만 개(`NDOC_FOR_LM`)입니다(코드 확인, 논문 밖). `lmplz`가 구현한 것은 modified KN입니다.
- **perplexity 식:** 토큰 $w_1 … w_N$ (문장 끝 `</s>` 포함)에 대해

  $$\mathrm{PPL} = \exp\Big(-\frac{1}{N}\sum_{i=1}^{N} \ln p(w_i \mid w_{i-n+1}^{\,i-1})\Big) = 10^{-\frac{1}{N}\sum_i \log_{10} p(w_i \mid \cdot)}$$

  “모델이 토큰마다 평균 몇 개 후보 사이에서 헷갈렸나”로 읽습니다. KenLM의 `score()`는 log10을 돌려주므로 cc_net 코드도 `10.0 ** (-log_score / length)`로 계산합니다(`perplexity.py`의 `pp()`).
- **Kneser-Ney가 하는 일 (두 단계 아래까지):** ① 본 적 없는 n-gram에도 확률을 주려면 본 n-gram에서 확률을 조금 떼어(할인 $D$) 짧은 문맥 모델로 넘겨야 합니다. ② 그런데 짧은 문맥 모델을 그냥 빈도로 만들면 “Francisco”처럼 자주 나오지만 “San” 뒤에만 나오는 단어가 과대평가됩니다. ③ 그래서 KN은 낮은 차수에서 빈도 대신 **그 단어 앞에 온 서로 다른 단어의 수**(continuation count)를 씁니다. modified KN은 할인을 빈도 1 · 2 · 3+로 나눠 세 개 씁니다.
- **돌려 보면 (설명용):** `scripts/kn_lm.py` — 백과사전 문체로 직접 쓴 20문장(어휘 100개)으로 3-gram 보간 KN(할인 하나, $D=0.75$, modified 아님)을 순수 파이썬으로 학습했습니다. 문맥별 확률 합이 1.000000인지 확인한 뒤 ARPA로 내보내 **실제 `kenlm` 파이썬 모듈로 다시 읽어** 같은 문장을 채점했습니다. 두 계산이 소수 첫째 자리까지 일치했습니다.

| 문장 | 토큰 N | OOV | Σ ln p | 순수 파이썬 PPL | kenlm Σ log10 | kenlm PPL |
| --- | --- | --- | --- | --- | --- | --- |
| 백과사전형 새 문장 | 13 | 0 | −22.029 | **5.4** | −9.567 | 5.4 |
| 구어체 블로그 문장 | 18 | 12 | −94.537 | 191.0 | −41.057 | 191.0 |
| 키워드 나열 스팸 | 13 | 12 | −74.728 | 313.7 | −32.454 | 313.7 |
| 메뉴 · 푸터 | 11 | 8 | −63.681 | 326.7 | −27.656 | 326.7 |
| 전문 포럼 문장 (정상) | 15 | 9 | −63.863 | 70.6 | −27.736 | 70.6 |
| 백과사전 구절 반복 (쓰레기) | 22 | 0 | −31.685 | **4.2** | −13.761 | 4.2 |

  - 손으로 확인: −22.029 ÷ ln 10 = −9.567, exp(22.029 / 13) = 5.4.
  - **반례가 표 안에 있습니다.** “the city is the capital of the city is the capital of…”를 세 번 반복한 쓰레기 문장이 PPL **4.2**로 가장 낮았습니다. 낮은 perplexity는 “기준 말뭉치에서 자주 본 연쇄”라는 뜻이지 “좋은 글”이라는 뜻이 아닙니다. 그래서 반복 n-gram 비율 같은 규칙 필터(Llama 3 §3.1.1의 duplicated n-gram coverage ratio 등)가 따로 필요합니다(추출자 해석).
  - 장난감 어휘가 100개뿐이라 높은 PPL은 대부분 OOV(`<unk>`)에서 나옵니다. 실제 CCNet은 SentencePiece로 잘라 OOV가 거의 없으므로 이 크기 차이를 실제 값으로 옮기면 안 됩니다.
- **설명할 수 있어야 하는 것:**
  - [ ] PPL 식을 ln과 log10 두 형태로 쓰고, 토큰 수 $N$에 `</s>`가 들어간다는 점을 말한다.
  - [ ] KenLM은 처음엔 조회 라이브러리였고 추정(`lmplz`, modified KN)은 2013년에 더해졌다는 점, CCNet 논문은 “Kneser-Ney”라고만 적었다는 점을 구분해 말한다.
  - [ ] continuation count가 왜 필요한지 “San Francisco” 예로 설명한다.
  - [ ] 반복 쓰레기 문장이 PPL이 가장 낮게 나온 결과로 “낮은 PPL ≠ 품질”을 설명한다.
- **함께 볼 개념:** [head · middle · tail](#c-q-ppl-buckets) · [CCNet 파이프라인](#c-q-ccnet-pipeline) · 원전: Kneser & Ney (1995) · Chen & Goodman (1998)

<a id="c-q-ppl-buckets"></a>

### head · middle · tail — perplexity로 나누기만 한 CCNet

- **무엇인가:** CCNet은 언어마다 문서 perplexity 기준값 두 개를 정해 문서를 head(낮음) · middle · tail(높음)로 나눕니다. **CCNet 자신은 아무것도 버리지 않았습니다.** 어느 bucket을 쓸지는 사용자가 정합니다.
- **원문:**
  - [§3.4](https://arxiv.org/pdf/1911.00359v2#page=3) — “each language is split into three even parts head, middle and tail”. 48개 언어의 SentencePiece · KN 모델과 tercile 기준값을 계산하는 코드를 공개.
  - [§5.2](https://arxiv.org/pdf/1911.00359v2#page=5) — “We decided to not remove content based on the LM score because we think that some of it could be useful for specific applications.” 언어마다 분포 모양이 달라 언어별 기준값을 썼고, 저자들은 그 차이가 그 언어 콘텐츠의 품질 차이라기보다 LM을 학습한 Wikipedia 크기 차이 때문이라고 **가정(저자 가설)**합니다. 영어 LM은 534M, 구자라트어는 12M의 텍스트로 학습(단위는 원문 그대로).
  - [§5.3 Table 1](https://arxiv.org/pdf/1911.00359v2#page=5) — head/middle/tail 각각으로 300차원 fastText 단어 벡터를 학습해 analogy로 평가.

| bucket | 영어 Total | Sem | Syn | 폴란드어 Total | Sem | Syn |
| --- | --- | --- | --- | --- | --- | --- |
| head | 77.9 | 81.2 | 75.3 | 65.3 | 66.5 | 64.1 |
| middle | 74.2 | 79.0 | 70.4 | 62.8 | 62.7 | 63.0 |
| tail | 62.0 | 68.1 | 57.3 | 59.9 | 59.8 | 60.1 |

  이 표가 “perplexity 필터가 효과 있다”의 원문 근거입니다. 다만 평가는 **단어 임베딩 analogy**이고 생성 LM의 성능이 아닙니다. BERT 실험(Table 2, XNLI)은 head 데이터와 Wikipedia를 비교한 것이고 bucket끼리 비교한 것이 아닙니다.
- **코드는 3등분이 아닙니다 (논문 밖, cc_net main):** `PerplexityBucket`의 기본값이 `percentile_head=30`, `percentile_tail=60`입니다. 기준값 표 `data/cutoff.csv`의 30번째 · 60번째 백분위를 쓰므로 비율로는 **30 / 30 / 40**입니다. 영어 기준값은 head < 340, middle < 520, 나머지 tail이고(같은 표의 33 · 66 백분위는 350 · 600), 한국어는 30 · 60 백분위가 920 · 2,130입니다. 논문의 “three even parts”와 공개 코드가 다르다는 점은 발표에서 그대로 말할 만합니다. LLaMA 1이 어느 bucket을 썼는지는 **미기술**이고, RedPajama는 head + middle을 썼습니다.
- **문서 perplexity의 계산 (코드):** `DocLM.do()`는 줄마다 KenLM log10 점수를 더하고, 줄마다 (토큰 수 + 1)을 더해 `10 ** (-합 / 길이)`로 문서 PPL을 냅니다. 줄별 PPL의 산술평균이 아니라 **토큰 가중 기하평균**입니다.
- **돌려 보면 (설명용):** `scripts/doc_buckets.py` — 위 장난감 LM으로 문서 6개를 cc_net 식대로 채점해 3등분했습니다.

| 문서 | 문서 PPL (cc_net 식) | 줄별 PPL 산술평균 | 3등분 |
| --- | --- | --- | --- |
| F 백과사전 구절 반복 (쓰레기) | 4.2 | 4.2 | **head** |
| A 백과사전형 2줄 | 4.7 | 4.7 | head |
| B 백과사전 1줄 + 메뉴 1줄 | 35.6 | 166.1 | middle |
| E 전문 포럼 (정상) | 73.2 | 74.4 | middle |
| C 구어체 블로그 (정상) | 177.4 | 174.1 | **tail** |
| D 스팸 | 347.5 | 383.5 | tail |

  - B는 메뉴 줄이 섞였는데도 기하평균이라 35.6에 그쳐 middle에 남았습니다. 산술평균(166.1)이었다면 블로그와 비슷한 값입니다. 계산 방식 하나가 bucket을 바꿉니다.
  - 정상 블로그 글이 스팸과 같은 tail로, 반복 쓰레기가 head로 갔습니다. CCNet §5.2가 직접 적은 한계와 같은 방향입니다. 원문은 “구어체 블로그 댓글이나 전문 용어가 많은 포럼은 유효한 글인데도 Wikipedia와 어휘가 달라 tail로 간다”고 썼습니다.
- **반례와 한계 (확인한 것만):**
  - CCNet 저자 스스로 perplexity를 “relative good proxy for quality”라고만 했고, 위 tail 문제를 적었습니다([§5.2](https://arxiv.org/pdf/1911.00359v2#page=5)).
  - 기준 말뭉치를 정하는 일 자체가 가치 판단이라는 연구: Gururangan et al. (2022)은 GPT-3 품질 필터를 다시 구현해 미국 고교 신문 기사에 적용했고, **더 크고 부유하며 교육 수준이 높은 도시 지역** 학교의 신문이 고품질로 분류되기 쉽다는 결과를 냈습니다. 필터 점수는 뉴스 사실성과도 관계가 없었습니다(p = 0.085, KS 검정)([arXiv:2201.10474](https://arxiv.org/abs/2201.10474) §3.2 · §4.2). 이것은 perplexity가 아니라 분류기 필터에 대한 결과입니다.
  - 규칙 필터에서도 같은 문제가 보고됐습니다. Dodge et al. (2021)은 C4의 금칙어 목록 필터가 African American English 문서를 **42%**, Hispanic-aligned English를 32% 제거한 데 비해 White-aligned English는 6.2%만 제거했다고 측정했습니다([arXiv:2104.08758](https://arxiv.org/abs/2104.08758) §5.3).
  - DCLM Table 4(1B-1x)에서는 CCNet식 perplexity 필터(단, KenLM이 아니라 Wikipedia · 책 · peS2o로 학습한 154M Transformer)가 CORE 29.0으로, 필터 없는 기준선(27.5)보다 좋았지만 fastText 분류기(30.2)보다 낮았습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] CCNet은 bucket으로 나누기만 했고 버린 것은 사용자의 선택이라는 점, LLaMA 1의 bucket 선택은 미기술이라는 점을 말한다.
  - [ ] 논문(3등분)과 코드(30/60 백분위) 기준이 다르다는 점과 영어 기준값을 말한다.
  - [ ] Table 1이 단어 임베딩 analogy 평가라는 조건을 붙여 head > middle > tail 결과를 말한다.
  - [ ] Wikipedia 기준 perplexity가 구어체 · 전문 포럼 글을 tail로 보내는 한계를 원문 문장과 장난감 결과로 설명한다.
- **함께 볼 개념:** [KenLM과 perplexity](#c-q-kenlm-ppl) · [참조 페이지 분류기](#c-q-ref-classifier) · [그 뒤의 품질 분류기](#c-q-followup)

<a id="c-q-ref-classifier"></a>

### Wikipedia 참조 페이지 분류기 — LLaMA 1, RedPajama 재현, GPT-3와 비교

- **무엇인가:** CCNet 위에 LLaMA 1이 더한 네 번째 필터입니다. Wikipedia 문서가 참고문헌으로 인용한 웹 페이지를 양성, 무작위 CommonCrawl 페이지를 음성으로 놓고 선형 분류기를 학습해, 참조로 분류되지 않은 페이지를 버립니다.
- **원문:** [LLaMA 1 §2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — “we trained a linear model to classify pages used as references in Wikipedia v.s. randomly sampled pages, and discarded pages not classified as references.” 이 한 문장이 전부입니다. 모델 종류(fastText인지), 특징, 학습 페이지 수, 기준값, 이 필터로 줄어든 양은 모두 **미기술**입니다. Llama 2에는 이 분류기가 나오지 않습니다.
- **RedPajama v1의 재현 (논문 밖, [rp_v1 브랜치](https://github.com/togethercomputer/RedPajama-Data/tree/rp_v1/data_prep/cc) README와 코드):**

| 항목 | RedPajama가 정한 값 |
| --- | --- |
| 앞 단계 | cc_net 그대로, 덤프 5개(2019-30 · 2020-05 · 2021-04 · 2022-05 · 2023-06), **head + middle**만 사용 |
| 양성 | 2023-04-01 영어 Wikipedia 덤프에서 참조 URL 3,800만 개를 뽑고, 약 **30만 페이지**까지 받아 cc_net을 다시 통과시킨 것. `create_corpus.py`는 head · middle 파일에서 1,000자 미만 페이지를 뺌 |
| 음성 | 양성과 같은 수의 CommonCrawl 페이지(head · middle 파일에서 고르게 추출) |
| 모델 | `fasttext supervised -input data_train -output model` (옵션 없음 = 기본값) |
| 점수 | `wiki_prob` = `__label__wiki` 확률 (예측이 `__label__cc`면 1 − 확률) |
| 기준값 | **`wiki_prob ≥ 0.25`**면 유지 (`filter/cc_classifier.sh`) |

  기준값 0.25는 RedPajama가 정한 값이고 LLaMA의 값이 아닙니다. 코드에서 하나 더 보입니다. `create_corpus.py`의 중복 검사는 `unique["digest"] = 1`처럼 문자열 키를 써서, 실제로는 양성 페이지의 digest 중복을 걸러내지 못하는 것으로 보입니다(추출자 코드 해석, 실행 확인 안 함).
- **GPT-3와 비교 ([App. A](https://arxiv.org/pdf/2005.14165v4#page=43)):** WebText · Wikipedia · 웹 책 말뭉치를 양성, 필터 안 한 CommonCrawl을 음성으로 둔 로지스틱 회귀(Spark 표준 tokenizer + HashingTF 특징)입니다. 점수로 자르지 않고 `np.random.pareto(α) > 1 − document_score`인 문서만 남겼고, α = 9는 “WebText에 대한 분류기 점수 분포에 맞추려고” 골랐다고 적었습니다. 그 뒤 같은 특징으로 Spark MinHashLSH(해시 10개) 퍼지 중복 제거를 해서 데이터가 평균 10% 줄었습니다.
- **계산해 보면 (`scripts/gpt3_pareto.py`):** NumPy의 `pareto(a)`는 Lomax(Pareto II) 분포라서 $P(X > x) = (1+x)^{-a}$입니다. 그러므로 점수 $s$인 문서를 남길 확률은 $(2-s)^{-9}$입니다. 100만 개 표본 시뮬레이션과 대조했습니다(표본 평균 0.1250 = 이론 $1/(a-1)$).

| 분류기 점수 s | 1.0 | 0.9 | 0.8 | 0.7 | 0.5 | 0.3 | 0.0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 남길 확률 $(2-s)^{-9}$ | 1.000 | 0.424 | 0.194 | 0.094 | 0.026 | 0.008 | 0.002 |
| 시뮬레이션 | 1.000 | 0.424 | 0.194 | 0.094 | 0.026 | 0.009 | 0.002 |

  점수 0.5인 문서도 2.6%, 0점 문서도 0.2%는 남습니다. 원문이 말한 “still include some documents that were out of distribution”이 이 꼬리입니다. LLaMA 1은 “discarded pages not classified as references”라고 적었으므로 결정적 기준값으로 읽히지만, 그 값은 미기술입니다.
- **왜 Wikipedia 본문이 아니라 “인용된 페이지”인가:** 원문은 이유를 적지 않았습니다(**미기술**). 본문을 양성으로 두면 백과사전 문체만 남기 쉬운데, 편집자가 출처로 고른 뉴스 · 기관 · 논문 페이지는 문체가 다양하면서도 사람의 선택을 한 번 거쳤다는 설명이 가능합니다(**추출자 해석**). Llama 3도 같은 발상을 “text would be referenced by Wikipedia”로 다시 적고 LLaMA 1(Touvron et al., 2023a)을 인용했습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA 1 원문이 이 분류기에 대해 적은 것(양성 · 음성 · 선형 모델 · 버림)과 적지 않은 것(모델 종류 · 기준값 · 규모)을 나눠 말한다.
  - [ ] RedPajama의 재현값(30만 페이지, 기본값 fastText, `wiki_prob ≥ 0.25`, head+middle)이 LLaMA 값이 아니라는 점을 말한다.
  - [ ] GPT-3의 Pareto 규칙을 $(2-s)^{-9}$로 풀어 점수 0.5 문서가 남을 확률을 계산한다.
- **함께 볼 개념:** [fastText 분류기의 구조](#c-q-fasttext) · [그 뒤의 품질 분류기](#c-q-followup) · W01 [공개 재현: RedPajama](../w01/llama1-reading-map.html#c-redpajama)

<a id="c-q-followup"></a>

### 그 뒤의 품질 분류기 — Llama 3 · DCLM · FineWeb-Edu (논문 밖)

- **무엇인가:** Llama 2 이후 공개된 보고서에서 LLaMA 1식 분류기 필터가 어떻게 이어지고 바뀌었는지입니다. 모두 원문 PDF를 열어 확인했습니다.
- **Llama 3 ([arXiv:2407.21783v3 §3.1.1](https://arxiv.org/pdf/2407.21783v3#page=5)):**
  - 줄 단위 중복 제거를 “ccNet과 비슷하게” 하되 기준을 적었습니다. 3,000만 문서 bucket마다 **6번 넘게** 나온 줄을 지웁니다. 저자들은 이 작업이 boilerplate뿐 아니라 자주 나오는 고품질 텍스트도 지운다는 것을 확인했지만, 실험에서는 성능이 크게 좋아졌다고 적었습니다.
  - 규칙 필터: 중복 n-gram 비율(Rae et al. 2021), dirty word 수(Raffel et al. 2020), 토큰 분포 KL divergence.
  - 모델 필터: “Wikipedia가 인용할 만한 텍스트인가”를 학습한 fastText(Joulin et al., 2017 인용, LLaMA 1을 출처로 표기)와, **Llama 2 chat이 품질 요구를 만족하는지 판정한** 문서로 학습한 RoBERTa 계열 분류기(효율 때문에 DistilRoberta). 다국어는 176개 언어 fastText 언어 식별과 다국어 Llama 2 기반 분류기를 씁니다.
  - “we experiment with … various quality filtering configurations”라고만 적어서 **최종 설정과 기준값은 미기술**입니다. KenLM perplexity 필터는 이 절에 나오지 않습니다.
- **DCLM ([arXiv:2406.11794v4](https://arxiv.org/abs/2406.11794)):**
  - Table 4(1B-1x, CORE): RefinedWeb 재현 27.5 · PageRank 상위 20% 26.1 · SemDedup 27.1 · BGE 임베딩 분류기 27.2 · AskLLM 28.6 · perplexity 필터 29.0 · top-k 평균 logit 29.2 · **fastText OH-2.5+ELI5 30.2**.
  - Table 5(7B-1x, 상위 10% 기준): 양성을 무엇으로 두느냐에 따라 CORE가 **OH-2.5+ELI5 41.0 · GPT-3 Approx 37.5 · Wikipedia 35.7 · OpenWebText2 34.7**. 같은 OH-2.5+ELI5에서 상위 15%는 39.8, 20%는 38.7입니다. 학습 데이터는 양성 20만 · 음성 20만, 음성은 RefinedWeb 재현본의 무작위 표본, fastText 기본값에 wordNgrams만 2로 바꿨습니다(App. J.1).
  - 이 표가 LLaMA 1 계열에 주는 반례입니다. **Wikipedia를 양성으로 둔 분류기는 이 실험에서 가장 낮은 축**이었습니다. 다만 조건은 DCLM의 7B-1x 설정과 CORE 지표이고, LLaMA 1의 “Wikipedia가 **인용한** 페이지”를 직접 시험한 것은 아닙니다.
  - App. N: 사람이 매긴 품질 라벨에 대한 필터의 ROC-AUC와 다운스트림 점수 사이의 관계가 약했습니다(R² < 0.3). “사람이 보기에 좋은 글을 잘 고르는 필터”가 곧 “좋은 학습 데이터를 고르는 필터”는 아니라는 결과입니다.
- **FineWeb-Edu ([arXiv:2406.17557v2](https://arxiv.org/abs/2406.17557)):**
  - Llama-3-70B-Instruct가 FineWeb CC-MAIN-2024-10에서 무작위로 뽑은 46만 페이지에 교육적 가치를 0–5점으로 매겼습니다(가산식 프롬프트, 초 · 중학교 수준 지식에 초점). Snowflake-arctic-embed-m 위의 선형 회귀를 41만 개로 학습하고(인코더 고정, 20 epoch, lr 3e-4) 나머지 5만 개로 검증했습니다. 반올림 점수 **≥ 3**을 남겼고, 그 기준에서 검증 F1은 82%입니다. FineWeb 15T 토큰 전체에 적용하는 데 H100 6,000 GPU시간이 들었고, 결과는 1.3T 토큰입니다(§4, p.8).
  - 기준값 3은 MMLU · ARC 같은 지식 · 추론 벤치마크와 HellaSwag 같은 다른 벤치마크 사이의 절충으로 골랐다고 적었습니다.
  - 한계도 같은 논문에 있습니다(§4.2 Domain fit). FineWeb-Edu로 학습한 모델은 Wikipedia · 학술(S2ORC · arXiv) 도메인에서 perplexity가 낮았고, FineWeb은 C4 · Reddit · Twitter AAE 같은 넓은 웹 도메인에서 더 낮았습니다. 분류기가 고르는 쪽으로 도메인 범위가 좁아진다는 뜻입니다.
- **흐름 한 줄:** 채점 모델은 n-gram LM → fastText → LLM 라벨로 학습한 작은 인코더로 커졌습니다. 그러나 문서 수십억 개를 훑어야 하는 마지막 채점 단계는 여전히 fastText나 작은 인코더처럼 싼 모델이 맡습니다. 비싼 LLM은 라벨을 만드는 데만 씁니다(추출자 해석, Llama 3 · FineWeb-Edu 구조에서).
- **설명할 수 있어야 하는 것:**
  - [ ] Llama 3가 LLaMA 1의 참조 페이지 아이디어를 이어받고(fastText), Llama 2를 라벨러로 쓴 분류기를 더했다는 점을 말한다. 최종 기준값은 미기술이라는 점도 말한다.
  - [ ] DCLM Table 5로 “양성 예시 선택이 모델 종류보다 크게 작용했다”는 결과를 조건(7B-1x, CORE, 상위 10%)과 함께 말한다.
  - [ ] FineWeb-Edu의 라벨러 · 채점 모델 · 기준값 · 비용을 말하고, Domain fit 결과로 한계를 말한다.
- **함께 볼 개념:** [로드맵](#c-q-roadmap) · [참조 페이지 분류기](#c-q-ref-classifier) · W02 [Llama 3의 데이터](#c-data-followup) · 보충 [S1 — Llama 3 Herd 비교](../supplementary.md#s1)

- 직접 돌린 코드와 확인한 원전은 검토 기록의 [Data 검증 메모](#memo-data)에 있습니다.

<!-- part: post -->
## Post-training

### 이 파트의 질문

- **담당:** 송용우 · 임병극 (데이터 & Post-training)
- **범위:** [§3 Fine-tuning ~ §3.2.1 Human Preference Data Collection](https://arxiv.org/pdf/2307.09288v2#page=8)(p.8–10) · [§3.3 System Message for Multi-Turn Consistency ~ §3.4 Limitations of human evaluations](https://arxiv.org/pdf/2307.09288v2#page=16)(p.16–19). §3.2.2–§3.2.3은 Alignment가 맡습니다.
- **RQ1. Llama 2-Chat의 후학습은 어떤 골격이고, SFT는 무엇을 어떻게 학습했나?**
  - 필수 원문: [Fig. 4](https://arxiv.org/pdf/2307.09288v2#page=5) · [§3 도입 · §3.1 · Table 5](https://arxiv.org/pdf/2307.09288v2#page=8)
  - 개념: [RLHF 3단계 골격](#c-rlhf-pipeline) · [SFT 데이터 27,540개](#c-sft-data) · [SFT의 loss: 답 토큰에만](#c-sft-loss) · [후학습 단계별 설정 비교](#c-sft-settings)
- **RQ2. 선호 데이터는 어떤 절차로, 어떤 단위로 모았나?**
  - 필수 원문: [§3.2 도입 · §3.2.1 · Table 6](https://arxiv.org/pdf/2307.09288v2#page=9) · (부록) [App. A.3.1–A.3.2 · Table 26 · Fig. 25–26](https://arxiv.org/pdf/2307.09288v2#page=51)
  - 개념: [선호 수집 절차](#c-pref-protocol) · [도움됨 · 안전성 지침과 안전 label](#c-safety-labels) · [비교 · 예시 · 토큰: 선호 데이터의 단위](#c-pref-units) · [공개 선호 데이터셋 6종](#c-open-pref-datasets) · [주간 batch 14개와 분포 이동](#c-weekly-batches)
- **RQ3. 여러 턴 동안 처음 지시를 지키게 하려면?**
  - 필수 원문: [§3.3 · Fig. 9–10](https://arxiv.org/pdf/2307.09288v2#page=16) · (부록) [App. A.3.5 · Table 30 · Fig. 28](https://arxiv.org/pdf/2307.09288v2#page=53)
  - 개념: [Ghost Attention(GAtt)](#c-gatt) · [GAtt의 평가](#c-gatt-eval)
- **RQ4. RLHF의 결과는 무엇으로 쟀고, 얼마나 믿을 수 있나?**
  - 필수 원문: [§3.4.1 · Fig. 11](https://arxiv.org/pdf/2307.09288v2#page=17) · [§3.4.2 · Fig. 12 · IRR · Limitations of human evaluations](https://arxiv.org/pdf/2307.09288v2#page=18) · (부록) [App. A.3.6–A.3.7 · Fig. 29–31 · Table 31–32](https://arxiv.org/pdf/2307.09288v2#page=54)
  - 개념: [모델 기반 평가: RM과 GPT-4 판정](#c-model-based-eval) · [사람 평가와 그 한계](#c-human-eval)
- **(선택, 논문 밖) 이 후학습 recipe는 후속 모델에서 어떻게 이어졌나?**
  - 개념: [Llama 3의 후학습](#c-post-followup) · [Llama 3의 데이터](#c-data-followup)

<a id="c-rlhf-pipeline"></a>

### RLHF 3단계 골격

- **무엇인가:** InstructGPT(Ouyang et al. 2022)가 정리한 **SFT → reward model → PPO** 세 단계입니다. Llama 2 §3은 이 골격 위에서 무엇을 바꿨는지 읽어야 합니다.
- **원전:** [InstructGPT §3.1–§3.5 · App. C](https://arxiv.org/abs/2203.02155v1) — ① 사람이 쓴 시연으로 SFT ② 한 prompt의 응답 K = 4–9개를 사람이 순위 매기고 RM 학습(6B RM) ③ RM 점수 − KL(β = 0.02)을 보상으로 PPO, 사전학습 gradient를 섞은 PPO-ptx.

| | InstructGPT (2022) | Llama 2-Chat (2023) |
| --- | --- | --- |
| 선호 형식 | 4–9개 순위 | 이진 비교 + 강도 4단계 |
| RM | 6B 하나 | 도움 · 안전 두 개, chat checkpoint에서 초기화, margin |
| 정책 갱신 | PPO 한 번 | RS 반복(V1–V5) → 그 위에 PPO |
| 데이터 수집 | 한 번에 | 주간 batch, 최신 모델로 다시 수집 |
| 안전 | RM 하나에 포함 | 안전 SFT · 안전 RM · 안전 context distillation |

- **설명할 수 있어야 하는 것:**
  - [ ] 세 단계가 각각 무엇을 입력받아 무엇을 내놓는지 말한다.
  - [ ] Llama 2가 바꾼 다섯 가지를 표로 말한다.
  - [ ] InstructGPT의 데이터 수 · 설정을 Llama 2의 사실로 옮기지 않는다는 원칙을 지킨다.
- **함께 볼 개념:** [두 개의 RM](#c-rm-arch) · [RLHF V1–V5](#c-rlhf-versions) · 원전: Christiano et al. [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) · Stiennon et al. [arXiv:2009.01325](https://arxiv.org/abs/2009.01325)

<a id="c-sft-data"></a>

### SFT 데이터 27,540개

- **무엇인가:** Llama 2-Chat의 첫 단계 지도 학습 데이터입니다. 공개 instruction 데이터로 시작했다가, **양보다 질**을 이유로 vendor가 만든 고품질 대화 데이터로 바꿨습니다.
- **원문:** [§3.1 · Table 5](https://arxiv.org/pdf/2307.09288v2#page=9)
  1. **Getting Started:** LLaMA 1(LLaMA-I)처럼 공개 instruction 데이터(Chung et al., 2022, Flan)로 시작.
  2. **Quality Is All You Need:** 제3자 SFT 데이터 수백만 건은 다양성과 품질이 부족해 **제외**하고, vendor annotation으로 수천 건의 고품질 데이터를 먼저 모았더니 결과가 눈에 띄게 좋아짐. 수만 건 수준이면 충분하다고 판단해 **27,540건**에서 수집을 멈춤.
  3. **품질 확인:** 180건을 사람이 직접 검토해, SFT 모델이 생성한 답이 사람이 쓴 답과 비슷한 수준임을 확인 → 이후 annotation 예산을 선호 데이터로 돌림.
  4. **주의:** vendor · 플랫폼에 따라 하류 성능이 크게 달랐다고 적습니다.
- **형식:** 한 예시 = annotator가 직접 쓴 prompt + 답. Table 5에 도움됨 예시(주기율표 시)와 안전 예시(욕설 roast 요청 거절)가 있습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] SFT 데이터 수(27,540)와 선호 비교 수(1,418,091)의 단위 · 규모 차이를 말한다.
  - [ ] “적은 고품질 데이터로 충분하다”는 관찰이 LIMA(Zhou et al. 2023)와 같은 방향이지만, 양 · vendor · 품질이 함께 바뀐 비교라 통제 실험은 아니라는 점을 말한다.
  - [ ] 27,540건의 과제 · 도메인 구성과 공개 데이터와의 최종 혼합 비율은 원문에 없다는 점을 말한다.
- **함께 볼 개념:** [SFT의 loss](#c-sft-loss) · 원전: LIMA [arXiv:2305.11206](https://arxiv.org/abs/2305.11206) · W01: [Flan 프로토콜](../w01/llama1-reading-map.html#c-flan)

<a id="c-sft-loss"></a>

### SFT의 loss: 답 토큰에만

- **무엇인가:** prompt와 답을 이어 붙여 입력하되, **prompt 토큰의 loss는 0으로 두고 답 토큰에서만** 다음 토큰 예측 loss를 계산하는 지도 학습입니다.
- **원문:** [§3.1 Fine-Tuning Details](https://arxiv.org/pdf/2307.09288v2#page=9)
  - 각 샘플 = prompt + 답. 시퀀스 길이(4,096)를 채우려고 학습셋의 **모든 prompt와 답을 이어 붙입니다**(packing).
  - prompt와 답 사이에 special token을 둡니다.
  - autoregressive objective를 쓰되 user prompt 토큰의 loss를 0으로 둬 **답 토큰으로만 역전파**합니다.
- **그림 (설명용):**

  ```
  [prompt₁ ─ loss 0][SEP][답₁ ─ loss ✓][prompt₂ ─ loss 0][SEP][답₂ ─ loss ✓] … (4,096 토큰까지)
  ```

  prompt 30토큰 + 답 200토큰이면 230토큰을 입력하지만 loss는 200토큰에서만 생깁니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 사전학습 loss(모든 토큰)와 SFT loss(답 토큰만)의 차이를 말한다.
  - [ ] prompt loss를 지우는 이유를 말한다: 모델이 배워야 할 것은 사용자의 말투가 아니라 답하는 방식이기 때문입니다(일반적 설명, 원문은 이유 미기술).
  - [ ] packing 시 앞 샘플의 토큰이 뒤 샘플의 attention에 보이는지(문서 경계 마스킹)는 원문에 없다는 점을 말한다.
  - [ ] SFT target은 사람이 쓴 답 하나이고, 선호 쌍의 순위를 배우는 RM과 다르다는 점을 말한다.
- **함께 볼 개념:** [SFT 데이터 27,540개](#c-sft-data) · [GAtt](#c-gatt)(이전 turn 전체를 loss 0으로 두는 변형)

<a id="c-sft-settings"></a>

### 후학습 단계별 설정 비교

- **무엇인가:** 사전학습 · SFT · RM · PPO의 학습 설정을 한 표에 놓은 것입니다. 모두 같은 AdamW(β₁ 0.9 · β₂ 0.95 · eps 10⁻⁵)를 씁니다.
- **원문:** [§2.2](https://arxiv.org/pdf/2307.09288v2#page=5) · [§3.1](https://arxiv.org/pdf/2307.09288v2#page=9) · [§3.2.2 Training Details](https://arxiv.org/pdf/2307.09288v2#page=12) · [§3.2.3 PPO](https://arxiv.org/pdf/2307.09288v2#page=15)

| 설정 | 사전학습 | SFT | Reward model | PPO |
| --- | --- | --- | --- | --- |
| 학습률 | 3.0e-4 / 1.5e-4 (peak) | 2e-5 | 1e-5 (70B 5e-6) | 1e-6 |
| 스케줄 | cosine → 10%, warmup 2,000 step | cosine | cosine → 10%, warmup 3% (최소 5 step) | **상수** |
| batch | 4M 토큰 | 64 시퀀스 × 4,096 | 512 pairs (1,024 rows) | 512 prompts, minibatch 64 |
| 반복 | 2T 토큰 | **2 epochs** | **1 epoch** (더 길면 과적합) | 200–400 iterations |
| weight decay · clip | 0.1 · 1.0 | 0.1 · 미기술 | 기반 모델과 같음 | 0.1 · 1.0 |

- **계산해 보면 (추출자 계산):** SFT 한 step = 64 × 4,096 = 약 26만 토큰. 학습률은 사전학습 peak의 약 1/15(7B)입니다. PPO 학습률은 SFT의 1/20입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 단계가 뒤로 갈수록 학습률이 작아진다는 점(3e-4 → 2e-5 → 1e-5 → 1e-6)을 말한다.
  - [ ] RM을 1 epoch만 학습한 이유(저자: 길게 하면 과적합)를 말한다.
  - [ ] LLaMA-I(W01)는 같은 설정을 공개하지 않았다는 점과 비교한다.
- **함께 볼 개념:** [optimizer 설정값의 출처](#c-opt-values) · [PPO 설정을 InstructGPT와 비교](#c-ppo-settings)

<a id="c-pref-protocol"></a>

### 선호 수집 절차

- **무엇인가:** reward model을 학습시킬 사람 선호 데이터를 모으는 방법입니다. **이진 비교**(두 응답 중 하나 고르기)에 **선호 강도 4단계**를 덧붙입니다.
- **원문:** [§3.2.1](https://arxiv.org/pdf/2307.09288v2#page=10)
  1. annotator가 prompt를 **직접 씀**.
  2. 그 prompt에 대한 응답 두 개를 **서로 다른 두 모델 변형**에서, **temperature를 바꿔** sampling — 다양성을 최대화하려는 설계.
  3. 기준에 따라 하나를 고름(forced choice).
  4. 고른 쪽이 얼마나 나은지 표시: significantly better / better / slightly better / negligibly better · unsure.
- **왜 이진 비교인가:** 저자는 다른 방식(여러 응답 순위 매기기 등)보다 **수집할 수 있는 prompt의 다양성이 커서** 골랐다고 적습니다. InstructGPT는 한 prompt에 4–9개 응답 순위를 받았습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 네 단계 절차를 순서대로 말한다.
  - [ ] 선호 강도 4단계가 나중에 RM loss의 margin으로 쓰인다는 점을 연결한다.
  - [ ] 두 응답을 “다른 모델 변형”에서 뽑는다는 점이 같은 모델 두 번 sampling과 어떻게 다른지(응답 차이가 더 커짐) 말한다(추출자 해석).
- **함께 볼 개념:** [rating margin](#c-margin) · [InstructGPT의 3단계 골격](#c-rlhf-pipeline)

<a id="c-safety-labels"></a>

### 도움됨 · 안전성 지침과 안전 label

- **무엇인가:** 선호를 **도움됨(helpfulness)**과 **안전성(safety)** 두 지침으로 따로 모으고, 안전 단계에서는 응답마다 안전 여부 label을 하나 더 받습니다.
- **원문:** [§3.2.1](https://arxiv.org/pdf/2307.09288v2#page=10) — 도움됨은 요청을 얼마나 잘 들어주고 정보를 주는가, 안전성은 응답이 안전 지침에 비추어 위험한가입니다. 예: “폭탄 제조법 상세 안내”는 도움은 되지만 안전하지 않습니다. 두 지침을 나누면 각각에 맞는 지시를 줄 수 있습니다(안전 annotator는 적대적 prompt에 집중).

| 안전 label 분류 | 안전 데이터 중 비율 |
| --- | --- |
| 고른 응답 안전 · 다른 응답 위험 | 18% |
| 둘 다 안전 | 47% |
| 둘 다 위험 | 35% |
| 고른 응답 위험 · 다른 응답 안전 | **제외** (안전한 쪽이 사람에게도 선호될 것이라 봄) |

- **설명할 수 있어야 하는 것:**
  - [ ] 선호(상대 비교)와 안전 label(절대 판정)이 서로 다른 정보라는 점을 말한다.
  - [ ] 네 번째 경우를 버린 이유(저자의 믿음)를 말한다.
  - [ ] 이 label이 safety RM의 보조 loss와 Table 29의 세 범주로 이어진다는 점을 연결한다.
- **함께 볼 개념:** [안전 보조 loss](#c-safety-aux-loss) · [두 개의 RM](#c-rm-arch)

<a id="c-pref-units"></a>

### 비교 · 예시 · 토큰: 선호 데이터의 단위

- **무엇인가:** 선호 데이터를 셀 때 쓰는 세 단위입니다. **비교 1개 = 같은 prompt(+ 이전 대화)를 공유하는 응답 2개(chosen · rejected)**, **예시 1개 = prompt + 응답 1개 = RM 입력 1행**입니다.
- **원문:** [Table 6](https://arxiv.org/pdf/2307.09288v2#page=11) — Meta 데이터 1,418,091 비교, 대화당 평균 3.9턴, 예시당 798.5토큰, prompt 31.4토큰, 응답 234.1토큰. 전체(공개 데이터 포함) 2,919,326 비교.
- **계산해 보면 (추출자 계산):**
  - Meta 데이터의 RM 입력 토큰 ≈ 1,418,091 × 2 × 798.5 ≈ **22.6억 토큰**. 사전학습 2T의 약 0.1%입니다.
  - 예시당 798.5토큰이 prompt + 응답(31.4 + 234.1 = 265.5)보다 훨씬 큰 것은, 예시가 **이전 대화 turn까지 포함**하기 때문으로 보입니다(평균 3.9턴, 추출자 해석).
  - RM batch 512 pairs = 1,024 rows가 바로 이 “비교 = 2행” 단위입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] “141만 개 데이터”라고 할 때 그것이 SFT 예시가 아니라 **비교 쌍**이라는 점을 말한다.
  - [ ] Meta 데이터가 공개 데이터보다 대화 turn이 많고 길다는 저자 설명을 표로 확인한다.
- **함께 볼 개념:** [RM 학습 혼합과 설정](#c-rm-mix) · [주간 batch 14개](#c-weekly-batches)

<a id="c-open-pref-datasets"></a>

### 공개 선호 데이터셋 6종

- **무엇인가:** Meta 데이터 수집 초기에 RM을 띄우고(bootstrap), 이후에도 혼합에 남겨 둔 공개 선호 데이터입니다.
- **원문:** [Table 6](https://arxiv.org/pdf/2307.09288v2#page=11) · [§3.2.2 Data Composition](https://arxiv.org/pdf/2307.09288v2#page=11)

| 데이터셋 | 무엇이 들어 있나 | 비교 수 | 턴 | prompt / 응답 토큰 |
| --- | --- | --- | --- | --- |
| Anthropic Helpful | 사람–모델 대화에서 더 도움되는 응답 선택 | 122,387 | 3.0 | 17.7 / 88.4 |
| Anthropic Harmless | 레드팀 대화에서 덜 해로운 응답 선택 | 43,966 | 3.0 | 15.7 / 46.4 |
| OpenAI Summarize | Reddit 글 요약 두 개 중 더 나은 요약 | 176,625 | 1.0 | 336.0 / 35.1 |
| OpenAI WebGPT | 웹 검색으로 답한 긴 답변 비교 | 13,333 | 1.0 | 48.3 / 188.9 |
| StackExchange | 질문의 답변들을 투표 점수로 비교 | 1,038,480 | 1.0 | 200.1 / 240.2 |
| Stanford SHP | Reddit 답글을 사람 추천 수로 비교 | 74,882 | 1.0 | 199.5 / 138.8 |
| Synthetic GPT-J | GPT-J 생성 응답으로 만든 합성 비교 | 33,139 | 1.0 | 13.0 / 110.3 |

- **계산해 보면 (추출자 계산):** 공개 데이터의 합은 1,502,812로, Meta와 더하면 2,920,903입니다. 표의 Total 2,919,326과 **1,577 차이**가 납니다(원문 표 그대로). 공개 데이터의 69%가 StackExchange 한 곳입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 공개 데이터 수(약 150만)가 Meta(약 142만)보다 많지만 대부분 단일 턴 · 다른 도메인이라는 점을 말한다.
  - [ ] RM이 배워야 하는 것은 “Llama 2-Chat 출력에 대한 선호”인데도 공개 데이터를 남긴 이유(부정적 전이가 관찰되지 않음, 일반화 · reward hacking 방지 기대)를 말한다.
  - [ ] StackExchange · SHP는 사람이 직접 비교한 것이 아니라 투표 · 추천 수에서 만든 선호라는 점을 말한다(추출자 설명).
- **원전:** [Anthropic HH](https://arxiv.org/abs/2204.05862) · [Summarize from Feedback](https://arxiv.org/abs/2009.01325) · [WebGPT](https://arxiv.org/abs/2112.09332) · [SHP](https://huggingface.co/datasets/stanfordnlp/SHP)

<a id="c-weekly-batches"></a>

### 주간 batch 14개와 분포 이동

- **무엇인가:** 선호 데이터를 한 번에 모으지 않고 **매주 batch로** 모으며, 매번 그 시점의 최신 Llama 2-Chat으로 응답을 sampling한 방식입니다.
- **원문:** [§3.2.1](https://arxiv.org/pdf/2307.09288v2#page=10) — 모델이 좋아지면 출력 분포가 바뀌고, 새 분포를 보지 못한 RM은 정확도가 빠르게 떨어집니다(hyper-specialization, Scialom et al. 2020b). 그래서 새 튜닝 전에 **최신 모델로 새 선호 데이터를 모아** RM을 on-distribution으로 유지합니다. [Table 26](https://arxiv.org/pdf/2307.09288v2#page=52) · [Fig. 25–26](https://arxiv.org/pdf/2307.09288v2#page=53)

| batch | 비교 수 | 예시당 토큰 | 응답 토큰 |
| --- | --- | --- | --- |
| 1 | 5,561 | 547.1 | 159.3 |
| 4 | 36,206 | 652.8 | 182.9 |
| 7 | 84,388 | 662.2 | 210.0 |
| 10 | 136,729 | 723.9 | 230.2 |
| 14 | 249,356 | 1,008.0 | 258.9 |
| 합계 | 1,418,091 | 798.5 | 234.1 |

- **계산해 보면 (추출자 계산):** 앞 7개 batch가 전체의 20%(280,494), 마지막 3개 batch가 45%(641,530)입니다. batch 크기는 45배 커졌습니다.
- **원문이 밝힌 세 가지 추세:**
  - **규모:** annotator가 늘고 익숙해져 뒤 batch가 큼(A.3.1).
  - **난이도:** 처음엔 쉬운 prompt, 점점 복잡한 prompt로 가는 **curriculum**(A.3.2). Fig. 26에서 같은 RM 점수가 batch마다 내려가는 것을 prompt가 어려워진 근거로 해석합니다.
  - **비슷한 응답 증가:** 모델이 좋아질수록 두 응답이 비슷해져 “negligibly better / unsure” 비율이 크게 늘고 “significantly better”가 줄어듦(Fig. 25).
- **설명할 수 있어야 하는 것:**
  - [ ] 왜 최신 모델로 다시 모아야 하는지(RM의 분포 이동)를 한 문장으로 말한다.
  - [ ] “비슷한 응답 비율 증가”가 RM의 어려운 문항(Table 8의 낮은 정확도) 증가로 이어진다는 점을 연결한다.
  - [ ] curriculum의 효과를 따로 뗀 실험은 없다는 점을 말한다.
- **함께 볼 개념:** [RM 평가](#c-rm-eval) · [RLHF V1–V5](#c-rlhf-versions)

<a id="c-gatt"></a>

### Ghost Attention(GAtt)

- **무엇인가:** “계속 나폴레옹처럼 말해” 같은 **대화 전체에 적용되는 지시**를 몇 턴 뒤에도 잊지 않도록 만드는 **학습 데이터 구성법**입니다. 이름과 달리 attention 구조를 바꾸지 않습니다. Context Distillation(Bai et al. 2022b)에서 착안했습니다.
- **원문:** [§3.3 GAtt Method](https://arxiv.org/pdf/2307.09288v2#page=16)
  1. 다중 턴 대화 `[u₁, a₁, …, uₙ, aₙ]`와 지켜야 할 지시 `inst`를 준비합니다.
  2. **모든 user 메시지 앞에 inst를 붙여** 최신 RLHF 모델로 답을 sampling합니다 → 지시를 계속 지키는 답이 나옴.
  3. 학습용 데이터에서는 inst를 **첫 턴에만 남기고** 나머지 턴에서 지웁니다.
  4. 이렇게 하면 중간 assistant 메시지(inst가 붙은 채 생성됨)와 학습 입력이 어긋나므로, **이전 턴의 모든 토큰(assistant 메시지 포함)의 loss를 0**으로 둡니다.
- **그림 (설명용):**

  ```
  생성할 때:  [inst+u₁][a₁][inst+u₂][a₂][inst+u₃] → a₃
  학습할 때:  [inst+u₁][a₁][u₂][a₂][u₃] → a₃     (a₃만 loss, 나머지 loss 0)
  ```

- **합성 지시:** 취미(“You enjoy e.g. Tennis”) · 언어(“Speak in e.g. French”) · 인물(“Act as e.g. Napoleon”). 취미와 인물 목록은 Llama 2-Chat이 생성하게 해 모델이 모르는 인물을 요구하지 않도록 했습니다. 지시는 무작위로 조합하고, 절반은 “Figure: Napoleon.”처럼 짧게 바꿉니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 생성 입력과 학습 입력이 다르다는 점을 그림으로 말한다: 반복 지시로 얻은 행동을, 첫 지시만 있는 대화에서 학습합니다.
  - [ ] 이전 턴 loss를 0으로 두는 이유(중간 답이 inst를 본 상태로 생성되어 학습 입력과 맞지 않음)를 말한다.
  - [ ] GAtt가 attention 연산을 바꾸는 기법이 아니라는 점을 말한다.
- **함께 볼 개념:** [SFT의 loss](#c-sft-loss) · 안전 context distillation([§4.2.4](https://arxiv.org/pdf/2307.09288v2#page=27), 배정 밖)

<a id="c-gatt-eval"></a>

### GAtt의 평가

- **무엇인가:** GAtt가 실제로 지시를 몇 턴까지 유지하는지 본 결과입니다.
- **원문:** [§3.3 GAtt Evaluation](https://arxiv.org/pdf/2307.09288v2#page=17) — RLHF V3 이후에 적용. [Table 30](https://arxiv.org/pdf/2307.09288v2#page=54) — 첫 메시지에 취미 · 인물을 정하고 2–20턴에서 직접 물어본 사람 평가.

| 대화 턴 | GAtt 없음 | GAtt |
| --- | --- | --- |
| 2 | 100% | 100% |
| 4 | 10% | 100% |
| 6 | 0% | 100% |
| 20 | 0% | 100% |

  - [Fig. 10](https://arxiv.org/pdf/2307.09288v2#page=17): GAtt 모델은 대화 후반까지 system message(“Act as Oscar Wilde”) 쪽 attention 활성이 크게 유지됩니다.
  - 학습에 없던 제약(“Always answer with Haiku” · “answer in one sentence only”)도 지켰습니다(Fig. 28).
  - LLaMA 1(2,048로 사전학습, 4,096으로 fine-tune)에 먼저 적용했을 때 2,048을 넘어서도 속성을 이해하는 것으로 보였다고 적습니다(A.3.5).
- **설명할 수 있어야 하는 것:**
  - [ ] Table 30이 인물 · 취미 속성만, 20턴까지만, 총 4,048토큰 미만에서 잰 결과라는 범위를 말한다.
  - [ ] Fig. 10의 attention 시각화는 정성적 근거라는 점을 말한다.
  - [ ] 저자도 현재 구현이 “vanilla”이고 대화 중 system message를 바꾸는 학습은 하지 않았다고 적은 한계를 말한다.

<a id="c-model-based-eval"></a>

### 모델 기반 평가: RM과 GPT-4 판정

- **무엇인가:** 매 iteration마다 사람 평가를 할 수 없어서, 여러 ablation 중 최고 모델을 고를 때 **최신 RM 점수**를 먼저 보고, 주요 버전만 사람 평가로 확인한 방식입니다.
- **원문:** [§3.4.1](https://arxiv.org/pdf/2307.09288v2#page=17) · [Fig. 11](https://arxiv.org/pdf/2307.09288v2#page=18) · [Fig. 29](https://arxiv.org/pdf/2307.09288v2#page=55)
  - **RM이 지표로 쓸 만한가:** 도움 · 안전 test prompt의 답을 annotator 3명이 7점 Likert로 매긴 결과와 RM 점수가 잘 맞았습니다(Fig. 29). pairwise loss로 학습했어도 점수 하나를 지표로 쓸 수 있다는 근거입니다.
  - **Goodhart의 법칙:** 지표가 목표가 되면 좋은 지표가 아니게 되므로, 다양한 공개 데이터로 학습한 **더 일반적인 RM**으로도 확인했고 아직 발산은 보지 못했다고 적습니다.
  - **GPT-4 판정:** Meta RM은 Llama 2-Chat에 유리할 수 있어 GPT-4로 ChatGPT 대비 승률을 다시 계산했습니다. 응답 순서는 무작위로 바꿉니다. 안전 1,586개 · 도움 584개 prompt. 최신 모델 승률 60% 이상.
- **계산해 보면 (설명용):** 동점을 빼는 승률 = win ÷ (win + loss). 사람 평가의 70B vs ChatGPT(승 36%, 무 31.5%, 패 32.5%)에 적용하면 36 ÷ 68.5 = **52.6%**입니다(Fig. 2는 GPT-4 판정에 이 식을 썼고, 여기 숫자는 식을 보이기 위한 대입).
- **설명할 수 있어야 하는 것:**
  - [ ] RM을 학습 보상과 평가 지표로 함께 쓰면 생기는 문제(Goodhart)와 저자의 두 대응(일반 RM · GPT-4 판정)을 말한다.
  - [ ] 다음 annotation 라운드에서 새 모델과 이전 모델을 함께 sampling해 “무료로” 비교했다는 점을 말한다.
  - [ ] Fig. 11의 승률은 판정 모델에 따라 크게 다르다는 점(Meta RM에서 더 높음)을 말한다.
- **함께 볼 개념:** [사람 평가와 그 한계](#c-human-eval) · [KL penalty와 reward hacking](#c-kl-penalty)

<a id="c-human-eval"></a>

### 사람 평가와 그 한계

- **무엇인가:** 주요 모델 버전을 공개 · 비공개 chat 모델과 **나란히 놓고 사람이 고르게 한** 평가입니다.
- **원문:** [§3.4.2 · Fig. 12](https://arxiv.org/pdf/2307.09288v2#page=18) · [App. A.3.7 · Table 31–32 · Fig. 30–31](https://arxiv.org/pdf/2307.09288v2#page=56)

| 항목 | 내용 |
| --- | --- |
| prompt | 4,000개 이상, 단일 · 다중 턴. 범주: 사실 질문 · 글쓰기 · 언어 도움 · 추천 · 대화. 코드 · 추론 prompt는 없음 |
| 질문 | “두 응답 중 어느 쪽이 더 나은가(도움되면서 안전하고 정직한)?” |
| 척도 | 7점: A much better … About the same … B much better → 승 · 무 · 패로 집계 |
| 평가자 | 생성 쌍마다 3명, A/B 위치 무작위. 5명으로 해 봐도 결과 · 일치도가 크게 바뀌지 않음 |
| 길이 | 공개 모델 비교는 context · 생성 각 1,000토큰(공정성), 비공개 모델은 2,000토큰 |
| system prompt | Llama 2-Chat · ChatGPT · PaLM · Falcon에 같은 system prompt(Table 31) |
| 비교 모델 | ChatGPT(gpt-3.5-turbo-0301) · PaLM(chat-bison-001) · Falcon-40B-Instruct · MPT-7B-chat · Vicuna-13B/33B |

- **결과:** 70B vs ChatGPT 승 36% · 무 31.5%. 7B는 MPT-7B-chat에 60% prompt에서 이김. 34B는 Vicuna-33B · Falcon-40B에 75% 넘게 이김. ChatGPT에 system prompt를 빼면 70B 승률이 36% → 44%로 오릅니다(Fig. 30).
- **평가자 일치도 (IRR):** Gwet의 AC2로 0.37–0.55. 승률이 비슷한 비교(70B vs ChatGPT)일수록 낮고, 승자가 뚜렷할수록 높습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 저자가 직접 든 네 가지 한계(prompt 4k가 실사용을 다 덮지 못함 · 코드 · 추론 없음 · 다중 턴은 마지막 응답만 평가 · 주관성)를 말한다.
  - [ ] system prompt 하나로 승률이 8%p 바뀌었다는 점으로 평가 조건의 민감도를 말한다.
  - [ ] 사실 질문에서 이긴 이유가 답의 정확도가 아니라 **문체 선호**였다는 저자 분석(A.3.7)을 말한다.
- **원전:** Gwet's AC1/AC2 (Gwet 2008, 2014)

<a id="c-post-followup"></a>

### Llama 3의 후학습

- **무엇인가 (논문 밖):** Llama 2의 “SFT → RS → PPO 반복”이 다음 모델에서 어떻게 바뀌었는지입니다.

| 항목 | Llama 2-Chat | Llama 3 |
| --- | --- | --- |
| 반복 | RLHF V1–V5 | 6 라운드 |
| 한 라운드 | RM 학습 → RS(70B) → SFT → (V5 무렵부터) PPO | RM 학습 → RS → SFT → **DPO** |
| RS의 K | 원문 미기술 | 보통 10–30 |
| RS 효율 | PPO 생성 때 FSDP로 약 20배 느려진 문제를 가중치 통합으로 완화 | PagedAttention으로 2배 넘는 처리량 |
| 정책 최적화 | PPO + KL | DPO(큰 모델에서 compute가 적고 성능이 더 좋았다고 보고) |

- **설명할 수 있어야 하는 것:**
  - [ ] RS → SFT라는 Llama 2의 뼈대는 남고, PPO가 DPO로 바뀌었다는 점을 말한다.
  - [ ] 보충 S1(Llama 3 Herd)에서 이 비교를 자세히 본다는 점을 연결한다.
- **출처:** [Llama 3 §4.1–§4.3](https://arxiv.org/abs/2407.21783) (2026-10-17 확인) · [보충 S1](../supplementary.md#s1)

<a id="c-data-followup"></a>

### Llama 3의 데이터

- **무엇인가 (논문 밖):** 같은 계열 다음 모델에서 사전학습 · 선호 데이터 설명이 어떻게 바뀌었는지입니다.

| 항목 | Llama 2 (2023.07) | Llama 3 (2024.07) |
| --- | --- | --- |
| 사전학습 토큰 | 2T | 약 15T |
| 혼합 공개 | 비율 미공개, factual up-sampling만 | 영역 비율: 일반 지식 50% · 수학 · 추론 25% · 코드 17% · 다국어 8% |
| 선호 강도 | 4단계 (significantly / better / slightly / negligibly · unsure) | 4단계 (significantly / better / slightly / marginally) + 고친 응답(edited) |
| RM loss의 margin | 사용 | **제거** |
| 선호 수집 | 주간 batch, 최신 모델 sampling | 라운드마다 최신 모델 sampling |

- **설명할 수 있어야 하는 것:**
  - [ ] Llama 3가 같은 4단계 강도를 유지하면서 margin은 뺐다는 점을 말하고, Alignment의 [rating margin](#c-margin) 페이지와 연결한다.
  - [ ] 데이터 공개 범위는 Llama 2와 비슷하게 제한적이라는 점을 말한다. 보충 S1에서 다시 봅니다.
- **출처:** [Llama 3 §3.1 · §4.1–§4.2](https://arxiv.org/abs/2407.21783) (2026-10-17 확인) · [보충 S1](../supplementary.md#s1)

<!-- part: alignment -->
## Alignment & RL

### 이 파트의 질문

- **담당:** 김민제 · 강민우
- **범위:** [§3.2.2 Reward Modeling ~ Scaling Trends](https://arxiv.org/pdf/2307.09288v2#page=10)(p.10–13) · [§3.2.3 Iterative Fine-Tuning ~ PPO](https://arxiv.org/pdf/2307.09288v2#page=13)(p.13–16)
- **RQ1. 사람의 선호 쌍은 어떻게 scalar reward model이 되고, 얼마나 정확한가?**
  - 필수 원문: [§3.2.2 · Eq. (1)–(2)](https://arxiv.org/pdf/2307.09288v2#page=10) · [Reward Model Results · Table 7–8](https://arxiv.org/pdf/2307.09288v2#page=12) · [Scaling Trends · Fig. 6](https://arxiv.org/pdf/2307.09288v2#page=13) · (부록) [App. A.3.3–A.3.4 · Table 27–29 · Fig. 27](https://arxiv.org/pdf/2307.09288v2#page=52)
  - 개념: [Bradley–Terry 선호 모델](#c-bradley-terry) · [두 개의 RM: 구조와 초기화](#c-rm-arch) · [Ranking loss](#c-ranking-loss) · [rating margin](#c-margin) · [안전 보조 loss](#c-safety-aux-loss) · [RM 학습 혼합과 설정](#c-rm-mix) · [RM 평가와 scaling](#c-rm-eval)
- **RQ2. Rejection sampling은 무엇을 다시 학습시키고, RLHF V1–V5에서 PPO와 어떤 순서로 결합됐나?**
  - 필수 원문: [§3.2.3 · Rejection Sampling · Fig. 7–8](https://arxiv.org/pdf/2307.09288v2#page=13)
  - 개념: [RLHF V1–V5와 RS → PPO 순서](#c-rlhf-versions) · [Rejection sampling fine-tuning](#c-rs-ft) · [K개 중 최고: max와 median의 차이](#c-rs-gain) · [Sampling temperature의 재조정](#c-rs-temperature) · [이전 iteration 샘플을 버렸다가 다시 넣은 이유](#c-rs-history) · [70B에서만 sampling하고 작은 모델로 증류](#c-distill-70b)
- **RQ3. PPO는 어떤 보상으로, 어떤 제약 아래 정책을 갱신하나?**
  - 필수 원문: [PPO 문단 · Eq. (3)–(4)](https://arxiv.org/pdf/2307.09288v2#page=15) · [Training Details · p.16](https://arxiv.org/pdf/2307.09288v2#page=16)
  - 개념: [PPO clip](#c-ppo-clip) · [PPO objective (Eq. 3)](#c-ppo-objective) · [조건부 reward와 whitening](#c-reward-shaping) · [KL penalty와 reward hacking](#c-kl-penalty) · [PPO 설정을 InstructGPT와 비교](#c-ppo-settings) · [70B PPO의 시스템 비용](#c-ppo-system)
- **(선택, 논문 밖) RM + PPO는 이후 무엇으로 바뀌었나?**
  - 개념: [PPO 이후: DPO · GRPO](#c-align-followup)

<a id="c-bradley-terry"></a>

### Bradley–Terry 선호 모델

- **무엇인가:** 두 항목 i, j가 각자 점수 r_i, r_j를 가질 때 “i가 j를 이길 확률”을 `P(i ≻ j) = σ(r_i − r_j)`로 두는 모델입니다(Bradley & Terry 1952, 원래 식은 지수 비율 형태). 사람 선호 쌍을 이 모델의 관측으로 보고 로그 가능도를 최대화하면 Eq. (1)의 ranking loss가 됩니다.
- **원문과의 연결:** [Eq. (1)](https://arxiv.org/pdf/2307.09288v2#page=11) = `−log P(y_c ≻ y_r)`. Eq. (2)의 margin은 “강하게 선호된 쌍은 σ(Δ − m)도 높아야 한다”로 이 모델을 바꾼 것입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 점수 차 0이면 50%, 점수 차가 커질수록 승률이 1에 가까워진다는 점을 말한다.
  - [ ] 점수의 절대값은 의미가 없고 차이만 의미가 있다는 점(그래서 InstructGPT는 bias로 정규화)과, Llama 2가 logit · whitening으로 점수 척도를 다룬 이유를 연결한다.
- **함께 볼 개념:** [Ranking loss](#c-ranking-loss) · [조건부 reward와 whitening](#c-reward-shaping)

<a id="c-rm-arch"></a>

### 두 개의 RM: 구조와 초기화

- **무엇인가:** reward model은 prompt(+ 이전 대화)와 응답 하나를 입력받아 **품질 점수 하나(scalar)**를 내는 모델입니다. Llama 2는 **Helpfulness RM**과 **Safety RM** 두 개를 따로 학습합니다.
- **원문:** [§3.2.2](https://arxiv.org/pdf/2307.09288v2#page=10)
  - **왜 둘인가:** 도움됨과 안전성은 서로 충돌할 때가 있어(Bai et al. 2022a) RM 하나로 둘 다 잘하기 어렵습니다. 한 모델이 둘 다 하려면 더 나은 답을 고르는 것과 함께 적대적 prompt를 구분하는 것까지 배워야 합니다. 둘로 나누면 과제가 쉬워진다고 적습니다(저자 설명). [A.4.1 · Fig. 32](https://arxiv.org/pdf/2307.09288v2#page=58): 안전한 답인데 도움 점수가 낮은 경우, 위험한 답인데 도움 점수가 높은 경우가 실제로 있습니다.
  - **초기화:** “pretrained chat model checkpoints”에서 시작합니다. RM이 chat 모델이 아는 것을 알게 해, 정보 불일치로 환각을 선호하는 일을 막으려는 의도입니다.
  - **구조:** 사전학습 모델과 같은 구조 · 하이퍼파라미터에서 **다음 토큰 분류 head를 scalar 회귀 head로** 바꿨습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] RM의 입력(prompt + 응답 1개)과 출력(점수 1개)을 말하고, 학습할 때만 쌍을 쓴다는 점을 말한다.
  - [ ] “chat model checkpoints”가 SFT인지 어느 RLHF 버전인지는 원문에서 확정되지 않는다는 점을 말한다.
  - [ ] 크기별 RM(7B · 13B · 70B)이 있고 Fig. 6에서 비교된다는 점, 실제 RLHF에 어느 크기를 썼는지는 명시되지 않았다는 점을 말한다.
- **함께 볼 개념:** [Ranking loss](#c-ranking-loss) · [조건부 reward](#c-reward-shaping)

<a id="c-ranking-loss"></a>

### Ranking loss

- **무엇인가:** 선호 쌍에서 고른 답(chosen, y_c)의 점수가 버린 답(rejected, y_r)보다 높아지도록 학습하는 손실입니다. InstructGPT(Ouyang et al. 2022)와 같은 이진 ranking loss입니다.
- **원문:** [Eq. (1)](https://arxiv.org/pdf/2307.09288v2#page=11)

  `L_ranking = −log σ( r_θ(x, y_c) − r_θ(x, y_r) )`

  r_θ(x, y)는 prompt x와 응답 y에 대한 scalar 점수, σ는 sigmoid입니다.
- **계산해 보면 (설명용):**

| r(x, y_c) | r(x, y_r) | 차이 Δ | σ(Δ) = “c가 더 낫다”의 모델 확률 | loss |
| --- | --- | --- | --- | --- |
| 0.8 | 0.2 | +0.6 | 0.646 | 0.437 |
| 0.5 | 0.5 | 0 | 0.5 | 0.693 |
| 0.2 | 0.8 | −0.6 | 0.354 | 1.037 |

- **설명할 수 있어야 하는 것:**
  - [ ] loss가 점수의 **차이**에만 의존하므로 모든 점수에 같은 값을 더해도 loss가 같다는 점(shift 불변)을 말한다.
  - [ ] 학습은 쌍으로 하지만 추론 때는 응답 하나에 점수를 매긴다는 점을 말한다(원문 p.12 명시).
  - [ ] σ(Δ)가 Bradley–Terry 모델의 “c가 이길 확률”이라는 해석을 말한다.
- **함께 볼 개념:** [rating margin](#c-margin) · [Bradley–Terry 선호 모델](#c-bradley-terry)

<a id="c-margin"></a>

### rating margin

- **무엇인가:** 선호 강도(4단계)에 따라 margin m(r)을 빼서, **차이가 큰 쌍일수록 점수 차를 더 크게** 벌리도록 만든 변형입니다.
- **원문:** [Eq. (2)](https://arxiv.org/pdf/2307.09288v2#page=11) — `L = −log σ( r_θ(x, y_c) − r_θ(x, y_r) − m(r) )`. 뚜렷이 다른 쌍에 큰 margin, 비슷한 쌍에 작은 margin. [Table 27–28 · Fig. 27](https://arxiv.org/pdf/2307.09288v2#page=52)

| m(r) | significantly | better | slightly | negligibly / unsure | Meta Helpful 평균 정확도 |
| --- | --- | --- | --- | --- | --- |
| 없음 | – | – | – | – | 62.5 (79.1 / 66.9 / 59.8 / 54.5) |
| Small | 1 | 2/3 | 1/3 | 0 | 63.0 (80.4 / 67.3 / 60.4 / 55.0) |
| Large | 3 | 2 | 1 | 0 | 62.9 (80.7 / 67.5 / 60.5 / 54.3) |

- **계산해 보면 (설명용, Δ = 1인 같은 쌍):**
  - margin 없음: −log σ(1) = **0.313**
  - Small, significantly(m = 1): −log σ(0) = **0.693**
  - Large, significantly(m = 3): −log σ(−2) = **2.127**

  같은 점수 차라도 “significantly better”로 표시된 쌍은 loss가 커서, RM이 차이를 더 벌리도록 밀립니다.
- **부작용:** margin은 점수 분포를 양 끝으로 몰아 **이분된(binary split) 분포**를 만들고, Large일수록 심합니다(Fig. 27). 저자는 PPO가 reward 분포 변화에 민감할 수 있어 reward calibration을 후속 과제로 둡니다.
- **설명할 수 있어야 하는 것:**
  - [ ] margin이 큰 쌍에서 정확도를 올리고(79.1 → 80.7), Large는 비슷한 쌍에서 오히려 떨어뜨린다(54.5 → 54.3)는 점을 표로 말한다.
  - [ ] 최종 Helpfulness RM에 Small · Large 중 무엇을 썼는지 원문이 밝히지 않는다는 점, Safety RM에 margin을 썼는지도 부록에 별도 ablation이 없다는 점을 말한다.
  - [ ] margin ablation이 Helpfulness RM에 대해서만 보고됐다는 점을 말한다.
- **함께 볼 개념:** [선호 수집 절차](#c-pref-protocol) · [조건부 reward와 whitening](#c-reward-shaping)

<a id="c-safety-aux-loss"></a>

### 안전 보조 loss

- **무엇인가:** Safety RM에 ranking loss 외에, 응답이 **안전한지 위험한지 구분**하도록 하는 보조 손실을 더한 것입니다. 안전 label(18 / 47 / 35% 분류)을 씁니다.
- **원문:** [App. A.3.4 · Table 29](https://arxiv.org/pdf/2307.09288v2#page=52) — 보조 loss의 정확한 식과 가중치는 적지 않습니다. 점수 0.5(sigmoid 전 음수)를 임계값으로 위험 응답을 얼마나 잡는지(recall)를 봅니다.

| | 평균 | 안전 chosen · 위험 rejected | 둘 다 안전 | 둘 다 위험 | 위험 응답 recall |
| --- | --- | --- | --- | --- | --- |
| Baseline | 63.7 | 93.0 | 56.0 | 59.5 | 73.0 |
| + 보조 loss | 64.5 | 94.3 | 56.9 | 59.9 | **90.4** |

- **설명할 수 있어야 하는 것:**
  - [ ] ranking 정확도는 조금 오르고(63.7 → 64.5) 위험 응답 recall이 크게 오른다(73.0 → 90.4)는 점을 말한다.
  - [ ] RM 점수를 sigmoid로 0–1에 놓고 0.5를 기준으로 쓴다는 점이 PPO의 0.15 임계값과 어떻게 이어지는지 말한다.
  - [ ] 식이 공개되지 않아 재현에는 추가 정보가 필요하다는 점을 말한다.
- **함께 볼 개념:** [도움됨 · 안전성 지침과 안전 label](#c-safety-labels) · [조건부 reward](#c-reward-shaping)

<a id="c-rm-mix"></a>

### RM 학습 혼합과 설정

- **무엇인가:** 두 RM이 각각 어떤 데이터를 어떤 비율로, 얼마나 학습했는지입니다.
- **원문:** [§3.2.2 Data Composition · Training Details](https://arxiv.org/pdf/2307.09288v2#page=11)

| | Helpfulness RM | Safety RM |
| --- | --- | --- |
| 데이터 | Meta Helpfulness **전부** + 같은 양의 나머지(Meta Safety · 공개 데이터에서 균등 sampling) | Meta Safety + Anthropic Harmless **전부**, 여기에 Meta Helpfulness · 공개 도움 데이터를 **90 / 10**으로 섞음 |
| 근거 | “extensive experimentation” | 10% 도움 데이터가 특히 **둘 다 안전한 쌍**의 정확도에 도움 |

  공통 설정: **1 epoch**(더 길면 과적합), 기반 모델과 같은 optimizer, 최대 LR 70B 5e-6 · 그 외 1e-5, cosine → 10%, warmup 전체 step의 3%(최소 5), batch 512 pairs = 1,024 rows.
- **계산해 보면 (추출자 계산):** 공개 데이터까지 모두 썼다면 2,919,326 ÷ 512 ≈ 5,700 step이고 warmup은 약 170 step입니다. 실제로는 혼합 규칙에 따라 일부만 sampling하므로 이 값은 상한입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 두 RM의 혼합 규칙을 말하고, Safety RM에도 도움 데이터를 10% 섞은 이유를 말한다.
  - [ ] 공개 데이터를 남긴 이유(일반화 · reward hacking 방지 기대, 부정적 전이 미관찰)가 저자 기대라는 점을 말한다.
- **함께 볼 개념:** [공개 선호 데이터셋 6종](#c-open-pref-datasets) · [후학습 단계별 설정 비교](#c-sft-settings)

<a id="c-rm-eval"></a>

### RM 평가와 scaling

- **무엇인가:** RM 정확도 = 사람이 고른 답에 RM이 더 높은 점수를 준 쌍의 비율입니다. 동점이면 무작위인 50%가 기준선입니다.
- **원문:** [Reward Model Results · Table 7–8](https://arxiv.org/pdf/2307.09288v2#page=12) · [Fig. 6](https://arxiv.org/pdf/2307.09288v2#page=13) — 매 batch에서 1,000개를 test로 떼어 모은 것이 Meta Helpfulness · Meta Safety test set입니다. 비교 기준선: SteamSHP-XL(FLAN-T5-xl), Open Assistant RM(DeBERTa V3 Large), GPT-4(“Choose the best answer between A and B” zero-shot).

| | Meta Helpful. | Meta Safety | Anthropic Helpful | Anthropic Harmless | OpenAI Summ. | Stanford SHP | 평균 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SteamSHP-XL | 52.8 | 43.8 | 66.8 | 34.2 | 54.7 | 75.7 | 55.3 |
| Open Assistant | 53.8 | 53.4 | 67.7 | 68.4 | 71.7 | 55.0 | 63.0 |
| GPT-4 | 58.6 | 58.1 | – | – | – | – | – |
| Safety RM | 56.2 | **64.5** | 55.4 | 74.7 | 71.7 | 65.2 | 64.3 |
| Helpfulness RM | **63.2** | 62.8 | 72.0 | 71.0 | 75.5 | 80.0 | 70.6 |

  **선호 강도별 (Table 8):** Helpfulness RM on Meta Helpful — significantly 80.7 · better 67.5 · slightly 60.9 · negligibly 54.5. 비슷한 쌍은 동전 던지기에 가깝습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Meta RM은 Meta 데이터로 학습했고 기준선은 그렇지 않다는 비교 조건(원문 캡션 명시)을 말한다.
  - [ ] 각 RM이 자기 영역에서 가장 좋다는 결과를 두 목표의 긴장으로 설명한다(저자 해석).
  - [ ] Fig. 6에서 데이터와 모델이 클수록 정확도가 오르고 아직 포화되지 않았다는 관찰과, 저자가 “RM 정확도는 Llama 2-Chat 최종 성능의 가장 중요한 대리 지표 중 하나”라고 본다는 점을 말한다.
  - [ ] 사람끼리의 일치율도 뚜렷한 쌍에서 더 높다는 원문 언급과 함께, 비슷한 쌍의 정확도 54%가 RM만의 실패가 아니라는 점을 말한다.
- **함께 볼 개념:** [주간 batch 14개와 분포 이동](#c-weekly-batches) · [모델 기반 평가](#c-model-based-eval)

<a id="c-rlhf-versions"></a>

### RLHF V1–V5와 RS → PPO 순서

- **무엇인가:** 선호 데이터가 batch로 쌓일 때마다 RM을 다시 학습하고 그 RM으로 새 RLHF 모델을 만든 반복입니다. 버전 이름은 SFT-v1 · SFT-v2 → RLHF-V1 … RLHF-V5입니다.
- **원문:** [§3.2.3](https://arxiv.org/pdf/2307.09288v2#page=13) — “Until RLHF (V4), we used only Rejection Sampling fine-tuning, and after that, we combined the two sequentially, applying PPO on top of the resulted Rejection Sampling checkpoint before sampling again.” [Fig. 11](https://arxiv.org/pdf/2307.09288v2#page=18)
- **한 라운드의 흐름 (설명용 재구성):**

  ```
  최신 정책으로 새 선호 데이터 수집 → RM 재학습
   → 70B로 K개 생성 · RM으로 최고 답 선택 → RS fine-tune (V1–V5)
   → (V4 이후) RS checkpoint 위에 PPO
   → 다음 라운드 sampling
  ```

- **V4 경계:** “Until RLHF (V4)”가 V4를 포함하는지 원문은 모호합니다. Fig. 11은 **RLHF-v5 (no PPO)**와 **RLHF-v5 (with PPO)**를 따로 표시하고 V4에는 PPO 표시가 없습니다. 그래서 PPO가 처음 쓰인 것은 V5로 읽는 쪽이 그림과 맞습니다(추출자 해석). W02 학습목표의 “V4 이전 RS, 이후 PPO”는 원문 문장 그대로의 표현으로 쓰고 버전을 단정하지 않습니다.
- **그 밖의 버전별 사실:** GAtt는 RLHF V3 이후, RS 샘플 bag의 변경은 V3 이후, Fig. 11에서 Meta RM 판정으로 V3부터 ChatGPT 대비 도움 · 안전 모두 50% 넘음.
- **설명할 수 있어야 하는 것:**
  - [ ] RS와 PPO가 “둘 중 하나”가 아니라 **RS 뒤에 PPO**를 얹는 순서라는 점을 말한다.
  - [ ] V4 경계가 모호한 이유를 원문 문장과 Fig. 11로 설명한다.
  - [ ] 매 버전마다 RM도 새 데이터로 갱신된다는 점을 말한다.
- **함께 볼 개념:** [Rejection sampling fine-tuning](#c-rs-ft) · [PPO objective](#c-ppo-objective)

<a id="c-rs-ft"></a>

### Rejection sampling fine-tuning

- **무엇인가:** prompt마다 현재 모델로 **K개 답을 생성** → RM으로 점수 매겨 **최고 점수 답 하나**를 고름 → 그 답을 새 정답(gold)으로 삼아 **SFT처럼 다시 학습**하는 방법입니다. Bai et al.(2022b)과 같은 re-ranking에 “고른 답으로 gradient update까지 한다”를 더했습니다.
- **원문:** [§3.2.3](https://arxiv.org/pdf/2307.09288v2#page=13) — PPO와의 차이를 두 가지로 적습니다.

| | Rejection sampling | PPO |
| --- | --- | --- |
| **폭(Breadth)** | prompt 하나에 K개 탐색 | prompt 하나에 생성 1개 |
| **깊이(Depth)** | 처음 정책으로 데이터셋 전체를 먼저 모은 뒤 SFT처럼 학습 | step t의 생성이 step t−1에 갱신된 정책에서 나옴 |
| 학습 신호 | 고른 답의 다음 토큰 loss | reward − KL로 정한 정책 objective |

  저자는 반복적으로 모델을 갱신했기 때문에 두 방법의 근본 차이가 “덜 두드러진다”고 덧붙입니다.
- **흐름 (설명용):** `prompt → 최신 70B가 y₁…y_K 생성 → RM이 점수 → y* = argmax → (prompt, y*)로 fine-tune`
- **설명할 수 있어야 하는 것:**
  - [ ] RS가 “RM으로 고른 데이터에 대한 SFT”라는 점을 말하고, PPO의 정책 갱신과 다른 연산이라는 점을 구분한다.
  - [ ] 학습 때 실제로 쓴 K값은 원문에 없다는 점을 말한다(그림의 N = 1–100은 분석용 sweep).
  - [ ] 고를 때 쓴 RM이 “실험 당시 쓸 수 있는 가장 좋은 RM”이라는 점을 말한다.
- **함께 볼 개념:** [K개 중 최고](#c-rs-gain) · [RS와 PPO의 결합 순서](#c-rlhf-versions) · 원전: Constitutional AI [arXiv:2212.08073](https://arxiv.org/abs/2212.08073)

<a id="c-rs-gain"></a>

### K개 중 최고: max와 median의 차이

- **무엇인가:** Fig. 7은 N개 샘플의 RM 점수 최대값과 중앙값을 N에 따라 그립니다. 저자는 **max − median의 간격을 RS로 얻을 수 있는 잠재 이득**으로 해석합니다.
- **원문:** [Fig. 7](https://arxiv.org/pdf/2307.09288v2#page=14) · [p.15](https://arxiv.org/pdf/2307.09288v2#page=15) — 샘플이 많을수록 최대값은 오르고 중앙값은 그대로라 간격이 커집니다. 탐색과 얻을 수 있는 최대 reward가 직접 연결된다고 적습니다.
- **왜 그런가 (설명용 계산):** 점수가 평균 μ, 표준편차 σ인 정규분포라고 가정하면 N개 중 최대값의 기대값은 대략 μ + 1.54σ(N = 10), μ + 2.51σ(N = 100)입니다. 중앙값은 N과 관계없이 μ입니다. 그래서 N을 10배 늘려도 이득은 1.6배 정도로 **로그처럼** 느리게 커집니다.
- **설명할 수 있어야 하는 것:**
  - [ ] max − median이 왜 “잠재” 이득인지 말한다: 고른 답을 학습한다고 모델이 그 최대값을 그대로 내게 된다는 보장은 없습니다.
  - [ ] 샘플 수가 늘면 생성 비용은 선형으로, 이득은 그보다 느리게 늘어난다는 점을 말한다(추출자 해석).
- **함께 볼 개념:** [Sampling temperature의 재조정](#c-rs-temperature)

<a id="c-rs-temperature"></a>

### Sampling temperature의 재조정

- **무엇인가:** RS에서 K개를 생성할 때 쓰는 temperature가 RLHF 단계마다 최적값이 달라진다는 관찰입니다. temperature가 높을수록 다양한 답이 나와 탐색이 넓어집니다.
- **원문:** [Fig. 8](https://arxiv.org/pdf/2307.09288v2#page=14) · [p.15](https://arxiv.org/pdf/2307.09288v2#page=15) — SFT 모델과 RLHF 모델에서 temperature 0.6–1.5별 최대 reward 곡선을 비교합니다. RLHF 모델은 10–100개를 뽑을 때 **T ∈ [1.2, 1.3]**이 최적입니다. RLHF가 temperature를 “rescale”한다고 적고, 정해진 compute 안에서는 temperature를 점진적으로 다시 조정해야 한다고 결론냅니다.
- **설명할 수 있어야 하는 것:**
  - [ ] RLHF를 거친 모델은 분포가 좁아져(확신이 커져) 같은 다양성을 얻으려면 더 높은 temperature가 필요하다는 해석을 말한다(추출자 해석).
  - [ ] 이 관찰이 §5.1의 “prompt 유형에 따라 temperature 반응이 다르다”(Fig. 21)로 이어진다는 점을 연결한다.
- **함께 볼 개념:** §5.1의 prompt별 temperature 관찰([Fig. 21](https://arxiv.org/pdf/2307.09288v2#page=33), 배정 밖)

<a id="c-rs-history"></a>

### 이전 iteration 샘플을 버렸다가 다시 넣은 이유

- **무엇인가:** RS 데이터를 직전 iteration의 샘플만으로 만들다가, 능력 퇴행이 보여 **이전 모든 iteration의 상위 샘플**을 함께 쓰도록 바꾼 변경입니다.
- **원문:** [p.14–15](https://arxiv.org/pdf/2307.09288v2#page=14)
  - RLHF V3까지: 직전 iteration이 만든 샘플 “bag” 안에서만 고름. 예: V3는 V2의 샘플로만 학습.
  - 문제: 전반적으로는 좋아졌지만 일부 능력이 퇴행. V3는 이전 버전보다 시에서 각운(rhyme)을 맞추는 데 더 어려움을 보였습니다(정성 분석).
  - 수정: 이후 iteration은 V1 · V2 등 **모든 이전 iteration의 상위 샘플**을 포함. 구체적 수치는 제시하지 않지만 성능이 상당히 좋아지고 문제가 해결됐다고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 이 퇴행을 저자가 망각(catastrophic forgetting) 연구와 연결했다는 점을 말한다.
  - [ ] 수정의 효과가 수치 없이 서술로만 보고됐다는 점을 말한다.
  - [ ] RL의 replay buffer와 비슷한 발상이라는 저자의 비유(Synnaeve · Vinyals 2019)를 말한다.
- **함께 볼 개념:** [RLHF V1–V5](#c-rlhf-versions) · 원전: Kirkpatrick et al. 2017 [arXiv:1612.00796](https://arxiv.org/abs/1612.00796)

<a id="c-distill-70b"></a>

### 70B에서만 sampling하고 작은 모델로 증류

- **무엇인가:** RS의 생성 · 선택은 가장 큰 **70B Llama 2-Chat에서만** 하고, 작은 모델들은 그 70B가 만든 RS 데이터로 fine-tune한 방식입니다. 저자는 이를 큰 모델 능력의 **증류(distillation)**라고 부릅니다.
- **원문:** [Rejection Sampling](https://arxiv.org/pdf/2307.09288v2#page=14) — “We perform rejection sampling only with our largest 70B Llama 2-Chat. All smaller models are fine-tuned on rejection sampled data from the larger model.” 증류 효과 분석은 후속 과제로 남깁니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 작은 모델이 직접 K개를 탐색한 것이 아니라 **70B가 고른 답**을 학습했다는 점을 말한다.
  - [ ] 이 방식이 생성 비용을 70B 한 곳에 모으는 대신, 작은 모델의 RS가 “자기 분포에서 고른 답”이 아니게 된다는 점을 말한다(추출자 해석).
  - [ ] 증류의 독립 효과는 측정하지 않았다는 점을 말하고, W04(Qwen3의 strong-to-weak distillation) · W07(R1 증류)과 연결한다.

<a id="c-ppo-clip"></a>

### PPO clip

- **무엇인가:** PPO(Schulman et al. 2017)는 새 정책과 직전 정책의 확률 비 ρ = π_θ(a|s) / π_old(a|s)를 [1 − ε, 1 + ε]로 잘라(clip), 한 번의 update로 정책이 너무 많이 바뀌지 않게 하는 policy gradient 방법입니다.

  `L_clip = E[ min( ρ · A, clip(ρ, 1−ε, 1+ε) · A ) ]`   (A = advantage, 평균보다 얼마나 나은 행동인가)
- **계산해 보면 (설명용, ε = 0.2):**

| A | ρ | ρ · A | clip(ρ) · A | 쓰는 값 |
| --- | --- | --- | --- | --- |
| +1 | 1.5 | 1.5 | 1.2 | **1.2** (더 올려도 이득 없음) |
| +1 | 0.9 | 0.9 | 0.9 | 0.9 |
| −1 | 0.5 | −0.5 | −0.8 | **−0.8** (줄이는 쪽 이득도 제한) |

- **언어모델에서:** 행동 = 토큰, 상태 = prompt + 앞 토큰들. advantage를 구하려면 value function(critic)이 필요합니다. Llama 2는 clip 0.2만 적고 value function은 적지 않습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] clip이 직전 정책 기준, Llama 2 Eq. (4)의 KL이 처음 정책 기준이라는 차이를 말한다.
  - [ ] 표의 세 줄을 계산해 clip이 “이득이 나는 방향의 과도한 이동”만 막는다는 점을 말한다.
- **원전:** PPO [arXiv:1707.06347](https://arxiv.org/abs/1707.06347v2) §3 · GAE [arXiv:1506.02438](https://arxiv.org/abs/1506.02438)

<a id="c-ppo-objective"></a>

### PPO objective (Eq. 3)

- **무엇인가:** RM을 진짜 보상(사람 선호)의 추정치로 놓고, 언어모델을 정책으로 두어 기대 보상을 최대화하는 학습입니다. Stiennon et al.(2020)의 RL 방식을 따릅니다.
- **원문:** [Eq. (3)](https://arxiv.org/pdf/2307.09288v2#page=15)

  `arg max_π  E_{p∼D, g∼π} [ R(g | p) ]`

  데이터셋 D에서 prompt p를 뽑고, 정책 π로 생성 g를 만들어, PPO 알고리즘과 loss로 이 목표를 최적화합니다.
- **RL 용어로 옮기면 (설명용):** 상태 = prompt + 지금까지 생성한 토큰, 행동 = 다음 토큰, 에피소드 = 응답 하나, 보상 = 응답이 끝난 뒤 R(g | p) 한 번.
- **설명할 수 있어야 하는 것:**
  - [ ] Eq. (3)이 “목표”이고, 그것을 푸는 방법이 PPO의 clipped update라는 구분을 말한다.
  - [ ] PPO에 필요한 value function(critic), advantage 추정(GAE) 방식, value 초기화는 원문에 없다는 점을 말한다(InstructGPT는 RM에서 초기화한 6B value function을 명시).
  - [ ] RS와 달리 매 step 생성이 직전에 갱신된 정책에서 나온다는 점(on-policy)을 말한다.
- **함께 볼 개념:** [PPO clip](#c-ppo-clip) · [KL penalty](#c-kl-penalty)

<a id="c-reward-shaping"></a>

### 조건부 reward와 whitening

- **무엇인가:** PPO에 쓰는 보상 R_c를 Safety RM(R_s)과 Helpfulness RM(R_h)의 **조건부 조합**으로 만들고, logit으로 되돌린 뒤 정규화(whitening)하는 과정입니다.
- **원문:** [p.15](https://arxiv.org/pdf/2307.09288v2#page=15)

  ```
  R_c(g|p) = R_s(g|p)   if is_safety(p) or R_s(g|p) < 0.15
             R_h(g|p)   otherwise
  R̃_c(g|p) = whiten( logit( R_c(g|p) ) )
  ```

  - 안전 위험이 있는 prompt에는 미리 tag를 달고(is_safety), 그때는 Safety RM 점수를 씁니다.
  - tag가 없어도 **Safety RM 점수가 0.15 미만**이면 위험한 응답으로 보고 Safety RM 점수를 씁니다. 0.15는 Meta Safety test에서 precision 0.89 · recall 0.55에 해당합니다.
  - RM 출력(sigmoid 후 0–1)을 logit으로 되돌려 선형 점수로 만들고 whitening해 안정성을 높이고 KL 항과 균형을 맞춥니다.
- **계산해 보면 (설명용):**

| 경우 | 선택 | 원점수 | logit |
| --- | --- | --- | --- |
| 일반 prompt, R_s = 0.6, R_h = 0.9 | R_h | 0.9 | +2.20 |
| 일반 prompt, R_s = 0.10, R_h = 0.9 | **R_s** (0.15 미만) | 0.10 | −2.20 |
| 안전 tag prompt, R_s = 0.7 | R_s | 0.7 | +0.85 |
| 경계값 R_s = 0.15 | – | 0.15 | −1.73 |

  두 번째 줄처럼 도움이 매우 되는 답이라도 위험하면 큰 음의 보상을 받습니다. whitening은 batch 평균을 빼고 표준편차로 나누는 것이 일반적 의미이며, 원문은 계산 단위를 적지 않습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Safety RM을 쓰는 두 조건을 말하고, tag가 없는 prompt에도 안전 RM이 개입한다는 점을 말한다.
  - [ ] 0.15가 precision · recall로 정한 임계값이라는 점과, recall 0.55는 위험 응답의 절반 가까이를 놓친다는 뜻이라는 점을 말한다.
  - [ ] logit이 sigmoid의 역함수라 0–1 점수를 다시 (−∞, ∞)로 펼친다는 점을 말한다.
- **함께 볼 개념:** [안전 보조 loss](#c-safety-aux-loss) · [KL penalty](#c-kl-penalty)

<a id="c-kl-penalty"></a>

### KL penalty와 reward hacking

- **무엇인가:** 학습 중인 정책 π_θ가 처음 정책 π₀에서 너무 멀어지면 보상을 깎는 항입니다.
- **원문:** [Eq. (4)](https://arxiv.org/pdf/2307.09288v2#page=15)

  `R(g | p) = R̃_c(g | p) − β · D_KL( π_θ(g | p) ‖ π₀(g | p) )`

  다른 연구(Stiennon 2020, Ouyang 2022)처럼 이 제약이 **학습 안정성**과 **reward hacking 감소**에 유용했다고 적습니다. reward hacking = RM 점수는 높은데 사람 평가는 낮아지는 현상. β는 7B · 13B 0.01, 34B · 70B 0.005.
- **계산해 보면 (설명용):** 응답 200토큰에서 토큰마다 log π_θ − log π₀가 평균 0.05라면 KL 추정 ≈ 200 × 0.05 = 10. β = 0.005면 보상에서 0.05, β = 0.01이면 0.1을 뺍니다. whitening된 보상의 표준편차가 1이라면 이 정도 차이에서는 KL이 보상보다 작아, 정책이 크게 벗어날 때만 강하게 작동합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] KL의 기준 π₀(처음 정책, 원문 “original policy”)와 PPO clip의 기준(직전 정책 π_old)이 다르다는 점을 말한다. KL은 **처음에서 얼마나 멀어졌나**, clip은 **한 번에 얼마나 움직이나**를 제한합니다.
  - [ ] 큰 모델의 β가 절반인 이유는 원문에 없다는 점을 말한다.
  - [ ] π₀가 SFT 모델인지 RS checkpoint인지 원문이 명시하지 않는다는 점을 말한다.
  - [ ] KL이 reward hacking을 “줄인다”이지 막는다는 보장은 아니라는 점과, 저자가 따로 일반 RM으로 발산 여부를 확인했다는 점(§3.4.1)을 연결한다.
- **함께 볼 개념:** [PPO clip](#c-ppo-clip) · [모델 기반 평가](#c-model-based-eval)

<a id="c-ppo-settings"></a>

### PPO 설정을 InstructGPT와 비교

- **무엇인가:** Llama 2의 PPO 하이퍼파라미터를 PPO 원 논문(MuJoCo 실험)과 InstructGPT의 값과 나란히 본 것입니다.
- **원문:** [p.15–16](https://arxiv.org/pdf/2307.09288v2#page=15) — 이유는 적지 않습니다. 비교 원전: PPO [Table 3](https://arxiv.org/abs/1707.06347v2) · InstructGPT [App. C.4](https://arxiv.org/pdf/2203.02155v1#page=42)

| 설정 | PPO 원 논문 (MuJoCo) | InstructGPT (2022) | Llama 2-Chat |
| --- | --- | --- | --- |
| clip ε | 0.2 | 0.2 | 0.2 |
| batch | 2,048 timestep | 512 | 512 |
| minibatch | 64 | 64 | 64 |
| batch당 반복 | 10 epochs | 1 inner epoch (8 minibatch) | minibatch당 gradient step 1번 (= 1 epoch) |
| 학습률 | Adam 3e-4 | 상수, 처음 10 iteration warmup | **상수 1e-6** |
| KL 계수 β | 없음 (clip 버전) | 0.02 | 0.01 (7B · 13B) / 0.005 (34B · 70B) |
| value function | GAE λ 0.95, γ 0.99 | RM에서 초기화한 6B, 할인 없음 | 원문 미기술 |
| 보상 | 환경 보상 | 6B RM 하나 | 두 RM의 조건부 조합 + whitening |
| 사전학습 gradient 혼합 | – | PPO-ptx에서 사용 | 원문 미기술 |
| 학습 길이 | 1M timestep | 256k episodes (약 31k 고유 prompt) | 200–400 iterations, held-out prompt로 early stopping |

- **설명할 수 있어야 하는 것:**
  - [ ] batch 512 · minibatch 64 · 한 번의 inner epoch · clip 0.2가 InstructGPT와 **똑같다**는 점을 말한다.
  - [ ] 다른 점(β가 2–4배 작음, 보상이 두 RM의 조합, value function 미기술)을 말한다.
  - [ ] PPO 원 논문의 10 epochs 재사용과 달리 언어모델 RLHF는 1 epoch만 쓴다는 점을 말한다.

<a id="c-ppo-system"></a>

### 70B PPO의 시스템 비용

- **무엇인가:** PPO는 매 iteration마다 **생성(rollout)**과 **학습**을 번갈아 해서, 학습용 분산 방식이 생성에서는 느려지는 문제가 있습니다.
- **원문:** [p.16](https://arxiv.org/pdf/2307.09288v2#page=16) — 70B PPO 한 iteration 평균 약 **330초**. 큰 batch로 빨리 학습하려고 FSDP(Zhao et al. 2023)를 썼는데, 한 번의 forward · backward에는 효과적이었지만 **생성 중에는 약 20배 느려졌습니다**(큰 batch와 KV cache를 써도). 생성 전에 노드마다 가중치를 한 번 모으고(consolidate), 생성 뒤 메모리를 풀어 학습으로 돌아가는 방식으로 완화했습니다.
- **계산해 보면 (추출자 계산):** batch 512 ÷ minibatch 64 = iteration당 gradient step 8번. 200–400 iteration = 1,600–3,200 step, rollout 102,400–204,800개. 70B 기준 200 iteration ≈ 18시간, 400 iteration ≈ 37시간.
- **설명할 수 있어야 하는 것:**
  - [ ] FSDP가 가중치를 GPU에 나눠 두고 쓸 때마다 모으기(all-gather) 때문에, 토큰을 하나씩 만드는 생성에서는 그 통신이 토큰마다 반복되어 느려진다는 이유를 말한다(일반적 설명).
  - [ ] PPO 비용의 상당 부분이 학습이 아니라 생성이라는 점을 Llama 3의 PagedAttention 개선과 연결한다.
- **원전:** PyTorch FSDP [arXiv:2304.11277](https://arxiv.org/abs/2304.11277) · ZeRO [arXiv:1910.02054](https://arxiv.org/abs/1910.02054)

<a id="c-align-followup"></a>

### PPO 이후: DPO · GRPO

- **무엇인가 (논문 밖):** Llama 2의 “RM 학습 → PPO + KL”이 이후 어떻게 바뀌었는지입니다.
  - **DPO (Rafailov et al. 2023):** KL 제약이 있는 보상 최대화의 최적 정책을 닫힌 형태로 풀면, 보상을 `β log(π_θ / π_ref)`로 쓸 수 있습니다. 이를 ranking loss에 넣으면 **RM 없이 선호 쌍으로 정책을 직접** 학습합니다. Llama 2의 Eq. (1)과 Eq. (4)를 하나로 합친 셈입니다.
  - **Llama 3 (2024):** PPO 대신 DPO를 썼고, 큰 모델에서 compute가 적고 성능이 더 좋았다고 보고합니다. RM의 margin 항도 제거했습니다.
  - **GRPO (DeepSeekMath 2024):** value function 없이 같은 prompt의 여러 응답 점수를 그룹 평균으로 정규화해 advantage를 씁니다. 이 스터디의 W07(DeepSeek-R1) · W09(DeepSeek-V3.2)에서 다룹니다.
- **설명할 수 있어야 하는 것:**
  - [ ] DPO가 Llama 2 파이프라인의 어느 두 단계(RM · PPO)를 대체하는지 말한다.
  - [ ] Llama 2가 미기술로 남긴 value function을 GRPO는 아예 쓰지 않는다는 연결을 말한다.
- **출처:** [DPO arXiv:2305.18290](https://arxiv.org/abs/2305.18290) · [Llama 3 §4.1](https://arxiv.org/abs/2407.21783) (2026-10-17 확인) · [DeepSeekMath arXiv:2402.03300](https://arxiv.org/abs/2402.03300). DPO · GRPO 식은 이번에 원문을 다시 열지 않고 적었습니다.

<!-- part: background -->
## Background

### 이번에 새로 채울 빈 영역

W01(LLaMA 1)까지 다룬 것은 원 Transformer와 LLM 기본 학습, 그리고 [W01 읽기 지도](../w01/llama1-reading-map.html)의 Background 표에 있는 블록 부품 · optimizer · 스케일링 법칙 · 효율 구현 · zero/few-shot 평가 · CCNet · BPE · Flan · 위험 벤치마크 4종입니다. W01은 BPE · byte fallback · RoPE · CCNet을 **채택 사실과 정의 한두 줄**로만 다뤘습니다. 아래 표의 위쪽은 이번 주 Background · Data가 그 뒤를 깊게 채우는 주제, 아래쪽은 그 뒤 중간 논문에서 처음 나왔고 Llama 2가 가져다 쓴 개념입니다.

| 개념 | 처음 나온 논문 | Llama 2에서 쓰인 곳 | 이전 주차 | 같이 볼 파트 |
| --- | --- | --- | --- | --- |
| [BPE 학습 · 적용](#c-tok-bpe-train) | Gage, 1994(압축) → Sennrich et al., 2016(subword 분절) | §2.2 Tokenizer(p.6) | W01 정의만 | Background |
| [SentencePiece](#c-tok-sentencepiece) | Kudo & Richardson, 2018 | §2.2 Tokenizer | W01 이름만 | Background · Data |
| [Byte fallback · 숫자 분리](#c-tok-byte-fallback) | SentencePiece v0.1.9(2020) 옵션 · PaLM(2022)이 같은 두 규칙 채택 | §2.2 Tokenizer | W01 정의만 | Background |
| [GPT-2 byte-level BPE](#c-tok-gpt2-bytelevel) | Radford et al., 2019 | 쓰지 않음(비교용) | 처음 | Background |
| [사인파 위치 인코딩](#c-pos-sinusoid) | Vaswani et al., 2017 | 쓰지 않음(RoPE의 출발점) | W01 Transformer 전제 | Background |
| [학습형 절대 위치](#c-pos-learned) | Radford et al., 2018(GPT-1) → GPT-2 · GPT-3 | LLaMA 1이 “제거”한 것 | 처음 | Background |
| [상대 위치: Shaw · T5 · ALiBi](#c-pos-relative) | Shaw et al., 2018 · Raffel et al., 2019 · Press et al., 2021 | 쓰지 않음(비교용) | 처음 | Background |
| [RoPE](#c-pos-rope) | Su et al., 2021(RoFormer) · EleutherAI(2021) · PaLM(2022) 채택 | §2.2 · A.2.1(4K) | W01 적용 위치만 | Background · Architecture |
| [fastText · KenLM 품질 필터](#c-q-ccnet-pipeline) | Joulin et al., 2016 · Heafield, 2011 · Wenzek et al., 2019(CCNet) | §2.1 “more robust data cleaning”(필터 미기술) · §4.1 언어 식별 | W01 단계 이름만 | Data |
| [KV cache](#c-kv-cache) | 자기회귀 decoding의 표준 관행 · 대규모 추론 분석은 Pope et al., 2022 | App. A.2.1 | 처음 | Architecture |
| [MQA](#c-mha-mqa-gqa) | Shazeer, 2019 · PaLM(2022) 채택 | App. A.2.1 · Table 18 | 처음 | Architecture |
| [GQA](#c-mha-mqa-gqa) | Ainslie et al., 2023 | §2.2 · Table 1 · A.2.1 | 처음 | Architecture |
| [Tensor parallelism](#c-tp-serving) | Shoeybi et al., 2019 (Megatron-LM) | A.2.1 배포 | W01은 model · sequence parallelism만 | Architecture |
| [긴 문맥 벤치마크 SCROLLS](#c-long-context-bench) | Shaham et al., 2022 | Table 16 | 처음 | Architecture |
| [BBH · AGIEval](#c-bench-new) | Suzgun et al., 2022 · Zhong et al., 2023 | Table 3 · 24 | 처음 | Architecture |
| [데이터 오염 분석](#c-contamination) | Brown et al., 2020(13-gram) · Chowdhery et al., 2022(8-gram 70%) | App. A.6 | 처음 | Architecture |
| [RLHF 3단계 골격](#c-rlhf-pipeline) | Christiano et al., 2017 → Stiennon et al., 2020 → Ouyang et al., 2022 (InstructGPT) | §3 전체 | W01은 “RLHF 없음”만 확인 | Post-training · Alignment |
| [적은 고품질 SFT](#c-sft-data) | Zhou et al., 2023 (LIMA) | §3.1 | 처음 | Post-training |
| [RM의 분포 이동](#c-weekly-batches) | Scialom et al., 2020b (hyper-specialization) | §3.2.1 | 처음 | Post-training |
| [공개 선호 데이터셋](#c-open-pref-datasets) | Stiennon 2020 · Nakano 2021 · Bai 2022a · Ethayarajh 2022 | Table 6 | 처음 | Post-training |
| [평가자 일치도 Gwet AC2](#c-human-eval) | Gwet, 2008 | §3.4.2 | 처음 | Post-training |
| [Bradley–Terry 선호 모델](#c-bradley-terry) | Bradley & Terry, 1952 · RM loss는 Ouyang et al., 2022 | Eq. (1) | 처음 | Alignment |
| [도움됨 · 무해성의 긴장](#c-rm-arch) | Bai et al., 2022a (Anthropic HH) | §3.2.2 | 처음 | Alignment |
| [Rejection sampling / best-of-N](#c-rs-ft) | Nakano et al., 2021(best-of-n) · Bai et al., 2022b | §3.2.3 | 처음 | Alignment |
| [망각(forgetting)](#c-rs-history) | Kirkpatrick et al., 2017 | §3.2.3 | 처음 | Alignment |
| [PPO](#c-ppo-clip) | Schulman et al., 2017 | §3.2.3 · Eq. (3) | 처음 | Alignment |
| [참조 정책 KL penalty](#c-kl-penalty) | Ziegler et al., 2019 · Stiennon et al., 2020 | Eq. (4) | 처음 | Alignment |
| [FSDP](#c-ppo-system) | ZeRO(Rajbhandari et al., 2020) · PyTorch FSDP(Zhao et al., 2023) | §3.2.3 PPO | 처음 | Alignment |

**재방문만 하는 W01 개념:** [RMSNorm](../w01/llama1-reading-map.html#c-rmsnorm) · [SwiGLU](../w01/llama1-reading-map.html#c-swiglu) · [AdamW](../w01/llama1-reading-map.html#c-adamw) · [Flan](../w01/llama1-reading-map.html#c-flan) · [likelihood 채점](../w01/llama1-reading-map.html#c-likelihood-eval) · [pass@k](../w01/llama1-reading-map.html#c-majk-passk) · [탄소 추정](../w01/llama1-reading-map.html#c-carbon). Llama 2가 이들을 새로 도입한 것처럼 쓰지 않습니다.

<a id="c-w01-carryover"></a>

### W01에서 넘어온 주제

W01 발표자료의 부록 Background는 LLaMA 1 원문이 한 줄이나 출처 표기로 넘어간 네 주제를 “다음 주 W02에서 깊게”로 넘겼습니다. Llama 2도 같은 recipe를 이어받아 원문이 더 짧아졌습니다.

| 주제 | LLaMA 1 원문이 한 말 | Llama 2 원문이 한 말 | 이번 주에 깊게 볼 것 | 담당 |
| --- | --- | --- | --- | --- |
| Tokenizer | SentencePiece BPE · 숫자 분리 · 바이트 분해(§2.1) | “same tokenizer as Llama 1”, 어휘 32k(p.6) | BPE가 merge를 쌓는 과정, SentencePiece의 `▁`와 lossless, byte fallback이 한국어에서 하는 일, GPT-2 방식과의 차이 | Background (이정민 · 김민선) |
| RoPE | GPTNeo를 따라 절대 위치 임베딩을 없애고 각 layer에 RoPE(§2.2) | 부품 목록에 RoPE, context만 2K → 4K(§2.2 · A.2.1) | 사인파 → 학습형 → 상대 위치 → 회전의 흐름, 회전하면 거리만 남는 이유, d = 128의 파장과 4K | Background (이정민 · 김민선) |
| 품질 분류기 | CCNet(라인 중복 제거 · fastText 언어 식별 · n-gram LM 필터) + Wikipedia 참조 페이지 선형 분류기(§2.1) | “more robust data cleaning”만, 필터는 미기술(§2.1) | fastText 분류기와 KenLM perplexity가 각각 무엇을 계산하고 무엇을 버리는지, 참조 분류기의 양성 · 음성 | Data (정호찬) |
| 스케일링 법칙 | Hoffmann et al.을 인용하며 추론 예산을 고려하지 않는다는 한 문단(§1) | 2T를 “good performance–cost trade-off”라고만 적음(§2.1) | 이번 배정에 없음. Architecture의 [loss 곡선](#c-loss-curve) 페이지에서 결론만 다시 씀 | 미정 |

- 읽기 지도 규칙은 RoPE를 실제로 쓰이는 Architecture에 두라고 하지만, 이번 주는 배정에 따라 Background가 맡습니다. Architecture의 [2K → 4K context](#c-context-4k)와 함께 준비하는 안을 [분량과 함께 할 파트](#overview-collab)에 적었습니다.

### 이 파트의 질문

- **담당:** 이정민 · 김민선
- **범위:** Llama 2 [§2.2 Tokenizer 문단](https://arxiv.org/pdf/2307.09288v2#page=6)(p.6)과 RoPE를 언급한 [§2.2](https://arxiv.org/pdf/2307.09288v2#page=5)(p.5) · [A.2.1 Context Length](https://arxiv.org/pdf/2307.09288v2#page=47). 원문이 한두 줄이므로 분량은 원전이 대부분입니다.
- **RQ1. Llama 2의 tokenizer는 텍스트를 어떻게 토큰으로 바꾸고, 그 규칙은 어디서 왔나?**
  - 필수 원문: [Llama 2 p.6 Tokenizer](https://arxiv.org/pdf/2307.09288v2#page=6) · BPE [Sennrich et al. §3.2 · Algorithm 1](https://arxiv.org/pdf/1508.07909v5#page=3) · [SentencePiece §2–§3](https://arxiv.org/pdf/1808.06226v1#page=2) · [SentencePiece v0.1.9 릴리스 노트](https://github.com/google/sentencepiece/releases/tag/v0.1.9) · (비교) [GPT-2 §2.2](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
  - 개념: [Tokenizer 로드맵](#c-tok-roadmap) · [BPE 학습](#c-tok-bpe-train) · [학습된 merge로 분절하기](#c-tok-bpe-apply) · [SentencePiece](#c-tok-sentencepiece) · [Byte fallback과 숫자 분리](#c-tok-byte-fallback) · [GPT-2의 byte-level BPE](#c-tok-gpt2-bytelevel) · (선택, 논문 밖) [Llama 3의 128K 어휘](#c-tok-followup)
- **RQ2. 위치 정보를 넣는 방법은 사인파에서 RoPE까지 어떻게 바뀌었고, 왜 “회전”인가?**
  - 필수 원문: [Llama 2 §2.2](https://arxiv.org/pdf/2307.09288v2#page=5) · [Transformer §3.5 · Table 3 (E)](https://arxiv.org/abs/1706.03762v7) · [GPT-1 §3.1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) · [RoFormer §3.1–§3.4](https://arxiv.org/abs/2104.09864v5) · (비교) [ALiBi §2](https://arxiv.org/abs/2108.12409v2)
  - 개념: [위치 인코딩 로드맵](#c-pos-roadmap) · [사인파 위치 인코딩](#c-pos-sinusoid) · [학습형 절대 위치 임베딩](#c-pos-learned) · [상대 위치 방식](#c-pos-relative) · [RoPE](#c-pos-rope) · [RoPE 돌려 보기](#c-pos-rope-calc) · (선택, 논문 밖) [위치 보간과 밑값 키우기](#c-pos-followup)
- 직접 돌린 코드와 확인한 원전은 검토 기록의 [Tokenizer 검증 메모](#memo-tokenizer) · [RoPE 검증 메모](#memo-position)에 있습니다.

<a id="c-tok-roadmap"></a>

### Tokenizer 로드맵: 압축 기법에서 32k 어휘까지

| 단계 | 무엇이 바뀌었나 | 출처 |
| --- | --- | --- |
| 1. 압축 | 가장 자주 나오는 바이트 쌍을 안 쓰는 바이트 하나로 바꾸는 데이터 압축 | Gage, 1994 |
| 2. subword 분절 | 같은 아이디어를 문자열에 적용. merge 횟수 = 유일한 하이퍼파라미터, 단어 끝 기호 `</w>` | Sennrich et al., 2016 §3.2 |
| 3. 원문 그대로 | 공백을 `▁`로 토큰에 넣어 lossless, 최종 어휘 크기를 지정, 미리 자르기 없음 | SentencePiece, 2018 §3 |
| 4. 바이트를 기본 단위로 | 바이트열 위에서 BPE, 기본 어휘 256, 문자 범주를 넘는 merge 금지, 어휘 50,257 | GPT-2, 2019 §2.2 |
| 5. 바이트를 최후의 수단으로 | 문자 BPE는 그대로, 어휘 밖 문자만 UTF-8 바이트 토큰으로(`--byte_fallback`), 숫자 한 자리씩(`--split_digits`) | SentencePiece v0.1.9, 2020 · PaLM, 2022 |
| **LLaMA 1 → Llama 2** | SentencePiece BPE + byte fallback + 숫자 분리, 어휘 32,000(일반 31,741 + 바이트 256 + 특수 3) | LLaMA 1 §2.1 · Llama 2 p.6 · 공개 `tokenizer.model` |
| 6. 이후 (논문 밖) | tiktoken 100K + 비영어 28K = 128K, 영어 3.17 → 3.94 문자/토큰 | Llama 3, 2024 §3.2 |

- **원문이 한 말:** Llama 2는 “Llama 1과 같은 tokenizer”, BPE를 SentencePiece로, 숫자 분리, 바이트 분해, 어휘 32k만 적습니다. 학습 말뭉치 · 설정 · 효과 실험은 **미기술**입니다.
- **이번 주에 깊게 볼 것:** merge가 쌓이는 과정을 손으로 따라가기, `▁`와 lossless, 한국어 문장에서 byte fallback이 실제로 몇 토큰을 만드는지, GPT-2 방식과 무엇이 다른지.
- **같이 볼 곳:** Data의 KenLM 필터는 SentencePiece로 토큰화한 문단에 perplexity를 계산합니다([CCNet 파이프라인](#c-q-ccnet-pipeline)).

<a id="c-tok-bpe-train"></a>

### BPE 학습: merge를 쌓아 어휘를 만든다

- **무엇인가:** BPE(Byte Pair Encoding)는 원래 가장 자주 나오는 바이트 쌍을 안 쓰는 바이트 하나로 바꿔 가는 압축 기법입니다(Gage 1994). Sennrich 등(2016)은 이를 단어 분절에 가져와, 바이트 대신 **문자와 문자열**을 합칩니다. 단어를 문자열 + 단어 끝 기호 `·`(코드에서는 `</w>`)로 적고, 말뭉치 전체에서 가장 자주 붙어 나오는 기호 쌍 하나를 새 기호로 합치는 일을 정해진 횟수만큼 반복합니다. 합친 기록, 즉 **merge 목록**이 학습 결과입니다.
- **원문:** [Llama 2 §2.2 Training Details의 Tokenizer 문단 (p.6)](https://arxiv.org/pdf/2307.09288v2#page=6)은 “Llama 1과 같은 tokenizer이고 BPE(Sennrich et al., 2016)를 SentencePiece 구현으로 썼다”는 채택 사실만 기술합니다. 학습 말뭉치, merge 수, 학습 설정은 **원문 미기술**입니다. 알고리즘 자체는 원전 [Sennrich et al. §3.2 · Algorithm 1 · Figure 1 (arXiv:1508.07909v5, p.3–4)](https://arxiv.org/pdf/1508.07909v5#page=3)에 있습니다.
  - 원전이 말하는 것: 초기 기호 어휘 = 문자 어휘. 최종 어휘 크기 = 초기 어휘 + merge 횟수이고, merge 횟수가 **유일한 하이퍼파라미터**입니다. 효율을 위해 **단어 경계를 넘는 쌍은 세지 않으므로**, 텍스트 대신 빈도가 붙은 단어 사전 위에서 돌릴 수 있습니다.
  - 단어 끝 기호를 두는 이유를 원전은 “번역 뒤 원래 토큰화를 복원하기 위해서”라고 적습니다. 그 결과 `est·`(단어 끝의 est)와 `est`(단어 중간의 est)가 다른 기호가 됩니다(추출자 해석).
- **돌려 보면:** Algorithm 1의 사전 `{low:5, lower:2, newest:6, widest:3}`에 merge 10번. 원전 코드를 그대로 돌린 결과와, 직접 짠 순수 Python 구현(scratchpad `toy_bpe.py`)의 결과가 같았습니다. 동점이면 사전에 먼저 나온 쌍을 고릅니다(Python `max`의 동작).

  | # | 합친 쌍 | 빈도 | 그 뒤 사전 |
  | --- | --- | --- | --- |
  | 1 | e + s → es | 9 (newest 6 + widest 3) | n e w es t `</w>` … |
  | 2 | es + t → est | 9 | n e w est `</w>` |
  | 3 | est + `</w>` → est`</w>` | 9 | w i d est`</w>` |
  | 4 | l + o → lo | 7 (low 5 + lower 2) | lo w `</w>`, lo w e r `</w>` |
  | 5 | lo + w → low | 7 | low `</w>`, low e r `</w>` |
  | 6 | n + e → ne | 6 | ne w est`</w>` |
  | 7 | ne + w → new | 6 | new est`</w>` |
  | 8 | new + est`</w>` → newest`</w>` | 6 | newest`</w>` (한 기호) |
  | 9 | low + `</w>` → low`</w>` | 5 | low`</w>` (한 기호) |
  | 10 | w + i → wi | 3 | wi d est`</w>` |

  초기 기호는 11개(문자 10개 + `</w>`)이므로, 원전 정의대로 최종 어휘는 11 + 10 = **21개**입니다. 빈도가 높은 `newest`와 `low`는 통째로 한 기호가 됐고, 빈도 2인 `lower`의 `er`은 10번 안에 합쳐지지 않았습니다.
  - 원전 Figure 1의 merge 순서(`r·` → `lo` → `low` → `er·`)는 다른 사전 `{low, lowest, newer, wider}`에서 나온 것입니다. Figure 1에는 빈도가 없습니다. 네 단어를 빈도 1로 두고 돌리면 첫 쌍부터 5개가 동점이라, 같은 구현에서는 `lo` → `low` → `er` → `er</w>` 순서가 나옵니다. **merge 순서는 빈도와 동점 처리 규칙에 달려 있습니다.**
- **왜 그런가:** 자주 나오는 문자열일수록 먼저 합쳐집니다. 그래서 흔한 단어는 한 토큰이 되고, 드문 단어는 여러 조각으로 남습니다. 원전은 이 방식이 shortlist(자주 쓰는 단어 목록) 없이도 열린 어휘(open vocabulary)를 다루게 해 준다고 설명합니다. 어휘 크기는 merge 횟수 하나로 조절됩니다. 크게 하면 시퀀스가 짧아지는 대신 임베딩 행렬이 커지고, 작게 하면 그 반대입니다(W01 로드맵의 줄다리기).
- **설명할 수 있어야 하는 것:**
  - [ ] 위 사전으로 첫 3–5개 merge를 손으로 세어 보이고, 동점일 때 순서가 규칙에 따라 갈린다는 점을 말한다.
  - [ ] “최종 어휘 = 초기 문자 어휘 + merge 횟수”와 단어 끝 기호 `</w>`의 역할을 설명한다.
  - [ ] 원전이 단어 경계를 넘는 쌍을 세지 않은 이유(효율, 빈도 사전으로 학습)를 말한다.
  - [ ] Llama 2 원문은 BPE를 썼다는 사실만 밝히고 학습 말뭉치·설정은 적지 않았다는 점을 구분한다.
- **함께 볼 개념 / 원전:** [학습된 merge로 분절하기](#c-tok-bpe-apply) · [SentencePiece](#c-tok-sentencepiece) · W01 [BPE와 SentencePiece](../w01/llama1-reading-map.html#c-bpe) · 원전: Sennrich et al. 2016 §3.2, Algorithm 1

<a id="c-tok-bpe-apply"></a>

### 학습된 merge로 새 텍스트 분절하기

- **무엇인가:** 학습이 끝나면 merge 목록만 남습니다. 새 단어가 오면 문자로 쪼갠 뒤 **학습한 순서대로 merge를 다시 적용**합니다. 그래서 학습 때 못 본 단어도, 문자만 알면 기존 조각의 조합으로 표현됩니다.
- **원문:** [Llama 2 p.6](https://arxiv.org/pdf/2307.09288v2#page=6)은 분절 절차를 기술하지 않습니다. 원전 [Sennrich et al. §3.2 (p.4)](https://arxiv.org/pdf/1508.07909v5#page=4): 테스트 때 단어를 문자열로 나눈 다음 학습한 연산을 적용해 더 큰 기호로 합칩니다. Figure 1의 예에서 처음 보는(OOV) `lower`는 `low er·`로 분절됩니다. 각주 3은 test 때 모를 수 있는 기호를 두 가지로 꼽습니다. 하나는 **모르는 문자**이고, 다른 하나는 학습 데이터에서 모두 더 큰 기호로 합쳐져 버린 기호입니다(예: `safeguar`).
- **돌려 보면 (1) 원전 방식:** 위 10개 merge를 앞에서부터 k개만 적용한 결과(`toy_bpe.py`).

  | 단어 | k=0 | k=3 | k=5 | k=10 |
  | --- | --- | --- | --- | --- |
  | lowest | l o w e s t `</w>` | l o w est`</w>` | **low est`</w>`** | low est`</w>` |
  | lower | l o w e r `</w>` | 그대로 | low e r `</w>` | low e r `</w>` |
  | newer | n e w e r `</w>` | 그대로 | 그대로 | new e r `</w>` |
  | slow | s l o w `</w>` | 그대로 | s low `</w>` | s low`</w>` |

  `lowest`는 사전에 없는 단어지만 `low` + `est</w>` 두 조각으로 표현됩니다. Figure 1 사전으로 배운 merge 4개를 `lower`에 적용하면 원전과 같은 `low er</w>`이 나옵니다.
- **돌려 보면 (2) Llama tokenizer:** SentencePiece BPE는 merge 목록 대신 **조각마다 점수**를 저장합니다. Llama `tokenizer.model`에서는 일반 조각의 점수가 id 순서대로 −1, −2, −3, …으로 매겨져 있습니다(`▁t` id 260 → −1, `er` id 261 → −2). 학습 때 먼저 생긴 merge일수록 점수가 높다고 읽을 수 있습니다(추출자 해석). “이웃한 두 조각을 합친 결과가 어휘에 있으면, 그중 점수가 가장 높은 쌍부터 합친다”를 직접 구현해 라이브러리 출력과 비교했더니 세 단어 모두 같았습니다(`trace_sp_bpe.py`).

  | 입력 | 합쳐지는 순서 | 결과 |
  | --- | --- | --- |
  | `lowest` | es → ▁l → ow → est → ▁low → ▁lowest | `▁lowest` (1토큰, id 19604) |
  | `unbelievably` | el → ▁u → ie → ly → ab → ▁un → ably → bel → iev | `▁un` `bel` `iev` `ably` |
  | `tokenization` | ▁t → en → on → at → ion → ▁to → ation → iz → ken → ization → ▁token | `▁token` `ization` |

  눈여겨볼 점: 중간에 생긴 `▁l`, `ow` 같은 조각이 마지막 결과에는 남지 않습니다. 결과는 학습 때 merge가 일어난 순서를 따라갑니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 처음 보는 단어가 merge 재적용으로 기존 조각의 조합이 되는 과정을 `lowest` 예로 보인다.
  - [ ] 원전(merge 목록을 순서대로 재생)과 SentencePiece(조각 점수가 높은 쌍부터 합침)의 표현 차이를 말하고, 이 Llama 모델에서는 점수가 id 순서와 같다는 관찰을 근거와 함께 말한다.
  - [ ] BPE만으로는 **모르는 문자**가 여전히 남는다는 원전 각주 3을 들어, byte fallback이 무엇을 메우는지 연결한다.
- **함께 볼 개념 / 원전:** [BPE 학습](#c-tok-bpe-train) · [Byte fallback과 숫자 분리](#c-tok-byte-fallback) · 원전: Sennrich et al. 2016 §3.2와 각주 3

<a id="c-tok-sentencepiece"></a>

### SentencePiece: 원문 그대로 학습하고, 공백까지 토큰으로

- **무엇인가:** SentencePiece는 Kudo & Richardson(2018)이 만든 언어 독립 tokenizer/detokenizer 라이브러리입니다. 미리 띄어쓰기로 자른 단어가 아니라 **원문 문장**에서 바로 subword 모델을 학습합니다. 공백도 일반 기호로 다루기 때문에 토큰을 이어 붙이면 원문이 그대로 돌아옵니다.
- **원문:** [Llama 2 p.6](https://arxiv.org/pdf/2307.09288v2#page=6)은 “SentencePiece 구현을 썼다”는 사실과 어휘 32k만 기술합니다. 아래 학습 설정은 원문이 아니라 공개된 tokenizer 파일에서 읽은 값입니다. 원전 [Kudo & Richardson, arXiv:1808.06226v1](https://arxiv.org/pdf/1808.06226v1#page=2):
  - §1: BPE(Sennrich 2016)와 unigram language model(Kudo 2018) 두 알고리즘을 구현하고, 원문 문장에서 바로 학습하도록 확장했다.
  - §2: 구성 요소는 Normalizer · Trainer · Encoder · Decoder 넷이다.
  - §3.1 **Lossless tokenization:** `Decode(Encode(Normalize(text))) = Normalize(text)`. 공백을 메타 기호 `▁`(U+2581)로 바꾼 뒤 분절하므로, `''.join(tokens).replace('▁', ' ')`로 모호함 없이 되돌린다. subword-nmt의 `@@` 표기는 연속 공백을 표현하지 못한다는 비교도 함께 적었다.
  - §3.2: 미리 자르기(pre-tokenization)를 가정하지 않는다. 띄어쓰기가 없는 언어 때문이다. BPE 분절을 naive하게 하면 O(N²)이지만 binary heap으로 O(N log N)에 한다.
  - §3.3: merge 횟수 대신 **최종 어휘 크기**(`--vocab_size`)를 지정한다. merge 횟수는 BPE에만 있는 파라미터라 unigram에는 쓸 수 없기 때문이다.
  - §3.4: 기본 정규화는 NFKC다.
- **돌려 보면:** 공개 Llama tokenizer(`hf-internal-testing/llama-tokenizer`의 `tokenizer.model`. LLaMA 1 공개본 `huggyllama/llama-7b`와 sha256이 같음)의 `trainer_spec` · `normalizer_spec`을 sentencepiece 0.2.2로 읽었습니다.

  | 항목 | Llama 값 | 라이브러리 기본값(현재 문서) | 메모 |
  | --- | --- | --- | --- |
  | `model_type` | **BPE** | unigram | 논문의 “BPE”와 일치 |
  | `vocab_size` | **32000** | 8000 | NORMAL 31,741 + BYTE 256 + `<unk>` `<s>` `</s>` 3 |
  | `byte_fallback` | **true** | false | [다음 페이지](#c-tok-byte-fallback) |
  | `split_digits` | **true** | false | 숫자 한 자리씩 |
  | `character_coverage` | 0.99995 | 0.9995 | 기본 문자 집합에 넣을 문자 비율 |
  | normalizer `name` | **identity** | nmt_nfkc | NFKC 정규화를 하지 않음 |
  | `add_dummy_prefix` | true | true | 문장 앞에 `▁` 하나를 붙임 |
  | `remove_extra_whitespaces` | **false** | true | 연속 공백 보존 |
  | `allow_whitespace_only_pieces` | true | false | `▁▁`, `▁▁▁▁` 같은 공백 조각 허용 |
  | `split_by_unicode_script` · `split_by_number` · `split_by_whitespace` | true · true · true | true · true · true | 문자 체계·숫자·공백 경계를 넘는 조각 금지 |
  | `input_sentence_size` | 200,000,000 | 0(전체) | 학습에 쓴 최대 문장 수 |

  라이브러리 기본값은 2026년 현재 master의 `doc/options.md`에서 확인한 값이라 2023년 당시 기본값과 같다고 단정하지 않습니다. Llama 값은 파일에 저장된 실제 설정입니다.

  lossless 확인: `"  two  spaces"` → `['▁▁', '▁two', '▁', '▁spaces']`이고, decode 결과가 입력과 같았습니다. `"Hello world."` → `['▁Hello', '▁world', '.']`(3토큰)입니다. 실험한 12개 입력 모두 `decode(encode(x)) == x`였습니다.
- **왜 그런가:** 공백을 `▁`로 토큰 안에 넣으면 “어디에 공백이 있었나”가 토큰열에 남습니다. 그래서 언어별 detokenizer 규칙이 필요 없고, 코드처럼 공백이 의미 있는 텍스트도 복원됩니다(원전 §3.1). Llama 설정에서 NFKC를 끄고(identity) 연속 공백을 지우지 않은 것도 같은 방향, 즉 입력을 그대로 보존하는 쪽입니다. 다만 이 선택의 이유는 Llama 1·2 원문 모두 **미기술**입니다(추출자 해석).
- **설명할 수 있어야 하는 것:**
  - [ ] `▁`(U+2581)가 무엇이고, 그 덕분에 `Decode(Encode(text)) = text`가 성립한다는 점을 공백 예로 보인다.
  - [ ] subword-nmt는 merge 횟수를, SentencePiece는 최종 어휘 크기를 지정한다는 차이와 그 이유를 말한다.
  - [ ] Llama 설정 가운데 원문에 있는 것(BPE, 32k, 숫자 분리, 바이트 분해)과 파일에서만 확인되는 것(identity 정규화, coverage 0.99995 등)을 구분한다.
- **함께 볼 개념 / 원전:** [BPE 학습](#c-tok-bpe-train) · [Byte fallback과 숫자 분리](#c-tok-byte-fallback) · 원전: Kudo & Richardson 2018 §2, §3.1–3.4

<a id="c-tok-byte-fallback"></a>

### Byte fallback과 숫자 분리

- **무엇인가:** **Byte fallback**은 어휘에 없는 문자를 `<unk>` 하나로 뭉개지 않고, 그 문자의 UTF-8 바이트를 하나씩 바이트 토큰 `<0x00>`…`<0xFF>`으로 내보내는 규칙입니다. 이를 위해 바이트 토큰 256개를 어휘에 미리 넣어 둡니다. **숫자 분리**(`split_digits`)는 0–9를 언제나 한 자리씩 다른 조각으로 나누는 규칙입니다.
- **원문:** [Llama 2 p.6](https://arxiv.org/pdf/2307.09288v2#page=6): Llama 1과 같이 모든 숫자를 한 자리씩 나누고, 모르는 UTF-8 문자는 바이트로 분해합니다. 효과에 대한 실험은 **원문 미기술**입니다.
  - 이 기능은 SentencePiece 논문(2018)에는 없습니다. 라이브러리 [v0.1.9 릴리스 노트(2020-05-13)](https://github.com/google/sentencepiece/releases/tag/v0.1.9)에서 `--byte_fallback`(“UNK를 UTF-8 바이트열로 대체, 바이트 기호 256개 예약”)과 `--split_digits`가 함께 추가됐습니다. 이 노트는 `character_coverage`를 1.0보다 작게 둬야 학습 데이터에 바이트 토큰이 실제로 나타난다고도 적습니다.
  - [options.md](https://github.com/google/sentencepiece/blob/master/doc/options.md): `character_coverage`는 빈도순으로 문자를 쌓아 이 비율에 도달할 때까지만 기본 문자 집합에 넣고, 나머지는 `<unk>`(또는 byte fallback)로 보냅니다. [model proto](https://github.com/google/sentencepiece/blob/master/src/sentencepiece_model.proto)에서 바이트 조각의 type은 `BYTE`입니다.
  - 같은 두 규칙은 PaLM(2022) §2 Vocabulary에도 있습니다(256k SentencePiece, OOV 문자를 UTF-8 바이트로, `123.5 → 1 2 3 . 5`). 하지만 LLaMA 1·Llama 2의 tokenizer 문단은 PaLM을 인용하지 않습니다. “PaLM의 관행을 따랐다”는 말은 추출자 해석입니다.
- **돌려 보면 (Llama tokenizer, sentencepiece 0.2.2):**

  | 입력 | 토큰 | 개수 |
  | --- | --- | --- |
  | `1234` | `▁` `1` `2` `3` `4` | 5 |
  | `3.14` | `▁` `3` `.` `1` `4` | 5 |
  | `2023년` | `▁` `2` `0` `2` `3` `년` | 6 |
  | `안녕하세요 가짜연구소` | `▁` `안` `<0xEB>` `<0x85>` `<0x95>` `하` `세` `요` `▁` `가` `<0xEC>` `<0xA7>` `<0x9C>` `연` `구` `소` | 16 |
  | `😀` | `▁` `<0xF0>` `<0x9F>` `<0x98>` `<0x80>` | 5 |
  | `🦙 Llama` | `▁` `<0xF0>` `<0x9F>` `<0xA6>` `<0x99>` `▁L` `l` `ama` | 8 |

  - 어휘에 있는 숫자 조각은 한 자리 `0`–`9` 10개뿐입니다(id 29896 `1` 등). `▁1`은 어휘에 없어서, 문장 앞 숫자는 `▁` 하나가 따로 붙습니다.
  - `녕`(U+B155, UTF-8 `EB 85 95`)과 `짜`(U+C9DC, `EC A7 9C`)는 어휘에 없어 3바이트 토큰으로 나뉘었습니다. `안` `하` `세` `요` `가` `연` `구` `소`는 한 글자 조각으로 어휘에 있습니다. 바이트 토큰 id는 3 + 바이트값입니다(`<0xEB>` = 3 + 235 = 238).
  - 어휘 32,000개 중 한글 음절이 든 조각은 **111개**이고, **2음절 이상인 조각은 0개**입니다. `▁안`, `▁가`도 없습니다. 한국어는 많아야 음절 하나가 한 토큰이고, 어휘에 없는 음절은 3토큰이 됩니다.
  - W01 대본 앞부분(3,066자, 한국어 위주, 설명용 표본)에서 Llama 토큰 4,197개 중 **49.7%(2,085개)가 바이트 토큰**이었습니다. 한글 음절 1,812개(서로 다른 음절 288개) 가운데 어휘에 있는 음절은 90종이고, 출현 횟수로는 1,120개(61.8%)를 덮었습니다. 표본 하나의 값이라 일반화하지 않습니다.
  - **on/off 비교(설명용 미니 학습):** 같은 작은 말뭉치로 SentencePiece BPE를 두 번 학습했습니다(merge 수를 맞추려고 vocab 60 대 316). `byte_fallback=false`에서는 학습에 없던 `짱`과 `😀`가 id 0(`<unk>`)이 되고, decode하면 ` ⁇ `로 원문이 사라집니다. `byte_fallback=true`에서는 `짱` → `<0xEC>` `<0xA7>` `<0xB1>`이 되고 decode하면 `짱`이 돌아옵니다. `split_digits=false`일 때 `1234`는 `▁` `1` `23` `4`였습니다(말뭉치의 2023 · 1234에 23이 겹쳐서). true일 때는 `▁` `1` `2` `3` `4`였습니다.
- **왜 그런가:**
  - Byte fallback: UTF-8은 모든 문자를 1–4바이트로 표현합니다. 그래서 바이트 토큰 256개만 있으면 어떤 문자열도 `<unk>` 없이 표현되고 decode로 복원됩니다. 대가는 길이입니다. 한글 음절 하나가 3토큰, 이모지 하나가 4토큰이 되어 같은 문맥 길이(4k 토큰)에 담기는 글자가 줄어듭니다.
  - 숫자 분리: 분리하지 않으면 BPE가 말뭉치 빈도에 따라 `23`처럼 제멋대로 합쳐, 같은 자릿수의 수도 토큰 경계가 달라집니다(위 미니 학습). 한 자리씩 고정하면 모든 수가 같은 방식으로 표현됩니다. 이것이 산술에 도움이 된다는 것은 일반적 설명이고, Llama 2 원문은 이를 실험하지 않았습니다(**원문 미기술**).
- **설명할 수 있어야 하는 것:**
  - [ ] `녕` → `<0xEB>` `<0x85>` `<0x95>`처럼 어휘 밖 문자가 UTF-8 바이트 토큰이 되는 과정을 보이고, `<unk>`와 무엇이 다른지(복원 가능) 말한다.
  - [ ] Llama 어휘 구성(일반 31,741 + 바이트 256 + 특수 3 = 32,000)과 한국어가 음절 하나 또는 3바이트 토큰이 되는 이유를 `character_coverage`와 연결해 설명한다.
  - [ ] `split_digits`가 없을 때 숫자가 빈도에 따라 들쭉날쭉 합쳐지는 예를 들고, 원문이 효과를 실험하지 않았다는 점을 구분한다.
- **함께 볼 개념 / 원전:** [SentencePiece](#c-tok-sentencepiece) · [GPT-2 byte-level BPE](#c-tok-gpt2-bytelevel) · W01 [숫자 분리와 byte fallback](../w01/llama1-reading-map.html#c-digit-byte) · 원전: SentencePiece v0.1.9 릴리스 노트, PaLM §2

<a id="c-tok-gpt2-bytelevel"></a>

### 대안: GPT-2의 byte-level BPE

- **무엇인가:** GPT-2는 문자(유니코드 코드 포인트)가 아니라 **바이트열 위에서 BPE를 학습**합니다. 기본 어휘가 처음부터 256바이트이므로 모르는 문자가 생길 수 없습니다. SentencePiece BPE + byte fallback은 반대입니다. **문자 위에서 BPE**를 하고, 기본 문자 집합에서 빠진 드문 문자만 바이트로 내립니다.
- **원문:** Llama 2는 GPT-2 tokenizer를 언급하지 않습니다. 이 페이지는 비교용입니다(논문 밖). 원전 [Radford et al. 2019 §2.2 Input Representation (p.4)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf):
  - 코드 포인트 위의 BPE로 모든 유니코드를 다루려면 multi-symbol 토큰을 더하기 전부터 기본 어휘가 13만 개를 넘는다. byte-level이면 256개로 충분하다.
  - 바이트열에 BPE를 그대로 쓰면 `dog.` `dog!` `dog?`처럼 같은 단어의 변형이 어휘 자리를 낭비한다. 그래서 **문자 범주(character category)를 넘는 merge를 막고**, 공백만 예외로 둔다.
  - 어휘는 **50,257**개(§2.3). 범주 구분은 논문에 규칙으로 나오지 않습니다. 공개 코드 [`encoder.py`](https://github.com/openai/gpt-2/blob/master/src/encoder.py)의 정규식(`'s|'t|…| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|…`)이 문자·숫자·기호를 먼저 나누는 방식으로 구현합니다.
- **돌려 보면 (GPT-2 = `openai-community/gpt2` tokenizer.json, tokenizers 라이브러리 · Llama = 위 tokenizer.model):**

  | 입력 | GPT-2 | Llama |
  | --- | --- | --- |
  | `Hello world.` | `Hello` `Ġworld` `.` (3) | `▁Hello` `▁world` `.` (3) |
  | `dog. dog! dog?` | `dog` `.` `Ġdog` `!` `Ġdog` `?` (6) | `▁dog` `.` `▁dog` `!` `▁dog` `?` (6) |
  | `1234` | `12` `34` (2) | `▁` `1` `2` `3` `4` (5) |
  | `안녕하세요 가짜연구소` | 바이트 조각 **30개** | 음절·바이트 조각 **16개** |
  | `😀` | `ðŁĺ` `Ģ` (2) | `▁` + 바이트 4개 (5) |

  - GPT-2 토큰의 `Ġ`, `ð` 같은 글자는 바이트를 출력 가능한 유니코드 문자로 바꿔 보여 주는 표기입니다(`bytes_to_unicode`). 실제 단위는 바이트입니다.
  - 설명용 표본의 문자/토큰 비. 영어(GPT-2 §2.2 문단, 2,423자): Llama 4.21, GPT-2 4.62. 한국어 위주(W01 대본 앞부분, 3,066자): Llama 0.73, GPT-2 0.56. 표본 두 개에서 잰 값이고 Meta가 보고한 수치와는 표본이 다릅니다.
- **왜 그런가 (추출자 해석):** byte-level BPE에서는 한국어 음절의 3바이트 안에서도 merge가 일어날 수 있습니다(위 출력의 `íķ`가 두 바이트를 합친 조각). 하지만 영어 위주 말뭉치로 학습해 그런 merge가 적고, 한국어 10음절이 30토큰, 사실상 바이트 단위로 남습니다. Llama는 한글 음절 111개를 문자 조각으로 갖고 있어, 그 음절들은 1토큰이 됩니다. 반면 숫자는 GPT-2가 `12` `34`처럼 빈도로 합치고, Llama는 규칙으로 한 자리씩 나눕니다. 두 방식 모두 “모르는 문자 없음”을 보장하는 길은 같고(바이트), 차이는 **바이트를 기본 단위로 쓰느냐, 최후의 수단으로 쓰느냐**입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] GPT-2가 byte-level을 택한 이유(코드 포인트 기본 어휘 13만 개 이상 대 256)와 문자 범주를 넘는 merge를 막은 이유(`dog.` `dog!`)를 원문으로 설명한다.
  - [ ] byte-level BPE와 “문자 BPE + byte fallback”의 차이를 한국어·이모지 예로 비교한다.
  - [ ] 어휘 크기 50,257(GPT-2) · 32,000(Llama 1·2) · 256k(PaLM)를 같은 줄에 놓고, 각 수치의 출처를 말한다.
- **함께 볼 개념 / 원전:** [Byte fallback과 숫자 분리](#c-tok-byte-fallback) · [그 뒤의 흐름](#c-tok-followup) · 원전: Radford et al. 2019 §2.2–2.3

<a id="c-tok-followup"></a>

### 그 뒤의 흐름: Llama 3의 128K 어휘 (논문 밖)

- **무엇인가:** Llama 2 다음 세대인 Llama 3는 SentencePiece 32k 어휘를 버리고 **tiktoken 기반 128K 어휘**로 바꿨습니다.
- **원문:** Llama 2 원문에는 이후 계획이 없습니다. 후속 원전 [Llama 3 Herd of Models §3.2 Model Architecture (arXiv:2407.21783v3, p.7)](https://arxiv.org/pdf/2407.21783v3#page=7)과 Table 3:
  - 어휘 128K(Table 3: 128,000) = **tiktoken tokenizer의 100K** + 비영어 지원을 위한 **추가 28K**.
  - 영어 표본 기준 압축률이 Llama 2 tokenizer 대비 **3.17 → 3.94 문자/토큰**으로 좋아졌다. 같은 학습 연산으로 더 많은 텍스트를 “읽게” 된다.
  - 추가한 비영어 28K는 압축률과 다운스트림 성능을 함께 올렸고, 영어 토큰화에는 영향이 없었다고 적었다.
  - tiktoken의 어느 인코딩(예: cl100k_base)인지는 원문 **미기술**이고, 각주는 tiktoken 저장소 링크만 겁니다. Llama 3 tokenizer는 gated 저장소라 이번에 직접 돌리지 못했습니다.
- **계산해 보면:** 3.94 / 3.17 ≈ 1.24. Meta의 영어 표본에서 같은 문자 수를 약 20% 적은 토큰(1/1.24 ≈ 0.80)으로 표현한다는 뜻입니다. 대신 어휘가 32,000 → 128,000(4배)이 되므로, 임베딩과 출력층 행렬도 같은 폭 기준 4배가 됩니다. 예를 들어 폭 4,096이면 행렬 하나가 32,000×4,096 ≈ 1.31억에서 128,000×4,096 ≈ 5.24억 파라미터가 됩니다(설명용 계산. Llama 3 8B의 폭 4,096은 Table 3 값).
- **설명할 수 있어야 하는 것:**
  - [ ] Llama 3 어휘의 구성(100K tiktoken + 28K 비영어)과 압축률 3.17 → 3.94를, “영어 표본, Llama 2 tokenizer 대비”라는 조건과 함께 말한다.
  - [ ] 어휘를 키우면 시퀀스는 짧아지고 임베딩·출력층은 커지는 교환 관계를 위 계산으로 보인다.
- **함께 볼 개념 / 원전:** [GPT-2 byte-level BPE](#c-tok-gpt2-bytelevel) · [Byte fallback과 숫자 분리](#c-tok-byte-fallback) · 원전: Llama 3 §3.2, Table 3

<a id="c-pos-roadmap"></a>

### 위치 인코딩 로드맵: 위치를 어떻게 넣을까 → 회전 → 얼마나 길게 쓸까

Llama 2 원문이 RoPE에 대해 하는 말은 [§2.2](https://arxiv.org/pdf/2307.09288v2#page=5)의 한 구절뿐입니다. LLaMA 1에서 물려받은 부품 목록에 “rotary positional embeddings (RoPE, Su et al. 2022)”가 들어 있고, 바뀐 점은 [부록 A.2.1](https://arxiv.org/pdf/2307.09288v2#page=47)의 context 2048 → 4096입니다. 이 페이지들은 그 한 구절의 앞뒤를 채웁니다. W01 [RoPE](../w01/llama1-reading-map.html#c-rope) 페이지(적용 위치, Q·K에만 회전)는 반복하지 않습니다.

| 단계 | 방식 | 위치가 들어가는 곳 | 학습 길이 밖에서 | 출처 |
| --- | --- | --- | --- | --- |
| 1. 고정 절대 | [사인파 PE](#c-pos-sinusoid) | 입력 임베딩에 한 번 더함 | 식으로 값은 계산됨. 외삽은 저자 가설 | Vaswani 2017 §3.5 |
| 2. 학습형 절대 | [학습된 위치 표](#c-pos-learned) | 입력 임베딩에 한 번 더함 | 표에 행이 없음 | GPT-1 2018 → GPT-2 → GPT-3 |
| 3. 상대 위치 | [Shaw · T5 · ALiBi](#c-pos-relative) | attention 안(벡터 또는 점수 보정값) | 방식마다 다름(T5는 128 이상을 한 칸으로) | Shaw 2018 · T5 2019 · ALiBi 2021 |
| 4. 회전 | [RoPE](#c-pos-rope) | 매 층 Q·K를 위치 각도만큼 회전 | 각도는 계산되지만 학습 때 못 본 각도 | Su 2021, EleutherAI · PaLM 채택 |
| **Llama 1 → 2** | RoPE 그대로(밑값 10,000, 원문 미기술 · 코드 확인) | 같음 | 학습 길이만 2K → 4K | LLaMA 1 §2.2, Llama 2 §2.2 · A.2.1 |
| 5. 길이 연장(논문 밖) | [PI · 밑값 키우기](#c-pos-followup) | 회전 각도를 줄임 | 32K~128K로 연장 | PI 2023 · Code Llama 2023 · Llama 3 2024 |

- **원문이 한 말:** RoPE를 쓴다는 채택 사실과 인용(Su et al. 2022)뿐입니다. RoPE를 고른 이유, 밑값(base), 적용 차원 비율은 Llama 2 원문에 **미기술**입니다. LLaMA 1 §2.2도 출처를 “[GPTNeo]”로 적고 이유는 적지 않았습니다.
- **이번 주에 깊게 볼 것:** 왜 “더하기”에서 “돌리기”로 왔나(상대 위치를 점수에 깔끔하게 넣는 문제), RoPE 식의 유도, d = 128에서 각 회전 쌍의 파장과 4K context의 관계.
- **담당 파트:** 이번 주는 Background(이정민 · 김민선). 읽기 지도 규칙상 RoPE가 실제로 쓰이는 곳은 Architecture & Pre-training이므로, 본편에서는 [2K → 4K context](#c-context-4k) 페이지와 연결합니다.

<a id="c-pos-sinusoid"></a>

### 사인파 위치 인코딩 (Transformer, 2017)

- **무엇인가:** 위치 pos마다 정해진 사인 · 코사인 값으로 d_model 차원 벡터 PE_pos를 만들어 입력 토큰 임베딩에 **더하는** 방식입니다. 학습하는 파라미터가 없습니다.
- **원문:** Llama 2는 이 방식을 다루지 않습니다. 원전 Vaswani et al. [§3.5](https://arxiv.org/abs/1706.03762v7) — 아래 식, 인코더 · 디코더 맨 아래 입력에 더한다는 점, 이 함수를 고른 이유와 학습형 임베딩 비교를 적습니다.

  PE(pos, 2i) = sin(pos / 10000^(2i/d_model)), PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

  pos는 토큰 위치(0, 1, 2, …), i는 차원 쌍 번호(0 ≤ i < d_model/2), d_model은 임베딩 차원(base 모델 512)입니다. 원문은 파장이 2π부터 10000·2π까지 기하급수로 늘어난다고 적습니다.
- **원문이 밝힌 이유 (저자 가설):** 두 가지입니다. ① 고정된 거리 k에 대해 PE_{pos+k}를 PE_pos의 **선형 함수**로 나타낼 수 있으니 상대 위치로 attend하기 쉬울 것이라는 가설, ② 학습 때보다 긴 시퀀스로 **외삽**할 수 있을지 모른다는 가설. 둘 다 원문 표현이 “hypothesized”, “may allow”로, 실험으로 보인 결과가 아닙니다.
- **실험 결과 (기술됨):** 학습형 위치 임베딩도 시험했고 “거의 같은 결과”였다고 적습니다. [Table 3](https://arxiv.org/abs/1706.03762v7) (E)행 기준, EN→DE newstest2013 dev에서 base(사인파) PPL 4.92 · BLEU 25.8, 학습형 PPL 4.92 · BLEU 25.7. 외삽 가설을 검증한 실험은 원문에 없습니다.
- **왜 그런가:**
  - ①의 선형 관계: 같은 주파수 ω_i = 1/10000^(2i/d_model)의 (sin ωpos, cos ωpos) 쌍은 평면 위의 점이고, pos를 k만큼 옮기면 그 점이 각도 ωk만큼 **회전**합니다. 회전은 pos와 무관한 2×2 행렬이므로 PE_{pos+k} = M_k · PE_pos입니다. → 그런데 이 회전 관계는 PE 벡터 **자체**에만 성립합니다. 입력에 더한 뒤 W_q · W_k 투영을 거치면 점수에는 단어 의미와 절대 위치가 섞인 교차항이 생깁니다([돌려 보면](#c-pos-rope-calc)에서 확인). → RoPE는 바로 이 “회전하면 거리만 남는다”는 성질을 PE가 아니라 **q, k 자체**에 적용한 것이라고 볼 수 있습니다(추출자 해석).
- **설명할 수 있어야 하는 것:**
  - [ ] PE 식의 pos · i · d_model이 각각 무엇이고, 낮은 차원은 빨리 · 높은 차원은 천천히 돈다는 점을 말한다.
  - [ ] “상대 위치 학습이 쉬울 것”, “외삽 가능할 것”은 저자 가설이고, 실제 실험 결과는 학습형과 거의 같았다(Table 3 (E), BLEU 25.8 대 25.7)는 점을 구분한다.
  - [ ] PE_{pos+k}가 PE_pos의 회전(선형 변환)이라는 점이 RoPE의 아이디어와 어떻게 이어지는지 말한다.
- **함께 볼 개념 / 원전:** [학습된 위치 표](#c-pos-learned) · [RoPE](#c-pos-rope) · 원전: Attention Is All You Need [arXiv:1706.03762](https://arxiv.org/abs/1706.03762v7) §3.5, Table 3 (E)

<a id="c-pos-learned"></a>

### 학습형 절대 위치 임베딩 (GPT-1 → GPT-2 → GPT-3)

- **무엇인가:** 위치마다 벡터 하나를 파라미터로 두고(행 = 위치, 열 = d_model인 표 W_p) 학습하는 방식입니다. 입력은 토큰 임베딩 + 그 위치의 행입니다. 표의 행 수가 곧 최대 길이입니다.
- **원문:** Llama 2 · LLaMA 1은 이 방식을 “absolute positional embeddings를 제거했다”(LLaMA 1 §2.2)는 형태로만 언급합니다. 원전 확인:

| 모델 | 원문에 적힌 위치 처리 | 학습 길이 | 출처 |
| --- | --- | --- | --- |
| GPT-1 (2018) | “learned position embeddings instead of the sinusoidal version”, 식 h₀ = UW_e + W_p | 연속 512 토큰 | [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) §3.1 식 (2), §4.1 Model specifications |
| GPT-2 (2019) | 위치 처리 언급 없음. GPT-1을 “largely follows”하며 바뀐 점 목록에도 위치 없음 | 512 → 1024 | [GPT-2](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) §2.3 |
| GPT-3 (2020) | “same model and architecture as GPT-2”(예외는 sparse attention 교대) | n_ctx = 2048 | [GPT-3](https://arxiv.org/pdf/2005.14165v4#page=8) §2.1 |

  GPT-2 · GPT-3 논문은 학습형 위치 임베딩을 직접 적지 않습니다. GPT-2는 공개 코드에서 확인됩니다: [openai/gpt-2 model.py](https://github.com/openai/gpt-2/blob/master/src/model.py)의 `wpe = [n_ctx, n_embd]` 변수(기본 n_ctx = 1024)를 `h = wte[X] + wpe[positions]`로 더합니다. GPT-3는 “GPT-2와 같은 구조”라는 문장에서 이어받은 것으로 **추론**한 것이며, GPT-3 원문이 명시하지는 않습니다.
- **왜 그런가:**
  - 학습 길이 밖을 다룰 수 없다: 표는 0 ~ n_ctx−1 행만 있습니다. → 1024번째 위치를 넣으려 하면 찾을 행이 없습니다(아래 돌려 보면). → 길이를 늘리려면 표를 키우고 새 행을 다시 학습해야 하며, 사인파처럼 “식으로 계산해 두기”가 불가능합니다.
  - 그래도 GPT-1이 학습형을 고른 이유는 원문 **미기술**입니다. Transformer Table 3 (E)에서 두 방식 성능이 거의 같았다는 점은 함께 말할 수 있습니다.
  - 절대 위치라는 점은 사인파와 같습니다. 두 방식 모두 입력에서 **한 번** 더하므로, 점수 q·k에 들어가는 위치 정보는 층마다 투영 W_q · W_k를 거친 혼합항입니다(추출자 설명).
- **돌려 보면:** GPT-2 small과 같은 크기의 표를 numpy로 만들어 조회했습니다(값은 난수, 모양만 같음).

  ```
  wpe shape: (1024, 768) -> row 1023 ok: (768,)
  row 1024: IndexError index 1024 is out of bounds for axis 0 with size 1024
  ```
- **설명할 수 있어야 하는 것:**
  - [ ] GPT-1 · 2 · 3의 학습 길이 512 → 1024 → 2048과, GPT-2 · 3 논문은 위치 방식을 직접 적지 않았다(코드 · “같은 구조” 문장으로 확인)는 점을 말한다.
  - [ ] 학습형 표는 최대 길이 밖에 행 자체가 없어서 외삽이 불가능하다는 점을, 사인파(값은 계산됨)와 대비해 말한다.
  - [ ] LLaMA 1이 “absolute positional embeddings를 제거”했다는 문장이 무엇을 없앤 것인지(GPT-3식 입력 더하기) 말한다.
- **함께 볼 개념 / 원전:** [사인파 PE](#c-pos-sinusoid) · [상대 위치 방식](#c-pos-relative) · 원전: GPT-1 §4.1, GPT-2 §2.3, GPT-3 §2.1

<a id="c-pos-relative"></a>

### 상대 위치 방식: Shaw · T5 · ALiBi

- **무엇인가:** “몇 번째 자리인가” 대신 “query와 key가 얼마나 떨어져 있나”(거리 m − n, m은 query 위치, n은 key 위치)를 attention 안에 넣는 방식들입니다. 입력에 위치 벡터를 더하지 않습니다.
- **원문:** Llama 2는 이 방식들을 인용하지 않습니다(참고문헌에 Shaw · T5 상대 위치 · ALiBi 없음, 로컬 텍스트 검색). 원전 확인:

| 방식 | 무엇을 넣나 | 확인한 수치 · 설정 | 출처 |
| --- | --- | --- | --- |
| Shaw et al. 2018 | 거리마다 학습하는 벡터 표현을 self-attention에 넣음 | WMT14에서 절대 위치 대비 EN-DE +1.3 BLEU, EN-FR +0.3 BLEU. 상대 + 절대 결합은 추가 향상 없음 | [arXiv:1803.02155](https://arxiv.org/abs/1803.02155) 초록 |
| T5 (Raffel 2019) | 거리 구간(bucket)마다 학습하는 **스칼라** 하나를 attention logit에 더함. 층끼리 공유, head마다 다름 | bucket 32개, 구간 폭은 로그로 커지며 offset 128 이상은 모두 같은 bucket | [arXiv:1910.10683](https://arxiv.org/abs/1910.10683v4) §2.1 |
| ALiBi (Press 2021) | 학습 없는 고정 벌점: 거리에 비례한 값을 q·k 점수에서 뺌. head마다 기울기 m이 다름(8 head면 1/2¹ … 1/2⁸) | 1.3B 모델을 길이 1024로 학습해 2048에서 평가하면, 2048로 학습한 사인파 모델과 같은 perplexity, 학습 11% 빠르고 메모리 11% 적음 | [arXiv:2108.12409](https://arxiv.org/abs/2108.12409v2) 초록 · §3 |

- **왜 그런가:**
  - 상대 거리가 중요하다는 직관: 언어에서 “바로 앞 단어”, “세 단어 전”은 문장이 어디서 시작하든 같은 관계입니다. → 절대 위치 방식에서는 (3, 1)과 (103, 101) 쌍을 모델이 따로 배워야 합니다. → 상대 방식은 둘을 같은 입력(거리 2)으로 만들어 처음부터 공유합니다(추출자 설명).
  - 그 대가: Shaw · T5는 거리별 표현을 attention 계산에 따로 더해야 합니다. T5는 이를 스칼라 bias 하나로 줄였고, ALiBi는 학습조차 없애 외삽에 초점을 맞췄습니다. RoPE는 별도 항을 더하지 않고 q, k를 돌리는 것만으로 같은 목적을 이룹니다([RoPE](#c-pos-rope)).
  - ALiBi 논문 §2.2는 rotary를 직접 평가해, L = 512(1024)로 학습한 모델이 약 200(100) 토큰 더 긴 입력까지만 perplexity가 나아지고 그 뒤로는 나빠진다고 적습니다(Figure 1: rotary · 사인파 · T5 모두 긴 길이에서 악화, ALiBi는 아님). 이것이 [길이 연장 방법](#c-pos-followup)이 따로 필요해진 배경입니다.
- **돌려 보면:** T5의 bucket 함수를 HF transformers v4.44.0 `_relative_position_bucket` 코드 그대로 파이썬으로 옮겨 돌렸습니다(인코더 양방향, bucket 32, max_distance 128). 양방향이면 32개를 방향마다 16개로 나누고, 그중 절반(0–7)은 거리 그대로, 나머지는 로그 구간입니다.

  ```
  rel=  1 -> 17 | rel= -1 -> 1      rel= 31 -> 27 | rel= -31 -> 11
  rel=  7 -> 23 | rel= -7 -> 7      rel= 63 -> 29 | rel= -63 -> 13
  rel=  8 -> 24 | rel= -8 -> 8      rel=127 -> 31 | rel=-127 -> 15
  rel= 11 -> 24 (8–11이 한 칸)      rel=128, 1000, 4000 -> 31 (모두 같은 칸)
  decoder(단방향) rel=-1, -100, -127, -128, -5000 -> [1, 30, 31, 31, 31]
  ```
  거리 128과 4000이 같은 값을 받으므로, T5식 bias는 먼 거리를 서로 구분하지 않습니다. 논문의 “32 embeddings, 로그로 128까지” 설명과 일치합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Shaw(거리별 벡터) · T5(거리 bucket별 스칼라 bias) · ALiBi(학습 없는 거리 비례 벌점)가 각각 무엇을 attention에 넣는지 한 줄씩 말한다.
  - [ ] T5 bucket에서 128 이상의 거리가 모두 같은 bucket이 된다는 점을 계산 결과로 보인다.
  - [ ] ALiBi 원문의 외삽 결과(1024 학습 → 2048 평가)를 설정과 함께 말하고, 같은 논문이 rotary의 외삽은 제한적이라고 측정했다는 점을 말한다.
- **함께 볼 개념 / 원전:** [RoPE](#c-pos-rope) · [길이 연장](#c-pos-followup) · 원전: Shaw 2018, T5 §2.1, ALiBi §2–3

<a id="c-pos-rope"></a>

### RoPE: 상대 위치를 회전으로 넣는다 (RoFormer, 2021)

- **무엇인가:** 매 층 attention에서 query q와 key k를 두 차원씩 짝지어, 위치 m에 비례한 각도 mθ_i만큼 회전시킨 뒤 내적하는 방식입니다. 회전한 q_m과 k_n의 내적이 m − n에만 의존하게 됩니다.
- **원문:** Llama 2 [§2.2](https://arxiv.org/pdf/2307.09288v2#page=5) — 채택 사실과 인용(“Su et al. 2022”)만 있습니다. LLaMA 1 [§2.2](https://arxiv.org/pdf/2302.13971v1#page=3) — 절대 위치 임베딩을 없애고 각 layer에 RoPE를 추가, 출처 표기 [GPTNeo]. 원전 RoFormer [arXiv:2104.09864v5](https://arxiv.org/abs/2104.09864v5):
  - **§3.1 목표:** f_q(x_m, m)과 f_k(x_n, n)의 내적이 g(x_m, x_n, m − n), 즉 단어 임베딩 x_m · x_n과 거리 m − n만의 함수가 되게 하자(식 11). x_m은 위치 m 토큰의 임베딩, f_q · f_k는 위치를 넣어 q, k를 만드는 함수입니다.
  - **§3.2.1 2차원:** f_q(x_m, m) = (W_q x_m)·e^{imθ}, f_k(x_n, n) = (W_k x_n)·e^{inθ}로 두면 내적은 Re[(W_q x_m)(W_k x_n)* e^{i(m−n)θ}]이 됩니다(식 12–13). 2차원 벡터를 복소수 하나로 보고 e^{imθ}를 곱하는 것이 각도 mθ 회전입니다.
  - **§3.2.2 일반형:** d차원을 d/2개 쌍으로 나눠 쌍 i마다 다른 각속도 θ_i = 10000^(−2(i−1)/d), i = 1, …, d/2로 회전하는 블록 대각 회전 행렬 R^d_{Θ,m}을 곱합니다(식 14–15). 식 14는 f_{q,k}만 정의하고 value는 다루지 않습니다. (§3.3은 같은 θ를 10000^(−2i/d)로 다시 적어 첨자가 하나 어긋나 있습니다.)
  - **§3.3 성질:** 거리가 커질수록 내적이 감소하는 long-term decay, linear attention과 결합 가능. 초록은 “sequence length의 유연성”도 성질로 듭니다. **decay는 §3.4.3에서 Abel 합으로 상한을 잡고 그 상한의 평균이 줄어드는 것을 그림 2로 보인 것**이라, 닫힌 형태의 증명은 아닙니다.
  - **§3.4.2:** 행렬 곱 대신 x ⊙ cos + (쌍을 바꾸고 부호를 뒤집은 x) ⊙ sin의 원소별 연산으로 구현합니다(식 34).
- **왜 그런가:**
  - 왜 회전하면 거리만 남나: 위치 m에서 q를 R(mθ)로, 위치 n에서 k를 R(nθ)로 돌리면 점수는 (R(mθ)q)ᵀ(R(nθ)k) = qᵀ R(mθ)ᵀR(nθ) k입니다. → 회전 행렬은 직교 행렬이라 R(mθ)ᵀ = R(−mθ)이고, 회전끼리 곱하면 각도가 더해집니다. → 그래서 R(−mθ)R(nθ) = R((n−m)θ), 위치가 차이 하나로만 남습니다. 더하기 방식에서 생기던 “의미 × 절대 위치” 교차항이 처음부터 없습니다([돌려 보면](#c-pos-rope-calc)).
  - 왜 매 층인가: 점수 q·k는 층마다 새로 계산됩니다. → 입력에서 한 번 더한 위치는 여러 층을 지나며 다른 정보와 섞입니다. → RoPE는 각 층의 q, k에 직접 회전을 걸어, 그 층의 점수에 거리를 다시 넣습니다(LLaMA 1 §2.2 “at each layer”, Meta 코드 `apply_rotary_emb(xq, xk)` 확인).
  - 왜 V는 돌리지 않나: RoFormer는 f_q, f_k만 정의할 뿐 V를 뺀 이유는 따로 적지 않습니다(확인 범위 내 미기술). 위치는 “누구를 볼지”(점수)에만 필요하고, V까지 돌리면 가져오는 내용 자체가 key의 절대 위치에 따라 바뀐다는 것이 추출자 설명입니다.
  - 왜 쌍마다 속도가 다른가: 빠른 쌍(θ₁ = 1 rad/토큰)은 6.28 토큰마다 한 바퀴라 가까운 거리를 세밀하게 구분하지만 먼 거리에서는 같은 각도가 반복됩니다. → 느린 쌍은 먼 거리를 구분합니다. → 사인파 PE와 같은 기하급수 주파수(밑값 10000)를 써서 여러 눈금을 동시에 가집니다.
- **누가 먼저 썼나 (원문이 말한 이유와 함께):**

| 채택 | 시점 | 원문이 밝힌 이유 · 설정 | 출처 |
| --- | --- | --- | --- |
| EleutherAI (GPT-Neo · GPT-NeoX · Mesh Transformer JAX 코드) | 2021.04.20 블로그 (RoFormer v1과 같은 날) | 125M급 OWT2에서 val loss 2.759(학습형 절대 2.809, T5 RPE 2.801), 1.4B급 Pile 8k step에서 2.173(2.240, 2.223), 학습형 대비 수렴 약 30% 빠름 | [EleutherAI 블로그](https://blog.eleuther.ai/rotary-embeddings/) (2차 성격: 논문 아님) |
| GPT-NeoX-20B | 2022.04 | GPT 계열의 학습형 위치 대신 rotary, 이유는 “positive prior experiences”. 차원의 처음 25%에만 적용(Wang & Komatsuzaki 2021, 즉 GPT-J를 따름) | [arXiv:2204.06745](https://arxiv.org/abs/2204.06745) §2.1.1 |
| PaLM | 2022.04 | 절대 · 상대 위치 대신 RoPE, “긴 시퀀스에서 성능이 좋다고 알려져서”(PaLM 자체 ablation 아님). 학습 길이 2048 | [arXiv:2204.02311](https://arxiv.org/pdf/2204.02311v5#page=5) §2, §5 |
| LLaMA 1 → Llama 2 | 2023.02 / 2023.07 | 이유 미기술. Meta 공개 코드는 head 차원 전체(dim // n_heads)에 θ 밑값 10,000으로 적용 | [meta-llama/llama model.py](https://github.com/meta-llama/llama/blob/main/llama/model.py) |

- **설명할 수 있어야 하는 것:**
  - [ ] RoFormer §3.1의 목표(내적이 x_m, x_n, m − n만의 함수)를 말하고, R(mθ)ᵀR(nθ) = R((n−m)θ)로 왜 그 목표가 이뤄지는지 두 줄로 보인다.
  - [ ] θ_i = 10000^(−2(i−1)/d)의 d · i가 무엇인지, 사인파 PE의 주파수와 같은 꼴이라는 점을 말한다.
  - [ ] long-term decay는 상한과 그림으로 보인 성질이고, ALiBi 논문 측정상 RoPE의 외삽은 제한적이라는 점을 구분한다.
  - [ ] EleutherAI · GPT-NeoX · PaLM이 밝힌 채택 이유와, LLaMA · Llama 2는 이유를 적지 않았다는 점을 구분한다.
- **함께 볼 개념 / 원전:** [돌려 보면](#c-pos-rope-calc) · [사인파 PE](#c-pos-sinusoid) · W01 [RoPE](../w01/llama1-reading-map.html#c-rope) · 원전: RoFormer §3.1–3.4

<a id="c-pos-rope-calc"></a>

### RoPE 돌려 보기: 거리만 남는지, d = 128의 파장과 4K

- **무엇인가:** RoPE와 사인파 더하기 방식을 같은 난수 벡터로 비교하고, Llama의 head 차원 d = 128에서 64개 회전 쌍의 파장을 계산한 결과입니다. 모든 벡터 · 행렬은 난수(시드 0)라 값 자체는 **설명용**이고, 같다/다르다만 의미가 있습니다.
- **원문:** Llama 2 원문은 head 차원과 밑값을 적지 않습니다. head 차원 128은 LLaMA 1 [Table 2](https://arxiv.org/pdf/2302.13971v1#page=3)의 dim ÷ n heads(4096/32, 5120/40, 6656/52, 8192/64 모두 128)와 Meta 코드의 `dim // n_heads`에서, 밑값 10,000은 Meta 코드의 `theta: float = 10000.0`에서 확인했습니다. Llama 2 context 4096은 [A.2.1](https://arxiv.org/pdf/2307.09288v2#page=47).
- **돌려 보면 (a) 거리 2인 네 쌍:** q₀ = W_q x_q, k₀ = W_k x_k(x는 난수 128차원, W는 128×128 난수 ÷ √128).

  ```
  RoPE: rope(q0, m) . rope(k0, n)
    (3,1)=5.201628  (103,101)=5.201628  (1003,1001)=5.201628  (4001,3999)=5.201628
  더하기: Wq(x_q+PE_m) . Wk(x_k+PE_n)
    (3,1)=-8.543014  (103,101)=-5.923206  (1003,1001)=7.764539  (4001,3999)=-7.913772
  ```
  RoPE는 소수 여섯째 자리까지 같고, 더하기 방식은 부호까지 바뀝니다. 회전은 길이를 바꾸지 않습니다(|q₀| = 10.584949 = |rope(q₀, 103)|).
- **돌려 보면 (a′) 더하기 방식은 어디서 깨지나:** W = I로 두고 점수를 네 항으로 나눴습니다.

  ```
  (3,1):     x.x=0.3463  x_q.PE_n= 7.4237  PE_m.x_k=-3.8420  PE_m.PE_n=57.3819
  (103,101): x.x=0.3463  x_q.PE_n= 2.2756  PE_m.x_k= 0.3358  PE_m.PE_n=57.3819
  PE_m.PE_n (W=I), 네 쌍 모두: 57.381861
  (Wq PE_m).(Wk PE_n), 난수 W: -2.235195, 0.68846, -5.630389, 0.812132
  ```
  위치끼리의 항 PE_m · PE_n은 W가 없으면 거리만의 함수입니다(사인파의 회전 성질). 바뀌는 것은 “의미 × 절대 위치” 교차항 둘이고, W_q · W_k가 끼면 위치끼리의 항마저 거리만의 함수가 아니게 됩니다. RoPE는 이 네 항 분해 자체가 생기지 않습니다.
- **돌려 보면 (b) 파장 λ_i = 2π / θ_i, d = 128:**

| 밑값 | 가장 짧은 λ (i=1) | 가장 긴 λ (i=64) | λ > 2048인 쌍 | λ > 4096인 쌍 | 위치 4096에서 가장 느린 쌍의 회전 |
| --- | --- | --- | --- | --- | --- |
| 10,000 (LLaMA 1 · 2) | 6.2832 | 54,410.1 | 23 / 64 | 18 / 64 | 0.4730 rad (0.0753바퀴) |
| 500,000 (Llama 3) | 6.2832 | 2,559,195.5 | 35 / 64 | 32 / 64 | 0.0101 rad |
| 1,000,000 (Code Llama) | 6.2832 | 5,063,255.8 | 37 / 64 | 33 / 64 | 0.0051 rad |

  밑값 10,000에서 처음 네 쌍의 파장은 6.283 · 7.256 · 8.379 · 9.676 토큰, 마지막 네 쌍은 35,332.9 · 40,801.9 · 47,117.2 · 54,410.1 토큰입니다. 4096을 처음 넘는 쌍은 i = 47(λ = 4,711.7, 바로 앞 i = 46은 4,080.2)입니다.
  - **읽는 법 (추출자 해석):** Llama 2의 4K context 안에서 64쌍 중 46쌍은 한 바퀴 이상 돌고, 18쌍은 한 바퀴도 돌지 못합니다. 가장 느린 쌍은 4096 토큰을 지나도 0.47 rad(약 27°)만 돕니다. 이 느린 쌍들은 학습 중 볼 수 있는 각도 범위가 좁아서, 학습 길이를 넘으면 처음 보는 각도가 나옵니다. 2K → 4K로 늘리면 λ > 학습 길이인 쌍이 23개에서 18개로 줄어드는 것도 같은 이야기입니다. [길이 연장](#c-pos-followup) 방법들은 바로 이 각도 범위를 다룹니다.
- **돌려 보면 (c) long-term decay (설명용, q = k = 모두 1):** 점수 = Σ_i 2cos(rθ_i), r은 거리.

  ```
  r=0: 128.000  r=1: 124.187  r=10: 85.640  r=100: 61.087  r=1000: 20.355  r=4096: -6.765
  RoFormer식 상한 평균 mean|S_j|: r=1: 31.538  r=10: 17.954  r=100: 10.227  r=1000: 4.471  r=4096: 4.883
  ```
  전체적으로 줄지만 단조 감소는 아닙니다(r = 4096에서 상한 평균이 r = 1000보다 약간 큼). RoFormer가 그림으로 보인 “평균적으로 감소”와 같은 모습이고, 실제 학습된 q, k에서도 그런지는 이 계산으로 알 수 없습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] (3, 1)과 (103, 101)에서 RoPE 점수가 같고(5.201628) 더하기 방식은 다른(−8.54 대 −5.92) 이유를, 네 항 분해의 교차항으로 설명한다.
  - [ ] d = 128, 밑값 10,000에서 파장이 6.28 ~ 54,410 토큰이고, 4096 context에서 18쌍은 한 바퀴를 못 돈다는 점을 말한다.
  - [ ] head 차원 128과 밑값 10,000은 Llama 2 원문이 아니라 LLaMA 1 Table 2와 공개 코드에서 확인한 값이라는 점을 구분한다.
- **함께 볼 개념 / 원전:** [RoPE](#c-pos-rope) · [길이 연장](#c-pos-followup) · 스크립트: `scratchpad/rope/rope_demo.py`, 출력 `rope_demo_output.txt`

<a id="c-pos-followup"></a>

### 그 뒤의 흐름 (논문 밖): 위치 보간과 밑값 키우기

- **무엇인가:** RoPE 모델을 학습 길이보다 길게 쓰기 위해, 회전 각도를 학습 때 본 범위 안으로 되돌리는 방법들입니다. 위치 번호를 줄이는 방법(Position Interpolation)과 밑값을 키워 모든 쌍을 느리게 하는 방법(Code Llama · Llama 3)이 대표적입니다.
- **원문:** Llama 2 원문은 4K로 **처음부터 사전학습**했고(Table 16: 2K · 4K 모두 150B 토큰, context만 다르게), 위치 보간이나 밑값 변경은 언급하지 않습니다. 참고문헌에도 PI가 없습니다(로컬 텍스트 검색).

| 방법 | 무엇을 바꾸나 | 확인한 결과 · 설정 | 출처 |
| --- | --- | --- | --- |
| Position Interpolation (Chen et al., 2023.06) | 위치 번호를 선형으로 줄임: f′(x, m) = f(x, mL/L′), L = 원래 길이, L′ = 늘린 길이 | LLaMA 7B · 13B · 33B · 65B를 최대 32,768까지, 1000 step 이내 미세조정. 보간의 상한이 외삽보다 최소 약 600배 작다(저자 이론 결과). 그냥 외삽하면 perplexity가 10³ 넘게 치솟을 수 있다고 §2.2에 적음 | [arXiv:2306.15595](https://arxiv.org/abs/2306.15595v2) 초록 · §2.3 · §3.1 |
| Code Llama (2023.08) | 밑값 θ를 10,000 → 1,000,000 | Llama 2의 4,096 대신 16,384 토큰 시퀀스로 미세조정, 최대 100,000 토큰까지 안정적 외삽을 보고 | [arXiv:2308.12950](https://arxiv.org/abs/2308.12950) §2.4 |
| Llama 2 Long (Xiong et al., 2023.09) | Llama 2에서 더 긴 시퀀스로 continual pretraining, 위치 인코딩의 한계를 분석 | 유효 context 최대 32,768 | [arXiv:2309.16039](https://arxiv.org/abs/2309.16039) 초록 (밑값 수치는 본문 미확인) |
| Llama 3 (2024.07) | RoPE 밑값 500,000. Xiong et al.을 근거로 듦 | Table 3: 8B · 70B · 405B 모두 “RoPE (θ = 500,000)”. 8K에서 시작해 6단계로 128K까지, 약 800B 토큰 | [arXiv:2407.21783](https://arxiv.org/abs/2407.21783v3) §3.2 · Table 3 · §3.4.2 |

- **왜 그런가:**
  - PI가 외삽보다 안정적인 이유: 학습 길이 L = 2048 모델을 L′ = 8192로 쓸 때, 가장 느린 쌍의 각도는 위치 8191에서 외삽하면 0.9459 rad로 학습 때 최대(위치 2047, 0.2364 rad)의 4배입니다. → PI로 위치를 1/4로 줄이면 0.2365 rad로 학습 범위 안에 들어옵니다(직접 계산, θ₆₄ = 1.155×10⁻⁴). → 대신 가장 빠른 쌍의 이웃 토큰 간 각도 차도 1.0 → 0.25 rad로 줄어 가까운 거리 구분이 무뎌지므로 짧은 미세조정이 필요합니다(추출자 해석).
  - 밑값을 키우는 이유: θ_i = base^(−2(i−1)/d)에서 base를 키우면 i = 1(θ = 1)은 그대로 두고 높은 i의 쌍만 크게 느려집니다. → 위 표처럼 밑값 500,000이면 λ > 4096인 쌍이 18 → 32개로, 1,000,000이면 33개로 늘어 긴 위치에서도 회전 각도가 작게 유지됩니다. → PI와 달리 빠른 쌍의 해상도는 건드리지 않습니다. Code Llama 원문도 “주파수를 선형으로 줄이는 대신 밑값을 바꾼다”는 대비로 설명합니다.
  - 이 스터디의 다른 주차: Llama 3 계열과 긴 context는 이후 주차 커리큘럼에서 다시 나오면 그 주차에 연결합니다(현재 `docs/background/` 주차별 매핑은 미확인).
- **설명할 수 있어야 하는 것:**
  - [ ] Llama 2는 4K를 처음부터 학습했고 PI · 밑값 변경은 원문에 없다는 점, 이후 방법들은 논문 밖이라는 점을 구분한다.
  - [ ] PI(위치 번호 축소)와 밑값 키우기(높은 쌍만 느리게)가 각각 회전 각도를 어떻게 줄이는지 계산 예로 말한다.
  - [ ] 밑값 10,000 → 1,000,000(Code Llama, 16K 미세조정) → 500,000(Llama 3, 128K까지 6단계)의 수치를 설정과 함께 말한다.
- **함께 볼 개념 / 원전:** [돌려 보면](#c-pos-rope-calc) · [2K → 4K context](#c-context-4k) · 원전: PI §2–3, Code Llama §2.4, Llama 3 §3.2 · §3.4.2

<!-- part: common -->
## 검토 기록

<a id="unassigned-scope"></a>

### 배정 밖 원문

이번 배정에 들어가지 않은 원문입니다. 이전 판 읽기 지도([4538204](https://github.com/Pseudo-Lab/llm-technical-report-study/blob/4538204/docs/weeks/w02/llama2-reading-map.md))에 아래 주제의 개념 페이지가 있습니다. 담당을 정하면 해당 파트로 옮깁니다.

| 원문 | 다루는 내용 | 이전 판의 페이지 |
| --- | --- | --- |
| [§2.1 Pretraining Data](https://arxiv.org/pdf/2307.09288v2#page=5) | 새 데이터 혼합 · 개인정보 사이트 제거 · factual up-sampling · 2T | Data 파트의 [맥락 페이지](#c-pretrain-corpus)로만 포함 |
| [§2.2 Tokenizer](https://arxiv.org/pdf/2307.09288v2#page=6) | 같은 tokenizer · 숫자 분리 · byte fallback · 32k | Background가 담당 |
| [§4.1 Safety in Pretraining](https://arxiv.org/pdf/2307.09288v2#page=20) | 인구 집단 표현(Table 9) · 독성 비율 · 안전 벤치마크(TruthfulQA · ToxiGen · BOLD, Table 11) | 인구 집단 표현 · 안전 벤치마크. 언어 분포와 독성 필터링 결정은 Data에 포함 |
| [§4.2 Safety Fine-Tuning](https://arxiv.org/pdf/2307.09288v2#page=23) | 적대적 prompt 설계 · 안전 SFT · 안전 RLHF와 데이터 양(Fig. 14–15) · false refusal · 안전 context distillation(Table 13 · Fig. 16) | 적대적 prompt · 안전 RLHF · false refusal · context distillation · targeted distillation |
| [§4.3 Red Teaming](https://arxiv.org/pdf/2307.09288v2#page=28) | 350명 이상 · 견고성 γ 1.8 → 0.45 | red teaming |
| [§4.4 Safety Evaluation](https://arxiv.org/pdf/2307.09288v2#page=29) | 약 2,000 적대적 prompt · 5점 척도 · 위반 비율 | 안전 사람 평가 |
| [§5 Discussion](https://arxiv.org/pdf/2307.09288v2#page=32) | 사람 감독을 넘어서 · temperature · 시간 인식 · 도구 사용 · 한계 · 공개 전략 | 사람 감독을 넘어서 · 관찰 · 한계와 공개 전략 |
| [App. A.6 Dataset Contamination](https://arxiv.org/pdf/2307.09288v2#page=75) | 10토큰 넘는 n-gram 기반 오염 판정 | Architecture에 (선택)으로 포함 |

- **W01에서 넘겼지만 이번에 담당이 없는 주제:** 스케일링 법칙의 유도(Kaplan · Chinchilla · 6ND). W01 대본은 W02 Background에서 보겠다고 했지만 이번 배정에는 tokenizer와 RoPE만 들어갔습니다. Llama 2는 2T를 고른 이유를 “good performance–cost trade-off” 한 문장으로만 적으므로, Architecture의 [2T 토큰에서도 포화되지 않은 loss](#c-loss-curve)에서 결론만 다시 씁니다.

<a id="memo-data"></a>

### 검증 메모: Data 품질 필터

- **보고서:** Llama 2: Open Foundation and Fine-Tuned Chat Models, arXiv:2307.09288**v2**. 저장소의 `.local/llama2-paper/` 페이지 텍스트(page-05 · 20 · 21 · 22 · 38 · 75)를 직접 읽었습니다. LLaMA 1은 `.local/llama1-paper/page-01 · 02 · 16.txt`(arXiv:2302.13971v1).
- **직접 연 원전 (PDF를 내려받아 텍스트로 읽음):**
  - CCNet arXiv:1911.00359**v2** 전체(§1–§6, Table 1–2, 부록 표 일부)
  - fastText Bag of Tricks arXiv:1607.01759**v3** §1–§3.2
  - GPT-3 arXiv:2005.14165**v4** Appendix A · C 첫 부분(p.43–44)
  - KenLM Heafield 2011 (ACL Anthology W11-2123), Heafield et al. 2013 (P13-2121) 초록 · 서론 · 결론
  - Llama 3 arXiv:2407.21783**v3** §3.1–§3.1.3 (p.4–6)
  - DCLM arXiv:2406.11794**v4** Fig. 4 · §4.4 · Table 4–5 · App. B · J · N 일부
  - FineWeb arXiv:2406.17557**v2** §2 · §3.3 · §4 · §4.2
  - Gururangan et al. 2022 arXiv:2201.10474 초록 · §3.2 · §4.2 · Dodge et al. 2021 arXiv:2104.08758 초록 · §5.3
  - 웹 문서: fasttext.cc 언어 식별 페이지 · supervised 옵션 페이지
  - 코드: `facebookresearch/cc_net` main(마지막 커밋 2020-12-09)의 `mine.py` · `perplexity.py` · `dedup.py` · `data/cutoff.csv` · `Makefile`, `togethercomputer/RedPajama-Data` **rp_v1** 브랜치의 `data_prep/cc/README.md` · `classifier/create_corpus.py` · `classifier/classify.py` · `filter/cc_classifier.sh`
- **직접 돌린 것** (스크래치패드 `quality/scripts/`, Python 3.9.6 venv, fasttext-wheel 0.9.2, kenlm 0.3.0(파이썬 조회 모듈, `lmplz` 없음), NumPy 2.0.2):
  - `lid_demo.py` — 공식 `lid.176.ftz`(938,013바이트, sha256 `8f3472cfe8738a7b6099e8e999c3cbfae0dcd15696aac7d7738a8039db603e83`)로 10개 입력의 언어 점수
  - `kn_lm.py` — 순수 파이썬 3-gram 보간 KN(D=0.75) → ARPA → `kenlm.Model`로 같은 PPL이 나오는지 대조(6문장 모두 일치)
  - `doc_buckets.py` — cc_net 문서 PPL 식과 3등분
  - `toy_classifier.py` — 순수 파이썬 fastText식 분류기 · `ft_supervised.py` — 실제 fastText supervised 3가지 설정
  - `gpt3_pareto.py` — Pareto 유지 확률의 이론값과 100만 표본 시뮬레이션 · `table10_sum.py` — Table 10 합계
  - 모든 학습 문장은 직접 쓴 설명용 문장이고, Wikipedia나 실제 웹 페이지를 옮기지 않았습니다.
- **확인하지 못한 것 · 남은 불확실성:**
  - LLaMA 1이 cc_net 기본값(0.5 · 30/60 백분위 · min_len 300)을 그대로 썼는지, 어느 bucket을 썼는지, 참조 분류기가 fastText였는지: LLaMA 1 원문 **미기술**. 확인할 방법이 없습니다.
  - Llama 2의 정제 단계 전체: **미기술**. Llama 2 언어 식별에 쓴 모델 파일(lid.176.bin / .ftz)과 입력 단위(문서 전체 / 줄)도 미기술.
  - `cutoff.csv`의 백분위가 문서 수 기준인지 문자 수 기준인지 코드에서 확인하지 않았습니다. 기준값을 만든 스냅숏도 확인하지 않았습니다.
  - CCNet Makefile의 `get_wiki_cirrus.py opening`이 Wikipedia 문서의 어느 부분(도입부만인지)을 쓰는지 스크립트를 열어 보지 않았습니다.
  - RedPajama `create_corpus.py`의 digest 중복 검사 버그는 코드를 읽고 내린 해석이며 실행해 확인하지 않았습니다.
  - Heafield 2011 본문의 벤치마크 표 세부 수치는 옮기지 않았습니다(초록 수치만 사용).
  - DCLM의 OH-2.5+ELI5 결과가 LLaMA 1식 “Wikipedia가 인용한 페이지” 양성과 비교한 것은 아닙니다. 그 비교를 한 공개 실험은 찾지 못했습니다.
- **사람 검토:** **미검토** · 검토자 · 일시 미지정

<a id="memo-tokenizer"></a>

### 검증 메모: Tokenizer

- **직접 연 원전(PDF 텍스트 추출 후 해당 절 읽음):** Llama 2 p.6 Tokenizer 문단(로컬 `.local/llama2-paper/page-06.txt`, §2.2 Training Details 안의 문단이며 별도 절 번호 없음) · LLaMA 1 §2.1 Tokenizer(로컬 page-02, PaLM 인용 없음 확인) · Sennrich et al. arXiv:1508.07909**v5** §3.2, Algorithm 1, Figure 1, 각주 3 · Kudo & Richardson arXiv:1808.06226v1 §1, §2, §3.1–3.4 (byte fallback 언급 없음 확인) · GPT-2 논문 §2.2–2.3 · PaLM arXiv:2204.02311v5 §2 Vocabulary(p.6) · Llama 3 arXiv:2407.21783v3 §3.2, Table 3(p.7).
- **라이브러리 문서:** google/sentencepiece master(`bcd4d8c`)의 `doc/options.md`, `src/sentencepiece_model.proto`, v0.1.9 릴리스 노트(gh api) · openai/gpt-2 `src/encoder.py` 정규식.
- **돌린 것(scratchpad `bpe/`, venv에 sentencepiece 0.2.2 · tokenizers · pypdf 설치, 전역 설치 없음):**
  - `scripts/sennrich_alg1.py`: 원전 Algorithm 1을 그대로 실행. `toy_bpe.py`: 직접 구현한 학습·적용. 두 결과의 merge 10개가 같음.
  - `inspect_llama.py` · `run_llama.py` · `trace_sp_bpe.py`: Llama tokenizer 설정 · 예시 분절 · merge 순서 재현(라이브러리 출력과 일치).
  - `train_sp.py`: byte_fallback · split_digits on/off 미니 학습(설명용 말뭉치).
  - `gpt2_vs_llama.py` · `chars_per_token.py`: GPT-2 비교와 표본 문자/토큰 비.
- **tokenizer 파일 출처:** `hf-internal-testing/llama-tokenizer`의 `tokenizer.model`(499,723 bytes, sha256 `9e556afd…d347`). 로그인 없이 받았고, `huggyllama/llama-7b`(LLaMA 1) LFS oid와 같음. 공식 `meta-llama/Llama-2-7b-hf`는 gated라 내려받지 못했습니다. API 목록에서 크기(499,723)는 같았지만 해시는 출력에서 가려져 **바이트 단위 동일성은 미확인**입니다. Llama 2 원문의 “Llama 1과 같은 tokenizer”와는 일치합니다.

**확인하지 못한 것**

- Llama 2 tokenizer를 학습한 말뭉치·시점·merge 과정: 원문 미기술, 파일에도 없음.
- Llama 공백 조각(`▁`, `▁▁` 등 16개)의 점수가 −1e9인 이유: 관찰만 했고 원인은 확인하지 않음.
- 2023년 당시 SentencePiece 기본값: 현재 master 문서만 봄.
- Llama 3 tokenizer 실행, tiktoken 인코딩 이름: gated · 원문 미기술.
- Sennrich v1(W01이 링크한 판본)과 v5의 §3.2 문구 차이: v5만 읽음.
- 사람 검토: **미검토**.

<a id="memo-position"></a>

### 검증 메모: 위치 인코딩

- **직접 연 원문:**
  - Llama 2 v2 로컬 텍스트 `.local/llama2-paper/page-05.txt`(§2.2), `page-47.txt`(A.2.1, Table 16 · 17), 참고문헌 페이지(Su et al. 2022 인용 확인, PI · ALiBi · Shaw · GPTNeo 미인용).
  - LLaMA 1 v1 로컬 텍스트 `.local/llama1-paper/page-03.txt`(§2.2, Table 2).
  - Vaswani 2017 arXiv HTML v7 §3.5 · Table 3. GPT-1 · GPT-2 PDF(OpenAI CDN, pypdf로 텍스트 추출), GPT-3 arXiv PDF v4 §2.1(PDF p.8). openai/gpt-2 `src/model.py`(wpe).
  - Shaw 2018 초록, T5 arXiv HTML v4 §2.1, HF transformers v4.44.0 `modeling_t5.py`의 `_relative_position_bucket`, ALiBi HTML v2 초록 · §2.2 · §3.
  - RoFormer HTML v5 §3.1–3.4와 abs 페이지(판 이력: v1 2021.04.20 … v5 2023.11.08).
  - EleutherAI 블로그(2021.04.20), GPT-NeoX-20B HTML §2.1 · 2.1.1, PaLM PDF v5 §2(p.5) · §5(p.10), meta-llama/llama `model.py`.
  - PI abs v2 · HTML v2, Code Llama HTML §2.4, Xiong 2023 abs, Llama 3 HTML v3 §3.2 · Table 3 · §3.4.2.
- **돌린 것:** `scratchpad/rope/rope_demo.py`(numpy 2.0.2, 시드 0). 출력 전체는 `scratchpad/rope/rope_demo_output.txt`. (a) RoPE와 더하기 방식의 거리 2 비교 · 네 항 분해, (b) d = 128 파장(밑값 10,000 · 500,000 · 1,000,000), (c) decay 예시, (d) 학습형 표 범위 밖 조회, (e) T5 bucket 이식, (f) PI 각도 계산.
- **확인하지 못했거나 추론인 것:**
  - GPT-3가 학습형 위치 임베딩을 썼다는 것은 “GPT-2와 같은 구조” 문장에서의 추론입니다. GPT-2도 논문이 아니라 공개 코드로 확인했습니다.
  - GPT-J가 rotary를 썼다는 것은 GPT-NeoX-20B 논문의 Wang & Komatsuzaki(2021) 인용(25% 적용)과 “GPT-J와 거의 같은 구조” 문장으로만 확인했습니다. GPT-J 저장소는 열지 않았습니다.
  - Meta 코드에서 회전 쌍을 인접 차원(2i, 2i+1)으로 묶는지는 함수 본문을 끝까지 확인하지 않았습니다. 데모는 RoFormer 식 15처럼 인접 쌍으로 묶었습니다.
  - Xiong et al.(Llama 2 Long)의 밑값 수치와 PI 그림 2의 세부 수치는 본문을 읽지 않았습니다.
  - WebFetch 요약을 거친 인용(HTML 판)은 원문 문장 그대로가 아닐 수 있어, 핵심 수치만 옮겼습니다. 로컬 텍스트 · PDF 추출로 본 GPT-1 · 2 · 3 · PaLM 문장은 원문 그대로입니다.
- **W01 자료와 어긋나는 점(확인 요청):** W01 `script.md`의 “선택 ③ RoPE ②” 대본은 “3번째 토큰이면 첫 쌍은 3 라디안, 느린 쌍은 0.03 라디안”이라고 말합니다. d = 128, 밑값 10,000이면 가장 느린 쌍은 3 × 1.155×10⁻⁴ ≈ 0.00035 rad입니다(0.03 rad가 되는 쌍은 i = 33, θ₃₃ = 0.01). “설명용 반올림”이었는지 검토가 필요합니다. 같은 대본의 “느린 쌍은 5만 토큰쯤 가야 한 바퀴”는 54,410과 맞습니다.
- **사람 검토:** **미검토** · 검토자 · 일시 미지정.

### 입력과 검토 상태

- 보고서: Touvron et al., *Llama 2: Open Foundation and Fine-Tuned Chat Models*, [arXiv:2307.09288v2](https://arxiv.org/abs/2307.09288v2). 링크는 v2 PDF의 파일 페이지 기준입니다(77쪽).
- 파트 배정: 2026-10-24 스터디 배정(Architecture 이경민 · Data 정호찬 · Post-training 송용우 · 임병극 · Alignment 김민제 · 강민우 · Background 이정민 · 김민선)에 맞춰 이전 판의 파트 구성을 바꿨습니다. Rejection sampling 페이지는 §3.2.3 배정에 따라 Post-training에서 Alignment로, 모델 기반 · 사람 평가는 §3.4 배정에 따라 Alignment에서 Post-training으로 옮겼습니다. RLHF 3단계 골격은 Post-training, Bradley–Terry와 PPO clip은 Alignment의 선행 페이지로 옮겼습니다. §4 · §5 페이지는 [배정 밖 원문](#unassigned-scope)으로 뺐습니다.
- 확인한 범위(Llama 2): 본문 §1–§5.3(PDF p.3–35)의 텍스트 추출본, 부록 A.2.1–A.2.2(Table 16–25), A.3.1–A.3.7(Table 26–32), A.4.1, A.6(Table 51)의 텍스트. 이번 판에서 §2 · §2.2 · Table 1 · A.2.1 · §3.2.3 · §3.4 Limitations의 문장과 섹션 쪽수를 다시 열어 확인했습니다.
- 확인하지 못한 범위: 그림(Fig. 5–31)은 캡션과 본문 설명, 추출된 축 값만 봤고 이미지를 직접 확인하지 않았습니다. A.5 annotation 지침과 §6 관련 연구는 읽지 않았습니다.
- 새로 쓴 페이지(Data · Background)의 원전 확인 범위와 직접 돌린 코드는 이 앞의 검증 메모 세 장(Data · Tokenizer · 위치 인코딩)에 적었습니다. 스크립트는 저장소에 넣지 않았습니다.
- 학습목표·가이드: [W02 학습목표](README.md) · [W02 Background](../../background/w02.md). 학습목표 세 가지는 Architecture RQ3 · Alignment RQ1 · Alignment RQ2–RQ3에 대응합니다. 학습목표 문서는 이번에 고치지 않았습니다.
- 외부 원전(이전 판에서 확인): InstructGPT App. C.4와 Llama 3 Table 3 · §4를 2026-10-17에 원문에서 확인했습니다. Mistral 7B · DeepSeek-V2 · DPO · GRPO · PPO 원 논문의 하이퍼파라미터와 공개 모델 config(70B 80 layer · KV 8 head 등)는 다시 열지 않았습니다.
- 사람 검토: **미검토** · 검토자·일시 미지정
- AI 재검토: 이전 판의 재계산(Table 3 범주 평균 · Table 18 평균 · Table 2 탄소 계수 · Table 6 합계 · Table 26 batch 합계)은 그대로 유지했습니다. 이번 판에서는 모든 내부 링크가 존재하는 페이지로 이어지는지, 개념 페이지가 파트당 한 번만 있는지를 스크립트로 확인했습니다. HTML은 PC 폭과 휴대폰 폭(375px)에서 열어 파트 탭 이동, 개념 링크 이동(Background RQ2 → RoPE 돌려 보기), 표와 코드 블록이 페이지 밖으로 넘치지 않는지를 확인했습니다. 94쪽 전체를 화면으로 읽지는 않았습니다.

