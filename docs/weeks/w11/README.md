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
  - **함께 읽을 자료와 범위:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §3.1과 §3.3.2에서 cold-start SFT, agent RL 뒤 self-distillation, 다시 RL로 이어지는 자체 순서를 먼저 확인한다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §2.3 “Mid-Training”, §3 “Post-Training: Expert Model Iteration”, §3.1 “Supervised Fine-Tuning”. Overall SFT의 전문가 데이터 구성, 긴 CoT와 즉답의 혼합, tool-call 형식을 확인하고 GRPO·MoE는 기반 기법으로 구분한다.

- [ ] **GLM-4.5의 reasoning RL이 reward variance와 긴 출력 길이를 관리하고, agent RL이 tool trajectory의 성공을 보상으로 바꾸는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** two-stage difficulty curriculum, 64K single-stage RL, dynamic temperature, token-weighted loss, outcome verifier, format failure.
  - **함께 읽을 자료와 범위:** GRPO 정의는 W06의 [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3만 다시 참조한다. 이 주차에서는 GLM-4.5의 `pass@8=0, pass@512>0` difficulty 전환, progressive length와 대비되는 single-stage 64K, code의 token-weighted loss만 읽는다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §3.2 “Reasoning RL”, Figures 5–7, §3.3 “Agentic RL”. 정답·도구 종료 상태·형식 오류가 같은 reward가 아닌지 구분한다.

- [ ] **agent SFT 데이터를 도구·과제·trajectory·검증의 네 단계로 합성하고, XML형 function-call 표기가 왜 학습 부담을 줄이는지 설명할 수 있다.**
  - **짚고 갈 개념:** tool/API collection, task synthesis, user simulator, terminal-state verification, rejection filtering, serialization/escaping.
  - **함께 읽을 자료와 범위:** [GLM-4.5 v1 §3.1·Figure 4](https://arxiv.org/abs/2508.06471v1)의 네 단계와 filter 규칙을 읽고, user simulator가 만드는 대화와 terminal-state judge가 검증하는 결과를 구분한다.
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
