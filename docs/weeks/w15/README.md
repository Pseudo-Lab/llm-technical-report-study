# W15 — Motif 2 → Motif 3

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Motif 2 → Motif 3
- arXiv: [Motif 2 v1](https://arxiv.org/abs/2511.07464v1) → [Motif 3 v1](https://arxiv.org/abs/2608.09119v1)
- 핵심 주제: 차분 attention의 신호·잡음 분리·잠재 KV · 학습 안정화
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **Differential Attention에서 GDA를 거쳐 GDLA로 이어지는 설계 차이를 설명할 수 있다.**
  - **짚고 갈 개념:** 두 attention map의 차분은 잡음을 억제하고, GDA는 신호 head를 더 많이 둔다. GDLA는 여기에 압축 KV를 결합한다.
  - **함께 읽을 자료와 범위:** [Differential Transformer v2](https://arxiv.org/abs/2410.05258v2) `2.1`, [Grouped Differential Attention v1](https://arxiv.org/abs/2510.06949v1) `2.2` — 차분과 비대칭 grouping의 출발점이다.
  - **원문에서 읽을 부분:** Motif 2 `2 Architecture`; Motif 3 `2.2 Grouped Differential Latent Attention`.

- [ ] **GDLA가 공유 잠재 KV와 토큰별 잡음 조절을 한 attention 흐름으로 묶는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** 신호·잡음 경로는 같은 압축 KV를 쓰고, 반복된 잡음 출력을 토큰별 계수로 뺀 뒤 출력 게이트를 적용한다. KV 압축과 잡음 억제가 해결하는 병목은 다르다.
  - **함께 읽을 자료와 범위:** [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5) `2.1 Multi-head Latent Attention` — MLA의 압축 KV가 GDLA에 들어오는 이유를 확인한다.
  - **원문에서 읽을 부분:** Motif 3 `2.2.1 Latent Query and Key-Value Representations`–`2.2.3 Output Gating`, `Figure 1`.

- [ ] **Motif 2와 Motif 3의 안정화가 각각 분산 optimizer와 모델 내부 상태를 다룬다는 점을 설명할 수 있다.**
  - **짚고 갈 개념:** Parallel Muon은 통신·메모리·부하의 학습 시스템 문제이고, 수정 mHC·QK-Clip·MoE 안정화는 잔차·logit·expert 사용의 모델 안정성 문제다.
  - **함께 읽을 자료와 범위:** [mHC v2](https://arxiv.org/abs/2512.24880v2) `3`, `4.1`–`4.2`; [Muon 저자 노트](https://kellerjordan.github.io/posts/muon/) `Definition`, `The design of Muon`; [Muon Is Scalable v1](https://arxiv.org/abs/2502.16982v1) `2.1`–`2.3` — residual read/write와 Newton–Schulz 갱신을 확인한다.
  - **원문에서 읽을 부분:** Motif 2 `4.3 Parallel Muon`; Motif 3 `2.3 Modified Manifold-Constrained Hyper-Connections`, `3.3 Muon Optimizer`, `4.2 MoE Training Stabilization`.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료
