# W03 — Qwen1.5 → Qwen2

[주차 목록](../README.md) · [W03 Background](../../background/w03.md) · [주간 템플릿](../../../templates/week.md)

**읽기 분담:** [이번 주 공통 읽기와 팀별 심화](../../background/workload.md)를 기준으로 개인 준비 3–4시간을 배분합니다. 상세 Background는 공통 범위와 담당 갈래에 필요한 부분을 찾아 읽고, 세 학습목표는 모임 후 함께 설명할 수 있도록 정리합니다.

## 논문 정보

- 논문: Qwen1.5 → Qwen2
- 공식 자료: [Qwen1.5 공식 출시 글](https://qwenlm.github.io/blog/qwen1.5/) · [Qwen1.5-7B 고정 config](https://huggingface.co/Qwen/Qwen1.5-7B/blob/831096e3a59a0789a541415da25ef195ceb802fe/config.json)
- arXiv: [Qwen2 (v4)](https://arxiv.org/abs/2407.10671v4)
- **자료 경계:** Qwen1.5에는 이 주차에서 대응시키는 technical report가 없다. 출시 글·고정 config는 공개 구현/제품 자료이며, Qwen2 v4 본문과 같은 종류의 evidence가 아니다.
- 핵심 주제: 7B MHA→GQA · long-context 처리 · dense-to-MoE initialization · instruction pool과 scalable synthesis
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] Qwen1.5-7B와 Qwen2-7B의 config 및 Qwen2 본문을 대조해 MHA→GQA, native long-context training과 inference extension, dense-to-MoE initialization을 구분해 설명할 수 있다.
  - **짚고 갈 개념:** Q/KV head · KV cache · MHA/GQA · DCA · YaRN · configured maximum과 training length · fine-grained/shared-routed expert · upcycling
  - **함께 읽을 자료와 범위:** [구조 전환 가이드](../../background/w03.md#qwen-architecture)의 Qwen1.5/Qwen2 7B config와 GQA v3 §2–§3, DCA v2 §1·§3.1–§3.4, YaRN v3 §2–§4, DeepSeekMoE v1 §3.1–§3.2·Fig.2, Sparse Upcycling v2 §3·§3.1·§4.2.2를 따른다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §2.1–§2.2·§3.2, Eq. (1)–(2), Table 1](https://arxiv.org/abs/2407.10671v4). Qwen1.5는 출시 글·고정 config에서만 대조하며, 7B의 MHA→GQA를 계열 전체 변화로 일반화하지 않는다.
- [ ] Qwen2가 instruction pool에서 ontology를 추출하고 representative instruction을 고른 뒤 constraint를 더해 evolution하는 순서를 설명할 수 있다.
  - **짚고 갈 개념:** open-set ontology · intent tag · tag diversity · semantic richness · complexity · intent completeness · instruction selection · self-evolution · demonstration/preference data
  - **함께 읽을 자료와 범위:** [Instruction pool 가이드](../../background/w03.md#instruction-pool)에서 InsTag v2 §3.1–§3.4·§4–§4.1, SFT Data Composition v4 §2–§3, Tree-Instruct §3·Fig.2를 Qwen2 본문 인용 순서로 읽는다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §4.1·§4.1.1](https://arxiv.org/abs/2407.10671v4). ontology→tag/selection→constraint addition→human ranking을 automated synthesis와 섞지 말고, 공개되지 않은 selection score/threshold를 만들어 내지 않는다.
- [ ] Qwen2의 role-play, rejection sampling, execution feedback이 profile faithfulness·정답·실행 제약 중 무엇을 각각 판정하는지, IFEval 평가와 생성한 학습 자료의 경계를 포함해 설명할 수 있다.
  - **짚고 갈 개념:** profile-conditioned role-play · rejection sampling · final-answer check · reasoning path · Python verifier · unit test · executable constraint · evaluation contamination
  - **함께 읽을 자료와 범위:** [Qwen2 synthesis 가이드](../../background/w03.md#qwen2-synthesis)의 Ditto v1 §3.2–§3.4와 AutoIF v1 §3.2–§3.4를 읽는다. [IFEval v1 §2.1–§2.2](https://arxiv.org/abs/2311.07911v1)은 generated SFT data가 아닌 benchmark로 확인한다.
  - **원문에서 읽을 부분:** [Qwen2 v4 §4.1.2·§5.2.1](https://arxiv.org/abs/2407.10671v4). `profile→response`, `reasoning path→answer`, `instruction→verifier/test→execution`이 동일한 quality signal인지 작은 예시로 대조한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen1.5 공식 출시 글](https://qwenlm.github.io/blog/qwen1.5/)
- [Qwen1.5-7B 고정 config](https://huggingface.co/Qwen/Qwen1.5-7B/blob/831096e3a59a0789a541415da25ef195ceb802fe/config.json)
- [Qwen2 Technical Report (v4)](https://arxiv.org/abs/2407.10671v4)
