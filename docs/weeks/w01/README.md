# W01 — LLaMA 1 → Llama 2

[주차 목록](../README.md) · [배경 개념과 읽기 순서](../../background/README.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: LLaMA 1 → Llama 2
- arXiv: [LLaMA 1 (v1)](https://arxiv.org/abs/2302.13971v1) → [Llama 2 (v2)](https://arxiv.org/abs/2307.09288v2)
- 핵심 주제: LLaMA recipe의 계승·조합 · Llama 2의 실제 구조 변경 · 대화형 정렬과 안전성
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] LLaMA 1의 “Transformer recipe”가 기존 기법을 어떤 순서로 조합했는지와, 계산 예산에서 모델 크기·학습 토큰·추론비용을 함께 고려한 이유를 설명할 수 있다.
  - **짚고 갈 개념:** BPE와 byte fallback · pre-normalization(RMSNorm) · gated FFN(SwiGLU) · RoPE · AdamW · parameter/token/FLOPs allocation
  - **함께 읽을 자료와 범위:** [LLaMA 계열 배경 가이드의 recipe 표](../../background/llama.md#llama1-recipe)에서 BPE→RMSNorm→SwiGLU→RoPE→AdamW의 필요한 범위와 작은 확인 질문을 먼저 따른다. 이 순서는 이해를 위한 편집 순서이며, 보고서가 인용을 나열한 순서가 아니다.
  - **원문에서 읽을 부분:** [LLaMA 1 v1 §1, §2.1–§2.4 및 Table 1–2 — tokenizer·architecture·optimizer·효율 구현](https://arxiv.org/abs/2302.13971v1). 본문이 BPE(§2.1)→block recipe(§2.2)→optimizer(§2.3)로 적은 순서를 확인한 뒤, “LLaMA가 이 기법들을 발명했다”가 아니라 각 출처와 LLaMA의 조합·학습 예산을 대조한다.
- [ ] Llama 2의 아키텍처 변경을 LLaMA 1의 유지 항목과 분리하여, 2K→4K 문맥과 큰 모델의 GQA가 KV cache·처리량에 미치는 영향을 설명할 수 있다.
  - **짚고 갈 개념:** MHA와 KV cache · MQA/GQA의 KV-head 수 · 2K/4K context · inference throughput · 유지된 BPE/RMSNorm/SwiGLU/RoPE/AdamW
  - **함께 읽을 자료와 범위:** [LLaMA 계열 배경 가이드의 Llama 2 변경 표](../../background/llama.md#llama2-delta)에서 먼저 “유지된 recipe / 바뀐 context·GQA / data-scale 변화”를 분리한다. 이어 [GQA v3 §2.1–§2.2](https://arxiv.org/abs/2305.13245v3)와 Llama 2 Appendix A.2.1의 MHA·MQA·8-KV-head GQA 비교, Figure 24를 읽는다. 구현 확인은 해당 가이드의 pinned Transformers 코드 범위까지만 보조로 쓴다.
  - **원문에서 읽을 부분:** [Llama 2 v2 §2.1–§2.2, Table 1, Appendix A.2.1 — Llama 1과의 실제 차이와 ablation](https://arxiv.org/abs/2307.09288v2). 7B·13B가 GQA를 썼다고 일반화하지 말고, Table 1의 34B·70B 적용 범위와 나머지 recipe의 유지 여부를 확인한다.
- [ ] Llama 2가 사람의 두 응답 비교를 ranking loss로 바꾸고, rejection sampling과 PPO를 어떤 순서로 결합했는지 수식과 한계까지 설명할 수 있다.
  - **짚고 갈 개념:** 선호 쌍(chosen/rejected) · 두 개의 도움됨/안전성 보상 모델 · ranking loss와 margin · rejection sampling · PPO의 KL penalty · reward hacking
  - **함께 읽을 자료와 범위:** [InstructGPT v1 §3.1–§3.2](https://arxiv.org/abs/2203.02155v1)에서 SFT→선호 데이터→보상 모델→PPO의 골격을 읽고, [PPO v2 §3](https://arxiv.org/abs/1707.06347v2)에서 clipped update의 목적만 확인한다. 이어 Llama 2의 “K개 생성 후 재학습”은 PPO와 다른 별도 단계임을 표시한다.
  - **원문에서 읽을 부분:** [Llama 2 v2 §3.1–§3.2.3, Eq. (1)–(4), Figure 4·7·8, §5.1–§5.2 — preference ranking, iterative RLHF, 한계](https://arxiv.org/abs/2307.09288v2). helpfulness/safety를 분리한 이유, V4 전에는 rejection sampling만 썼고 이후 PPO를 순차 결합한 사실, RM 분포 이탈·환각 한계를 한 흐름으로 확인한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [LLaMA: Open and Efficient Foundation Language Models (v1)](https://arxiv.org/abs/2302.13971v1)
- [Llama 2: Open Foundation and Fine-Tuned Chat Models (v2)](https://arxiv.org/abs/2307.09288v2)
