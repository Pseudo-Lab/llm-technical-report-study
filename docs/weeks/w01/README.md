# W01 — LLaMA 1 → Llama 2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: LLaMA 1 → Llama 2
- arXiv: [LLaMA 1 (v1)](https://arxiv.org/abs/2302.13971v1) → [Llama 2 (v2)](https://arxiv.org/abs/2307.09288v2)
- 핵심 주제: 계산 예산에 맞춘 사전학습 · 위치 정보와 KV 공유 · 대화형 정렬과 안전성
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] 같은 계산 예산에서 모델 크기와 학습 토큰, 추론 비용을 함께 맞추는 LLaMA의 사전학습 설계를 설명할 수 있다.
  - **짚고 갈 개념:** 계산 최적 스케일링 · 데이터 혼합 · 중복 제거 · 자기회귀 사전학습
  - **함께 읽을 자료와 범위:** [Chinchilla v1 §1·§3](https://arxiv.org/abs/2203.15556v1)에서 고정 FLOPs의 매개변수·토큰 배분을 읽어, LLaMA의 출발점을 잡는다.
  - **원문에서 읽을 부분:** [LLaMA 1 v1 §2.1–§2.4 — Pre-training Data, Optimizer, Efficient implementation](https://arxiv.org/abs/2302.13971v1)
- [ ] RoPE와 MHA/GQA의 역할을 구분하고, Llama 2가 긴 문맥과 추론 비용을 고려해 GQA를 채택한 이유를 설명할 수 있다.
  - **짚고 갈 개념:** Transformer block · MHA · KV cache · GQA · RoPE
  - **함께 읽을 자료와 범위:** [RoFormer v5 §3.2](https://arxiv.org/abs/2104.09864v5)로 RoPE를, [GQA v3 §2.2](https://arxiv.org/abs/2305.13245v3)로 KV 공유를 읽어 채택과 제안을 구분한다.
  - **원문에서 읽을 부분:** [Llama 2 v2 §2.1 및 Appendix A.2.1 — Pretraining Data, Architecture Changes Compared to Llama 1](https://arxiv.org/abs/2307.09288v2)
- [ ] 기반 모델을 대화형 모델로 바꾸는 SFT·선호학습·안전 정렬의 순서와, 도움됨과 안전성 사이의 한계를 설명할 수 있다.
  - **짚고 갈 개념:** SFT · 선호 쌍 · 보상 모델 · 거절 샘플링 · 과잉 거절
  - **함께 읽을 자료와 범위:** [InstructGPT v1 §3.1·§3.5](https://arxiv.org/abs/2203.02155v1)에서 SFT→보상 모델→PPO의 기본 흐름을 읽어 Llama 2의 변형을 비교한다.
  - **원문에서 읽을 부분:** [Llama 2 v2 §3.1–§3.3, §4.2–§4.4 — Supervised Fine-Tuning, RLHF, System Message, Safety Fine-Tuning](https://arxiv.org/abs/2307.09288v2)

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [LLaMA: Open and Efficient Foundation Language Models (v1)](https://arxiv.org/abs/2302.13971v1)
- [Llama 2: Open Foundation and Fine-Tuned Chat Models (v2)](https://arxiv.org/abs/2307.09288v2)
