# W02 — Qwen1.5 → Qwen2 → Qwen2.5

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen1.5 → Qwen2 → Qwen2.5
- arXiv: [Qwen2 (v4)](https://arxiv.org/abs/2407.10671v4) → [Qwen2.5 (v2)](https://arxiv.org/abs/2412.15115v2)
- 핵심 주제: Qwen1.5 대비 구조·BBPE · instruction 선별·확장 · 검증 신호별 합성 데이터
- Qwen1.5 비교 자료: [공식 출시 글](https://qwenlm.github.io/blog/qwen1.5/) · [고정 checkpoint 비교](../../background/qwen.md#qwen-architecture) — 논문과 구현 자료를 구분해 읽습니다.
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] Qwen1.5 → Qwen2 → Qwen2.5의 구조·토크나이저 변경표를 만들고, 유지된 요소와 모델 크기에 따라 달라지는 요소를 설명할 수 있다.
  - **짚고 갈 개념:** MHA/GQA의 KV-head 공유 · dense/MoE 분기 · DCA와 YaRN · 학습 길이와 확장 길이 · BBPE의 regular/control token
  - **함께 읽을 자료와 범위:** [Qwen 계열 구조·토크나이저 가이드](../../background/qwen.md#qwen-architecture)의 대응 7B config와 GQA·DCA·YaRN·MoE 초기화·Qwen tokenizer 원전 범위를 따른다. Qwen1.5-7B의 MHA→Qwen2-7B의 GQA를 계열 전체 변화로 일반화하지 않는다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §2.1–§2.2·§3.2](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 v2 §2·§3.3](https://arxiv.org/abs/2412.15115v2). Qwen1.5는 공식 자료·고정 config를 대조한다. BBPE의 계승과 control token 확장, 32K 학습과 128K 처리 주장을 각각 구분한다.
- [ ] Qwen2가 instruction pool을 선별·확장하고 역할극 자료로 재구성하는 방법을, Qwen2.5의 system prompt·대화 일관성 설계와 연결해 설명할 수 있다.
  - **짚고 갈 개념:** instruction selection · instruction evolution · ontology extraction · profile-conditioned role-play · system-prompt consistency
  - **함께 읽을 자료와 범위:** [Instruction pool의 선별·확장](../../background/qwen.md#instruction-pool)에서 각 방법의 본문 인용과 원전을 읽고, [Ditto v1 §3.2–§3.4](https://arxiv.org/abs/2401.12474v1)의 profile→질문→역할 응답을 따른다. Qwen2.5의 robust system prompt가 Ditto의 전체 인물 생성 pipeline을 채택한 것인지는 본문이 밝힌 범위로 판단한다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §4.1.1–§4.1.2](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 v2 §4.1(8)](https://arxiv.org/abs/2412.15115v2). instruction을 고르는 단계, 새 instruction을 만드는 단계, 조건에 맞는 response를 만드는 단계를 구분한다.
- [ ] 지시 수행·수학·코드의 합성 데이터를 검증할 때 checker·정답·보상 모델·sandbox·critic이 제공하는 신호의 차이를 설명할 수 있다.
  - **짚고 갈 개념:** executable constraint · verification code/unit test · rejection sampling · final-answer check · reward model · critic agreement
  - **함께 읽을 자료와 범위:** [과제별 합성·검증 가이드](../../background/qwen.md#task-synthesis)의 AutoIF §3.2–§3.4, Qwen2.5-Math §3.1.1–§3.2.1, Qwen2.5-Coder §4.1을 읽는다. [IFEval v1 §2.1–§2.2](https://arxiv.org/abs/2311.07911v1)은 Qwen의 평가 자료로 구분한다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §4.1.2](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 v2 §3.1·§4.1(2)–(4)·(9)·§4.2·§5.2.1](https://arxiv.org/abs/2412.15115v2). instruction→checker/test→실행→pass/fail→SFT/DPO 경로를 그린 뒤, 수학·코드·critic 필터가 같은 정확도 보장을 주는지 대조한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen2 Technical Report (v4)](https://arxiv.org/abs/2407.10671v4)
- [Qwen2.5 Technical Report (v2)](https://arxiv.org/abs/2412.15115v2)
