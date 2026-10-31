# LLaMA 1 (arXiv:2302.13971v1) — 다섯 파트 읽기 지도

<!-- 원문 링크는 arXiv v1 PDF의 파일 페이지 기준이다. H3 하나가 HTML 한 페이지다. -->

<!-- part: overview -->
## 한눈에 보기

### 다섯 파트가 다루는 내용

LLaMA 1은 **공개 데이터만으로, 작은 모델을 권장치보다 오래 학습하면 훨씬 큰 비공개 모델과 견줄 수 있는가**를 묻습니다. 원문 본문은 사전학습(§2)과 평가(§3)가 대부분이고, 후학습(§4)과 위험 평가(§5)는 짧습니다.

| 파트 | 이번 논문에서 다루는 내용 | 필수 원문 | 개념 | 분량 |
| --- | --- | --- | --- | --- |
| Architecture & Pre-training | 원 Transformer 대비 세 군데 바뀐 블록, AdamW · cosine · warmup 설정과 그 출처, 추론 예산에 맞춘 토큰 배분, 65B를 21일에 학습한 구현, 벤치마크별로 무엇을 묻고 어떻게 채점하나(zero/few-shot · likelihood · 정규화 · exact match) | §1 · §2.2–§2.4 · §3 · App. A · Table 2–9 · Fig. 1–2 | 25개 | ■■■■■ 높음 |
| Data & Synthesis | 공개 소스 7개의 구성 · 비율 · 반복량, **소스마다 다른 전처리**, 언어 구성(웹은 영어, Wikipedia 20개 언어), tokenizer, 그리고 RedPajama · Llama 2 · 3 · FineWeb으로 이어진 후속 | §2.1 · Table 1 + 후속 논문 | 16개 (원문 12 + 논문 밖 4) | ■■■■□ 중간–높음 |
| Post-training | LLaMA-I: Flan 프로토콜로 한 번 한 instruction finetuning과 MMLU 결과 | §4 · Table 10 · App. D | 2개 | ■□□□□ 낮음 |
| Alignment & RL | 정렬 학습은 없음. 사전학습 모델의 독성 · 편향 · 사실성 측정과 탄소 발자국 | §5 · §6 · Table 11–15 | 6개 | ■■■□□ 중간 |
| Background | Chinchilla 스케일링 법칙과 손실 식(LLaMA의 출발점), 큰 모델일수록 loss가 낮은 이유, 블록 부품 · optimizer · 효율 구현의 원전 | §1 + 원전 약 12편의 지정 절 | 5개 + 빈 영역 14개 | ■■■■□ 중간–높음 |

분량 = 개념 수 + 필수 원문 분량. 원문 본문은 약 12쪽(PDF p.1–12)이며, Architecture & Pre-training이 그중 약 6쪽(§2.2–§2.4, §3)을 차지합니다. Data는 원문은 한 쪽 남짓이지만 소스별 전처리와 후속 연구까지 보면 분량이 큽니다. Background는 이번 논문 안의 분량은 적지만 원전 읽기가 많습니다.

### 분량과 함께 할 파트

- **분량 차이:** Architecture & Pre-training(25개, 그중 평가 10개)과 Data(16개)가 무겁고, Post-training(2개)이 가장 가볍습니다.
- **같이 보는 원문:** 같은 표나 같은 데이터가 두 파트의 질문에 동시에 쓰이는 곳이 다섯 군데 있습니다.

| 함께 준비 | 왜 같이 하나 | 공유하는 원문 |
| --- | --- | --- |
| Architecture RQ3 + Background | LLaMA의 출발점(작은 모델을 오래)은 Chinchilla 스케일링 법칙을 다시 읽은 것입니다. Background가 법칙과 손실 식을, Architecture가 Table 2의 토큰 배분과 Fig. 1을 맡습니다. | §1 · Table 2 · Fig. 1 · Chinchilla §3 |
| Architecture RQ1–RQ2 + Background | 블록 부품(RMSNorm · SwiGLU · RoPE)과 optimizer 설정(GPT-3)마다 원전이 따로 있습니다. | §2.2 · §2.3 · 빈 영역 표 |
| Architecture RQ4 + Post-training + Alignment | 세 파트 모두 **평가**를 읽습니다: 기반 모델 20개 벤치마크, LLaMA-I의 MMLU, 위험 벤치마크 4종. Post-training 분량이 적으니 §3 평가 방식과 MMLU를 함께 맡습니다. | §3 · §3.6 · §4 · §5 · Table 9–14 |
| Data + Alignment | 저자는 CommonCrawl(67%)을 편향의 원인으로 추정합니다. | Table 1 · §5.2 · Table 12 |
| Data + Architecture RQ3 · RQ4 | 1.0T / 1.4T 토큰과 소스별 epochs, 책 데이터 177GB와 MMLU 열세(저자 가설). | Table 1–2 · §3.6 |

제안 조합: **(Architecture RQ1–RQ3 + Background)** · **(Architecture RQ4 + Post-training + Alignment, 평가 묶음)** · **(Data 단독: 원문 + 후속)**. 최종 담당과 분량은 사람이 정합니다.

<!-- part: architecture -->
## Architecture & Pre-training

### 이 파트의 질문

