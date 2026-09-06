# W11 — GLM-4.5

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: GLM-4.5
- arXiv: [GLM-4.5 (v1)](https://arxiv.org/abs/2508.06471v1)
- 핵심 주제: 전문 모델의 SFT·RL과 능력 통합, reasoning/agent RL의 국소 설계, agent SFT 합성
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **Reasoning·Agent·General 전문가를 만든 뒤 하나의 모델로 통합한 이유와 실패 위험을 설명할 수 있다.**
  - **짚고 갈 개념:** cold-start SFT, expert model, self-distillation, capability interference, thinking/non-thinking, rejection filtering.
  - **함께 읽을 자료와 범위:** [W11 구성요소 가이드](../../background/w11.md)에서 expert/overall SFT, reasoning·agent·general reward, agent serialization이 어떻게 이어지는지 먼저 읽는다. GRPO 정의만 W06의 [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3으로 되돌아간다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §2.3 “Mid-Training”, §3 “Post-Training: Expert Model Iteration”, §3.1 “Supervised Fine-Tuning”, §3.3.2. 전문가가 생성한 응답을 모아 Overall SFT로 통합하는 절차와, agent RL 도중 cold-start 응답을 갱신하는 반복 self-distillation을 구분한다. 긴 CoT·즉답·tool-call 데이터를 각 절차에서 어떻게 구성하는지 확인한다.

- [ ] **GLM-4.5의 reasoning RL이 reward variance와 긴 출력 길이를 관리하고, agent RL이 tool trajectory의 성공을 보상으로 바꾸는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** two-stage difficulty curriculum, 64K single-stage RL, dynamic temperature, token-weighted loss, outcome verifier, format failure.
  - **함께 읽을 자료와 범위:** [W11 구성요소 가이드](../../background/w11.md)에서 reasoning·code·agent·general RL의 보상 단위를 나란히 본다. GRPO 정의는 W06의 [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3만 다시 참조한다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §3.2 “Reasoning RL”, Figures 5–7, §3.3 “Agentic RL”. 정답·도구 종료 상태·형식 오류가 같은 reward가 아닌지 구분한다.

- [ ] **agent SFT 데이터를 도구·과제·trajectory·검증의 네 단계로 합성하고, XML형 function-call 표기가 왜 학습 부담을 줄이는지 설명할 수 있다.**
  - **짚고 갈 개념:** tool/API collection, task synthesis, user simulator, terminal-state verification, rejection filtering, serialization/escaping.
  - **함께 읽을 자료와 범위:** [W11 구성요소 가이드](../../background/w11.md)에서 XML-like tag, four-stage synthesis, Slime data buffer를 분리해 읽는다. 이어 [GLM-4.5 v1 §3.1·Figure 4](https://arxiv.org/abs/2508.06471v1)의 네 단계와 filter 규칙을 확인한다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §3.1의 “Reducing Character Escaping in Function Call Templates”, “Rejection Sampling”, “Automatic Agentic SFT Data Construction”, Figure 4. 네 단계에서 실패한 trajectory가 어느 filter에서 제거되는지 그린다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [GLM-4.5 원문 v1](https://arxiv.org/abs/2508.06471v1)
