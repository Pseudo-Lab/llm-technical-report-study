# W06 — DeepSeek-V3

[주차 목록](../README.md) · [W06 Background](../../background/w06.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V3
- arXiv: [DeepSeek-V3](https://arxiv.org/abs/2412.19437v2)
- 핵심 주제: 채택한 auxiliary-loss-free MoE 균형 · sequential MTP · FP8 mixed-precision 학습
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] V3가 채택한 auxiliary-loss-free balancing이 MoE routing 불균형을 줄이는 방식을 설명할 수 있다.
  - **짚고 갈 개념:** MoE router, top-k routing, expert load, routing bias.
  - **함께 읽을 자료와 범위:** [DeepSeekMoE](https://arxiv.org/pdf/2401.06066v1) §2–§3.3과 [Loss-Free Balancing](https://arxiv.org/pdf/2408.15664v1) §2–§3. 이 기법은 V3의 신규 제안이 아니라 선행 방법의 채택이다.
  - **원문에서 읽을 부분:** [DeepSeek-V3](https://arxiv.org/pdf/2412.19437v2) §2.1.2 “DeepSeekMoE with Auxiliary-Loss-Free Load Balancing”.
- [ ] sequential MTP가 병렬 multi-token head와 달리 예측을 인과적으로 연결하는 방식을 설명할 수 있다.
  - **짚고 갈 개념:** next-token prediction, causal chain, shared head, speculative decoding.
  - **함께 읽을 자료와 범위:** [MTP](https://arxiv.org/pdf/2404.19737v1) §2 “Method”와 [Speculative Decoding](https://arxiv.org/pdf/2211.17192v2) §2.1–§2.3.
  - **원문에서 읽을 부분:** [DeepSeek-V3](https://arxiv.org/pdf/2412.19437v2) §2.2 “Multi-Token Prediction”–§2.2.2 “MTP Module”.
- [ ] V3의 FP8 mixed-precision 설계가 tile/block scaling과 FP32 accumulation으로 정확도와 안정성을 관리하는 범위를 설명할 수 있다.
  - **짚고 갈 개념:** FP8 format, tile/block scaling, outlier, FP32 accumulation.
  - **함께 읽을 자료와 범위:** [FP8 Formats](https://arxiv.org/pdf/2209.05433v2) §2–§3.2로 format/range를 확인한 뒤, V3가 직접 인용한 [FP8-LM §2.1–§2.2, Appendix A.2](https://arxiv.org/pdf/2310.18313v2)와 V3 §3.3.1–§3.3.3을 읽는다.
  - **원문에서 읽을 부분:** [DeepSeek-V3 §3.3.1–§3.3.3, Fig. 6–7, Appendix B.1 — FP8 Training](https://arxiv.org/pdf/2412.19437v2)

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [DeepSeek-V3](https://arxiv.org/abs/2412.19437v2)
- [Auxiliary-Loss-Free Load Balancing](https://arxiv.org/abs/2408.15664v1)
- [Multi-token Prediction](https://arxiv.org/abs/2404.19737v1)
- [FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433v2)
- [FP8-LM](https://arxiv.org/abs/2310.18313v2)
