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
4. [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5) §2.1.1–§2.1.3: MLA의 latent KV·decoupled RoPE를 복습한다. 이는 QSA **indexer의 MQA**와 동일 구조라는 뜻이 아니라, KV cache 압축의 비교 축이다.
5. [DeepSeek-V3.2 v1](https://arxiv.org/abs/2512.02556v1) §2.1·§2.1.1: DSA의 index-then-select와 dense-to-sparse 전환은 여기까지만 가져온다.
6. [Hyper-Connections v3](https://arxiv.org/abs/2409.19606v3) §2.1–§2.2, [mHC v2](https://arxiv.org/abs/2512.24880v2) §3–§4.2, [Muon author note](https://kellerjordan.github.io/posts/muon/)의 “Definition”–“The design of Muon”, [Muon is Scalable v1](https://arxiv.org/abs/2502.16982v1) §2.1–§2.3을 읽는다. W10은 이 기본식이 아니라 Qwen의 GR·fused matrix·TP 적용을 맡는다.

## 학습목표

- [ ] **GDN-전역 주의 혼합과 QSA가 긴 문맥에서 맡는 역할을 DSA와 구별해 설명할 수 있다.**
  - **짚고 갈 개념:** 고정 recurrent state, token retrieval, micro-block indexer, MQA, causal top-k.
  - **함께 읽을 자료와 범위:** 위 배경 1–5를 순서대로 읽고, 특히 GDN의 delta memory와 DSA의 token 선택을 QSA의 block 선택과 대조한다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.1.1 “GDN Hybrid Architecture”, §2.1.2 “Qwen Sparse Attention”. 예로 16개 key를 4개 block으로 묶어 causal top-k block을 token index로 다시 펴는 과정을 적고, GDN의 압축과 QSA indexer를 구별한다.

- [ ] **Gated Residual과 n-gram embedding이 각각 residual 경로와 외부 메모리에 용량을 배분하는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** pre-norm residual, HC의 read/write/mix, elementwise gate, sparse lookup, host-memory prefetch.
  - **함께 읽을 자료와 범위:** 위 배경 6의 HC/mHC를 확인한 뒤, Qwen의 GR이 H-res mixing을 생략한 선택과 Layer 2 n-gram lookup을 읽는다.
  - **원문에서 읽을 부분:** [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.2 “Residual”, §2.3 “N-gram Embedding”. branch×channel read와 branch별 scalar write를 구분하고, loss와 downstream 품질이 항상 같은 선택을 지시하는지 토론한다.

- [ ] **Muon을 tensor 형태와 병렬 배치에 맞춰 적용한 이유와 안정성 주장의 범위를 판단할 수 있다.**
  - **짚고 갈 개념:** Newton–Schulz 직교화, fused parameter, tensor/data parallel, gradient outlier, stress test.
  - **함께 읽을 자료와 범위:** 위 배경 6의 Muon 기본식을 전제로, Qwen이 어떤 행렬은 분할하고 어떤 parameter는 AdamW에 남기는지 추적한다.
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
