# W09 — DeepSeek-V4

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V4
- arXiv: [DeepSeek-V4 (v1)](https://arxiv.org/abs/2606.19348v1)
- 핵심 주제: CSA의 block compression+DSA · HCA의 강한 dense compression · specialist→OPD 통합
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 먼저 읽을 배경

1. [V4 전체 구성요소 가이드](../../background/w09.md)의 `전체 그림` 표에서 MoE/MTP·mHC·Muon·분산 실행·data/OPD 행을 먼저 훑는다. 이들은 CSA/HCA와 별도 층위이지만 V4가 어떤 recipe를 새로 바꾸었는지 가르는 기준이다.
2. 이어 같은 가이드의 CSA/HCA 행과 V4 §2.3을 읽는다. **KV 내용을 block entry로 압축하는 일**과 **압축 entry 중 top-k를 고르는 일**을 한 단계로 부르지 않는다.
3. 마지막으로 specialist GRPO/GRM → full-vocabulary OPD → hidden-state cache/teacher scheduling 순서로 §5.1–§5.2를 읽는다. scalar reward specialist training과 teacher-logit distillation은 같은 objective가 아니다.

## 학습목표

- [ ] CSA가 sequence 방향으로 KV block을 압축한 뒤 DSA로 top-k block을 선택하는 두 단계를 설명할 수 있다.
  - **짚고 갈 개념:** learned block compression, overlapping context, lightning indexer, MQA, causal top-k, sliding-window raw KV, partial RoPE.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1–§2.1.1에서 DSA의 indexer와 token-level selection을 확인한다. DeepSeek-V4의 CSA는 여기에 sequence block KV entry를 먼저 만든 뒤 DSA를 적용한다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.1 “Compressed Sparse Attention”, Fig. 3, 식 (9)–(19).

- [ ] HCA가 CSA와 달리 강하게 압축한 KV 전체에 dense attention을 적용하는 이유와, 두 층을 섞을 때의 역할 분담을 설명할 수 있다.
  - **짚고 갈 개념:** compression ratio, dense attention, shared-KV MQA, grouped output projection, information loss, attention sink, BF16/FP8 cache.
  - **함께 읽을 자료와 범위:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.3–§2.3.4의 sliding-window 보완과 비용 논의. 압축률만으로 품질을 단정할 수 없는 이유를 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.2 “Heavily Compressed Attention”, Fig. 4, 식 (20)–(26).

- [ ] **V4가 여러 specialist의 full-vocabulary OPD 신호를 hidden-state cache와 teacher별 batch scheduling으로 처리하는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** specialist SFT/GRPO, generative reward model, student on-policy support, reverse KL, full-vocabulary teacher signal, hidden-state/logit reconstruction.
  - **함께 읽을 자료와 범위:** V4가 인용한 [MiniLLM v1](https://arxiv.org/abs/2306.08543v1) §2.1–§2.2, 식 (1)–(7)로 reverse-KL과 student-sampled optimization을 확인한다. W07의 MiMo가 ORM/GRPO outcome advantage를 결합하는 경우와 달리, 이 목표의 중심은 V4 자체의 full-vocabulary OPD scheduling이다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §5.1.1–§5.1.2, 식 (29), §5.2.2. 특히 teacher hidden state cache→prediction head로 full logits 재구성, teacher-index batch ordering, TileLang exact-KL을 추적한다. student가 낸 위치에서 관련 teacher 분포를 맞추는 것과 offline teacher 답안을 모방하는 것을 구별한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [DeepSeek-V4 v1](https://arxiv.org/abs/2606.19348v1)
- [MiniLLM v1](https://arxiv.org/abs/2306.08543v1)
