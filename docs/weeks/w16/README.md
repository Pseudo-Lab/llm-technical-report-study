# W16 — Solar Open → Solar Open 2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Solar Open → Solar Open 2
- arXiv: [Solar Open v1](https://arxiv.org/abs/2601.07022v1) → [Solar Open 2 v2](https://arxiv.org/abs/2607.20062v2)
- 핵심 주제: 저자원 언어 데이터·SnapPO · NoPE 상태 · 선택적 weight transfer
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **Solar Open이 저자원 언어의 데이터 부족과 RL 운영을 서로 다른 개입으로 다룬 방식을 설명할 수 있다.**
  - **짚고 갈 개념:** 합성 데이터·curriculum·tokenizer는 데이터 병목을, SnapPO는 생성·보상·학습의 분리를 다룬다.
  - **함께 읽을 자료와 범위:** [Solar Open v1](https://arxiv.org/abs/2601.07022v1)의 tokenizer·데이터·SnapPO 절을 읽는다. 비동기 RL(W12)은 빼고 스냅샷·캐시만 확인한다.
  - **원문에서 읽을 부분:** Solar Open `1.2 Challenges and Our Solutions`, `2.1 Solar Open Tokenizer`, `3.1 Data Construction and Composition`, `3.2 Curriculum Learning Strategy`, `6.1 SnapPO Framework`.

- [ ] **KDA의 고정 상태가 Solar Open 2에서 NoPE와 음의 고유값으로 확장되는 이유를 설명할 수 있다.**
  - **짚고 갈 개념:** 선형 attention의 순차 상태와 softmax의 전역 회상을 섞는다. 음의 고유값은 상태가 감쇠·유지에만 머물지 않고 수정될 여지를 준다.
  - **함께 읽을 자료와 범위:** [Kimi Linear v2](https://arxiv.org/abs/2510.26692v2) `2.2`, `3`; [Unlocking State-Tracking v5](https://arxiv.org/abs/2411.12537v5) `3.1`, `4.1`–`4.2`; [PE Length Generalization v2](https://arxiv.org/abs/2305.19466v2) `4`–`5` — KDA 갱신·음의 고유값·NoPE를 확인한다.
  - **원문에서 읽을 부분:** Solar Open 2 `2.2 Solar Open 2 Architecture`, `Figure 3`.

- [ ] **선택적 weight transfer가 기존 모듈을 보존하면서 구조 전환을 시작하는 기준을 설명할 수 있다.**
  - **짚고 갈 개념:** 같은 표현·형상인 모듈만 옮기고, 새 attention 상태와 대응 없는 routed expert는 초기화한다. 이는 부분 warm start다.
  - **함께 읽을 자료와 범위:** [Sparse Upcycling v2](https://arxiv.org/abs/2212.05055v2) `3`–`3.1`, [Priming v1](https://arxiv.org/abs/2605.08301v1) `2.2`, `3.2.2`–`3.2.4` — checkpoint를 MoE·hybrid 구조에 잇는 대비를 확인한다.
  - **원문에서 읽을 부분:** Solar Open 2 `3.1 Selective Weight Transfer`, `Table 2`, `Figure 6`.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료
