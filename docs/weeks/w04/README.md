# W04 — DeepSeek-V2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V2
- arXiv: [DeepSeek-V2 (v5)](https://arxiv.org/abs/2405.04434v5)
- 핵심 주제: MLA가 저장하는 KV 상태 · latent KV 압축과 decoupled RoPE · 메모리 절감과 실제 추론 병목
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] MLA가 MHA·MQA·GQA와 비교해 decoding 중 무엇을 저장하는지 설명할 수 있다.
  - **짚고 갈 개념:** autoregressive decoding, KV cache, MHA, MQA, GQA.
  - **함께 읽을 자료와 범위:** [Transformer v7](https://arxiv.org/pdf/1706.03762v7) §3.2.1–§3.2.2, [MQA v1](https://arxiv.org/pdf/1911.02150v1) §2.4·§3–§3.1, [GQA v3](https://arxiv.org/abs/2305.13245v3) §2.1–§2.2에서 KV 공유 범위를 비교한다.
  - **원문에서 읽을 부분:** [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) §2.1.1 “Preliminaries: Standard Multi-Head Attention”과 §2.1.4 “Comparison of Key-Value Cache”.
- [ ] latent KV 압축과 decoupled RoPE가 위치 정보를 보존하는 흐름을 예시로 설명할 수 있다.
  - **짚고 갈 개념:** low-rank projection, latent vector, RoPE, positional key.
  - **함께 읽을 자료와 범위:** [RoFormer v5](https://arxiv.org/abs/2104.09864v5) §3.2·§3.4.2의 rotary position embedding.
  - **원문에서 읽을 부분:** [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) §2.1.2 “Low-Rank Key-Value Joint Compression”–§2.1.3 “Decoupled Rotary Position Embedding”.
- [ ] MLA의 메모리 절감이 실제 추론 속도와 항상 같은 비율로 이어지지 않는 이유를 설명할 수 있다.
  - **짚고 갈 개념:** memory bandwidth, cache footprint, throughput, context length.
  - **함께 읽을 자료와 범위:** [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) §3.2.3 “Training and Inference Efficiency”의 system-level 조건.
  - **원문에서 읽을 부분:** [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) Appendix D “Ablation of Attention Mechanisms”, 특히 D.1 “Ablation of MHA, GQA, and MQA”와 D.2 “Comparison Between MLA and MHA”.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5)
- [Grouped-Query Attention v3](https://arxiv.org/abs/2305.13245v3)
- [Fast Transformer Decoding (MQA) v1](https://arxiv.org/abs/1911.02150v1)
- [RoFormer v5](https://arxiv.org/abs/2104.09864v5)
