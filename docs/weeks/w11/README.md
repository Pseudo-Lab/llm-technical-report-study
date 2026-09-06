# W11 — GLM-4.5

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: GLM-4.5
- arXiv: [GLM-4.5 (v1)](https://arxiv.org/abs/2508.06471v1)
- 핵심 주제: 전문 모델의 SFT·RL과 능력 통합, 증류와 재학습, agent 학습·평가
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **Reasoning·Agent·General 전문가를 만든 뒤 하나의 모델로 통합한 이유와 실패 위험을 설명할 수 있다.**
  - **짚고 갈 개념:** cold-start SFT, expert model, self-distillation, capability interference, thinking/non-thinking, rejection filtering.
  - **함께 읽을 자료와 범위:** [InstructGPT v1](https://arxiv.org/abs/2203.02155v1) §3.1–§3.2와 [Hinton et al. v1](https://arxiv.org/abs/1503.02531v1) §2–§2.1에서 SFT와 teacher–student 증류의 기본 흐름을 확인한다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §2.3 “Mid-Training”, §3 “Post-Training: Expert Model Iteration”, §3.1 “Supervised Fine-Tuning”. Overall SFT의 전문가 데이터 구성, 긴 CoT와 즉답의 혼합, tool-call 형식을 확인하고 GRPO·MoE는 기반 기법으로 구분한다.

- [ ] **Reasoning과 agent 전문가의 reward·curriculum이 왜 달라야 하며, 반복 self-distillation이 무엇을 보완하는지 설명할 수 있다.**
  - **짚고 갈 개념:** group-relative reward, difficulty curriculum, outcome supervision, format constraint, on-policy self-distillation.
  - **함께 읽을 자료와 범위:** [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3에서 GRPO의 group-relative reward를 복습하고, 정답 검증과 tool-use 성공을 구분한다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §3.2 “Reasoning RL”, §3.3 “Agentic RL”. difficulty·sampling 조절, agent trace에서 최적화하는 token, plateau 뒤 SFT cold start를 교체하는 순서와 환경·format 오류의 영향을 따라간다.

- [ ] **ARC 통합 성능 주장을 평가 프로토콜과 함께 읽고 적용 범위를 판단할 수 있다.**
  - **짚고 갈 개념:** agent evaluation, execution-based reward, pass@k/Avg@k, LLM-as-a-judge, context truncation.
  - **함께 읽을 자료와 범위:** [평가·검색·agent 시스템 배경](../../background/README.md#evaluation-systems)에서 benchmark 점수·pass@k·verifier 통과가 서로 다른 지표임을 확인한다.
  - **원문에서 읽을 부분:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §4 “Evaluation”, 특히 §4.2 “ARC Benchmarks”와 §4.3 “Hands-on Experience”. TAU·BFCL·BrowseComp과 SWE-bench·Terminal-Bench이 측정하는 능력을 나누고, 전문가별 ablation이 없는 통합 이득은 제한적으로 해석한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [GLM-4.5 원문 v1](https://arxiv.org/abs/2508.06471v1)
