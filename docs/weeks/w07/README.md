# W07 — DeepSeek-R1

[주차 목록](../README.md) · [W07 Background](../../background/w07.md) · [주간 템플릿](../../../templates/week.md)

**읽기 분담:** [이번 주 공통 읽기와 팀별 심화](../../background/workload.md)를 기준으로 개인 준비 3–4시간을 배분합니다. 상세 Background는 공통 범위와 담당 갈래에 필요한 부분을 찾아 읽고, 세 학습목표는 모임 후 함께 설명할 수 있도록 정리합니다.

## 논문 정보

- 논문: DeepSeek-R1
- arXiv: [DeepSeek-R1 (v2)](https://arxiv.org/abs/2501.12948v2)
- 핵심 주제: R1-Zero의 pure RL · readable reasoning을 위한 다단계 post-training · 증류와 직접 RL의 조건부 비교
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] R1-Zero의 pure RL이 SFT 후 preference-RL과 어떻게 다르고, verifier의 accuracy/format reward가 왜 가능한 task를 제한하는지 설명할 수 있다.
  - **짚고 갈 개념:** group-relative advantage, critic 없는 GRPO, rule-based outcome reward, format reward, reliable verifier, long CoT.
  - **함께 읽을 자료와 범위:** [W07 개념 경로 §1](../../background/w07.md#verifiable-rl) → R1이 직접 채택한 [DeepSeekMath v3 §4.1.1–§4.1.3](https://arxiv.org/pdf/2402.03300v3). PPO는 비교 대상으로만 읽고, GRPO를 R1의 새 알고리즘으로 쓰지 않는다.
  - **원문에서 읽을 부분:** [DeepSeek-R1 v2 §2.1–§2.3, 식 (1)–(4), Fig. 1 및 Supplementary B.3.1](https://arxiv.org/pdf/2501.12948v2).
- [ ] R1이 R1-Zero의 language mixing·낮은 가독성·일반 대화 한계를 cold start, 두 SFT, 두 RL, 서로 다른 reward model로 각각 어떻게 다루는지 설명할 수 있다.
  - **짚고 갈 개념:** conversational CoT, language-consistency reward, rejection sampling, reasoning/non-reasoning SFT, pairwise helpfulness RM, pointwise safety RM.
  - **함께 읽을 자료와 범위:** [W07 개념 경로 §2](../../background/w07.md#staged-r1) → [DeepSeek-R1 v2 §3.1–§3.2.2](https://arxiv.org/pdf/2501.12948v2) → Supplementary B.3.2 “Cold Start”–B.3.3 “800K Supervised Data”. `rejection-sampling SFT`와 on-policy RL update의 target 차이를 표시한다.
  - **원문에서 읽을 부분:** [DeepSeek-R1 v2 §3–§3.2.2, Fig. 2, 식 (5)–(10) — DeepSeek-R1](https://arxiv.org/pdf/2501.12948v2)
- [ ] R1 teacher의 distillation이 작은 모델의 직접 RL보다 유리했던 조건과, long rollout을 가능하게 한 네 module RL system의 한계를 설명할 수 있다.
  - **짚고 갈 개념:** teacher-generated SFT, base capacity, RL compute, reward hacking, rollout/inference/rule-reward/training module, padding-aware packing.
  - **함께 읽을 자료와 범위:** [W07 개념 경로 §3–§4](../../background/w07.md#rl-system)에서 system 분해와 distillation target을 먼저 그리고, R1의 Supplementary B.1·F–F.1·§6으로 돌아간다.
  - **원문에서 읽을 부분:** [DeepSeek-R1 v2 Supplementary B.1 Fig. 5, F–F.1, §6](https://arxiv.org/pdf/2501.12948v2).

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [DeepSeek-R1 v2](https://arxiv.org/abs/2501.12948v2)
- [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3)
- [Proximal Policy Optimization v2](https://arxiv.org/abs/1707.06347v2)
