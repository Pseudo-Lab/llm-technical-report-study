# W11 — Qwen3.8-Next

[주차 목록](../README.md) · [W11 Background](../../background/w11.md) · [주간 템플릿](../../../templates/week.md)

**읽기 분담:** [이번 주 공통 읽기와 팀별 심화](../../background/workload.md)를 기준으로 개인 준비 3–4시간을 배분합니다. 상세 Background는 공통 범위와 담당 갈래에 필요한 부분을 찾아 읽고, 세 학습목표는 모임 후 함께 설명할 수 있도록 정리합니다.

## 논문 정보

- 논문: Qwen3.8-Next
- arXiv: [Qwen3.8-Next (v1)](https://arxiv.org/abs/2608.30320v1)
- 핵심 주제: GDN·전역 주의·QSA의 역할 분담, GR·n-gram memory, TP 환경의 Muon 적용
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 먼저 읽을 배경

1. [Qwen3.8 전체 구성요소 가이드](../../background/w11.md)의 표를 따라 `GDN → global attention/RoPE → QSA → GR → n-gram → Muon/parallelism → scaling/stress test`를 읽는다. 이것은 논문 본문 순서를 보존한 경로이며, 3개 목표에 없는 MoE capacity·FP8 state·hyperparameter scaling도 왜 필요한지 함께 표시한다.
2. QSA의 MQA indexer는 [DeepSeek-V3.2 v1](https://arxiv.org/abs/2512.02556v1) §2.1–§2.1.1을 직접 경로로 읽는다. [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5) §2.1의 MLA는 `Qwen → V3.2 → V2` 비교 경로일 뿐 Qwen이 직접 채택한 구조가 아니다.
3. 이 보고서는 tokenizer, data construction, SFT/RL·synthetic data pipeline을 제시하지 않는다. Qwen2/Qwen2.5의 BBPE·data synthesis를 W11의 신규 배경으로 반복하지 않고, 보고서가 실제로 공개한 architecture·pre-training optimization 범위에 머문다.

## 학습목표

- [ ] **GDN-전역 주의 혼합과 QSA가 긴 문맥에서 맡는 역할을 DSA와 구별해 설명할 수 있다.**
  - **짚고 갈 개념:** 고정 recurrent state, token retrieval, micro-block indexer, MQA, causal top-k.
  - **함께 읽을 자료와 범위:** [W11 구성요소 가이드](../../background/w11.md)의 `GDN`, `global-attention interval, RoPE/NoPE`, `QSA` 행과 `QSA: 16 → 4 → 2 blocks` 예를 읽고, GDN의 delta memory와 DSA의 token 선택을 QSA의 block 선택과 대조한다. QSA의 indexer는 full-attention teacher를 max-pool하여 block teacher distribution을 만들고 KL로 distill한 뒤 sparse CPT로 전환한다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.1.1 “GDN Hybrid Architecture”, §2.1.2 “Qwen Sparse Attention”, 식 (12)–(20). 예로 16개 key를 4개 block으로 묶어 causal top-k block을 token index로 다시 펴고, max-pool teacher→block-indexer KL→joint sparse training을 적는다.

- [ ] **Gated Residual과 n-gram embedding이 각각 residual 경로와 외부 메모리에 용량을 배분하는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** pre-norm residual, HC의 read/write/mix, elementwise gate, sparse lookup, host-memory prefetch.
  - **함께 읽을 자료와 범위:** [W11 구성요소 가이드](../../background/w11.md)의 `GR`, `GR path analysis`, `n-gram embedding`, `allocation/scale ablation` 행을 읽은 뒤 Qwen의 GR이 H-res mixing을 생략한 선택과 Layer 2 n-gram lookup을 분리한다. N-Grammer의 latent n-gram은 출발점일 뿐, Qwen의 hash lookup·contextual injection·prefetch와 같은 구현을 뜻하지 않는다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.2 “Residual”, §2.3 “N-gram Embedding”. branch×channel read와 branch별 scalar write를 구분하고, loss와 downstream 품질이 항상 같은 선택을 지시하는지 토론한다.

- [ ] **Muon을 tensor 형태와 병렬 배치에 맞춰 적용한 이유와 안정성 주장의 범위를 판단할 수 있다.**
  - **짚고 갈 개념:** Newton–Schulz 직교화, fused parameter, tensor/data parallel, gradient outlier, stress test.
  - **함께 읽을 자료와 범위:** [W11 구성요소 가이드](../../background/w11.md)의 `§3.1의 Muon`, `TP/DP, scaling law`, `stress test` 행을 전제로, Qwen이 어떤 행렬은 분할하고 어떤 parameter는 AdamW에 남기는지 추적한다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §3.1 “Optimizer”–§3.3 “Stability Stress Test”. QKV처럼 저장은 fused여도 논리적으로는 별도 2D map인 사례를 분류하고, 전체 recipe의 결과를 Muon 또는 GR 하나의 인과효과로 단정할 수 없는 이유를 확인한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen3.8-Next 원문 v1](https://arxiv.org/abs/2608.30320v1)
