# W03 — Qwen3

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen3
- arXiv: [Qwen3 (v1)](https://arxiv.org/abs/2505.09388v1)
- 핵심 주제: 생각·비생각 모드 통합 · 생각 예산 · 강한 교사에서 작은 모델로의 증류
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] Qwen3가 reasoning RL 모델의 능력을 보존하면서 instruction following·role-playing 같은 비생각 데이터를 한 모델에 합치는 데이터 구성과 chat template 규칙을 설명할 수 있다.
  - **짚고 갈 개념:** self-rejection sampling · thinking/non-thinking SFT data · quality checklist · `/think`·`/no think` · 빈 생각 블록 · 다회차 전환
  - **함께 읽을 자료와 범위:** [Qwen3 v1 §4.1–§4.2](https://arxiv.org/abs/2505.09388v1)에서 Stage-2 reasoning model이 만들어지는 범위만 확인한 뒤, §4.3의 thinking data rejection sampling, non-thinking data 구성, chat template 설계를 읽는다.
  - **원문에서 읽을 부분:** [Qwen3 v1 §4.3, Table 9 — Thinking Mode Fusion](https://arxiv.org/abs/2505.09388v1)
- [ ] 생각 예산을 늘리거나 중단할 때 답변이 어떻게 달라지는지, 길게 생각하는 것이 항상 유리하지 않은 이유와 함께 설명할 수 있다.
  - **짚고 갈 개념:** 추론 토큰 예산 · 강제 중단 · 테스트 시 계산량 · 긴 문맥 검색 · 추론 간섭
  - **함께 읽을 자료와 범위:** [Qwen3 v1 §4.3](https://arxiv.org/abs/2505.09388v1)의 강제 중단·`stop-thinking` 삽입을 먼저 읽고, [§4.7](https://arxiv.org/abs/2505.09388v1)의 budget 실험으로 이어 간다. 입력 문맥 길이 확장과 출력 생각 토큰 예산은 이 절들에서 별개로 다룬다.
  - **원문에서 읽을 부분:** [Qwen3 v1 §4.3·§4.7, Appendix A.1.1 — Thinking Budget, Discussion, Long-Context Ability](https://arxiv.org/abs/2505.09388v1)
- [ ] Qwen3의 strong-to-weak distillation이 생각·비생각 두 모드의 교사 출력을 옮긴 뒤, 학생이 생성한 같은 모드 prefix에서 logit을 맞추는 이유를 직접 강화학습과 비교해 설명할 수 있다.
  - **짚고 갈 개념:** mode-conditioned teacher distribution · off-policy response distillation · on-policy logit alignment · KL divergence · exploration
  - **함께 읽을 자료와 범위:** [Qwen3 v1 §4.5](https://arxiv.org/abs/2505.09388v1)에서 `/think`·`/no think` teacher response를 모두 쓰는 off-policy 단계와 학생 생성 sequence에서 logit을 맞추는 on-policy 단계를 읽고, [§4.7 Table 21](https://arxiv.org/abs/2505.09388v1)의 동일 checkpoint 직접 RL 비교로 이어 간다.
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
