# W09 — DeepSeek-V4

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V4
- arXiv: [DeepSeek-V4 (v1)](https://arxiv.org/abs/2606.19348v1)
- 핵심 주제: CSA의 block compression+DSA · HCA의 강한 dense compression · mHC와 Muon
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] CSA가 sequence 방향으로 KV block을 압축한 뒤 DSA로 top-k block을 선택하는 두 단계를, MLA/DSA와 비교해 설명할 수 있다.
  - **짚고 갈 개념:** KV compression, block representation, sparse retrieval, local uncompressed branch.
  - **함께 읽을 자료와 범위:** [DeepSeek-V2 v5](https://arxiv.org/pdf/2405.04434v5) §2.1의 MLA는 latent 차원의 KV 저장 압축이라는 비교 축이고, [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1의 DSA는 sparse selection의 출발점이다. CSA는 sequence block KV entry를 만든 뒤 DSA를 적용한다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.1 “Compressed Sparse Attention”, Fig. 3, 식 (9)–(19).

- [ ] HCA가 CSA와 달리 강하게 압축한 KV 전체에 dense attention을 적용하는 이유와, 두 층을 섞을 때의 역할 분담을 설명할 수 있다.
  - **짚고 갈 개념:** compression ratio, dense attention, shared-KV MQA, grouped output projection, information loss.
  - **함께 읽을 자료와 범위:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.3–§2.3.4의 sliding-window 보완과 비용 논의. 압축률만으로 품질을 단정할 수 없는 이유를 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.2 “Heavily Compressed Attention”, Fig. 4, 식 (20)–(26).

- [ ] mHC의 doubly stochastic residual mapping과 Muon의 Newton–Schulz 직교화가 각각 안정성 및 update geometry를 어떻게 바꾸는지 설명할 수 있다.
  - **짚고 갈 개념:** expanded residual stream, Birkhoff polytope, Sinkhorn–Knopp, SVD, semi-orthogonal update.
  - **함께 읽을 자료와 범위:** [Hyper-Connections v3](https://arxiv.org/pdf/2409.19606v3) §2.1–§2.2, [mHC v2](https://arxiv.org/pdf/2512.24880v2) §3–§4.2, [Muon author note](https://kellerjordan.github.io/posts/muon/) “Definition”–“The design of Muon”.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.2 “Manifold-Constrained Hyper-Connections” 및 §2.4 “Muon Optimizer”, 식 (5)–(8), (27)–(28), Algorithm 1.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [DeepSeek-V4 v1](https://arxiv.org/abs/2606.19348v1)
- [mHC v2](https://arxiv.org/abs/2512.24880v2)
- [Hyper-Connections v3](https://arxiv.org/abs/2409.19606v3)
- [Muon: author note](https://kellerjordan.github.io/posts/muon/)
