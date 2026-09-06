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
  - **함께 읽을 자료와 범위:** [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3에서 GLM-5가 직접 인용한 GRPO의 group-relative advantage를 확인한다. 이어 GLM-5 §3.2 식 (1)과 §4.1.2 식 (3)–(5)을 나란히 읽어 rollout log-probability를 쓰는 ratio와 token mask를 구분한다.
  - **원문에서 읽을 부분:** [GLM-5 v2](https://arxiv.org/abs/2602.15763v2) §4.1.2 “Optimizing Asynchronous Training Stability”와 식 (3)–(5). TITO의 token ID·metadata, rollout log-probability, stale trajectory·환경 실패·불완전 group 처리 규칙을 구분한다.

- [ ] **검증 가능한 장기 agent 환경과 context 관리가 ‘agentic engineering’ 주장을 어디까지 뒷받침하는지 판단할 수 있다.**
  - **짚고 갈 개념:** executable verifier, F2P/P2P, Dockerized task, web knowledge graph, bidirectional verification, reward hacking, context management.
  - **함께 읽을 자료와 범위:** GLM-5가 직접 인용한 [SWE-bench Goes Live! v1 §3.3–§3.4](https://arxiv.org/abs/2505.23419v1)의 live issue→reproducible Docker 환경과 [Harbor task tutorial](https://harborframework.com/docs/tasks/task-tutorial)의 task schema·validator를 읽는다. GLM-5의 four environment families는 자체 본문에서 확인한다.
  - **원문에서 읽을 부분:** [GLM-5 v2](https://arxiv.org/abs/2602.15763v2) §4.2.1–§4.2.5, §6.2, Appendix B.4.1. SWE는 issue–PR→setup/log parsing→F2P/P2P, terminal은 seed/web corpus→Harbor task→self-validation, search는 WKG→multi-hop QA→양방향 검증, slide는 static/runtime/perceptual reward와 reward-hacking 보완으로 각각 그린다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [GLM-5 원문 v2](https://arxiv.org/abs/2602.15763v2)
