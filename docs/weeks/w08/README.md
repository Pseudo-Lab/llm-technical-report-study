# W08 — MiMo → MiMo-V2-Flash

[주차 목록](../README.md) · [W08 Background](../../background/w08.md) · [주간 템플릿](../../../templates/week.md)

**읽기 분담:** [이번 주 공통 읽기와 팀별 심화](../../background/workload.md)를 기준으로 개인 준비 3–4시간을 배분합니다. 상세 Background는 공통 범위와 담당 갈래에 필요한 부분을 찾아 읽고, 세 학습목표는 모임 후 함께 설명할 수 있도록 정리합니다.

## 논문 정보

- 논문: MiMo → MiMo-V2-Flash
- arXiv: [MiMo (v2)](https://arxiv.org/abs/2505.07608v2) → [MiMo-V2-Flash (v2)](https://arxiv.org/abs/2601.02780v2)
- 핵심 주제: MiMo의 reasoning data·verifier-RL → Flash의 hybrid SWA/GA·deployment MTP·MOPD
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] MiMo가 reasoning pattern을 잃지 않도록 extraction·dedup·quality tagging·3-stage mixture를 어떻게 조합했고, MTP를 학습용 1개 layer와 추론용 여러 draft layer로 왜 나눴는지 설명할 수 있다.
  - **짚고 갈 개념:** reasoning-density preservation, MinHash deduplication, content-aware quality tagger, synthetic reasoning response, data mixture, MTP objective/draft/acceptance.
  - **함께 읽을 자료와 범위:** [W08 개념 경로 §1–§2](../../background/w08.md#mimo-pretraining) → MiMo가 직접 인용한 [MTP v1 §2·§3.2](https://arxiv.org/abs/2404.19737v1). GQA·RMSNorm·SwiGLU·RoPE는 이 보고서의 새 제안이 아니므로 [W01](../../background/w01.md)·[W03](../../background/w03.md)에서 필요한 만큼만 복습한다.
  - **원문에서 읽을 부분:** [MiMo v2 §2.1–§2.3, Fig. 2](https://arxiv.org/pdf/2505.07608v2).

- [ ] MiMo가 verifier-RL에서 code test 난도, dynamic sampling, easy-data re-sampling, Seamless Rollout Engine을 왜 함께 설계했는지 설명할 수 있다.
  - **짚고 갈 개념:** rule-based reward, test-case difficulty, strict/soft partial reward, effective gradient, dynamic sampling, straggler, asynchronous reward computation.
  - **함께 읽을 자료와 범위:** [W08 개념 경로 §3](../../background/w08.md#mimo-verifier-rl) → MiMo §3.1–§3.4. GRPO 기본식은 [W07](../../background/w07.md#verifiable-rl)에서 가져오되, MiMo의 reward/sampling/engine을 R1 recipe로 바꾸어 쓰지 않는다.
  - **원문에서 읽을 부분:** [MiMo v2 §3.1–§3.4.1, Fig. 5–6, §3.6](https://arxiv.org/pdf/2505.07608v2).

- [ ] Flash가 MiMo의 dense GQA model을 hybrid SWA/GA·lightweight MTP로 바꾸고, domain teacher MOPD와 MoE rollout system을 어떻게 결합했는지 설명할 수 있다.
  - **짚고 갈 개념:** sliding-window/global attention, learnable sink logit, self-speculative decoding, reverse-KL advantage, domain teacher routing, Rollout Routing Replay, sequence scheduler.
  - **함께 읽을 자료와 범위:** [W08 개념 경로 §4](../../background/w08.md#flash-changes) → SWA/GA의 [Longformer v2 §3–§3.1](https://arxiv.org/abs/2004.05150v2), sink의 [gpt-oss model card v1 §2.2](https://arxiv.org/pdf/2508.10925v1), student rollout distillation의 [On-Policy Distillation v3 §2–§3](https://arxiv.org/pdf/2306.13649v3). 각각 Flash가 본문에서 직접 인용한 배경이며, MOPD 자체는 Flash의 조합이다.
  - **원문에서 읽을 부분:** [MiMo-V2-Flash v2 §2.1–§2.3, Fig. 2, 식 (1)–(4), §4.1·§4.4 식 (5)–(9), §4.6, §5.1–§5.2](https://arxiv.org/pdf/2601.02780v2).

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
- [gpt-oss-120b & gpt-oss-20b Model Card v1](https://arxiv.org/abs/2508.10925v1)
