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
  - **함께 읽을 자료와 범위:** [Longformer v2](https://arxiv.org/abs/2004.05150v2) §3.1로 window·global pattern을 확인하고, Flash가 sink 구현의 출처로 밝힌 [gpt-oss model card v1 §2.2](https://arxiv.org/pdf/2508.10925v1)와 Flash §2.2 식 (1)–(4)을 읽는다.
  - **원문에서 읽을 부분:** [MiMo-V2-Flash v2](https://arxiv.org/pdf/2601.02780v2) §2.1–§2.2 “Hybrid SWA Architecture”, Fig. 1, 식 (1)–(4).

- [ ] Flash가 MTP를 self-speculative draft로 재목적화하면서 dense FFN·SWA·pretrain 1-head/posttrain K-head 설계로 KV I/O와 RL rollout 병목을 어떻게 줄이려 했는지 설명할 수 있다.
  - **짚고 갈 개념:** self-speculative decoding · arithmetic intensity · KV-cache I/O · draft/verify · acceptance length · rollout straggler
  - **함께 읽을 자료와 범위:** [MiMo-V2-Flash v2](https://arxiv.org/pdf/2601.02780v2) §2.3.1–§2.3.2 → §5.1–§5.2를 읽는다. [DeepSeek-V3 v2](https://arxiv.org/pdf/2412.19437v2) §2.2는 sequential MTP의 원형 비교에만 쓴다.
  - **원문에서 읽을 부분:** [MiMo v2 §2.2](https://arxiv.org/pdf/2505.07608v2)와 [MiMo-V2-Flash v2 §2.3, §5.1–§5.2 — Efficient MTP](https://arxiv.org/pdf/2601.02780v2)

- [ ] MOPD가 prompt의 도메인별 전문 교사를 선택해 학생 rollout의 token-level reverse-KL advantage를 만들고, 이를 ORM/GRPO outcome advantage와 결합하는 방식을 설명할 수 있다.
  - **짚고 갈 개념:** domain-specialized teacher · on-policy rollout · reverse KL · token-level advantage · outcome reward model
  - **함께 읽을 자료와 범위:** [GKD v3](https://arxiv.org/pdf/2306.13649v3) §2–§3은 student-generated sequence를 쓰는 단일 교사 배경으로만 읽고, Flash §4.1·§4.4에서 domain teacher 선택과 ORM 결합을 확인한다.
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
- [gpt-oss-120b & gpt-oss-20b Model Card v1](https://arxiv.org/abs/2508.10925v1)
