# W06 — DeepSeek-R1

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-R1
- arXiv: [DeepSeek-R1 (v2)](https://arxiv.org/abs/2501.12948v2)
- 핵심 주제: R1-Zero의 pure RL · readable reasoning을 위한 다단계 post-training · 증류와 직접 RL의 조건부 비교
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] R1-Zero의 pure RL이 SFT 후 preference-RL과 어떻게 다른지 설명할 수 있다.
  - **짚고 갈 개념:** outcome reward, format reward, verifier, GRPO, long CoT.
  - **함께 읽을 자료와 범위:** [PPO v2](https://arxiv.org/pdf/1707.06347v2) §3–§4와 [DeepSeekMath v3](https://arxiv.org/pdf/2402.03300v3) §4.1.1–§4.1.3. GRPO는 R1의 신규 알고리즘이 아니라 채택한 기법이다.
  - **원문에서 읽을 부분:** [DeepSeek-R1 v2](https://arxiv.org/pdf/2501.12948v2) §2.1–§2.3 “DeepSeek-R1-Zero”.
- [ ] R1이 R1-Zero의 language mixing·낮은 가독성을 cold start, language-consistency reward, 두 번째 rejection-sampling SFT와 general RL로 각각 어떻게 다루는지 설명할 수 있다.
  - **짚고 갈 개념:** conversational CoT · language-consistency reward · rejection sampling · reasoning/non-reasoning SFT · helpfulness/safety reward model
  - **함께 읽을 자료와 범위:** [DeepSeek-R1 v2 §3.1–§3.2.2](https://arxiv.org/pdf/2501.12948v2)에서 보상과 두 RL 단계를 읽은 뒤, Supplementary B.3.2 “Cold Start”–B.3.3 “800K Supervised Data”로 데이터 구성을 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-R1 v2 §3–§3.2.2, Fig. 2, 식 (5)–(10) — DeepSeek-R1](https://arxiv.org/pdf/2501.12948v2)
- [ ] R1 teacher의 distillation이 작은 모델의 직접 RL보다 유리했던 조건과 한계를 설명할 수 있다.
  - **짚고 갈 개념:** teacher-generated SFT, base capacity, RL compute, reward hacking.
  - **함께 읽을 자료와 범위:** [DeepSeek-R1 v2](https://arxiv.org/pdf/2501.12948v2) §6 “Conclusion, Limitation, and Future Work”.
  - **원문에서 읽을 부분:** [DeepSeek-R1 v2](https://arxiv.org/pdf/2501.12948v2) Supplementary F–F.1 “DeepSeek-R1 Distillation / Distillation v.s. Reinforcement Learning”.

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
