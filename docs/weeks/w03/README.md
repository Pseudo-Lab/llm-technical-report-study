# W03 — Qwen → Qwen2

[주차 목록](../README.md) · [W03 Background](../../background/w03.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen → Qwen2
- arXiv: [Qwen Technical Report](https://arxiv.org/abs/2309.16609v1) · [Qwen2](https://arxiv.org/abs/2407.10671v4)
- 공개 config: [Qwen-7B 고정 config](https://huggingface.co/Qwen/Qwen-7B/blob/ef3c5c9c57b252f3149c1408daf4d649ec8b6c85/config.json)
- **자료 경계:** Qwen1.5는 별도 technical report 없이 [출시 글](https://qwenlm.github.io/blog/qwen1.5/)로만 공개됐다. 이 주차는 Qwen 보고서(2023.9)와 Qwen2 보고서(2024.7)를 비교하며, 출시 글은 참고로만 쓴다.
- 핵심 주제: 7B MHA→GQA · long-context 처리 · dense-to-MoE initialization · instruction pool과 scalable synthesis
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] Qwen-7B와 Qwen2-7B의 구조(Qwen Table 1 · Qwen2 Table 1)와 두 보고서 본문을 대조해 MHA→GQA, native long-context training과 inference extension, dense-to-MoE initialization을 구분해 설명할 수 있다.
  - **짚고 갈 개념:** Q/KV head · KV cache · MHA/GQA · DCA · YaRN · configured maximum과 training length · fine-grained/shared-routed expert · upcycling
  - **함께 읽을 자료와 범위:** [구조 전환 가이드](../../background/w03.md#qwen-architecture)의 7B config 비교와 GQA §2–§3, DCA §1·§3.1–§3.4, YaRN §2–§4, DeepSeekMoE §3.1–§3.2·Fig.2, Sparse Upcycling §3·§3.1·§4.2.2를 따른다.
  - **원문에서 읽을 부분:** [Qwen §2.3–§2.5, Table 1·3](https://arxiv.org/abs/2309.16609v1) · [Qwen2 §2.1–§2.2·§3.2, Eq. (1)–(2), Table 1](https://arxiv.org/abs/2407.10671v4). Qwen의 학습 없는 추론 시 확장(NTK · LogN · window)과 Qwen2의 32K 학습 + DCA·YaRN을 구분하고, 7B의 MHA→GQA를 계열 전체 변화로 일반화하지 않는다.
- [ ] Qwen2가 instruction pool에서 ontology를 추출하고 representative instruction을 고른 뒤 constraint를 더해 evolution하는 순서를 설명할 수 있다.
  - **짚고 갈 개념:** open-set ontology · intent tag · tag diversity · semantic richness · complexity · intent completeness · instruction selection · self-evolution · demonstration/preference data
  - **함께 읽을 자료와 범위:** [Instruction pool 가이드](../../background/w03.md#instruction-pool)에서 InsTag §3.1–§3.4·§4–§4.1, SFT Data Composition §2–§3, Tree-Instruct §3·Fig.2를 Qwen2 본문 인용 순서로 읽는다.
  - **원문에서 읽을 부분:** [Qwen2 §4.1·§4.1.1](https://arxiv.org/abs/2407.10671v4). ontology→tag/selection→constraint addition→human ranking을 automated synthesis와 섞지 말고, 공개되지 않은 selection score/threshold를 만들어 내지 않는다.
- [ ] Qwen2의 role-play, rejection sampling, execution feedback이 profile faithfulness·정답·실행 제약 중 무엇을 각각 판정하는지, IFEval 평가와 생성한 학습 자료의 경계를 포함해 설명할 수 있다.
  - **짚고 갈 개념:** profile-conditioned role-play · rejection sampling · final-answer check · reasoning path · Python verifier · unit test · executable constraint · evaluation contamination
  - **함께 읽을 자료와 범위:** [Qwen2 synthesis 가이드](../../background/w03.md#qwen2-synthesis)의 Ditto §3.2–§3.4와 AutoIF §3.2–§3.4를 읽는다. [IFEval §2.1–§2.2](https://arxiv.org/abs/2311.07911v1)은 generated SFT data가 아닌 benchmark로 확인한다.
  - **원문에서 읽을 부분:** [Qwen2 §4.1.2·§5.2.1](https://arxiv.org/abs/2407.10671v4). `profile→response`, `reasoning path→answer`, `instruction→verifier/test→execution`이 동일한 quality signal인지 작은 예시로 대조한다.

## 발표자료

- Architecture & Pre-training · 우성현: [슬라이드](qwen-architecture-deck.html)
- Tokenizer · Data & Synthesis · Alignment & RL · RoPE와 Long-Context(Background) · 김현우: [슬라이드](alignment-background-study.html) · 원본 [JSON](alignment-background-study.json) — 덱에서 `N` 키로 대본을 봅니다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen Technical Report](https://arxiv.org/abs/2309.16609v1)
- [Qwen2 Technical Report](https://arxiv.org/abs/2407.10671v4)
- [Qwen-7B 고정 config](https://huggingface.co/Qwen/Qwen-7B/blob/ef3c5c9c57b252f3149c1408daf4d649ec8b6c85/config.json)
- 참고: [Qwen1.5 공식 출시 글](https://qwenlm.github.io/blog/qwen1.5/)