- **RQ1. LLaMA 블록은 원 Transformer 디코더 블록과 어디가 다른가?**
  - 필수 원문: [§2.2 Architecture](https://arxiv.org/pdf/2302.13971v1#page=3)
  - 개념: [Pre-normalization](#c-prenorm) · [RMSNorm](#c-rmsnorm) · [SwiGLU](#c-swiglu) · [RoPE](#c-rope)
- **RQ2. 학습은 무엇으로 제어했나?**
  - 필수 원문: [§2.3 Optimizer · Table 2](https://arxiv.org/pdf/2302.13971v1#page=3)
  - 개념: [AdamW](#c-adamw) · [β₂ = 0.95와 나머지 설정값의 출처](#c-opt-values) · [Cosine schedule](#c-cosine) · [Warmup 2,000 step](#c-warmup) · [Gradient clipping](#c-clipping) · [AdamW 이후: Muon](#c-muon)
- **RQ3. 왜 작은 모델을 오래 학습했고, 그 학습을 어떻게 실행했나?**
  - 필수 원문: [§1](https://arxiv.org/pdf/2302.13971v1#page=1) · [§2.4 · Table 2 · Fig. 1](https://arxiv.org/pdf/2302.13971v1#page=3)
  - 개념: [추론 예산과 토큰 배분](#c-token-budget) · Background의 [큰 모델일수록 loss가 낮은 이유](#c-size-loss) · [메모리 효율 causal attention](#c-efficient-attention) · [Activation checkpointing](#c-checkpointing) · [Model · sequence parallelism](#c-parallelism) · [65B 학습의 메모리와 처리량 계산](#c-memory-math)
- **RQ4. 어떤 벤치마크를, 어떤 입력으로, 어떻게 채점했나?**
  - 필수 원문: [§3 도입 · §3.1–§3.6](https://arxiv.org/pdf/2302.13971v1#page=4) · [App. A · Fig. 3](https://arxiv.org/pdf/2302.13971v1#page=17)
  - 개념: [벤치마크 목록과 ‘20개’](#c-bench-list) · [상식 추론 8개](#c-bench-commonsense) · [폐쇄형 QA · 독해](#c-bench-qa) · [수학 · 코드](#c-bench-mathcode) · [MMLU](#c-bench-mmlu) · Background의 [zero-shot · few-shot 프롬프트](#c-fewshot) · [Likelihood 채점](#c-likelihood-eval) · [길이 정규화와 “Answer:” 정규화](#c-length-norm) · [Greedy 생성과 exact match](#c-greedy-em) · [maj1@k와 pass@k](#c-majk-passk)
- **RQ5. 그렇게 잰 기반 모델은 어디까지 가나?**
  - 필수 원문: [Table 3–9](https://arxiv.org/pdf/2302.13971v1#page=4) · [§3.7 · Fig. 2](https://arxiv.org/pdf/2302.13971v1#page=8)
  - 개념: [학습 중 성능 추적](#c-training-curve) · 결과는 각 벤치마크 페이지 아래쪽에 함께 적었습니다

<a id="c-prenorm"></a>

### Pre-normalization

- **무엇인가:** 각 sublayer(attention, FFN)의 **출력**이 아니라 **입력**을 정규화하는 배치입니다. 축약하면 `x + Sublayer(Norm(x))`이고, 원 Transformer는 `Norm(x + Sublayer(x))`입니다(설명용 축약).
- **원문:** [§2.2](https://arxiv.org/pdf/2302.13971v1#page=3) — 학습 안정성을 위해 출력 대신 각 sublayer의 입력을 정규화했고, GPT-3에서 영감을 받았다고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] post-norm과 pre-norm에서 정규화가 잔차 경로의 어디에 놓이는지 그림으로 그린다.
  - [ ] 저자가 밝힌 이유(학습 안정성)와, 이 논문이 그 효과를 따로 실험하지 않았다는 점을 구분한다.
- **함께 볼 개념:** [RMSNorm](#c-rmsnorm) · [원 Transformer 디코더 블록](#c-transformer-base)

<a id="c-rmsnorm"></a>

### RMSNorm

- **무엇인가:** LayerNorm에서 평균 빼기를 생략하고, 제곱평균제곱근(RMS)으로만 나눈 뒤 학습되는 scale을 곱하는 정규화 함수입니다.
- **원문:** [§2.2](https://arxiv.org/pdf/2302.13971v1#page=3) — RMSNorm(Zhang & Sennrich, 2019)을 썼다는 채택 사실만 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LayerNorm과 RMSNorm의 식 차이(평균 μ를 빼는가)를 말한다.
  - [ ] “어디에 두는가(pre-norm)”와 “무슨 함수인가(RMSNorm)”가 서로 다른 선택임을 설명한다.
- **함께 볼 개념:** [Pre-normalization](#c-prenorm) · 원전: RMSNorm [arXiv:1910.07467](https://arxiv.org/abs/1910.07467v1) §3–§4

<a id="c-swiglu"></a>

### SwiGLU

- **무엇인가:** FFN의 ReLU 대신, 입력을 두 갈래로 투영해 한쪽에 Swish를 적용하고 다른 쪽과 원소별로 곱하는 게이트형 활성화입니다. `Swish(xW) ⊙ xV`.
- **원문:** [§2.2](https://arxiv.org/pdf/2302.13971v1#page=3) — PaLM을 따라 SwiGLU를 썼고, 중간 차원을 PaLM의 4d 대신 **(2/3)·4d**로 두었다고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 행렬이 2개(ReLU FFN)에서 3개로 늘어도 중간 폭을 2/3로 줄이면 파라미터 수가 비슷해지는 이유를 계산으로 보인다.
  - [ ] 원 제안은 Shazeer(2020), PaLM은 채택 선례라는 출처 관계를 말한다.
- **함께 볼 개념:** 원전: GLU Variants [arXiv:2002.05202](https://arxiv.org/abs/2002.05202v1) §2–§3.1

<a id="c-rope"></a>

### RoPE

- **무엇인가:** 위치 벡터를 입력에 더하는 대신, 각 layer에서 query·key 벡터를 위치에 비례한 각도로 회전시키는 위치 처리입니다. 회전 덕분에 attention 점수가 두 토큰의 상대 거리에 의존합니다.
- **원문:** [§2.2](https://arxiv.org/pdf/2302.13971v1#page=3) — GPTNeo를 따라 절대 위치 임베딩을 없애고 네트워크의 각 layer에 RoPE를 추가했다고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 절대 위치 임베딩(입력에 더함)과 RoPE(Q·K에 회전)의 적용 위치 차이를 말한다.
  - [ ] RoPE가 V가 아니라 Q·K에만 적용된다는 점과 그 이유(점수 계산에 위치를 넣기 위함)를 설명한다.
- **함께 볼 개념:** 원전: RoFormer [arXiv:2104.09864](https://arxiv.org/abs/2104.09864v5) §3.2

<a id="c-adamw"></a>

### AdamW

- **무엇인가:** Adam의 적응적 update에서 weight decay를 gradient에 섞지 않고 파라미터에 따로 적용하는(decoupled) optimizer입니다.
- **원문:** [§2.3](https://arxiv.org/pdf/2302.13971v1#page=3) — AdamW, β₁ = 0.9, β₂ = 0.95, weight decay 0.1.
- **설명할 수 있어야 하는 것:**
  - [ ] L2 penalty와 decoupled weight decay의 차이를 한 문장으로 말한다. Adam에서는 L2 항이 gradient에 섞여 적응적 스케일로 나뉘므로 파라미터마다 감쇠 강도가 달라지고, AdamW는 감쇠를 update와 따로 적용합니다.
  - [ ] LLaMA가 공개한 β₁ · β₂ · weight decay 값을 말하고, 새 optimizer가 아니라 설정값이라는 점을 구분한다.
  - [ ] AdamW가 파라미터마다 1차 · 2차 모멘트 두 개를 더 들고 있어 optimizer 상태 메모리가 크다는 점을 말한다(추출자 설명).
- **함께 볼 개념:** [β₂ = 0.95와 나머지 설정값의 출처](#c-opt-values) · [AdamW 이후: Muon](#c-muon) · 원전: AdamW [arXiv:1711.05101](https://arxiv.org/abs/1711.05101v3) §2

<a id="c-opt-values"></a>

### β₂ = 0.95와 나머지 설정값의 출처

- **무엇인가:** LLaMA의 optimizer 설정은 대부분 GPT-3가 쓴 값과 같습니다. 원문은 이 값들을 고른 이유를 설명하지 않습니다.
- **원문:** [§2.3](https://arxiv.org/pdf/2302.13971v1#page=3) — 값만 나열합니다. 비교 원전: GPT-3 [Appendix B](https://arxiv.org/abs/2005.14165) — Adam β₁ 0.9 · β₂ 0.95 · ε 1e-8, gradient norm clip 1.0, 학습률을 최대값의 10%까지 cosine decay, weight decay 0.1.

| 설정 | PyTorch AdamW 기본값 | GPT-3 (2020) | LLaMA 1 |
| --- | --- | --- | --- |
| β₁ / β₂ | 0.9 / 0.999 | 0.9 / 0.95 | 0.9 / 0.95 |
| weight decay | 0.01 | 0.1 | 0.1 |
| gradient clipping | 없음 | 1.0 | 1.0 |
| 마지막 학습률 | – | 최대값의 10% | 최대값의 10% |
| warmup | – | 375M 토큰 | 2,000 step (≈ 8B 토큰) |

- **설명할 수 있어야 하는 것:**
  - [ ] β₂ = 0.95는 라이브러리 기본값(0.999)이 아니라 GPT-3 이후 대형 LM에서 흔히 쓰는 값이라는 점을 말한다.
  - [ ] β₂가 작을수록 2차 모멘트가 최근 gradient 크기를 빨리 따라가, gradient가 갑자기 커질 때 update 크기가 덜 튄다는 직관을 설명한다(추출자 설명 · 원문 미기술).
  - [ ] 표의 LLaMA 값이 GPT-3와 거의 같고, 원문에 선택 이유나 ablation이 없다는 점을 말한다.
- **함께 볼 개념:** [Warmup 2,000 step](#c-warmup) · [Gradient clipping](#c-clipping)

<a id="c-cosine"></a>

### Cosine schedule

- **무엇인가:** warmup 뒤 학습률을 cosine 곡선을 따라 서서히 낮추는 스케줄입니다. 학습 후반에 학습률이 작아지면서 loss가 더 내려갑니다.
- **원문:** [§2.3 · Table 2](https://arxiv.org/pdf/2302.13971v1#page=3) — 마지막 학습률은 최대값의 10%. 최대 학습률은 7B·13B 3.0e-4, 33B·65B 1.5e-4. 큰 모델일수록 최대 학습률이 작습니다.
- **왜 cosine인가:** 원문은 이유를 적지 않습니다. 당시 GPT-3 · Chinchilla 계열의 관행이고, Chinchilla는 cosine 주기를 학습 토큰 수에 맞춰야 최종 loss가 가장 좋다고 보고했습니다. Kaplan et al.(2020)과 결론이 달랐던 주된 이유도 이 주기 설정이었습니다.
- **그 뒤의 흐름 (논문 밖):** cosine은 총 학습 길이를 미리 정해야 합니다. 그래서 일정한 학습률을 유지하다 마지막에만 낮추는 방식(constant + cooldown, WSD)이 쓰입니다. Hägele et al.(2024)은 마지막 20% 구간 cooldown으로 cosine과 거의 같은 결과를 보고했고, 학습 길이가 다른 실험끼리 중간 checkpoint를 재사용할 수 있다는 점을 장점으로 듭니다.
- **설명할 수 있어야 하는 것:**
  - [ ] optimizer(update 규칙)와 schedule(update 크기의 시간 변화)을 구분한다.
  - [ ] cosine의 약점(학습 길이를 미리 고정)과 constant + cooldown이 그것을 어떻게 피하는지 말한다.
- **함께 볼 개념:** [Warmup 2,000 step](#c-warmup) · 원전: [Hägele et al. 2024](https://arxiv.org/abs/2405.18392) · Chinchilla [arXiv:2203.15556](https://arxiv.org/abs/2203.15556v1) §3 · App. A

<a id="c-warmup"></a>

### Warmup 2,000 step

- **무엇인가:** 학습 초반에 학습률을 0에서 최대값까지 천천히 올리는 구간입니다. 초기에는 Adam의 2차 모멘트 추정이 불안정하고 가중치도 무작위라, 큰 학습률로 바로 시작하면 발산하기 쉽습니다(일반적 설명).
- **원문:** [§2.3](https://arxiv.org/pdf/2302.13971v1#page=3) — “2,000 warmup steps”만 적고, 2,000이라는 값의 근거는 밝히지 않습니다.
- **크기로 보면 (추출자 계산):** batch 4M 토큰 × 2,000 step ≈ 8B 토큰. 1.0T 학습(약 25만 step)의 0.8%, 1.4T 학습(약 35만 step)의 0.6%입니다. GPT-3의 warmup 375M 토큰보다 20배 이상 깁니다. OPT-175B도 2,000 step warmup을 썼다고 알려져 있습니다(2차 출처 기준, 원 논문 확인 필요).
- **설명할 수 있어야 하는 것:**
  - [ ] warmup이 왜 필요한지 한 문장으로 말한다.
  - [ ] 2,000 step이 전체 학습의 1% 미만이라는 점을 계산으로 보이고, 원문에 값의 근거가 없다는 점을 말한다.
- **함께 볼 개념:** [Cosine schedule](#c-cosine) · [β₂ = 0.95와 나머지 설정값의 출처](#c-opt-values)

<a id="c-clipping"></a>

### Gradient clipping

- **무엇인가:** gradient 전체의 크기(norm)가 정해진 값을 넘으면 그 값으로 잘라, 한 번의 update가 지나치게 커지지 않게 하는 장치입니다.
- **원문:** [§2.3](https://arxiv.org/pdf/2302.13971v1#page=3) — gradient clipping 1.0.
- **설명할 수 있어야 하는 것:**
  - [ ] clipping이 weight decay · 학습률 스케줄과 다른 제어(큰 gradient의 상한)라는 점을 말한다.
  - [ ] Fig. 1의 학습 loss 곡선에 보이는 순간적인 튐(spike)이 대형 모델 학습에서 흔하고, clipping · 낮은 β₂가 이런 불안정을 줄이려는 장치로 쓰인다는 점을 말한다(추출자 해석).
- **함께 볼 개념:** [AdamW](#c-adamw) · [β₂ = 0.95와 나머지 설정값의 출처](#c-opt-values)

<a id="c-muon"></a>

### AdamW 이후: Muon

- **무엇인가 (논문 밖):** Muon은 2D 가중치 행렬의 momentum update를 직교화(orthogonalize)해서 적용하는 optimizer입니다. 행렬의 모든 방향으로 고르게 update가 가도록 만듭니다.
- **원문:** LLaMA 1은 AdamW만 씁니다. 이 페이지는 이후 흐름입니다.
- **이후 흐름:** Moonshot AI의 [Muon is Scalable for LLM Training (2025)](https://arxiv.org/abs/2502.16982)은 weight decay를 더하고 파라미터별 update 크기를 맞추면 Muon이 대규모 학습에서 별도 튜닝 없이 동작하며, scaling law 실험에서 AdamW 대비 약 2배의 compute 효율을 보였다고 보고합니다. 이 스터디의 W11(Qwen3.8-Next)과 W15(Motif)도 Muon 적용을 다룹니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA 1 시점의 표준이 AdamW였고, 그 설정이 이후 Llama 2까지 거의 그대로 이어졌다는 점을 말한다.
  - [ ] Muon이 AdamW와 무엇이 다른지(행렬 단위 직교화 update) 한 문장으로 말하고, 이는 후속 주차에서 다시 본다는 점을 연결한다.
- **함께 볼 개념:** [AdamW](#c-adamw)

<a id="c-token-budget"></a>

### 추론 예산과 토큰 배분

- **무엇인가:** 같은 목표 성능이라면 학습 비용보다 **서비스할 때 반복해서 드는 추론 비용**을 기준으로, 작은 모델에 더 많은 학습 토큰을 주는 선택입니다.
- **원문:** [§1](https://arxiv.org/pdf/2302.13971v1#page=1) — 논리는 세 문장으로 이어집니다.
  1. Hoffmann et al.(2022)은 주어진 compute에서 가장 좋은 성능이 가장 큰 모델이 아니라 **더 많은 데이터로 학습한 더 작은 모델**에서 나온다고 보였다.
  2. 그 스케일링 법칙의 목적은 **특정 학습 compute 예산에서** 데이터와 모델 크기를 어떻게 키울지 정하는 것이고, **추론 예산은 고려하지 않는다**.
  3. 목표 성능이 정해지면 선호할 모델은 가장 빨리 학습되는 모델이 아니라 **가장 빨리 추론되는 모델**이다. Hoffmann은 10B 모델에 200B 토큰을 권하지만, 7B 모델은 1T 토큰 이후에도 계속 좋아졌다.

  [Table 2](https://arxiv.org/pdf/2302.13971v1#page=3): 7B·13B 1.0T, 33B·65B 1.4T 토큰. §2 도입은 학습 방식이 “Chinchilla 스케일링 법칙에서 영감을 받았다”고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Chinchilla가 최적화한 것(고정 학습 compute에서의 loss)과 LLaMA가 기준으로 삼은 것(추론 예산)을 구분한다.
  - [ ] 네 모델의 학습 토큰 수를 말하고, 파라미터당 토큰 수가 작은 모델일수록 크다는 점을 계산으로 보인다(추출자 계산).
  - [ ] 저자는 관찰을 근거로 들었고, 같은 compute에서 Chinchilla 최적점과 비교한 통제 실험은 없다는 점을 말한다.
- **함께 볼 개념:** [스케일링 법칙 ①](#c-scaling) · [학습 중 성능 추적](#c-training-curve)

<a id="c-efficient-attention"></a>

### 메모리 효율 causal attention

- **무엇인가:** attention weight 행렬을 저장하지 않고, causal mask로 가려질 query·key 점수는 계산하지 않아 메모리와 연산을 줄이는 구현입니다.
- **원문:** [§2.4](https://arxiv.org/pdf/2302.13971v1#page=3) — xformers 라이브러리의 구현을 썼고, Rabe & Staats(2021)에서 영감을 받아 Dao et al.(2022)의 backward를 쓴다고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 이 기법이 모델 구조가 아니라 같은 계산을 더 적은 메모리로 하는 **구현**이라는 점을 말한다.
  - [ ] causal mask 때문에 계산을 생략할 수 있는 점수가 무엇인지 설명한다. 길이 n의 시퀀스에서 n×n 점수 중 대각선 위쪽 약 절반은 미래 토큰이라 0으로 가려지므로 계산하지 않아도 됩니다.
  - [ ] attention weight를 저장하지 않는다는 것은, n×n 확률 행렬을 메모리에 두지 않고 backward에서 필요한 만큼 다시 계산한다는 뜻임을 말한다(Dao et al.의 FlashAttention backward).
- **원전:** Rabe & Staats, Self-attention Does Not Need O(n²) Memory [arXiv:2112.05682](https://arxiv.org/abs/2112.05682) · Dao et al., FlashAttention [arXiv:2205.14135](https://arxiv.org/abs/2205.14135) · [xformers](https://github.com/facebookresearch/xformers)
- **함께 볼 개념:** [Activation checkpointing](#c-checkpointing) · [65B 학습의 메모리와 처리량 계산](#c-memory-math)

<a id="c-checkpointing"></a>

### Activation checkpointing

- **무엇인가:** backward에 필요한 activation을 모두 저장하지 않고 일부만 저장했다가 필요할 때 다시 계산해 메모리를 아끼는 기법입니다.
- **원문:** [§2.4](https://arxiv.org/pdf/2302.13971v1#page=3) — 선형층 출력처럼 계산이 비싼 activation은 저장하고, PyTorch autograd 대신 Transformer layer의 backward를 직접 구현했다고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] “무엇을 저장하고 무엇을 재계산하나”의 선택이 메모리와 시간의 교환이라는 점을 말한다.
  - [ ] 이 절약을 위해 model · sequence parallelism으로 메모리를 확보했다는 연결을 설명한다.
- **함께 볼 개념:** [Model · sequence parallelism](#c-parallelism)

<a id="c-parallelism"></a>

### Model · sequence parallelism

- **무엇인가:** 한 모델의 가중치와 activation을 여러 GPU에 나눠 담는 병렬화입니다. sequence parallelism은 sequence 차원을 나눠 activation 메모리를 줄입니다.
- **원문:** [§2.4](https://arxiv.org/pdf/2302.13971v1#page=4) — Korthikanti et al.(2022)의 model · sequence parallelism을 쓰고, activation 계산과 GPU 간 통신(all_reduce)을 최대한 겹쳤다고 적습니다. 65B는 A100-80GB 2,048장에서 GPU당 약 380 tokens/sec, 1.4T 토큰에 약 21일.
- **설명할 수 있어야 하는 것:**
  - [ ] 2,048 GPU · 380 tokens/sec · 21일의 관계를 계산으로 확인한다(추출자 계산).
  - [ ] 네 가지 구현(attention · checkpointing · 병렬 · 통신 중첩)의 개별 효과는 원문이 측정하지 않았다는 점을 말한다.
  - [ ] 네 기법이 하나의 사슬이라는 점을 말한다: 재계산을 줄이려면 activation을 더 저장해야 하고 → 그 메모리를 model · sequence 병렬로 확보하고 → 병렬화로 생기는 all_reduce 통신을 계산과 겹쳐 숨긴다.
- **원전:** Korthikanti et al., Reducing Activation Recomputation in Large Transformer Models [arXiv:2205.05198](https://arxiv.org/abs/2205.05198)
- **함께 볼 개념:** [Activation checkpointing](#c-checkpointing) · [65B 학습의 메모리와 처리량 계산](#c-memory-math)

<a id="c-memory-math"></a>

### 65B 학습의 메모리와 처리량 계산

- **무엇인가:** §2.4의 숫자를 직접 계산해, 왜 병렬화가 필수였고 GPU를 얼마나 효율적으로 썼는지 보는 페이지입니다. 원문은 정밀도 · 병렬 차수 · MFU를 적지 않으므로 아래는 모두 **추출자 계산**입니다.
- **원문:** [§2.4](https://arxiv.org/pdf/2302.13971v1#page=4) — 65B, A100-80GB 2,048장, 약 380 tokens/sec/GPU, 1.4T 토큰에 약 21일.

| 계산 | 식 | 결과 |
| --- | --- | --- |
| 전체 처리량 | 2,048 GPU × 380 tokens/s | 약 78만 tokens/s |
| 학습 시간 | 1.4T ÷ 78만 tokens/s | 약 20.8일 (원문 “약 21일”과 일치) |
| 학습 compute | 6 × 65.2B × 1.4T | 약 5.5 × 10²³ FLOPs |
| GPU당 실효 연산 | 6 × 65.2B × 380 | 약 149 TFLOP/s |
| MFU | 149 ÷ 312 (A100 BF16 피크) | 약 48% (attention 연산 제외 어림) |
| 학습 상태 메모리 | 65.2B × 16 B (가중치 2 + gradient 2 + fp32 사본 4 + Adam 모멘트 8) | 약 1.0 TB → A100-80GB 13장 이상 |
| 추론 가중치 | 65.2B × 2 B (fp16) | 약 130 GB |

- **설명할 수 있어야 하는 것:**
  - [ ] 학습 상태만으로도 GPU 한 장(80GB)에 들어가지 않아 모델을 여러 GPU에 나눠야 한다는 점을 계산으로 보인다. 파라미터당 16바이트는 혼합 정밀도 + Adam의 통상 가정(ZeRO 논문)이며 원문 값이 아닙니다.
  - [ ] 380 tokens/sec/GPU를 MFU로 바꾸는 식(6N × 처리량 ÷ 피크)을 말한다.
  - [ ] 학습(약 1TB 상태)과 추론(약 130GB 가중치)의 메모리 차이가 [추론 예산](#c-token-budget) 논리와 이어진다는 점을 말한다.
- **함께 볼 개념:** [Model · sequence parallelism](#c-parallelism) · [AdamW](#c-adamw)

<a id="c-bench-list"></a>

### 벤치마크 목록과 ‘20개’

- **무엇인가:** §3이 쓰는 기반 모델 평가 전체입니다. 모두 **파인튜닝 없이** 프롬프트만으로 잽니다.
- **원문:** [§3](https://arxiv.org/pdf/2302.13971v1#page=4) — “a total of 20 benchmarks”라고 적습니다. 그런데 §3.1–§3.6에서 이름이 나오는 것은 아래 16개, RACE를 middle · high 둘로 세도 17개입니다. 나머지 셈법은 원문에 없습니다.

| 범주 | 벤치마크 | 답하는 방식 | 지표 | shot |
| --- | --- | --- | --- | --- |
| [상식 추론](#c-bench-commonsense) | BoolQ · PIQA · SIQA · HellaSwag · WinoGrande · ARC-e · ARC-c · OpenBookQA | 보기 순위 (likelihood) | 정확도 | 0 |
| [폐쇄형 QA](#c-bench-qa) | Natural Questions · TriviaQA | 답 생성 (greedy) | exact match | 0 / 1 / 5 / 64 |
| [독해](#c-bench-qa) | RACE-middle · RACE-high | 보기 순위 | 정확도 | 0 |
| [수학](#c-bench-mathcode) | MATH · GSM8k | 풀이 생성 | 정확도 · maj1@k | 미기술 |
| [코드](#c-bench-mathcode) | HumanEval · MBPP | 코드 생성 | pass@k | 0 / 3 |
| [종합 지식](#c-bench-mmlu) | MMLU | 보기 선택 | 정확도 | 5 |

- **설명할 수 있어야 하는 것:**
  - [ ] 범주마다 “보기 중 고르기”인지 “답을 직접 쓰기”인지 말한다. 채점 방식이 다릅니다.
  - [ ] 비교 모델의 수치는 직접 잰 것이 아니라 각 논문에서 인용했다는 점을 말한다.
  - [ ] “20개”라는 원문 표기와 실제로 나열된 수가 다르다는 점을 확인한다.

<a id="c-bench-commonsense"></a>

### 상식 추론 8개: 무엇을 묻나

- **무엇인가:** 일상 지식과 상식으로 보기 중 하나를 고르는 벤치마크들입니다. 모두 zero-shot, [likelihood 채점](#c-likelihood-eval), 정확도입니다.
- **원문:** [§3.1 · Table 3](https://arxiv.org/pdf/2302.13971v1#page=4). 아래 예시는 형식을 보이기 위한 설명용 문항입니다. 실제 데이터셋 문항 · 출처 · 라이선스는 [벤치마크 실제 예시](notes/benchmark-examples.md)에 있습니다.

| 벤치마크 | 무엇을 평가하나 | 형식 | 설명용 예시 | 65B |
| --- | --- | --- | --- | --- |
| BoolQ | 짧은 지문을 읽고 예/아니오 질문에 답하기. 질문은 실제 검색어에서 옴 | 지문 + 질문 → 예 / 아니오 | 지문: “고래는 아가미가 아니라 폐로 숨쉰다…” 질문: 고래는 아가미가 있나? → 아니오 | 85.3 |
| PIQA | 물리적 상식: 목표를 이루는 더 그럴듯한 방법 | 목표 + 방법 2개 | 목표: 유리병 뚜껑 열기 → (a) 뚜껑을 따뜻한 물에 담근다 (b) 병을 냉동실에 넣는다 | 82.8 |
| SIQA | 사회적 상식: 사람의 동기 · 감정 · 다음 행동 | 상황 + 질문 + 보기 3개 | 민수가 친구 생일을 깜빡했다. 민수는 어떤 기분일까? | 52.3 |
| HellaSwag | 장면을 보고 가장 자연스러운 다음 문장 고르기. 오답은 모델이 속기 쉽게 만듦 | 문맥 + 이어질 문장 4개 | “냄비에 물을 붓고 불을 켰다. 그다음…” | 84.2 |
| WinoGrande | 대명사 · 빈칸이 가리키는 대상 고르기(Winograd 형식) | 빈칸 문장 + 후보 2개 | 트로피가 가방에 안 들어갔다, ___가 너무 커서. (트로피 / 가방) | 77.0 |
| ARC-easy · challenge | 초등 · 중학 과학 시험 문제. challenge는 검색 · 단어 동시출현으로 못 푸는 문항 | 질문 + 보기 4개 | 식물이 햇빛으로 양분을 만드는 과정은? | 78.9 · 56.0 |
| OpenBookQA | 기초 과학 사실 하나 + 상식을 조합해야 풀리는 문제 | 질문 + 보기 4개 | 금속 숟가락이 뜨거운 국에서 빨리 뜨거워지는 이유는? | 60.2 |

- **설명할 수 있어야 하는 것:**
  - [ ] 각 벤치마크가 무엇을 재는지 한 줄로 말한다(예/아니오 독해 · 물리 · 사회 · 이어질 문장 · 대명사 · 과학 시험).
  - [ ] HellaSwag · WinoGrande는 기존 모델이 틀리기 쉬운 오답을 일부러 골라 만든 데이터라는 점을 말한다.
  - [ ] 결과: 65B는 BoolQ를 뺀 모든 항목에서 Chinchilla-70B를, BoolQ · WinoGrande를 뺀 모든 항목에서 PaLM-540B를 앞섭니다(§3.1).
- **원전:** [BoolQ](https://arxiv.org/abs/1905.10044) · [PIQA](https://arxiv.org/abs/1911.11641) · [SIQA](https://arxiv.org/abs/1904.09728) · [HellaSwag](https://arxiv.org/abs/1905.07830) · [WinoGrande](https://arxiv.org/abs/1907.10641) · [ARC](https://arxiv.org/abs/1803.05457) · [OpenBookQA](https://arxiv.org/abs/1809.02789)

<a id="c-bench-qa"></a>

### 폐쇄형 QA와 독해: 무엇을 묻나

- **무엇인가:** 폐쇄형(closed-book) QA는 근거 문서 없이 모델이 기억한 지식만으로 짧은 답을 **직접 써야** 합니다. 독해는 지문을 주고 보기 중에서 고릅니다.
- **원문:** [§3.2 · Table 4–5](https://arxiv.org/pdf/2302.13971v1#page=4) · [§3.3 · Table 6](https://arxiv.org/pdf/2302.13971v1#page=5) · [App. A](https://arxiv.org/pdf/2302.13971v1#page=17)

| 벤치마크 | 무엇을 평가하나 | 형식 · 채점 | 원문의 예시 · 결과 |
| --- | --- | --- | --- |
| Natural Questions | 실제 검색 질문에 대한 사실 지식 | 답 생성 · [exact match](#c-greedy-em) · 테스트 3,610문항 | “Who wrote the book the origin of species?” → Charles Darwin · 65B 64-shot 39.9 |
| TriviaQA | 퀴즈 질문의 사실 지식 | 답 생성 · exact match · filtered dev set | “The ancient city of Troy is located in what modern country?” → Turkey · 65B 64-shot 73.0 |
| RACE-middle · high | 중국 중 · 고교 영어 독해 시험 | 지문 + 질문 + 보기 4개 · 정확도 · GPT-3 설정을 따름 | 65B 67.9 · 51.6 (PaLM-540B 68.1 · 49.1) |

- **설명할 수 있어야 하는 것:**
  - [ ] 폐쇄형 QA가 “지식을 얼마나 외웠나”를 본다는 점과, 답을 생성하므로 채점 방식이 보기 순위와 다르다는 점을 말한다.
  - [ ] TriviaQA는 GPT-3 · PaLM이 쓴 unfiltered test set이 아니라 filtered dev set이라 그 수치와 직접 비교하기 어렵다는 점을 말한다(App. A).
- **원전:** [Natural Questions](https://aclanthology.org/Q19-1026/) · [TriviaQA](https://arxiv.org/abs/1705.03551) · [RACE](https://arxiv.org/abs/1704.04683)

<a id="c-bench-mathcode"></a>

### 수학과 코드: 무엇을 묻나

- **무엇인가:** 답을 맞히려면 여러 단계의 풀이나 실행되는 코드를 **생성**해야 하는 벤치마크입니다.
- **원문:** [§3.4 · Table 7](https://arxiv.org/pdf/2302.13971v1#page=5) · [§3.5 · Table 8](https://arxiv.org/pdf/2302.13971v1#page=6)

| 벤치마크 | 무엇을 평가하나 | 형식 · 채점 | 65B 결과 |
| --- | --- | --- | --- |
| MATH | 중 · 고교 경시 수준 수학 12K문항(LaTeX) | 풀이 생성 → 최종 답 비교 · maj1@k는 k = 256 | 10.6 (maj1@k 20.5) |
| GSM8k | 여러 단계 계산이 필요한 초등 · 중학 서술형 문제 | 풀이 생성 → 최종 숫자 비교 · maj1@k는 k = 100 | 50.9 (maj1@k 69.7) |
| HumanEval | 함수 시그니처 + docstring(설명 · 테스트)을 보고 Python 함수 완성 | zero-shot · 테스트 통과 여부 · pass@1 / pass@100 | 23.7 / 79.3 |
| MBPP | 짧은 설명 + 입출력 예시로 기초 Python 프로그램 작성 | 3-shot · 테스트 통과 · pass@1 / pass@80 | 37.7 / 76.8 |

- **설명할 수 있어야 하는 것:**
  - [ ] 수학 · 코드는 답의 문자열이 아니라 **최종 답 · 테스트 통과**로 채점한다는 점을 말한다.
  - [ ] Minerva는 수학 데이터 38.5B 토큰으로 추가 학습한 모델이고, LLaMA · PaLM은 수학 파인튜닝을 하지 않았다는 비교 조건을 말한다.
  - [ ] GSM8k의 shot 수와 일반 열의 decoding 세부는 원문에 없다는 점을 말한다.
- **함께 볼 개념:** [maj1@k와 pass@k](#c-majk-passk) · 원전: [MATH](https://arxiv.org/abs/2103.03874) · [GSM8k](https://arxiv.org/abs/2110.14168) · [HumanEval](https://arxiv.org/abs/2107.03374) · [MBPP](https://arxiv.org/abs/2108.07732)

<a id="c-bench-mmlu"></a>

### MMLU: 무엇을 묻나

- **무엇인가:** 인문 · STEM · 사회과학 · 기타 57개 과목의 4지선다 문제로 폭넓은 지식을 봅니다.
- **원문:** [§3.6 · Table 9](https://arxiv.org/pdf/2302.13971v1#page=6) — 벤치마크가 제공하는 예시로 **5-shot** 평가. 65B 평균 63.4로 Chinchilla-70B 67.5, PaLM-540B 69.3보다 낮고 대부분의 분야에서 그렇습니다. 저자 가설은 책 · 논문 데이터 부족(177GB vs 최대 2TB)입니다.
- **형식 (설명용):**

  ```
  다음은 고등학교 생물에 관한 객관식 문제입니다.        ← 과목 안내
  질문: … (A) … (B) … (C) … (D) …  정답: B          ← 예시 5개
  …
  질문: [테스트 문항] (A) … (B) … (C) … (D) …  정답:   ← 모델이 이어 씀
  ```

- **설명할 수 있어야 하는 것:**
  - [ ] MMLU가 과목별 지식을 본다는 점과 5-shot 예시가 과목별로 주어진다는 점을 말한다.
  - [ ] 보기 글자(A–D)를 고르는지, 보기 내용의 likelihood를 비교하는지는 원문에 없다는 점을 말한다.
- **원전:** [MMLU](https://arxiv.org/abs/2009.03300)

<a id="c-likelihood-eval"></a>

### Likelihood 채점: 보기 중 고르기

- **무엇인가:** 보기마다 “문맥 뒤에 이 보기가 이어질 확률”을 모델로 계산해, 가장 높은 보기를 답으로 고르는 방식입니다. 모델은 아무것도 생성하지 않습니다.
- **원문:** [§3](https://arxiv.org/pdf/2302.13971v1#page=4) — 객관식 과제는 주어진 문맥에서 likelihood가 가장 높은 완성문을 고른다.
- **계산 순서:**
  1. 문맥(질문)과 보기를 이어 붙인다: `[문맥] + [보기 c]`.
  2. 보기의 토큰마다 모델이 매긴 확률의 로그를 더한다: log P(c | 문맥) = Σ log p(cᵢ | 문맥, c₁…cᵢ₋₁).
  3. 보기마다 같은 계산을 하고 (정규화 후) 가장 큰 것을 고른다. 정답과 같으면 1점.
- **예시 (설명용):** 문맥 “냄비에 물을 붓고 불을 켰다. 그다음”

| 보기 | 토큰 수 | 토큰별 log p | 합계 |
| --- | --- | --- | --- |
| A. 물이 끓기를 기다렸다. | 6 | −0.9씩 | −5.4 |
| B. 잤다. | 2 | −2.0씩 | −4.0 |

  합계만 보면 짧고 어색한 B가 이깁니다. 그래서 [길이 정규화](#c-length-norm)가 필요합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 보기 순위 채점은 생성하지 않고 확률만 비교한다는 점을 말한다.
  - [ ] 로그 확률을 더하면 토큰이 많을수록 합이 작아진다는 점을 예시로 보인다.
- **함께 볼 개념:** [길이 정규화와 “Answer:” 정규화](#c-length-norm) · [Greedy 생성과 exact match](#c-greedy-em)

<a id="c-length-norm"></a>

### 길이 정규화와 “Answer:” 정규화

- **무엇인가:** 보기의 likelihood를 그대로 비교하면 생기는 두 가지 편향을 바로잡는 방법입니다.
- **원문:** [§3](https://arxiv.org/pdf/2302.13971v1#page=4)
  - 기본: Gao et al.(2021)을 따라 **완성문의 문자 수로 나눈 likelihood**를 씁니다.
  - OpenBookQA · BoolQ: Brown et al.(2020)을 따라 `P(completion | context) / P(completion | "Answer:")`로 고릅니다.
- **① 왜 길이로 나누나:** 확률은 1보다 작아서 로그를 더할수록 합이 계속 작아집니다. 그대로 비교하면 **긴 보기가 불리**합니다. 앞 페이지 예시에서 A(공백 포함 12자) −5.4 ÷ 12 = −0.45, B(3자) −4.0 ÷ 3 = −1.33이 되어 A가 이깁니다(설명용 수치). 토큰 수가 아니라 **문자 수**로 나누면 tokenizer가 다른 모델끼리도 같은 기준이 됩니다. Gao et al.(2021)의 lm-evaluation-harness에서 `acc_norm`으로 알려진 방식입니다.
- **② 왜 “Answer:”로 나누나:** 어떤 보기는 질문과 상관없이 원래 자주 나오는 말이라 확률이 높습니다. 문맥 없이 “Answer:” 뒤에서 그 보기가 나올 확률로 나누면, **질문이 그 보기의 확률을 얼마나 올렸는지**만 남습니다.

| BoolQ 보기 | P(보기 \| 지문·질문) | P(보기 \| “Answer:”) | 비율 |
| --- | --- | --- | --- |
| yes | 0.40 | 0.60 | 0.67 |
| no | 0.35 | 0.30 | **1.17** |

  그대로면 yes, 비율로 보면 no를 고릅니다(설명용 수치).
- **설명할 수 있어야 하는 것:**
  - [ ] 길이 정규화가 없으면 짧은 보기가 유리해지는 이유를 식으로 말한다.
  - [ ] 문자 수로 나누는 이유(모델마다 tokenizer가 달라도 공정)를 말한다.
  - [ ] “Answer:” 정규화가 보기 자체의 사전 확률을 지운다는 점을 예시로 말하고, LLaMA가 이를 OpenBookQA · BoolQ에만 썼다는 점을 말한다.
- **원전:** Gao et al. 2021 [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) · GPT-3 [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) §2.4

<a id="c-greedy-em"></a>

### Greedy 생성과 exact match: 답을 직접 쓰기

- **무엇인가:** 보기가 없는 과제에서는 모델이 답을 직접 생성합니다. greedy decoding은 매 단계 확률이 가장 높은 토큰 하나만 고르는 방식이라 결과가 항상 같습니다.
- **원문:** [App. A](https://arxiv.org/pdf/2302.13971v1#page=17) — Natural Questions · TriviaQA는 greedy decoding으로 생성하고, **첫 줄바꿈 · 마지막 마침표 · 쉼표에서 끊어** 답을 뽑습니다. 정답 목록 중 하나와 **정규화 후** 같으면 정답입니다. 정규화는 소문자화, 관사 · 구두점 · 중복 공백 제거입니다.
- **예시 (원문 Fig. 3 형식):**
  - 생성: `Charles Darwin.` → 끊기 → `Charles Darwin` → 정규화 → `charles darwin`
  - 정답 목록의 `Charles Darwin` → `charles darwin` → 일치 → 1점
  - `Darwin`만 생성했다면 정답 목록에 없으면 0점입니다. exact match는 부분 점수가 없습니다.
- **likelihood 채점과의 차이:**

| | Likelihood (보기 순위) | Greedy 생성 + exact match |
| --- | --- | --- |
| 모델이 하는 일 | 보기마다 확률 계산 | 답을 한 토큰씩 생성 |
| 쓰는 과제 | 상식 추론 · RACE · MMLU | NQ · TriviaQA (수학 · 코드도 생성) |
| 틀리는 방식 | 다른 보기에 확률을 더 줌 | 형식이 조금만 달라도 0점 |

- **설명할 수 있어야 하는 것:**
  - [ ] 두 채점 방식의 차이를 같은 질문으로 비교해 말한다.
  - [ ] exact match에서 정규화가 왜 필요한지(대소문자 · 관사 차이로 틀리지 않게) 말한다.
- **함께 볼 개념:** [zero-shot · few-shot 프롬프트](#c-fewshot) · [Likelihood 채점](#c-likelihood-eval)

<a id="c-majk-passk"></a>

### maj1@k와 pass@k

- **무엇인가:** 한 문제에 답을 여러 번 샘플링해서 채점하는 두 방식입니다.
  - **maj1@k:** k개 풀이를 생성해 최종 답의 **다수결** 하나를 제출(Wang et al., 2022). 수학에 씁니다.
  - **pass@k:** k개 코드 중 **하나라도** 테스트를 통과하면 정답. 코드에 씁니다.
- **원문:** [§3.4 · Table 7](https://arxiv.org/pdf/2302.13971v1#page=5) — Minerva와 같은 설정, GSM8k k = 100, MATH k = 256. [§3.5](https://arxiv.org/pdf/2302.13971v1#page=6) — pass@1은 temperature 0.1, pass@100 · pass@80은 temperature 0.8로 샘플링하고, Chen et al.(2021)의 **불편 추정**으로 pass@k를 구합니다.
- **pass@k 추정 (원전 식):** n개를 샘플링해 c개가 통과했다면 `pass@k = 1 − C(n−c, k) / C(n, k)`. k개를 무작위로 뽑았을 때 모두 실패할 확률을 1에서 뺀 값입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 65B GSM8k가 일반 열 50.9(Minerva-62B 52.4보다 낮음)에서 maj1@k 69.7(Minerva-62B 68.5보다 높음)로 순위가 바뀐다는 점을 말한다.
  - [ ] pass@1에는 낮은 temperature, pass@100에는 높은 temperature를 쓰는 이유(다양한 시도가 필요)를 말한다.
- **함께 볼 개념:** [수학과 코드](#c-bench-mathcode) · 원전: HumanEval [arXiv:2107.03374](https://arxiv.org/abs/2107.03374) §2.1 · Self-consistency [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)

<a id="c-training-curve"></a>

### 학습 중 성능 추적

- **무엇인가:** 학습 도중의 checkpoint로 벤치마크를 측정해, 학습 토큰이 늘수록 성능이 어떻게 변하는지 보는 방법입니다.
- **원문:** [§3.7 · Fig. 2](https://arxiv.org/pdf/2302.13971v1#page=8) — 대부분의 벤치마크가 꾸준히 오르고 학습 perplexity와 상관이 있습니다. 예외로 SIQA는 변동이 커서 신뢰성이 의심되고, WinoGrande는 perplexity와의 상관이 약하다고 적습니다. [Fig. 1](https://arxiv.org/pdf/2302.13971v1#page=3): 학습 loss 곡선.
- **설명할 수 있어야 하는 것:**
  - [ ] “권장치를 넘겨 학습해도 좋아진다”의 직접 근거가 이 곡선이라는 점을 말한다.
  - [ ] SIQA · WinoGrande 두 예외와 저자가 든 이유를 말한다.
- **함께 볼 개념:** [추론 예산과 토큰 배분](#c-token-budget)

<!-- part: data -->
## Data & Synthesis

### 이 파트의 질문

- **RQ1. 어떤 데이터를 얼마나 섞어서 학습했나?**
  - 필수 원문: [§2.1 · Table 1](https://arxiv.org/pdf/2302.13971v1#page=2) · [p.3 첫 문단](https://arxiv.org/pdf/2302.13971v1#page=3)
  - 개념: [데이터 구성 한눈에](#c-data-mix) · [Sampling 비율과 epochs](#c-sampling)
- **RQ2. 소스마다 어떻게 걸렀나? 일곱 소스의 전처리는 모두 다르다**
  - 필수 원문: [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2)
  - 개념: [CommonCrawl](#c-src-cc) · [C4](#c-src-c4) · [GitHub](#c-src-github) · [Wikipedia](#c-src-wiki) · [Gutenberg · Books3](#c-src-books) · [ArXiv](#c-src-arxiv) · [Stack Exchange](#c-src-se)
- **RQ3. 어떤 언어가 들어갔고, 무엇이 빠졌나?**
  - 필수 원문: [§2.1 Wikipedia · CommonCrawl](https://arxiv.org/pdf/2302.13971v1#page=2)
  - 개념: [다국어 구성](#c-multilingual)
- **RQ4. 텍스트를 어떻게 토큰으로 바꿨나?**
  - 필수 원문: [§2.1 Tokenizer](https://arxiv.org/pdf/2302.13971v1#page=2)
  - 개념: [BPE와 SentencePiece](#c-bpe) · [숫자 분리와 byte fallback](#c-digit-byte)
- **RQ5. 이 데이터 레시피는 후속 연구로 어떻게 이어졌나? (논문 밖)**
  - 필수 원문: 아래 각 페이지의 후속 논문
  - 개념: [공개 재현: RedPajama · SlimPajama](#c-redpajama) · [Llama 2 · Llama 3의 데이터](#c-llama-data) · [웹 품질 필터의 계보](#c-quality-lineage) · [Books3와 ‘공개 데이터’의 경계](#c-books3)

<a id="c-data-mix"></a>

### 데이터 구성 한눈에

- **무엇인가:** 공개되어 있고 오픈소스와 함께 쓸 수 있는 소스만 골라, 다른 LLM이 이미 써 온 소스를 재사용한 혼합입니다. 웹(CommonCrawl + C4)이 82%, 나머지 18%가 코드 · 백과 · 책 · 논문 · Q&A입니다.
- **원문:** [§2.1 · Table 1](https://arxiv.org/pdf/2302.13971v1#page=2)

| 소스 | 비율 | epochs | 디스크 | 무엇이 들어 있나 | 핵심 전처리 |
| --- | --- | --- | --- | --- | --- |
| [CommonCrawl](#c-src-cc) | 67.0% | 1.10 | 3.3 TB | 2017–2020 웹 덤프 5개, 영어 | CCNet + Wikipedia 참조 페이지 분류기 |
| [C4](#c-src-c4) | 15.0% | 1.06 | 783 GB | 다르게 가공한 CommonCrawl | 휴리스틱 품질 필터 |
| [GitHub](#c-src-github) | 4.5% | 0.64 | 328 GB | BigQuery 공개 저장소 코드 | 라이선스 · 휴리스틱 · 파일 dedup |
| [Wikipedia](#c-src-wiki) | 4.5% | 2.45 | 83 GB | 2022년 6–8월 덤프, 20개 언어 | 링크 · 주석 · 서식 제거 |
| [Books](#c-src-books) | 4.5% | 2.23 | 85 GB | Gutenberg + Books3 | 책 단위 90% 중복 제거 |
| [ArXiv](#c-src-arxiv) | 2.5% | 1.06 | 92 GB | 논문 LaTeX 원본 | 첫 절 이전 · 참고문헌 · 주석 제거, 매크로 전개 |
| [Stack Exchange](#c-src-se) | 2.0% | 1.03 | 78 GB | 상위 28개 사이트 Q&A | HTML 제거, 답변 점수순 |

- **설명할 수 있어야 하는 것:**
  - [ ] 웹 82% · 나머지 18%라는 큰 구성과, 소스를 고른 두 조건(공개 · 오픈소스 호환)을 말한다.
  - [ ] 표의 “비율”이 디스크 용량 비율이 아니라는 점을 CommonCrawl(3.3TB, 67%)과 GitHub(328GB, 4.5%)로 보인다.
- **함께 볼 개념:** [Sampling 비율과 epochs](#c-sampling)

<a id="c-sampling"></a>

### Sampling 비율과 epochs

- **무엇인가:** sampling 비율은 학습 토큰 중 각 소스가 차지하는 몫이고, epochs는 학습 중 그 소스를 평균 몇 번 지나갔는지입니다.
- **원문:** [Table 1](https://arxiv.org/pdf/2302.13971v1#page=2) — epochs는 1.4T 학습 기준이며 1T 학습도 같은 비율을 씁니다. [p.3](https://arxiv.org/pdf/2302.13971v1#page=3) — 대부분의 토큰은 한 번만 쓰고, Wikipedia와 Books만 약 2 epochs.
- **계산해 보면 (추출자 계산):** 학습에 쓴 토큰 = 비율 × 1.4T, 소스의 고유 토큰 ≈ 학습에 쓴 토큰 ÷ epochs.

| 소스 | 학습에 쓴 토큰 | 소스 고유 토큰(추정) |
| --- | --- | --- |
| CommonCrawl | 938B | 약 853B |
| C4 | 210B | 약 198B |
| GitHub | 63B | 약 98B (64%만 사용) |
| Wikipedia | 63B | 약 26B (2.45회 반복) |
| Books | 63B | 약 28B (2.23회 반복) |
| ArXiv | 35B | 약 33B |
| Stack Exchange | 28B | 약 27B |

- **설명할 수 있어야 하는 것:**
  - [ ] 같은 4.5%인데 Wikipedia는 2회 넘게, GitHub는 1회 미만으로 본 이유(소스 고유 크기 차이)를 표로 설명한다.
  - [ ] 비율을 바꿔 다시 학습한 비교는 원문에 없다는 점을 말한다. C4를 넣은 근거만 “탐색 실험에서 다양하게 가공한 CommonCrawl이 성능을 높였다”는 한 문장입니다.
- **함께 볼 개념:** [추론 예산과 토큰 배분](#c-token-budget) · [공개 재현: RedPajama](#c-redpajama)

<a id="c-src-cc"></a>
<a id="c-ccnet"></a>
<a id="c-ref-classifier"></a>

### CommonCrawl — 67%, 네 단계 필터

- **무엇인가:** 웹 크롤 원문입니다. 2017–2020년 덤프 5개를 [CCNet](https://arxiv.org/abs/1911.00359) 파이프라인으로 처리하고, LLaMA가 품질 분류기를 하나 더 붙였습니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2)
  1. **라인 단위 중복 제거** — 메뉴 · 푸터처럼 여러 페이지에 반복되는 줄을 지웁니다.
  2. **fastText 언어 식별** — 영어가 아닌 페이지를 버립니다.
  3. **n-gram 언어모델 품질 필터** — 저품질 콘텐츠를 거릅니다.
  4. **Wikipedia 참조 페이지 분류기 (LLaMA 추가)** — Wikipedia가 참고문헌으로 인용한 페이지와 무작위 페이지를 구분하는 선형 모델을 학습해, 참조 페이지로 분류되지 않은 페이지를 버립니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 네 단계가 각각 무엇을 버리는지 말한다.
  - [ ] 4단계가 유사도 점수가 아니라 **분류기**이며, 양성은 “Wikipedia가 인용한 페이지”, 음성은 “무작위 페이지”라는 점을 말한다.
  - [ ] 2단계 때문에 웹 데이터 전체가 영어뿐이라는 점을 [다국어 구성](#c-multilingual)과 연결한다.
- **함께 볼 개념:** [웹 품질 필터의 계보](#c-quality-lineage) · 원전: CCNet [arXiv:1911.00359](https://arxiv.org/abs/1911.00359)

<a id="c-src-c4"></a>

### C4 — 15%, 같은 웹을 다르게 거른 것

- **무엇인가:** CommonCrawl을 다른 방식으로 정제한 공개 데이터셋입니다([Raffel et al., 2020](https://arxiv.org/abs/1910.10683)).
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — 탐색 실험에서 **다양하게 가공한 CommonCrawl을 쓰면 성능이 좋아져서** C4를 넣었다고 적습니다. C4에도 중복 제거와 언어 식별이 있고, CCNet과의 주된 차이는 품질 필터입니다. C4는 구두점의 존재, 페이지의 단어 · 문장 수 같은 **휴리스틱**에 주로 의존합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] CommonCrawl(모델 기반 필터)과 C4(규칙 기반 필터)의 품질 필터 차이를 말한다.
  - [ ] 같은 원천(웹)을 두 방식으로 넣은 이유가 “다양성”이라는 저자 설명이며, 그 실험 수치는 공개되지 않았다는 점을 말한다.

<a id="c-src-github"></a>

### GitHub — 4.5%, 코드

- **무엇인가:** Google BigQuery의 공개 GitHub 데이터셋입니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2)
  - **라이선스:** Apache · BSD · MIT로 배포된 프로젝트만 남김.
  - **품질:** 줄 길이, 영숫자 비율 기반 휴리스틱으로 저품질 파일 제거.
  - **정리:** 헤더 같은 보일러플레이트를 정규식으로 제거.
  - **중복:** 파일 단위 exact match로 중복 제거.
- **설명할 수 있어야 하는 것:**
  - [ ] 일곱 소스 중 **라이선스로 거른 것은 GitHub뿐**이라는 점을 말한다.
  - [ ] epochs 0.64 = 보유량의 약 64%만 학습에 썼다는 뜻임을 말한다.
  - [ ] 원문은 코드 데이터의 언어 구성(Python 비율 등)을 적지 않는다는 점을 말한다.

<a id="c-src-wiki"></a>

### Wikipedia — 4.5%, 20개 언어

- **무엇인가:** 2022년 6–8월 Wikipedia 덤프입니다. 이 데이터셋에서 **유일하게 영어 외 언어가 명시된 소스**입니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — 라틴 또는 키릴 문자를 쓰는 20개 언어: bg, ca, cs, da, de, en, es, fr, hr, hu, it, nl, pl, pt, ro, ru, sl, sr, sv, uk. 하이퍼링크 · 주석 · 서식 보일러플레이트를 제거했습니다. 약 2.45 epochs로 반복했습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 20개 언어가 모두 유럽권 라틴 · 키릴 문자 언어이고, 한국어 · 중국어 · 일본어 · 아랍어 · 힌디어가 없다는 점을 말한다.
  - [ ] 양이 작고(83GB) 품질이 높은 소스를 업샘플링한 사례로 Books와 함께 설명한다.
- **함께 볼 개념:** [다국어 구성](#c-multilingual)

<a id="c-src-books"></a>

### Gutenberg · Books3 — 4.5%, 책

- **무엇인가:** 두 책 말뭉치입니다. Project Gutenberg는 저작권이 끝난 퍼블릭 도메인 책, Books3는 [The Pile](https://arxiv.org/abs/2101.00027)에 포함된 책 묶음입니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — **책 단위**로 중복 제거해, 내용이 90% 넘게 겹치는 책을 지웠습니다. 약 2.23 epochs. [§3.6](https://arxiv.org/pdf/2302.13971v1#page=6) — ArXiv · Gutenberg · Books3를 합쳐 177GB뿐이라 최대 2TB의 책을 쓴 비교 모델보다 MMLU가 낮다고 봅니다(저자 가설).
- **설명할 수 있어야 하는 것:**
  - [ ] 중복 제거 단위가 소스마다 다르다(웹 라인 · 코드 파일 · 책 단위)는 점을 말한다.
  - [ ] 책 데이터 양과 MMLU 열세를 잇는 것은 저자 가설이라는 점을 말한다.
- **함께 볼 개념:** [Books3와 ‘공개 데이터’의 경계](#c-books3)

<a id="c-src-arxiv"></a>

### ArXiv — 2.5%, 과학 논문

- **무엇인가:** 과학 데이터를 더하려고 넣은 arXiv 논문의 LaTeX 원본입니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — Minerva(Lewkowycz et al., 2022)를 따라 **첫 절 이전의 내용과 참고문헌**을 지우고, .tex의 **주석**을 지우고, 사용자가 정의한 **매크로를 본문에 펼쳐(inline-expand)** 논문 사이의 표기를 맞췄습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] PDF가 아니라 LaTeX 원본을 쓴 점과, 매크로 전개가 왜 일관성에 도움이 되는지 예로 설명한다(예: `\R`이 논문마다 다른 뜻).
  - [ ] 이 전처리가 Minerva의 수학 데이터 처리를 따른 것이라는 출처를 말한다.

<a id="c-src-se"></a>

### Stack Exchange — 2%, 질문과 답변

- **무엇인가:** 컴퓨터 과학부터 화학까지 여러 분야의 고품질 Q&A 사이트 덤프입니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — 규모가 큰 상위 28개 사이트만 남기고, HTML 태그를 지우고, 답변을 **점수 높은 순으로 정렬**했습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 답변을 점수순으로 놓으면 질문 뒤에 좋은 답이 먼저 오는 텍스트가 된다는 점을 말한다(추출자 해석).
  - [ ] 28개 사이트 목록은 원문에 없다는 점을 말한다.

<a id="c-multilingual"></a>

### 다국어 구성

- **무엇인가:** LLaMA 1 데이터에서 언어가 어떻게 정해졌는지입니다. 언어는 별도 비율로 정하지 않았고, 소스별 처리의 결과로 정해집니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2)
  - **웹 82% (CommonCrawl · C4):** 언어 식별로 비영어 페이지를 버림 → 영어만.
  - **Wikipedia 4.5%:** 20개 라틴 · 키릴 문자 언어.
  - **Books · ArXiv · Stack Exchange:** 언어 필터는 기술되지 않음.
  - **Tokenizer:** 어휘에 없는 UTF-8 문자는 바이트로 분해 → 한국어도 토큰화는 되지만 길게 쪼개질 수 있음.
- **후속 비교 (논문 밖):** 같은 tokenizer를 쓴 Llama 2는 사전학습 데이터의 언어 분포를 공개했습니다. 영어 89.70%, unknown 8.38%(코드 일부 포함), 독일어 0.17%, 프랑스어 0.16%, 중국어 0.13%, 일본어 0.10%, **한국어 0.06%**([Llama 2 Table 10](https://arxiv.org/abs/2307.09288)). LLaMA 1의 언어 분포는 공개되지 않았습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA 1이 사실상 영어 모델인 이유를 소스별 처리로 설명한다.
  - [ ] 원문에는 다국어 평가가 없다는 점을 말한다.
- **함께 볼 개념:** [CommonCrawl](#c-src-cc) · [Wikipedia](#c-src-wiki) · [숫자 분리와 byte fallback](#c-digit-byte)

<a id="c-bpe"></a>

### BPE와 SentencePiece

- **무엇인가:** BPE는 자주 붙어 나오는 문자열을 반복해 합쳐 어휘를 만드는 subword 분절 방법이고, SentencePiece는 이를 구현한 라이브러리입니다.
- **원문:** [§2.1 Tokenizer](https://arxiv.org/pdf/2302.13971v1#page=2) — SentencePiece 구현의 BPE로 토큰화했고, 전체 학습 데이터는 토큰화 후 약 1.4T 토큰입니다([p.3](https://arxiv.org/pdf/2302.13971v1#page=3)). 원문은 어휘 크기를 적지 않습니다. 흔히 인용되는 32,000은 공개된 모델 설정 값이며, Llama 2 논문이 “Llama 1과 같은 tokenizer, 어휘 32k”라고 적습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] BPE가 어휘를 만드는 과정을 예시로 설명한다.
  - [ ] tokenizer가 학습 토큰 수(1.0T · 1.4T)의 단위를 정한다는 점을 말한다.
- **함께 볼 개념:** [숫자 분리와 byte fallback](#c-digit-byte) · 원전: BPE [arXiv:1508.07909](https://arxiv.org/abs/1508.07909v1) §3.2

<a id="c-digit-byte"></a>

### 숫자 분리와 byte fallback

- **무엇인가:** 모든 숫자를 한 자리씩 나누고(digit splitting), 어휘에 없는 UTF-8 문자는 바이트로 분해하는(byte fallback) 두 가지 tokenizer 규칙입니다.
- **원문:** [§2.1 Tokenizer](https://arxiv.org/pdf/2302.13971v1#page=2) — 두 규칙을 썼다고만 적고 효과는 실험하지 않습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] `1234`가 네 토큰으로 나뉘는 예를 들고, 숫자 표현이 일관된다는 의도를 말한다(추출자 해석).
  - [ ] byte fallback 덕분에 어휘에 없는 문자도 unknown 토큰 없이 표현된다는 점을 설명한다.
- **함께 볼 개념:** [BPE와 SentencePiece](#c-bpe)

<a id="c-redpajama"></a>

### 공개 재현: RedPajama · SlimPajama

- **무엇인가 (논문 밖):** LLaMA는 소스와 전처리를 적었지만 데이터 자체는 배포하지 않았습니다. 2023년 4월 Together AI 등이 Table 1의 레시피를 따라 만든 [RedPajama-Data-1T](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T)가 약 1.2T 토큰으로 공개됐습니다. 이후 Cerebras가 이를 강하게 중복 제거한 SlimPajama(627B 토큰)를 냈습니다.

| 소스 | LLaMA 고유 토큰(추정, 위 계산) | RedPajama-Data-1T |
| --- | --- | --- |
| CommonCrawl | 약 853B | 878B |
| C4 | 약 198B | 175B |
| GitHub | 약 98B | 59B |
| Wikipedia | 약 26B | 24B |
| Books | 약 28B | 현재 비공개(저작권 문제로 중단) |
| ArXiv | 약 33B | 28B |
| Stack Exchange | 약 27B | 20B |

- **설명할 수 있어야 하는 것:**
  - [ ] Table 1의 비율 · epochs로 소스 크기를 역산하면 공개 재현본과 규모가 비슷하다는 점을 보인다(추출자 계산).
  - [ ] “레시피 공개”와 “데이터 공개”가 다르다는 점, 그래서 재현 데이터셋이 따로 필요했다는 점을 말한다.
- **함께 볼 개념:** [Sampling 비율과 epochs](#c-sampling) · [Books3와 ‘공개 데이터’의 경계](#c-books3)

<a id="c-llama-data"></a>

### Llama 2 · Llama 3의 데이터

- **무엇인가 (논문 밖):** 같은 계열의 후속 모델에서 데이터 설명이 어떻게 바뀌었는지입니다.

| 항목 | LLaMA 1 (2023.02) | Llama 2 (2023.07) | Llama 3 (2024.07) |
| --- | --- | --- | --- |
| 학습 토큰 | 1.0T / 1.4T | 2T | 약 15T (405B는 15.6T) |
| 소스 공개 | 7개 소스 · 비율 · 전처리 모두 기술 | “공개 소스의 새로운 혼합”만 기술 | 영역별 비율만: 일반 지식 50% · 수학·추론 25% · 코드 17% · 다국어 8% |
| 정제 | CCNet + Wikipedia 참조 페이지 분류기 | 개인정보가 많은 사이트 제거, 가장 사실적인 소스 업샘플링 | URL · 문서(MinHash) · 라인 단위 dedup, 휴리스틱, 모델 기반 품질 분류기 |
| 다국어 | 웹은 영어, Wikipedia 20개 언어 | 영어 89.70% · 한국어 0.06% | 176개 언어 식별, 언어별 dedup · 품질 순위 |
| Tokenizer | SentencePiece BPE | LLaMA 1과 동일, 32k | 128K (tiktoken 100K + 비영어 28K) |

- **설명할 수 있어야 하는 것:**
  - [ ] 토큰 수는 1.4T → 2T → 15T로 늘었지만, **소스 공개 범위는 오히려 줄었다**는 점을 말한다.
  - [ ] Llama 3의 “Wikipedia가 인용할 만한 텍스트인가”를 예측하는 fastText 분류기가 LLaMA 1의 참조 페이지 분류기와 같은 발상이라는 점을 연결한다.
  - [ ] Llama 3 논문은 Llama 2를 1.8T 토큰으로 적어, Llama 2 논문의 2T와 다르다는 점을 확인한다.
- **함께 볼 개념:** [웹 품질 필터의 계보](#c-quality-lineage) · 원전: [Llama 2](https://arxiv.org/abs/2307.09288) §2.1–§2.2 · [Llama 3](https://arxiv.org/abs/2407.21783) §3.1–§3.2

<a id="c-quality-lineage"></a>

### 웹 품질 필터의 계보

- **무엇인가 (논문 밖):** 웹 데이터를 “좋은 글처럼 보이는가”로 거르는 분류기 기반 필터가 어떻게 이어졌는지입니다.
  1. **GPT-3 (2020)** — WebText · 책 · Wikipedia 같은 고품질 말뭉치와 원시 CommonCrawl을 구분하는 분류기로 웹을 걸렀습니다.
  2. **LLaMA 1 (2023.02)** — Wikipedia가 **참고문헌으로 인용한 페이지**를 양성으로 둔 선형 분류기.
  3. **RefinedWeb (2023.06)** — 큐레이션 말뭉치 없이 **웹만** 엄격히 거르고 중복 제거해도 강한 모델이 나온다고 주장. CommonCrawl에서 5T 토큰, 그중 600B 공개([arXiv:2306.01116](https://arxiv.org/abs/2306.01116)).
  4. **FineWeb · FineWeb-Edu (2024)** — CommonCrawl 96개 스냅숏에서 15T 토큰. 교육적 가치를 매기는 분류기로 1.3T 토큰을 골라낸 FineWeb-Edu가 MMLU · ARC에서 크게 좋았다고 보고([arXiv:2406.17557](https://arxiv.org/abs/2406.17557)).
  5. **Llama 3 (2024.07)** — “Wikipedia가 인용할 만한가”를 예측하는 fastText 분류기와, Llama 2의 판단을 학습한 RoBERTa 계열 분류기.
- **설명할 수 있어야 하는 것:**
  - [ ] 양성 예시를 무엇으로 정했는지(고품질 말뭉치 → 인용된 페이지 → LLM의 판단)가 세대마다 바뀌었다는 흐름을 말한다.
  - [ ] LLaMA 1의 분류기는 이 계보의 한 단계이며, 원문에는 그 효과를 따로 잰 실험이 없다는 점을 말한다.
- **함께 볼 개념:** [CommonCrawl](#c-src-cc) · [Llama 2 · Llama 3의 데이터](#c-llama-data)

<a id="c-books3"></a>

### Books3와 ‘공개 데이터’의 경계

- **무엇인가 (논문 밖):** 논문의 “publicly available”은 **누구나 받을 수 있다**는 뜻이지, **써도 된다는 허가**를 보장하지 않았습니다.
- **원문:** [§2.1](https://arxiv.org/pdf/2302.13971v1#page=2) — Books3를 “a publicly available dataset for training large language models”로 소개합니다. 라이선스로 거른 소스는 GitHub뿐입니다.
- **이후:** Books3는 저작권 있는 책을 담고 있어 2023년 이후 저작권 소송(예: Kadrey v. Meta)의 쟁점이 되었고, 배포가 중단됐습니다. RedPajama도 Books 슬라이스를 저작권 문제로 내렸습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] “공개됨”과 “사용 허가됨”의 차이를 Books3로 설명한다.
  - [ ] Llama 2 · 3가 소스 목록을 공개하지 않게 된 흐름과 연결해 토론 질문으로 남긴다(추출자 해석).

<!-- part: post -->
## Post-training

### 이 파트의 질문

- **RQ1. LLaMA-I는 무엇을 학습했고, 무엇이 기술되지 않았나?**
  - 필수 원문: [§4 Instruction Finetuning · Table 10](https://arxiv.org/pdf/2302.13971v1#page=7) · [App. D](https://arxiv.org/pdf/2302.13971v1#page=22)
  - 개념: [Instruction finetuning](#c-instruction-ft) · [Flan 프로토콜](#c-flan)
  - 함께 맡기 제안: Architecture RQ4의 [zero-shot · few-shot 프롬프트](#c-fewshot)와 MMLU 결과

<a id="c-instruction-ft"></a>

### Instruction finetuning

- **무엇인가:** 지시문과 응답 쌍으로 사전학습 모델을 짧게 지도 학습해 지시를 따르게 만드는 단계입니다.
- **원문:** [§4 · Table 10](https://arxiv.org/pdf/2302.13971v1#page=7) — 아주 적은 양의 instruction 데이터로 파인튜닝하면 MMLU가 오른다고 적습니다. LLaMA-65B 63.4 → LLaMA-I 65B 68.9(MMLU 5-shot). 비교: Flan-PaLM-cont 62B 66.1, OPT-IML-Max 30B 43.2. 당시 최고인 code-davinci-002 77.4에는 못 미칩니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 63.4 → 68.9가 +5.5 percentage points의 차이라는 점을 말한다.
  - [ ] 이 실험은 한 번이며, 평가는 MMLU 하나이고 사람 평가는 없다는 범위를 말한다.
  - [ ] 데이터 양 · step · 학습률은 원문에 기술되지 않았다는 점을 말한다.
- **함께 볼 개념:** [Flan 프로토콜](#c-flan) · [측정과 정렬 학습의 구분](#c-measure-vs-align)

<a id="c-flan"></a>

### Flan 프로토콜

- **무엇인가:** 공개 NLP 데이터셋의 과제들을 지시문 템플릿으로 바꿔 모은 instruction 데이터와 그 파인튜닝 방식입니다(Chung et al., 2022).
- **원문:** [§4](https://arxiv.org/pdf/2302.13971v1#page=7) · [App. D](https://arxiv.org/pdf/2302.13971v1#page=22) — Chung et al.(2022)의 프로토콜과 instruction 데이터셋을 따랐다고만 적고, 부록 D에 생성 예시를 싣습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA-I의 설정은 원문이 아니라 Chung et al.에 기대고 있다는 점을 말한다.
  - [ ] 부록 D의 예시는 정량 평가가 아니라 생성 사례라는 점을 구분한다.
- **함께 볼 개념:** 원전: Scaling Instruction-Finetuned Language Models [arXiv:2210.11416](https://arxiv.org/abs/2210.11416)

<!-- part: alignment -->
## Alignment & RL

### 이 파트의 질문

- **RQ1. 사전학습 모델의 위험을 무엇으로 측정했나?**
  - 필수 원문: [§5 · Table 11](https://arxiv.org/pdf/2302.13971v1#page=8) · [Table 12](https://arxiv.org/pdf/2302.13971v1#page=9) · [Table 13–14](https://arxiv.org/pdf/2302.13971v1#page=10)
  - 개념: [RealToxicityPrompts](#c-rtp) · [CrowS-Pairs](#c-crows) · [WinoGender](#c-winogender) · [TruthfulQA](#c-truthfulqa)
- **RQ2. 정렬 학습(RLHF 등)은 있었나?**
  - 필수 원문: [§4–§5](https://arxiv.org/pdf/2302.13971v1#page=7)
  - 개념: [측정과 정렬 학습의 구분](#c-measure-vs-align)
- **RQ3. 학습의 환경 비용은 얼마로 추정했나?**
  - 필수 원문: [§6 · Table 15](https://arxiv.org/pdf/2302.13971v1#page=11)
  - 개념: [탄소 발자국 추정](#c-carbon)

<a id="c-rtp"></a>

### RealToxicityPrompts

- **무엇인가:** 약 10만 개 프롬프트를 모델이 이어 쓰게 하고, 그 완성문의 독성 점수(0–1)를 외부 PerspectiveAPI로 매기는 벤치마크입니다.
- **원문:** [§5.1 · Table 11](https://arxiv.org/pdf/2302.13971v1#page=8) — greedy 생성. Basic 7B 0.106 → 65B 0.128, “정중하게” 지시를 붙인 Respectful 7B 0.081 → 65B 0.141. 모델이 클수록 독성이 늘었습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] Basic과 Respectful 조건의 차이를 말한다.
  - [ ] 크기와 함께 독성이 늘었다는 관찰과, 다른 논문 수치와의 비교에 저자가 단서를 단 점을 말한다.
- **함께 볼 개념:** [측정과 정렬 학습의 구분](#c-measure-vs-align)

<a id="c-crows"></a>

### CrowS-Pairs

- **무엇인가:** 고정관념 문장과 반고정관념 문장 쌍에서 모델이 어느 쪽을 더 선호하는지(perplexity 비교)로 9개 범주의 편향을 재는 벤치마크입니다. 높을수록 편향이 큽니다.
- **원문:** [§5.2 · Table 12](https://arxiv.org/pdf/2302.13971v1#page=9) — LLaMA-65B 평균 66.6(GPT-3 67.2, OPT-175B 69.5). 종교 79.0, 나이 70.1, 성별 70.6에서는 비교 모델보다 높습니다. 저자는 필터를 거쳤어도 CommonCrawl이 원인일 것으로 추정합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 평균은 비교 모델보다 약간 낮지만 범주별로는 더 높은 곳이 있다는 점을 표에서 보인다.
  - [ ] CommonCrawl 원인은 저자 추정이라는 점을 말한다.
- **함께 볼 개념:** [Sampling 비율과 epochs](#c-sampling) · [WinoGender](#c-winogender)

<a id="c-winogender"></a>

### WinoGender

- **무엇인가:** 직업명과 대명사의 공지시 해소 정확도로 성별 편향을 보는 벤치마크입니다. 대명사가 직업의 다수 성별과 어긋나는 “gotcha” 문장에서 정확도가 떨어지면 편향 신호로 봅니다.
- **원문:** [§5.3 · Table 13](https://arxiv.org/pdf/2302.13971v1#page=10) — 65B는 their/them/someone 81.7, her/her/she 78.8, his/him/he 72.1, his/him/he gotcha 63.3.
- **설명할 수 있어야 하는 것:**
  - [ ] gotcha 문장이 무엇이고 왜 편향을 드러내는지 예시로 설명한다.
  - [ ] 성 중립 대명사에서 정확도가 가장 높다는 관찰을 말한다.
- **함께 볼 개념:** [CrowS-Pairs](#c-crows)

<a id="c-truthfulqa"></a>

### TruthfulQA

- **무엇인가:** 사람들이 흔히 믿는 오개념으로 유도하도록 만든 질문에서 모델 답이 사실인지(truthful), 사실이면서 정보가 있는지(truthful × informative)를 재는 벤치마크입니다.
- **원문:** [§5.4 · Table 14](https://arxiv.org/pdf/2302.13971v1#page=10) — 65B 0.57 / 0.53, GPT-3 175B 0.28 / 0.25. 채점은 OpenAI API의 판정 모델, 프롬프트 형식은 Ouyang et al.(2022)을 따랐습니다. 저자는 정답률이 여전히 낮아 환각 가능성이 크다고 봅니다.
- **설명할 수 있어야 하는 것:**
  - [ ] GPT-3보다 높지만 절대치는 낮다는 두 측면을 함께 말한다.
  - [ ] 채점이 외부 판정 모델에 의존한다는 조건을 말한다.
- **함께 볼 개념:** [측정과 정렬 학습의 구분](#c-measure-vs-align)

<a id="c-measure-vs-align"></a>

### 측정과 정렬 학습의 구분

- **무엇인가:** 모델의 위험을 **측정**하는 평가와, 사람 선호 · 보상으로 모델을 **바꾸는** 정렬 학습(RLHF 등)은 다른 단계입니다.
- **원문:** [§5](https://arxiv.org/pdf/2302.13971v1#page=7) — 네 벤치마크로 사전학습 모델을 측정했고, 이 평가들로는 위험을 충분히 이해할 수 없다고 저자 스스로 적습니다. 보상 모델 · RLHF 같은 정렬 학습은 원문에 기술되지 않았습니다.
- **설명할 수 있어야 하는 것:**
  - [ ] §5가 측정이라는 점을 말하고, “RLHF를 했다”거나 “해 봤더니 효과가 없었다”로 읽지 않는다(미기술).
  - [ ] 네 평가 모두 영어이며 사전학습 모델 대상이라는 범위를 말한다.
- **함께 볼 개념:** [Instruction finetuning](#c-instruction-ft) · Llama 2(W02)에서 이 칸이 채워집니다.

<a id="c-carbon"></a>

### 탄소 발자국 추정

- **무엇인가:** GPU 사용 시간과 전력, 데이터센터 효율(PUE), 전력망 탄소 집약도로 학습의 전력량과 CO₂ 배출을 추정하는 방법입니다.
- **원문:** [§6 · Table 15](https://arxiv.org/pdf/2302.13971v1#page=11) — Wu et al.(2022)의 식, A100 400W · PUE 1.1 · 0.385 kg CO₂eq/kWh 가정. LLaMA-65B 449 MWh · 173 tCO₂eq, OPT-175B 356 MWh, BLOOM-175B 475 MWh(같은 데이터센터 가정). 개발 전체는 약 5개월 · 2,638 MWh · 1,015 tCO₂eq로 추정합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 비교 모델을 실제 위치가 아니라 같은 데이터센터 가정으로 다시 계산했다는 조건을 말한다.
  - [ ] 최종 모델 네 개와 개발 전체의 추정치가 다르다는 점을 말한다.

<!-- part: background -->
## Background

### 이번에 새로 채울 빈 영역

W01은 스터디의 첫 논문입니다. 지금까지 다룬 것은 참여 전제인 원 Transformer와 LLM의 기본 학습 과정뿐입니다. 아래는 그 뒤 **중간 논문에서 처음 나왔고 LLaMA 1이 가져다 쓴** 개념으로, 이번에 새로 공부해야 합니다.

| 개념 | 처음 나온 논문 | LLaMA 1에서 쓰인 곳 | 이전 주차 | 같이 볼 파트 |
| --- | --- | --- | --- | --- |
| [Pre-normalization](#c-prenorm) | LLaMA는 GPT-3(Brown et al., 2020)를 출처로 표기 | §2.2 | 처음 | Architecture |
| [RMSNorm](#c-rmsnorm) | Zhang & Sennrich, 2019 | §2.2 | 처음 | Architecture |
| [SwiGLU](#c-swiglu) | Shazeer, 2020 제안 · PaLM(2022) 채택 | §2.2 | 처음 | Architecture |
| [RoPE](#c-rope) | Su et al., 2021(RoFormer) · GPTNeo 채택 | §2.2 | 처음 | Architecture |
| [AdamW](#c-adamw) | Loshchilov & Hutter, 2017 | §2.3 | 처음 | Architecture |
| [스케일링 법칙과 compute-optimal](#c-scaling) | Kaplan et al., 2020 → Hoffmann et al., 2022(Chinchilla) | §1 · §2 도입 | 처음 | Architecture |
| [Chinchilla 손실 식](#c-chinchilla-loss) | Hoffmann et al., 2022 §3.3 | §1 해석 | 처음 | Architecture |
| [메모리 효율 causal attention](#c-efficient-attention) | Rabe & Staats, 2021 · Dao et al., 2022 | §2.4 | 처음 | Architecture |
| [Model · sequence parallelism](#c-parallelism) | Korthikanti et al., 2022 | §2.4 | 처음 | Architecture |
| [zero-shot · few-shot 프롬프트](#c-fewshot) | Brown et al., 2020(GPT-3) | §3 | 처음 | Architecture |
| [길이 정규화](#c-length-norm) | Brown et al., 2020 · Gao et al., 2021(lm-evaluation-harness) | §3 | 처음 | Architecture |
| [CCNet 파이프라인](#c-ccnet) | Wenzek et al., 2020 | §2.1 | 처음 | Data |
| [BPE와 SentencePiece](#c-bpe) | Sennrich et al., 2016 · Kudo & Richardson, 2018 | §2.1 | 처음 | Data |
| [Flan 프로토콜](#c-flan) | Chung et al., 2022 | §4 | 처음 | Post-training |
| 위험 평가 벤치마크 4종 | RealToxicityPrompts 2020 · CrowS-Pairs 2020 · WinoGender 2018 · TruthfulQA 2021 | §5 | 처음 | Alignment |

원전은 각 개념 페이지에 적은 절만 읽습니다. LLaMA의 조합을 각 원전의 새 제안으로 되돌려 쓰지 않습니다.

### 이 파트의 질문

- **RQ1. LLaMA 1을 읽으려면 어떤 비교 기준과 배경을 먼저 알아야 하나?**
  - 필수 원문: [§1](https://arxiv.org/pdf/2302.13971v1#page=1) · [§3](https://arxiv.org/pdf/2302.13971v1#page=4) · 아래 원전의 지정 절
  - 개념: [이전 → LLaMA 1 → 현재](#c-then-now) · [원 Transformer 디코더 블록](#c-transformer-base) · [스케일링 법칙 ①](#c-scaling) · [스케일링 법칙 ②](#c-chinchilla-loss) · [큰 모델일수록 loss가 낮은 이유](#c-size-loss) · [zero-shot · few-shot 프롬프트](#c-fewshot)
- **RQ2. 위 빈 영역의 개념은 각각 어느 논문에서 처음 나왔고, LLaMA는 무엇을 가져왔나?**
  - 필수 원문: 빈 영역 표의 원전
  - 개념: 표의 각 개념 페이지(담당 파트와 함께 준비)

<a id="c-then-now"></a>

### 이전 → LLaMA 1 → 현재(2026): 세 주제 비교

| 주제 | LLaMA 1 이전 (2020–2022) | LLaMA 1 (2023.02) | 현재 (2026) |
| --- | --- | --- | --- |
| 모델 크기 | 크게 · 짧게: Kaplan(2020) N ∝ C^0.73 → GPT-3 175B · 300B 토큰, PaLM 540B. Chinchilla(2022)가 덜 학습됐다고 지적 | 작게 · 오래: 추론 비용 기준, 7B · 1T 토큰(파라미터당 149) | 총량은 크게, 활성은 작게: DeepSeek-V4-Pro 1.6T / 49B, Kimi K2 1T / 32B, MiMo-V2-Flash 309B / 15B. 활성 파라미터당 학습 토큰은 수백–1,800 |
| 만드는 방식 | 크기마다 처음부터 | 7B–65B를 각각 처음부터 | 큰 모델을 pruning + 증류로 줄이기(Minitron · Kanana 8B → 2.1B), 작은 모델을 키우기(SOLAR DUS · Kanana · Solar Open 2 weight transfer) |
| 데이터 | 비공개 · 미문서화(“Books – 2TB”), 300B 토큰 수준 | 공개 소스 7개 · 1.4T · 레시피 공개 | 10–36T 토큰, LLM 기반 품질 선별 · 합성 데이터, 다국어 확대(Qwen3 119개 언어), 비율은 대부분 비공개 |
| 안전 평가 | 생성문 독성 · 편향 분석 | 사전학습 모델에 4종 측정, 정렬 학습 없음 | 위반율과 과잉 거부율(Llama 3 · XSTest), jailbreak(HarmBench · StrongREJECT), CBRNE · 사이버 uplift, 에이전트 prompt injection |

- **왜 다시 커지나:** MoE가 총 파라미터(용량)와 활성 파라미터(토큰당 비용)를 분리했고, 고품질 데이터가 유한하며, 큰 모델이 증류의 teacher가 되고, MLA · sparse attention · FP8 · MTP가 큰 모델의 서빙 비용을 낮췄습니다. LLaMA 1의 추론 비용 논리는 활성 파라미터 위에서 계속됩니다.
- **설명할 수 있어야 하는 것:**
  - [ ] LLaMA 1 이전에 큰 모델을 택한 이유와 LLaMA 1이 작은 모델을 오래 학습한 이유를 각각 말한다.
  - [ ] 2026년 모델이 다시 커진 이유를 MoE의 총 · 활성 파라미터로 설명한다.
  - [ ] LLaMA 1의 네 위험 벤치마크가 지금의 채팅 · 에이전트 안전 평가와 무엇이 다른지 말한다.
- **출처:** [Sardana et al. 2024](https://arxiv.org/abs/2401.00448) · [DeepSeek-V4](https://arxiv.org/abs/2606.19348v1) · [Kimi K2](https://arxiv.org/abs/2507.20534) · [Kanana](https://arxiv.org/abs/2502.18934) · [Minitron](https://arxiv.org/abs/2408.11796) · [SOLAR](https://arxiv.org/abs/2312.15166) · [Llama 3 §5.4](https://arxiv.org/abs/2407.21783) · [Olmo 3](https://arxiv.org/abs/2512.13961)

<a id="c-transformer-base"></a>

### 원 Transformer 디코더 블록

- **무엇인가:** LLaMA가 바꾸기 전의 기준점입니다. attention과 FFN 두 sublayer를 잔차 연결로 감싸고, 출력에서 LayerNorm(post-norm), FFN은 ReLU, 위치는 입력 embedding에 더합니다.
- **원문:** [§2.2](https://arxiv.org/pdf/2302.13971v1#page=3) — LLaMA는 이 구조(Vaswani et al., 2017)를 기반으로 세 가지를 바꿨다고 적습니다. 스터디 참여 전제라 새 개념은 아니지만, 비교의 기준이라 다시 확인합니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 정규화 위치 · FFN 활성화 · 위치 정보의 세 자리에서 원 Transformer와 LLaMA를 나란히 말한다.
- **함께 볼 개념:** [Pre-normalization](#c-prenorm) · [SwiGLU](#c-swiglu) · [RoPE](#c-rope) · 원전: Transformer [arXiv:1706.03762](https://arxiv.org/abs/1706.03762v7) §3.1 · §3.3 · §3.5

<a id="c-scaling"></a>

### 스케일링 법칙 ①: Kaplan(2020)에서 Chinchilla(2022)로

- **무엇인가:** 모델 크기 N · 학습 토큰 D · compute C와 loss의 관계를 멱법칙으로 맞춘 연구입니다. 핵심 질문은 **“학습 compute가 정해졌을 때 N과 D를 어떻게 나눠야 loss가 가장 낮은가”**입니다(학습 compute ≈ 6ND).
- **원문:** [§1](https://arxiv.org/pdf/2302.13971v1#page=1) — “for a given compute budget, the best performances are not achieved by the largest models, but by smaller models trained on more data.” LLaMA의 출발점이 이 문장입니다.
- **두 연구의 결론 (원전):**

| | Kaplan et al. (2020) | Hoffmann et al. (2022, Chinchilla) |
| --- | --- | --- |
| compute가 늘 때 | 모델 크기를 주로 키움: N ∝ C^0.73, D ∝ C^0.27 | 둘을 같은 비율로: N ∝ C^≈0.5, D ∝ C^≈0.5 |
| 근거 | 고정된 학습률 스케줄로 여러 크기 학습 | 70M–16B 모델 400개 이상을 5B–500B 토큰으로 학습, 세 가지 방법(a = 0.50 / 0.49 / 0.46)이 같은 방향 |
| 실천 | GPT-3 175B · 300B 토큰, Gopher 280B · 300B 토큰 | 파라미터당 약 20토큰: 10B → 205.1B 토큰, 67B → 1.5T 토큰 |
| 검증 | – | Gopher와 같은 compute로 70B를 4배 많은 1.4T 토큰에 학습한 Chinchilla가 Gopher · GPT-3를 앞섬. MMLU 67.5%(Gopher보다 7%p 이상 높음) |

- **설명할 수 있어야 하는 것:**
  - [ ] Chinchilla의 질문과 결론(“모델 크기를 두 배로 하면 토큰도 두 배로”)을 말한다.
  - [ ] Kaplan과 결론이 달랐던 주된 이유로 Chinchilla가 학습률 스케줄(cosine 주기를 학습 길이에 맞추지 않은 점)을 든다는 것을 말한다.
  - [ ] “10B에 200B 토큰”이라는 LLaMA §1의 인용이 Chinchilla Table 3(10B → 205.1B)에서 나왔다는 점을 연결한다.
- **함께 볼 개념:** [스케일링 법칙 ②: 손실 식](#c-chinchilla-loss) · 원전: Kaplan [arXiv:2001.08361](https://arxiv.org/abs/2001.08361) · Chinchilla [arXiv:2203.15556](https://arxiv.org/abs/2203.15556v1) §1 · §3 · Table 2–3

<a id="c-chinchilla-loss"></a>

### 스케일링 법칙 ②: 손실 식과 LLaMA의 해석

- **무엇인가:** Chinchilla의 세 번째 방법은 loss를 N과 D의 함수로 맞춥니다.

  `L(N, D) = E + A / N^α + B / D^β`  (E = 1.69, A = 406.4, B = 410.7, α = 0.34, β = 0.28)

  - **E:** 데이터 자체의 엔트로피. 아무리 큰 모델도 넘을 수 없는 바닥.
  - **A / N^α:** 모델이 유한해서 생기는 손실. N이 커질수록 줄어듭니다.
  - **B / D^β:** 학습을 유한한 데이터로 끝내서 생기는 손실. D가 커질수록 줄어듭니다.
- **원문과의 연결:** Chinchilla는 6ND = C 제약에서 이 식을 최소화합니다. LLaMA는 같은 식을 **N을 고정하고 D를 늘리는 쪽**으로 읽습니다. 추론 비용을 정하는 N을 고정해도 B / D^β 항은 D가 커질수록 계속 줄어들기 때문입니다.
- **계산해 보면 (추출자 계산, Chinchilla 적합식 그대로):**

| 모델 · 토큰 | 추정 loss | 학습 compute 6ND |
| --- | --- | --- |
| 7B · 134B (≈ 20토큰/파라미터) | 2.19 | 5.4 × 10²¹ |
| 7B · 1.0T | 2.06 | 4.0 × 10²² |
| 13B · 1.0T | 2.02 | 7.8 × 10²² |
| 65B · 1.4T | 1.94 | 5.5 × 10²³ |

  Chinchilla의 데이터 · tokenizer 기준 적합식이라 LLaMA의 실제 loss 값과는 다릅니다. 모양 비교용입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] 식의 세 항이 각각 무엇을 뜻하는지 말한다.
  - [ ] 7B를 권장치(약 134B)보다 7배 넘게 학습해도 loss가 계속 내려가지만, 내려가는 폭은 점점 작아진다는 점을 표로 보인다.
  - [ ] LLaMA가 Chinchilla를 반박한 것이 아니라 **목적을 바꿨다**(학습 compute 최소 → 추론 비용 고려)는 점을 말한다.
- **함께 볼 개념:** [큰 모델일수록 loss가 낮은 이유](#c-size-loss) · [추론 예산과 토큰 배분](#c-token-budget)

<a id="c-size-loss"></a>

### 큰 모델일수록 loss가 낮은 이유

- **무엇인가:** Fig. 1에서 같은 토큰 수를 보면 언제나 65B < 33B < 13B < 7B 순으로 loss가 낮습니다. 이것은 당연한 법칙이 아니라 **경험적으로 반복 관찰된 현상**입니다. 조건이 맞을 때만 성립합니다.
- **원문:** [Fig. 1](https://arxiv.org/pdf/2302.13971v1#page=3) — 그림에서 읽은 근삿값으로 7B 약 1.80 · 13B 약 1.73(1.0T), 33B 약 1.62 · 65B 약 1.56(1.4T). 원문은 이 현상의 이유를 설명하지 않습니다.
- **왜 그런가 (배경 설명):**
  - **표현력:** 파라미터가 많으면 데이터의 더 많은 패턴을 담을 수 있습니다. 손실 식의 A / N^α 항이 이 한계입니다.
  - **표본 효율:** Kaplan et al.(2020)은 큰 모델이 같은 토큰 수에서 더 빨리 loss를 낮춘다고 보고했습니다. Fig. 1에서 200B 토큰 지점만 봐도 큰 모델이 아래에 있습니다.
  - **과적합이 없는 영역:** 대부분의 토큰을 한 번만 보는 학습이라, 큰 모델이 데이터를 외워 망가지는 영역에 들어가지 않습니다.
- **성립하지 않는 경우:** 학습률 등 하이퍼파라미터가 크기에 맞지 않으면(그래서 큰 두 모델의 최대 학습률이 절반), 데이터가 부족해 같은 데이터를 많이 반복하면, **compute가 고정**되면 큰 모델이 오히려 불리할 수 있습니다. 마지막이 Chinchilla의 결론입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] “같은 토큰 수에서”와 “같은 compute에서”의 비교가 다르다는 점을 말한다. 같은 토큰이면 큰 모델이 낮고, 같은 compute면 꼭 그렇지 않습니다.
  - [ ] Fig. 1의 곡선이 1.0T · 1.4T에서도 아직 평평해지지 않았다는 점을 RQ2(권장치를 넘겨도 좋아지나)의 근거로 말한다.
  - [ ] 곡선의 순간적인 튐(loss spike)을 짚고, 원문은 이를 설명하지 않는다는 점을 말한다.
- **함께 볼 개념:** [스케일링 법칙 ②](#c-chinchilla-loss) · [Gradient clipping](#c-clipping) · [학습 중 성능 추적](#c-training-curve)

<a id="c-fewshot"></a>

### zero-shot · few-shot 프롬프트

- **무엇인가:** 가중치를 바꾸지 않고 프롬프트만 바꿔 평가하는 방식입니다(GPT-3, Brown et al., 2020).
- **원문:** [§3](https://arxiv.org/pdf/2302.13971v1#page=4)
  - **Zero-shot:** 과제 설명과 테스트 예시 하나를 준다. 모델은 답을 생성하거나 보기에 순위를 매긴다.
  - **Few-shot:** 과제 예시 1–64개와 테스트 예시 하나를 준다. 모델은 이를 입력으로 답을 생성하거나 보기에 순위를 매긴다.
- **실제 프롬프트 (원문 App. A · Fig. 3, Natural Questions):**

  Zero-shot

  ```
  Answer these questions:
  Q: Who wrote the book the origin of species?
  A:
  ```

  1-shot — 풀이 예시 한 쌍을 앞에 붙입니다

  ```
  Answer these questions:
  Q: Who sang who wants to be a millionaire in high society?
  A: Frank Sinatra
  Q: Who wrote the book the origin of species?
  A:
  ```

  모델이 이어 쓴 `Charles Darwin`을 [exact match](#c-greedy-em)로 채점합니다. 64-shot이면 예시 쌍이 64개입니다.
- **설명할 수 있어야 하는 것:**
  - [ ] zero-shot · few-shot과 파인튜닝의 차이(가중치 갱신 여부)를 말한다.
  - [ ] few-shot 예시는 답의 **형식**(짧게 · 한 줄로)을 알려주는 역할도 한다는 점을 말한다(추출자 해석). NQ 65B가 0-shot 23.8 → 64-shot 39.9로 오릅니다.
  - [ ] 과제마다 shot 수가 다르다는 점(상식 추론 0, NQ 0/1/5/64, MBPP 3, MMLU 5)을 말한다.
- **함께 볼 개념:** [Likelihood 채점](#c-likelihood-eval) · [Greedy 생성과 exact match](#c-greedy-em) · 원전: GPT-3 [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) §2

<!-- part: common -->
## 검토 기록

### 입력과 검토 상태

- 보고서: Touvron et al., *LLaMA: Open and Efficient Foundation Language Models*, [arXiv:2302.13971v1](https://arxiv.org/abs/2302.13971v1). 링크는 v1 PDF의 파일 페이지 기준입니다.
- 확인한 범위: 본문 §1–§8(PDF p.1–12)의 텍스트 추출본, Table 1–15. App. D는 위치만 확인했습니다.
- 확인하지 못한 범위: 그림(Fig. 1–2)은 캡션과 본문 설명만 확인했습니다. 외부 원전은 이번 개편에서 다시 읽지 않았고, 이전 추출의 확인 기록을 따랐습니다.
- 학습목표·가이드: [W01 학습목표](README.md) · [W01 Background](../../background/w01.md)
- 사람 검토: **미검토** · 검토자·일시 미지정
- AI 재검토: 개념 페이지의 수치(Table 1–4, 6–15)를 원문 텍스트와 대조했습니다. 2026-10-17에 Chinchilla(Table 2–3, 식 (10) 상수), GPT-3 Appendix B, Llama 2 §2.1–§2.2 · Table 10, Llama 3 §3.1–§3.2, RedPajama 데이터 카드, RefinedWeb · FineWeb · Muon 논문 초록을 확인해 후속 페이지를 썼습니다. OPT의 2,000 step warmup은 2차 출처만 확인했습니다. 이 읽기 지도는 이전 K ID 형식(2026-10-15)을 다섯 파트 개요 · 파트별 질문 · 개념별 페이지로 다시 구성한 것입니다.
