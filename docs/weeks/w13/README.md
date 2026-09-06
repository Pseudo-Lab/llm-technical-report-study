# W13 — VibeThinker-1.5B → VibeThinker-3B

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: VibeThinker-1.5B → VibeThinker-3B
- arXiv: [VibeThinker-1.5B (v1)](https://arxiv.org/abs/2511.06221v1) → [VibeThinker-3B (v1)](https://arxiv.org/abs/2606.16140v1)
- 핵심 주제: SSP의 다양성 우선 증류 · MGPO의 능력 경계 가중 · 3B의 장기 추론·자기증류·CLR
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] VibeThinker-1.5B의 SSP가 단일 정답 정확도 중심 SFT와 달리 다양한 정답 경로를 먼저 확보하는 이유를 설명할 수 있다.
  - **짚고 갈 개념:** Pass@1·Pass@K, solution spectrum, domain-aware probing, expert fusion.
  - **함께 읽을 자료와 범위:** [Chen et al. v2](https://arxiv.org/abs/2107.03374v2) §2.1의 Pass@K 정의·추정만 읽고, Pass@1과 해법 다양성의 차이를 확인한다.
  - **원문에서 읽을 부분:** [1.5B v1](https://arxiv.org/abs/2511.06221v1) §3.1 *The Spectrum-to-Signal Principle*, §3.2–3.3, Fig. 3.
- [ ] MGPO가 GRPO의 공통 최적화 뼈대에 능력 경계 문제의 가중을 더하는 방식과, 3B가 이를 장기·다영역 추론으로 확장한 방식을 설명할 수 있다.
  - **짚고 갈 개념:** group-relative advantage, maximum-entropy weighting, curriculum SFT, Long2Short, offline self-distillation.
  - **함께 읽을 자료와 범위:** [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1–§4.1.1의 GRPO와 [Hinton et al. v1](https://arxiv.org/abs/1503.02531v1) §2의 teacher–student distillation을 읽고, MGPO의 문제 가중과 3B의 trace 재학습을 구분한다.
  - **원문에서 읽을 부분:** [1.5B v1](https://arxiv.org/abs/2511.06221v1) §3.4 *MaxEnt-Guided Policy Optimization*; [3B v1](https://arxiv.org/abs/2606.16140v1) §2.1–2.3, Fig. 3.
- [ ] 검증 가능한 추론과 지식 집약 과제를 구분하는 3B의 가설, 그리고 CLR의 test-time 재평가가 갖는 범위와 한계를 설명할 수 있다.
  - **짚고 갈 개념:** Parametric Compression–Coverage Hypothesis, claim-level reliability, test-time scaling, knowledge coverage.
  - **함께 읽을 자료와 범위:** [1.5B v1](https://arxiv.org/abs/2511.06221v1) §4.2의 reasoning·knowledge 평가 해석을 3B의 새 가설과 CLR로 연결한다.
  - **원문에서 읽을 부분:** [3B v1](https://arxiv.org/abs/2606.16140v1) §1 *Introduction*, §3.1 *Test-time scaling with claim-level reliability assessment*, §3.2, §4.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료
