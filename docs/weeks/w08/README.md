# W08 — DeepSeek-V3.2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V3.2
- arXiv: [DeepSeek-V3.2 (v1)](https://arxiv.org/abs/2512.02556v1)
- 핵심 주제: MLA 위의 DSA indexer·top-k KV 선택 · dense-to-sparse continued training · agent task synthesis
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] DSA가 MLA의 latent KV 전체에 dense attention하지 않고, indexer가 고른 top-k만 core attention에 보내는 흐름을 설명할 수 있다.
  - **짚고 갈 개념:** KV cache, MLA latent KV, MQA, indexer score, top-k retrieval.
  - **함께 읽을 자료와 범위:** V3.2 §2.1이 출처로 든 [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) §2.1.1–§2.1.4의 MLA와 [MQA v1](https://arxiv.org/pdf/1911.02150v1) §2.4를 읽는다. 이어 V3.2의 “Instantiate DSA Under MLA”에서 MQA-mode latent KV를 모든 query head가 공유하는 구현을 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1 “DeepSeek Sparse Attention” 및 Appendix A “MHA and MLA”.

- [ ] dense warm-up과 sparse continued training이 indexer와 본 attention을 어떻게 정렬하고 분리해 학습하는지 설명할 수 있다.
  - **짚고 갈 개념:** teacher attention distribution, KL alignment, L1 normalization, stop-gradient.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1.1의 두 단계 목적함수. top-k 선택은 미분 가능하지 않다는 전제를 식으로 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1.1 “Continued Pre-Training”, Fig. 2, 식 (1)–(4).

- [ ] V3.2의 general-agent 합성 pipeline이 environment·toolset·task·solution·verifier를 어떤 제약으로 함께 만들고(non-zero pass@100 filtering 포함), verifier-valid task와 out-of-domain transfer를 왜 별도 평가해야 하는지 설명할 수 있다.
  - **짚고 갈 개념:** tool-interface 제약·허용된 논리 계산 · verifier · iterative difficulty increase · pass@100 filter · synthetic-task transfer
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §3.2.3에서 solution 함수가 도구 호출·논리 계산만 수행하고 DB에 직접 접근할 수 없다는 제약과 generation loop를 읽고 §4.3 Fig. 5에서 synthetic task의 난도와 transfer를 별도로 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1 §3.2.3, Table 1, §4.3, Fig. 5 — Large-Scale Agentic Tasks](https://arxiv.org/pdf/2512.02556v1)

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [DeepSeek-V3.2 v1](https://arxiv.org/abs/2512.02556v1)
- [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5)
- [Fast Transformer Decoding / MQA v1](https://arxiv.org/abs/1911.02150v1)
