# W14 — LFM2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: LFM2
- arXiv: [LFM2 (v1)](https://arxiv.org/abs/2511.23404v1)
- 핵심 주제: hardware-in-the-loop Pareto 탐색 · gated short convolution과 GQA의 최소 하이브리드 · Top-K KD
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] LFM2가 architecture search의 목적을 proxy가 아닌 기기에서의 품질·지연·메모리 trade-off로 둔 이유를 설명할 수 있다.
  - **짚고 갈 개념:** hardware-in-the-loop, multi-objective search, Pareto frontier, TTFT, peak RSS.
  - **함께 읽을 자료와 범위:** [STAR v1](https://arxiv.org/abs/2411.17800v1) §4.1과 §5.3–§5.4의 quality·parameter·cache 목적을 읽고, LFM2가 기기 실측으로 탐색 목적을 바꾼 지점을 대조한다.
  - **원문에서 읽을 부분:** [LFM2 v1](https://arxiv.org/abs/2511.23404v1) §2.1 *Objectives and constraints*·*On-device profiling*·*Outcomes*, §9.2.
- [ ] gated short convolution과 소수의 GQA가 local mixing과 global context를 어떻게 분담하며, Hyena류의 구성요소와 무엇이 다른지 설명할 수 있다.
  - **짚고 갈 개념:** depthwise convolution, input-dependent gate, GQA, KV traffic, local/global context, minimal hybrid.
  - **함께 읽을 자료와 범위:** [Hyena v3](https://arxiv.org/abs/2302.10866v3) §2.1과 §3.1–§3.4에서 short convolution·gate와 long convolution을 구분한다. LFM2는 Hyena 전체가 아니라 gated short convolution과 소수 GQA를 선택했다.
  - **원문에서 읽을 부분:** [LFM2 v1](https://arxiv.org/abs/2511.23404v1) §2.2 *Gated short convolution block*·*Attention and MLP*, Fig. 2, §8.2 *Hybrid architectures*.
- [ ] **Top-K teacher logits만 저장할 때 LFM2의 decoupled·tempered KD가 support mismatch를 어떻게 피하는지 식으로 설명할 수 있다.**
  - **짚고 갈 개념:** truncated support, Top-K mass, conditional distribution, Bernoulli KL, temperature.
  - **함께 읽을 자료와 범위:** [Hinton et al. v1](https://arxiv.org/abs/1503.02531v1) §2에서 soft target·temperature·hard-label CE의 최소 전제를 읽고, [Decoupled Knowledge Distillation v2](https://arxiv.org/abs/2203.08679v2) §3.1–§3.3에서 KL을 분해하는 관점을 읽는다. DKD의 target/non-target class 분해와 LFM2의 Top-K membership/conditional 분해는 같은 식이 아님을 표시한다.
  - **원문에서 읽을 부분:** [LFM2 v1](https://arxiv.org/abs/2511.23404v1) §3.3, 식 (1)–(2), Appendix A. \(K=2\)인 작은 예에서 teacher tail logits가 없으므로 full KL을 계산하지 않고, temperature가 conditional Top-K 항에만 들어감을 확인한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료
