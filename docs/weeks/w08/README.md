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
  - **함께 읽을 자료와 범위:** [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) §2.1.1–§2.1.4의 MLA cache와 decoupled RoPE. DSA는 MLA를 대체하기보다 그 위에 sparse selection을 얹는다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1 “DeepSeek Sparse Attention” 및 Appendix A “MHA and MLA”.

- [ ] dense warm-up과 sparse continued training이 indexer와 본 attention을 어떻게 정렬하고 분리해 학습하는지 설명할 수 있다.
  - **짚고 갈 개념:** teacher attention distribution, KL alignment, L1 normalization, stop-gradient.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1.1의 두 단계 목적함수. top-k 선택은 미분 가능하지 않다는 전제를 식으로 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1.1 “Continued Pre-Training”, Fig. 2, 식 (1)–(4).

- [ ] agent 학습 과제를 환경·도구·정답/검증기로 합성할 때, 통과한 verifier가 실제 일반화를 보장하지 않는 이유를 설명할 수 있다.
  - **짚고 갈 개념:** sandbox, tool API, task generation, solution generation, verifier, reward hacking.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §3.2.1–§3.2.2의 context 관리·cold-start. RL 자체의 일반식은 W06에서 복습하고, 여기서는 검증 가능한 agent 환경 합성에 한정한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §3.2.3 “Large-Scale Agentic Tasks”와 §4.4 “Context Management of Search Agent”.

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
