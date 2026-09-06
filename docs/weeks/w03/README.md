# W03 — Qwen3

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen3
- arXiv: [Qwen3 (v1)](https://arxiv.org/abs/2505.09388v1)
- 핵심 주제: 생각·비생각 모드 통합 · 생각 예산 · 강한 교사에서 작은 모델로의 증류
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] 별도 추론 모델과 일반 대화 모델을 두는 대신, 한 Qwen3 모델에서 생각·비생각 모드를 전환하는 방법을 설명할 수 있다.
  - **짚고 갈 개념:** 긴 추론 흔적 · 모드 지시 · chat template · 빈 생각 블록 · 다회차 전환
  - **함께 읽을 자료와 범위:** [InstructGPT v1 §3.1](https://arxiv.org/abs/2203.02155v1)의 후학습 순서를 배경으로, Qwen3가 추론 능력 뒤에 비생각 모드를 합친 흐름을 비교한다.
  - **원문에서 읽을 부분:** [Qwen3 v1 §4.3 — Thinking Mode Fusion](https://arxiv.org/abs/2505.09388v1)
- [ ] 생각 예산을 늘리거나 중단할 때 답변이 어떻게 달라지는지, 길게 생각하는 것이 항상 유리하지 않은 이유와 함께 설명할 수 있다.
  - **짚고 갈 개념:** 추론 토큰 예산 · 강제 중단 · 테스트 시 계산량 · 긴 문맥 검색 · 추론 간섭
  - **함께 읽을 자료와 범위:** [Qwen2.5 v2 §3.3](https://arxiv.org/abs/2412.15115v2)의 긴 문맥 사전학습을 읽어, 입력 길이 확장과 생각 토큰 예산을 분리한다.
  - **원문에서 읽을 부분:** [Qwen3 v1 §4.3·§4.7, Appendix A.1.1 — Thinking Budget, Discussion, Long-Context Ability](https://arxiv.org/abs/2505.09388v1)
- [ ] 큰 교사의 답을 작은 학생에게 옮기는 오프라인·온폴리시 증류를 직접 강화학습과 비교해, 학습 신호와 한계를 설명할 수 있다.
  - **짚고 갈 개념:** 강한 교사 · 약한 학생 · 오프라인 증류 · 온폴리시 증류 · KL divergence
  - **함께 읽을 자료와 범위:** [GKD v3 §2–§3.2](https://arxiv.org/abs/2306.13649v3)에서 학생 생성 궤적·KL 방향을 읽어, 고정 자료 증류와 직접 보상 최적화를 구분한다.
  - **원문에서 읽을 부분:** [Qwen3 v1 §4.5·§4.7 — Strong-to-Weak Distillation, The Effectiveness and Efficiency of On-Policy Distillation](https://arxiv.org/abs/2505.09388v1)

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen3 Technical Report (v1)](https://arxiv.org/abs/2505.09388v1)
