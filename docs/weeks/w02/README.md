# W02 — Qwen2 → Qwen2.5

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen2 → Qwen2.5
- arXiv: [Qwen2 (v4)](https://arxiv.org/abs/2407.10671v4) → [Qwen2.5 (v2)](https://arxiv.org/abs/2412.15115v2)
- 핵심 주제: 데이터 품질과 도메인 혼합 · 단계적 문맥 확장 · 검증 가능한 후학습 자료
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] 학습 자료의 총량과 품질 선별·도메인 혼합을 구분하고, Qwen2에서 Qwen2.5로 바뀐 데이터 설계를 설명할 수 있다.
  - **짚고 갈 개념:** 품질 필터 · 합성 자료 · 도메인 혼합 · 다국어 자료 · 스케일링 실험
  - **함께 읽을 자료와 범위:** [Chinchilla v1 §1·§3](https://arxiv.org/abs/2203.15556v1)으로 토큰 규모의 배경을 읽고, 품질·도메인 비율은 별도 설계임을 구분한다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §3.1 — Pre-training Data](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 v2 §3.1–§3.2 — Pre-training Data, Scaling Law for Hyper-parameters](https://arxiv.org/abs/2412.15115v2)
- [ ] 실제로 학습한 문맥 길이와 위치 정보를 외삽해 처리하는 길이를 구분하고, 단계적 문맥 확장의 목적과 한계를 설명할 수 있다.
  - **짚고 갈 개념:** 문맥 길이 커리큘럼 · RoPE · YaRN · DCA · 길이 외삽
  - **함께 읽을 자료와 범위:** [YaRN v3 §3.1–§3.3](https://arxiv.org/abs/2309.00071v3)과 [DCA v2 §2.2·§3–§3.4](https://arxiv.org/abs/2402.17463v2)로 위치 스케일링과 chunk attention을 나누어 읽는다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §3.2 — Long-context Training](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 v2 §3.3·§4.4 — Long-context Pre-training, Long Context Fine-tuning](https://arxiv.org/abs/2412.15115v2)
- [ ] 수학·코드처럼 검증 가능한 과제와 사람 선호가 필요한 과제를 나누어, Qwen 계열이 후학습 자료를 생성·필터링한 흐름을 설명할 수 있다.
  - **짚고 갈 개념:** 실행 피드백 · 거절 샘플링 · 선호 쌍 · 데이터 검수 · 보상 모델
  - **함께 읽을 자료와 범위:** [DPO v3 §3–§4](https://arxiv.org/abs/2305.18290v3)로 선호 쌍의 직접 최적화를 읽고, Qwen의 검증 자료 생성과 구분한다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §4.1–§4.3 — Post-training Data, Collaborative Data Annotation, Automated Data Synthesis](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 v2 §4.1–§4.2 — Supervised Fine-tuning, Offline Reinforcement Learning](https://arxiv.org/abs/2412.15115v2)

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen2 Technical Report (v4)](https://arxiv.org/abs/2407.10671v4)
- [Qwen2.5 Technical Report (v2)](https://arxiv.org/abs/2412.15115v2)
