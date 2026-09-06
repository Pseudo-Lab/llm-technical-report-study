# W09 — DeepSeek-V4

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: DeepSeek-V4
- arXiv: [DeepSeek-V4 (v1)](https://arxiv.org/abs/2606.19348v1)
- 핵심 주제: CSA의 block compression+DSA · HCA의 강한 dense compression · specialist→OPD 통합
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] CSA가 sequence 방향으로 KV block을 압축한 뒤 DSA로 top-k block을 선택하는 두 단계를 설명할 수 있다.
  - **짚고 갈 개념:** KV compression, block representation, sparse retrieval, local uncompressed branch.
  - **함께 읽을 자료와 범위:** [DeepSeek-V3.2 v1](https://arxiv.org/pdf/2512.02556v1) §2.1–§2.1.1에서 DSA의 indexer와 token-level selection을 확인한다. DeepSeek-V4의 CSA는 여기에 sequence block KV entry를 먼저 만든 뒤 DSA를 적용한다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.1 “Compressed Sparse Attention”, Fig. 3, 식 (9)–(19).

- [ ] HCA가 CSA와 달리 강하게 압축한 KV 전체에 dense attention을 적용하는 이유와, 두 층을 섞을 때의 역할 분담을 설명할 수 있다.
  - **짚고 갈 개념:** compression ratio, dense attention, shared-KV MQA, grouped output projection, information loss.
  - **함께 읽을 자료와 범위:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.3–§2.3.4의 sliding-window 보완과 비용 논의. 압축률만으로 품질을 단정할 수 없는 이유를 확인한다.
  - **원문에서 읽을 부분:** [DeepSeek-V4 v1](https://arxiv.org/pdf/2606.19348v1) §2.3.2 “Heavily Compressed Attention”, Fig. 4, 식 (20)–(26).

- [ ] **V4가 여러 specialist의 full-vocabulary OPD 신호를 hidden-state cache와 teacher별 batch scheduling으로 처리하는 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** specialist, teacher routing, student on-policy support, reverse KL, full-vocabulary teacher signal.
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
