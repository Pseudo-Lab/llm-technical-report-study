# W10 — Qwen3.8-Next

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen3.8-Next
- arXiv: [Qwen3.8-Next (v1)](https://arxiv.org/abs/2608.30320v1)
- 핵심 주제: GDN·전역 주의·QSA의 역할 분담, GR·n-gram memory, TP 환경의 Muon 적용
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 먼저 읽을 배경

1. [Fast Weight Programmers v3](https://arxiv.org/abs/2102.11174v3) §2–§4.2: 선형 주의의 누적 outer-product memory와 delta update가 필요한 이유를 잡는다.
2. [Gated Delta Networks v3](https://arxiv.org/abs/2412.06464v3) §2.1–§3.3: decay·delta rule·gate와 chunkwise 학습을 연결한다.
3. [Gated Attention v1](https://arxiv.org/abs/2505.06708v1) §2.1–§2.2: attention output gate가 무엇을 조절하는지 확인한다.
4. [DeepSeek-V3.2 v1](https://arxiv.org/abs/2512.02556v1) §2.1·§2.1.1: Qwen §2.1.2가 직접 인용한 DSA의 index-then-select와 dense-to-sparse 전환을 확인한다.
5. [N-Grammer v1](https://arxiv.org/abs/2207.06366v1) §3.1–§3.4: latent n-gram lookup이 token representation에 더하는 정보를 읽고, Qwen §2.3의 deterministic lookup·host-memory prefetch와 구별한다.
6. [Hyper-Connections v3](https://arxiv.org/abs/2409.19606v3) §2.1–§2.2와 [mHC v2](https://arxiv.org/abs/2512.24880v2) §3–§4.2: GR이 넓힌 residual stream에서 read/write를 어디까지 남기는지 읽는다.
7. [Muon author note](https://kellerjordan.github.io/posts/muon/)의 “Definition”–“The design of Muon”, [Muon is Scalable v1](https://arxiv.org/abs/2502.16982v1) §2.1–§2.3: W10의 fused logical matrix·TP 적용 전제만 확인한다.

> 비교 메모: [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5) §2.1의 MLA는 Qwen 본문이 직접 전제하는 구조가 아니다. V3.2 §2.1.1을 거쳐 QSA의 MQA indexer와 latent-KV cache를 혼동하지 않기 위한 **선택 비교**로만 읽는다.

## 학습목표

- [ ] **GDN-전역 주의 혼합과 QSA가 긴 문맥에서 맡는 역할을 DSA와 구별해 설명할 수 있다.**
  - **짚고 갈 개념:** 고정 recurrent state, token retrieval, micro-block indexer, MQA, causal top-k.
  - **함께 읽을 자료와 범위:** 배경 1–4를 읽고, GDN의 delta memory와 DSA의 token 선택을 QSA의 block 선택과 대조한다. QSA의 indexer는 full-attention teacher를 max-pool하여 block teacher distribution을 만들고 KL로 distill한 뒤 sparse CPT로 전환한다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.1.1 “GDN Hybrid Architecture”, §2.1.2 “Qwen Sparse Attention”, 식 (12)–(20). 예로 16개 key를 4개 block으로 묶어 causal top-k block을 token index로 다시 펴고, max-pool teacher→block-indexer KL→joint sparse training을 적는다.

- [ ] **Gated Residual과 n-gram embedding이 각각 residual 경로와 외부 메모리에 용량을 배분하는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** pre-norm residual, HC의 read/write/mix, elementwise gate, sparse lookup, host-memory prefetch.
  - **함께 읽을 자료와 범위:** 배경 5–6을 읽은 뒤 Qwen의 GR이 H-res mixing을 생략한 선택과 Layer 2 n-gram lookup을 분리한다. N-Grammer의 latent n-gram은 출발점일 뿐, Qwen의 hash lookup·contextual injection·prefetch와 같은 구현을 뜻하지 않는다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.2 “Residual”, §2.3 “N-gram Embedding”. branch×channel read와 branch별 scalar write를 구분하고, loss와 downstream 품질이 항상 같은 선택을 지시하는지 토론한다.

- [ ] **Muon을 tensor 형태와 병렬 배치에 맞춰 적용한 이유와 안정성 주장의 범위를 판단할 수 있다.**
  - **짚고 갈 개념:** Newton–Schulz 직교화, fused parameter, tensor/data parallel, gradient outlier, stress test.
  - **함께 읽을 자료와 범위:** 배경 7의 Muon 기본식을 전제로, Qwen이 어떤 행렬은 분할하고 어떤 parameter는 AdamW에 남기는지 추적한다.
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
