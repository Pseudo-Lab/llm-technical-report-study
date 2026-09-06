# W13 — VibeThinker-1.5B → VibeThinker-3B

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: VibeThinker-1.5B → VibeThinker-3B
- arXiv: [VibeThinker-1.5B (v1)](https://arxiv.org/abs/2511.06221v1) → [VibeThinker-3B (v1)](https://arxiv.org/abs/2606.16140v1)
- 핵심 주제: SSP의 다양성 우선 증류 · 3B의 seed-to-trace curriculum · MGPO와 Long2Short
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] VibeThinker-1.5B의 SSP가 단일 정답 정확도 중심 SFT와 달리 다양한 정답 경로를 먼저 확보하는 이유를 설명할 수 있다.
  - **짚고 갈 개념:** Pass@1·Pass@K, solution spectrum, domain-aware probing, expert fusion.
  - **함께 읽을 자료와 범위:** [W13 구성요소 가이드](../../background/w13.md)의 base, Pass@K, domain-aware probing·fusion 절을 먼저 읽고, [VibeThinker-1.5B v1](https://arxiv.org/abs/2511.06221v1) §2의 Pass@K 정의와 §3.1–§3.3의 spectrum·probing·fusion을 이어 읽는다. base architecture/tokenizer는 W02의 [Qwen 가이드](../../background/qwen.md)를 재사용한다.
  - **원문에서 읽을 부분:** [1.5B v1](https://arxiv.org/abs/2511.06221v1) §3.1 *The Spectrum-to-Signal Principle*, §3.2–3.3, Fig. 3.
- [ ] **VibeThinker-3B가 신뢰 가능한 seed query에서 다경로 trace를 만들고 broad SFT에서 hard·long SFT로 옮기는 기준을 설명할 수 있다.**
  - **짚고 갈 개념:** trusted supervision seed, query expansion, multi-path teacher sampling, majority vote, trace verification, n-gram decontamination, length–difficulty curriculum.
  - **함께 읽을 자료와 범위:** [W13 구성요소 가이드](../../background/w13.md)의 trusted seed, multi-path trace/quality control, broad→hard·long SFT 절을 먼저 읽는다. [VibeThinker-1.5B v1](https://arxiv.org/abs/2511.06221v1) §3.3의 Pass@K 기반 specialist selection·fusion은 3B §2.1.2에서 이어받는 배경이다. 3B §2.1.1의 seed→query expansion→multiple trace→quality control은 새로 설명하는 데이터 구성 경로로 나누어 읽는다.
  - **원문에서 읽을 부분:** [VibeThinker-3B v1](https://arxiv.org/abs/2606.16140v1) §2.1.1–§2.1.2, Figure 3. stage 2에서 trace가 5K보다 짧은 표본과 1.5B 8회 rollout의 error rate가 0.75보다 낮은 쉬운 문제를 제외하는 기준을 확인한다.
- [ ] **MGPO의 능력 경계 가중과 Long2Short의 정답 trajectory 내 길이 재가중이 각각 무엇을 최적화하는지 설명할 수 있다.**
  - **짚고 갈 개념:** group-relative advantage, empirical correctness \(p(q)\), maximum-entropy point, accuracy-first, length-aware reward redistribution, zero-sum shift.
  - **함께 읽을 자료와 범위:** [W13 구성요소 가이드](../../background/w13.md)의 MGPO, Long2Short, offline self-distillation·CLR 절을 먼저 훑는다. GRPO의 공통 골격은 W06의 [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1만 참조한다. 1.5B의 MGPO와 3B의 Long2Short은 같은 기법으로 뭉치지 말고, 전자는 문제 선택 가중이고 후자는 맞은 답들 사이의 효율 선호라는 점을 식으로 대조한다.
  - **원문에서 읽을 부분:** [VibeThinker-1.5B v1](https://arxiv.org/abs/2511.06221v1) §3.4; [VibeThinker-3B v1](https://arxiv.org/abs/2606.16140v1) §2.2.1–§2.2.2, 식 (1)–(3). Long2Short에서 틀린 trajectory는 바꾸지 않고 맞은 trajectory 안에서만 보상이 이동하는지 확인한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료
