# W12 — GLM-5

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: GLM-5
- arXiv: [GLM-5 (v2)](https://arxiv.org/abs/2602.15763v2)
- 핵심 주제: 비동기 agent RL의 안정화, token-정렬 최적화, 검증 가능한 장기 agent 환경
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **동기 agent RL의 긴 꼬리 지연을 비동기 rollout–learner 분리로 어떻게 바꾸며, policy lag가 왜 생기는지 설명할 수 있다.**
  - **짚고 갈 개념:** synchronous barrier, straggler, rollout–learner decoupling, policy lag, on-policy 근사, multi-task scheduling.
  - **함께 읽을 자료와 범위:** [GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §3.3에서 agent RL의 rollout과 학습 흐름을 확인해 GLM-5의 비동기 확장과 비교한다.
  - **원문에서 읽을 부분:** [GLM-5 v2](https://arxiv.org/abs/2602.15763v2) §3.6 “RL Training Infrastructure: The slime Framework”, §4.1 “Asynchronous RL for Agentic Tasks”와 §4.1.1. weight synchronization, optimizer reset, Multi-Task Rollout Orchestrator를 흐름으로 그리고 처리량과 sample quality를 구분한다.

- [ ] **TITO와 Direct Double-sided Importance Sampling이 비동기 trajectory의 학습 신호를 어떻게 보존하고, 어떤 sample을 버리는지 설명할 수 있다.**
  - **짚고 갈 개념:** token-action alignment, importance ratio, trust-region mask, off-policy bias, stale policy, incomplete group.
  - **함께 읽을 자료와 범위:** [PPO v2](https://arxiv.org/abs/1707.06347v2) §3–§4에서 importance ratio·clipping·KL을 복습한다. DSA의 구조와 수식은 W08 범위로 남긴다.
  - **원문에서 읽을 부분:** [GLM-5 v2](https://arxiv.org/abs/2602.15763v2) §4.1.2 “Optimizing Asynchronous Training Stability”와 §3.2의 DSA 전환 조건. TITO의 token ID·metadata, rollout log-probability, stale trajectory·환경 실패·불완전 group 처리 규칙을 구분한다.

- [ ] **검증 가능한 장기 agent 환경과 context 관리가 ‘agentic engineering’ 주장을 어디까지 뒷받침하는지 판단할 수 있다.**
  - **짚고 갈 개념:** executable verifier, F2P/P2P, reward hacking, hierarchical context management, cumulative regression.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/abs/2512.02556v1) §3.2.3과 §4.4에서 검증 가능한 agent 과제와 context 관리의 앞선 사례를 확인한다.
  - **원문에서 읽을 부분:** [GLM-5 v2](https://arxiv.org/abs/2602.15763v2) §4.2 “Environment Scaling for Agents”, §6.2 “Evaluation of Real-world Agentic Engineering Experience”, Appendix B.4.1. issue–PR·terminal·search 환경의 검증 경로와 keep-recent-k/discard-all을 읽고, chained PR·내부 평가·judge 기반 평가의 적용 범위를 판단한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [GLM-5 원문 v2](https://arxiv.org/abs/2602.15763v2)
