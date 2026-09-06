# W01 — LLaMA 1

[주차 목록](../README.md) · [W01 Background](../../background/w01.md) · [주간 템플릿](../../../templates/week.md)

**읽기 분담:** [이번 주 공통 읽기와 팀별 심화](../../background/workload.md)를 기준으로 개인 준비 3–4시간을 배분합니다. 상세 Background는 공통 범위와 담당 갈래에 필요한 부분을 찾아 읽고, 세 학습목표는 모임 후 함께 설명할 수 있도록 정리합니다.

## 논문 정보

- 논문: LLaMA 1
- arXiv: [LLaMA 1 v1](https://arxiv.org/abs/2302.13971v1)
- 핵심 주제: 기존 Transformer 개선의 recipe · optimizer · compute/token budget
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] **LLaMA 1의 tokenization·Transformer block·position 처리 조합이 원 Transformer의 어느 위치를 바꾸며, 각 부품이 무엇을 담당하는지 설명할 수 있다.**
  - **짚고 갈 개념:** BPE/SentencePiece, unknown UTF-8 byte fallback, pre-normalization, RMSNorm, SwiGLU, RoPE, causal self-attention. BPE는 입력 분절, RMSNorm은 sublayer 입력 정규화, SwiGLU는 FFN 비선형, RoPE는 Q/K 위치 처리를 맡는다.
  - **함께 읽을 자료와 범위:** [LLaMA 가이드의 LLaMA 1 recipe](../../background/w01.md#llama1-recipe)에서 BPE v1 §3.2 → GPT-3 v1 §2.1/RMSNorm v1 §3–§4 → GLU Variants v1 §2–§3.1/PaLM v1 §2 → RoFormer v5 §3.2 경로를 따른다. 원전은 각 부품을 이해하는 데 필요한 절만 읽고, LLaMA의 조합을 각 원전의 신규 제안으로 되돌려 쓰지 않는다.
  - **원문에서 읽을 부분:** [LLaMA 1 v1 §2.1–§2.2, Table 2](https://arxiv.org/abs/2302.13971v1). 숫자 digit split·byte fallback, `x + Sublayer(RMSNorm(x))`인 pre-norm, `2/3·4d` SwiGLU intermediate width, absolute position embedding 제거와 layer별 RoPE를 원 Transformer와 한 블록 그림으로 대조한다.

- [ ] **LLaMA 1이 AdamW·cosine decay·warmup·gradient clipping을 어떤 역할로 조합했는지, optimizer update와 learning-rate schedule을 구분해 설명할 수 있다.**
  - **짚고 갈 개념:** AdamW, decoupled weight decay, cosine learning-rate schedule, warmup, gradient clipping, scale별 maximum learning rate. weight decay는 parameter regularization, schedule/warmup은 update step 크기 변화, clipping은 큰 gradient의 상한이라는 서로 다른 제어다.
  - **함께 읽을 자료와 범위:** [AdamW v3 §2](https://arxiv.org/abs/1711.05101v3)에서 L2 penalty와 decoupled weight decay의 차이만 확인한 뒤 LLaMA 1 §2.3으로 돌아온다. 이 주차에서는 Adam 계열의 유도 전체를 반복하지 않고, LLaMA가 실제로 공개한 `β`, decay, clipping, warmup, cosine 종료 비율과 Table 2의 scale별 LR만 추적한다.
  - **원문에서 읽을 부분:** [LLaMA 1 v1 §2.3, Table 2](https://arxiv.org/abs/2302.13971v1). `β1=.9`, `β2=.95`, weight decay, clipping, 2,000-step warmup과 cosine schedule을 확인하고, 7B/13B와 33B/65B의 maximum LR 차이를 “새 optimizer”가 아니라 recipe hyperparameter 차이로 설명한다.

- [ ] **LLaMA 1이 fixed training budget에서 model size·training token·serving cost를 함께 고려한 이유와, 그 budget을 실제로 실행한 효율 기법을 설명할 수 있다.**
  - **짚고 갈 개념:** parameter/token allocation, training FLOPs, inference budget, mostly-once data pass, activation checkpointing, causal-attention memory reduction, model/sequence parallelism, communication overlap. 더 큰 parameter 수와 더 많은 token은 같은 고정 FLOPs에서 동시에 무한히 늘릴 수 없다.
  - **함께 읽을 자료와 범위:** [Chinchilla v1 §1·§3](https://arxiv.org/abs/2203.15556v1)에서 training compute 아래 parameter/token 배분 문제만 확인한다. 이어 LLaMA 1 §1의 inference-budget 동기와 §2.1·Table 2의 token allocation, §2.4의 실제 memory/parallel implementation을 연결한다. Chinchilla의 최적 비율을 LLaMA가 그대로 사용했다고 단정하지 않는다.
  - **원문에서 읽을 부분:** [LLaMA 1 v1 §1, §2.1, §2.4, Table 2, Figure 1](https://arxiv.org/abs/2302.13971v1). 7B/13B의 1.0T와 33B/65B의 1.4T tokens, 대부분 token을 한 번만 사용한 data pass, attention weight 미저장·선택적 activation 저장·model/sequence parallelism을 읽고, architecture 부품이나 AdamW와 별개인 **budget과 실행**의 선택으로 분리한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [LLaMA: Open and Efficient Foundation Language Models (v1)](https://arxiv.org/abs/2302.13971v1)
