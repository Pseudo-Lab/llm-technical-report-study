# W15 — Motif 2 → Motif 3

[주차 목록](../README.md) · [W15 Background](../../background/w15.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Motif 2 → Motif 3
- arXiv: [Motif 2](https://arxiv.org/abs/2511.07464v1) → [Motif 3](https://arxiv.org/abs/2608.09119v1)
- 핵심 주제: GDA→GDLA의 신호·잡음 분리와 latent KV · Parallel Muon · seven-teacher MOPD
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **Differential Attention에서 GDA를 거쳐 GDLA로 갈 때, 비대칭 signal/noise head와 공유 latent KV가 각각 무엇을 해결하는지 설명할 수 있다.**
  - **짚고 갈 개념:** differential attention, asymmetric signal/noise head allocation, repeated noise head, low-rank latent KV, token-dependent \(\lambda\), output gate, sliding/full attention pattern. 차분·KV 압축·gate는 다른 병목을 다룬다.
  - **함께 읽을 자료와 범위:** [Differential Transformer](https://arxiv.org/abs/2410.05258v2) §2.1, [Grouped Differential Attention](https://arxiv.org/abs/2510.06949v1) §2.2, [DeepSeek-V2](https://arxiv.org/abs/2405.04434v5) §2.1을 순서대로 읽는다. 차분에 의한 잡음 억제, GDA의 capacity allocation, MLA의 KV-cache 압축을 한 효과로 합치지 않는다.
  - **원문에서 읽을 부분:** [Motif 2](https://arxiv.org/abs/2511.07464v1) §2; [Motif 3](https://arxiv.org/abs/2608.09119v1) §2.2.1–§2.2.3, Figure 1. 신호·잡음 경로가 shared latent를 한 번 확장한 뒤 어떻게 분기·차감·gate되는지 그린다.

- [ ] **Motif 2의 Parallel Muon이 full matrix Newton–Schulz update를 FSDP·TP+HSDP에서 어떻게 보존하면서 병렬화하는지 설명할 수 있다.**
  - **짚고 갈 개념:** full logical gradient matrix, Newton–Schulz update, gather–compute–scatter, All-to-All, pipelining, FLOPs-sorted scheduling, FSDP/TP/HSDP sharding semantics. optimizer collective와 long-context attention collective를 구별한다.
  - **함께 읽을 자료와 범위:** [Muon Is Scalable](https://arxiv.org/abs/2502.16982v1) §2.1–§2.3과 [Muon author note](https://kellerjordan.github.io/posts/muon/)의 “Definition”–“The design of Muon”으로 update 자체를 확인한다. Motif 2에서 full gradient matrix의 논리적 update가 gather–compute–scatter로 rank들에 어떻게 분할되는지 추적한다.
  - **원문에서 읽을 부분:** [Motif 2](https://arxiv.org/abs/2511.07464v1) §4.3, Algorithm 1, Figure 1, Table 4. non-pipelined·pipelined·FLOPs-sorted 설정을 throughput의 단일 원인으로 과장하지 않는다.

- [ ] **Motif 3가 verifier latency와 reward variance가 다른 domain을 seven specialist teacher와 MOPD로 통합하는 이유를 설명할 수 있다.**
  - **짚고 갈 개념:** domain reward surface, asynchronous GRPO, one-step staleness, token importance correction, teacher routing, frozen router/MTP, on-policy distillation, verifier type. 7 teacher는 6 GRPO teacher와 1 SWE SFT teacher이며 13 verifier domain을 다룬다.
  - **함께 읽을 자료와 범위:** Motif 3 §5.2.4가 직접 인용한 [Every Step Evolves (IcePop)](https://arxiv.org/abs/2510.18855v1) §2.3.2, 식 (1)–(3)을 읽어 probability-ratio interval과 범위 밖 token gradient masking을 확인한다. 이후 Motif 3의 `πold/πgen` filter가 IcePop의 training/inference mismatch 보정과 어떤 점에서 같고, teacher scalar log-probability만 쓰며 reward·reference KL을 빼는 MOPD와 어떤 점에서 다른지 구별한다.
  - **원문에서 읽을 부분:** [Motif 3](https://arxiv.org/abs/2608.09119v1) §5.1, §5.2.2–§5.2.4, 식 (35)–(37), Table 5. agent tool-use outcome verifier, professional-work judge reward, software-engineering successful-trajectory SFT를 한 reward로 뭉개지 않는다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료
