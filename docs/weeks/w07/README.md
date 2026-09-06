# W07 — MiMo → MiMo-V2-Flash

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: MiMo → MiMo-V2-Flash
- arXiv: [MiMo (v2)](https://arxiv.org/abs/2505.07608v2) → [MiMo-V2-Flash (v2)](https://arxiv.org/abs/2601.02780v2)
- 핵심 주제: hybrid SWA/GA와 learnable attention sink · 경량 MTP draft · MOPD
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] SWA/GA 혼합이 모든 층의 global attention과 무엇이 다르며, local 문맥과 장거리 연결을 어떻게 나누는지 설명할 수 있다.
  - **짚고 갈 개념:** sliding-window attention, global attention, receptive field, learnable sink logit.
  - **함께 읽을 자료와 범위:** [Longformer v2](https://arxiv.org/abs/2004.05150v2) §3.1의 window·global pattern. sink logit은 StreamingLLM의 캐시된 sink token과 구별한다.
  - **원문에서 읽을 부분:** [MiMo-V2-Flash v2](https://arxiv.org/pdf/2601.02780v2) §2.1–§2.2 “Hybrid SWA Architecture”, Fig. 1, 식 (1)–(4).

- [ ] MiMo의 MTP 학습 head가 Flash에서 왜 더 가벼운 speculative draft로 바뀌었는지, acceptance rate와 함께 설명할 수 있다.
  - **짚고 갈 개념:** sequential MTP, shared head, draft/verify, acceptance rate.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3 v2](https://arxiv.org/pdf/2412.19437v2) §2.2–§2.2.2의 sequential MTP. 기본 유도는 W05에서 복습하고 여기서는 MiMo 계열의 설계 변경을 본다.
  - **원문에서 읽을 부분:** [MiMo v2](https://arxiv.org/pdf/2505.07608v2) §2.2 “Model Architecture”와 [MiMo-V2-Flash v2](https://arxiv.org/pdf/2601.02780v2) §2.3 “Efficient MTP Architecture”.

- [ ] MOPD가 학생의 자체 생성 trajectory에 여러 전문 교사의 token 신호와 outcome reward를 결합하는 이유를 설명할 수 있다.
  - **짚고 갈 개념:** on-policy distillation, reverse KL, specialized teacher, outcome reward model.
  - **함께 읽을 자료와 범위:** [GKD v3](https://arxiv.org/pdf/2306.13649v3) §2–§3의 student-generated sequence와 reverse KL. 교사 답을 그대로 모사하는 KD와의 차이를 확인한다.
  - **원문에서 읽을 부분:** [MiMo-V2-Flash v2](https://arxiv.org/pdf/2601.02780v2) §4.1 “MOPD”와 §4.4 “Multi-Teacher Online Policy Distillation”, 식 (5)–(9).

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [MiMo v2](https://arxiv.org/abs/2505.07608v2)
- [MiMo-V2-Flash v2](https://arxiv.org/abs/2601.02780v2)
- [Longformer v2](https://arxiv.org/abs/2004.05150v2)
- [On-Policy Distillation of Language Models v3](https://arxiv.org/abs/2306.13649v3)
