# W08 — DeepSeek-V3.2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [W08 전체 개념 경로](../../background/w08.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V3.2
- arXiv: [DeepSeek-V3.2 (v1)](https://arxiv.org/abs/2512.02556v1)
- 핵심 주제: MLA 위 DSA indexer·top-k KV 선택 · scalable GRPO · thinking agent context·환경 합성
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] DSA가 MLA latent KV 전체에 dense attention하지 않고 indexer top-k만 core attention에 보내며, dense warm-up과 sparse training으로 selector를 어떻게 학습하는지 설명할 수 있다.
  - **짚고 갈 개념:** KV cache, MLA latent KV, MQA-mode sharing, lightning index score, top-k selector, L1-normalized attention target, KL alignment, stop-gradient.
  - **함께 읽을 자료와 범위:** [W08 개념 경로 §1](../../background/w08.md#dsa) → V3.2이 직접 연결한 [DeepSeek-V2 v5 §2.1.1–§2.1.4](https://arxiv.org/pdf/2405.04434v5)와 [MQA v1 §2.4](https://arxiv.org/pdf/1911.02150v1). DSA의 selection과 MQA의 KV-sharing을 다른 축으로 그린다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1 §2.1–§2.1.1, Fig. 2, 식 (1)–(4), Appendix A](https://arxiv.org/pdf/2512.02556v1).

- [ ] V3.2가 rollout을 여러 update에 재사용하고 MoE/top-p sampling을 쓸 때, unbiased KL·off-policy sequence masking·Keep Routing·Keep Sampling Mask로 GRPO를 어떻게 안정화하는지 설명할 수 있다.
  - **짚고 갈 개념:** importance-sampling ratio, K3 KL estimator, off-policy divergence, negative-advantage mask, expert routing consistency, truncated action support.
  - **함께 읽을 자료와 범위:** [W08 개념 경로 §2](../../background/w08.md#scaling-grpo) → GRPO 원전 [DeepSeekMath v3 §4.1.1–§4.1.3](https://arxiv.org/pdf/2402.03300v3) → V3.2 §3.1. “mask”가 모든 off-policy sample을 버리는 것인지, 어떤 조건의 negative sequence만 가리는지 식 (8)–(9)에서 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1 §3.1, 식 (5)–(9)](https://arxiv.org/pdf/2512.02556v1).

- [ ] V3.2가 thinking tool-use를 위한 context policy·cold start를 만들고, general-agent 합성 pipeline에서 environment·toolset·task·solution·verifier를 어떤 제약으로 함께 만드는지 설명할 수 있다.
  - **짚고 갈 개념:** role-aware context retention, `<think>`/tool-call system prompt, tool-interface restriction, verifier, iterative difficulty increase, non-zero pass@100 filter, synthetic-task transfer.
  - **함께 읽을 자료와 범위:** [W08 개념 경로 §3–§4](../../background/w08.md#thinking-agent) → V3.2 §3.2.1–§3.2.3. solution 함수가 tool call·논리 계산만 수행하고 DB에 직접 접근할 수 없다는 제약, 그리고 §4.3의 난도와 transfer를 각각 표시한다.
  - **원문에서 읽을 부분:** [DeepSeek-V3.2 v1 §3.2.1–§3.2.3, Fig. 4, Table 1, Appendix B Tables 6–8, §4.3 Fig. 5, §4.4 Fig. 6](https://arxiv.org/pdf/2512.02556v1).

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
