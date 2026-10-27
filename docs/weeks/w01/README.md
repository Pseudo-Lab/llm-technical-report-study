# W01 — LLaMA 1

[주차 목록](../README.md) · [W01 Background](../../background/w01.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: LLaMA 1
- arXiv: [LLaMA 1](https://arxiv.org/abs/2302.13971v1)
- 핵심 주제: 기존 Transformer 개선의 recipe · optimizer · compute/token budget
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 발표자료

- [W01 발표자료 HTML](index.html): 156장(본편 90 · 부록 Background 66). 준비 과정 → LLaMA 1 다섯 파트 읽기 지도와 담당 → LLM 생애주기 → LLaMA 1(배경 · 데이터 · 구조·학습 · 평가 · 후학습·정렬) → 다음 주 Llama 2 다섯 파트와 업무 분배 제안. W01 스터디 피드백은 아직 반영하지 않았습니다.
- [발표 대본](script.html) · [Markdown 원본](script.md): 장마다 같이 다듬는 대본입니다. 발표자료에서 `N` 키(넓은 화면은 오른쪽 아래 버튼)로 현재 장의 대본을 볼 수 있습니다.
- [발표자료 회고](retrospective.md): Skills 초안 · 중간본 · 최종본을 비교한 반성과 규칙입니다.
- [LLM 생애주기 지도](lifecycle-map.html): 발표자료 12장의 네 묶음 · 11단계를 단계마다 정하는 것과 스터디 주차로 펼친 페이지입니다. 상단 버튼으로 LLaMA 1이 다룬 칸을 표시할 수 있습니다.
- [벤치마크 실제 예시](benchmark-examples.md): LLaMA 1이 쓴 벤치마크 20개의 실제 문항 · 출처 · 라이선스.
- [LLaMA 1 읽기 지도](llama1-reading-map.html) · [Markdown](llama1-reading-map.md): Skills 1([#170](https://github.com/Pseudo-Lab/llm-technical-report-study/issues/170))로 만든 63쪽 읽기 지도입니다. 다섯 파트 개요와 협업 제안, 파트별 질문, 개념별 설명 페이지, Background 빈 영역 표로 되어 있습니다. 사람 검토 전 상태입니다.

HTML 파일을 내려받아 브라우저에서 열면 됩니다. `←` / `→`로 슬라이드를 넘기고 `Home` / `End`로 처음과 끝으로 이동합니다.

## 학습목표

- [ ] **LLaMA 1의 tokenization·Transformer block·position 처리 조합이 원 Transformer의 어느 위치를 바꾸며, 각 부품이 무엇을 담당하는지 설명할 수 있다.**
  - **짚고 갈 개념:** BPE/SentencePiece, unknown UTF-8 byte fallback, pre-normalization, RMSNorm, SwiGLU, RoPE, causal self-attention. BPE는 입력 분절, RMSNorm은 sublayer 입력 정규화, SwiGLU는 FFN 비선형, RoPE는 Q/K 위치 처리를 맡는다.
  - **함께 읽을 자료와 범위:** [LLaMA 가이드의 LLaMA 1 recipe](../../background/w01.md#llama1-recipe)에서 BPE §3.2 → GPT-3 §2.1/RMSNorm §3–§4 → GLU Variants §2–§3.1/PaLM §2 → RoFormer §3.2 경로를 따른다. 원전은 각 부품을 이해하는 데 필요한 절만 읽고, LLaMA의 조합을 각 원전의 신규 제안으로 되돌려 쓰지 않는다.
  - **원문에서 읽을 부분:** [LLaMA 1 §2.1–§2.2, Table 2](https://arxiv.org/abs/2302.13971v1). 숫자 digit split·byte fallback, `x + Sublayer(RMSNorm(x))`인 pre-norm, `2/3·4d` SwiGLU intermediate width, absolute position embedding 제거와 layer별 RoPE를 원 Transformer와 한 블록 그림으로 대조한다.

- [ ] **LLaMA 1이 AdamW·cosine decay·warmup·gradient clipping을 어떤 역할로 조합했는지, optimizer update와 learning-rate schedule을 구분해 설명할 수 있다.**
  - **짚고 갈 개념:** AdamW, decoupled weight decay, cosine learning-rate schedule, warmup, gradient clipping, scale별 maximum learning rate. weight decay는 parameter regularization, schedule/warmup은 update step 크기 변화, clipping은 큰 gradient의 상한이라는 서로 다른 제어다.
  - **함께 읽을 자료와 범위:** [AdamW §2](https://arxiv.org/abs/1711.05101v3)에서 L2 penalty와 decoupled weight decay의 차이만 확인한 뒤 LLaMA 1 §2.3으로 돌아온다. 이 주차에서는 Adam 계열의 유도 전체를 반복하지 않고, LLaMA가 실제로 공개한 `β`, decay, clipping, warmup, cosine 종료 비율과 Table 2의 scale별 LR만 추적한다.
  - **원문에서 읽을 부분:** [LLaMA 1 §2.3, Table 2](https://arxiv.org/abs/2302.13971v1). `β1=.9`, `β2=.95`, weight decay, clipping, 2,000-step warmup과 cosine schedule을 확인하고, 7B/13B와 33B/65B의 maximum LR 차이를 “새 optimizer”가 아니라 recipe hyperparameter 차이로 설명한다.

- [ ] **LLaMA 1이 fixed training budget에서 model size·training token·serving cost를 함께 고려한 이유와, 그 budget을 실제로 실행한 효율 기법을 설명할 수 있다.**
  - **짚고 갈 개념:** parameter/token allocation, training FLOPs, inference budget, mostly-once data pass, activation checkpointing, causal-attention memory reduction, model/sequence parallelism, communication overlap. 더 큰 parameter 수와 더 많은 token은 같은 고정 FLOPs에서 동시에 무한히 늘릴 수 없다.
  - **함께 읽을 자료와 범위:** [Chinchilla §1·§3](https://arxiv.org/abs/2203.15556v1)에서 training compute 아래 parameter/token 배분 문제만 확인한다. 이어 LLaMA 1 §1의 inference-budget 동기와 §2.1·Table 2의 token allocation, §2.4의 실제 memory/parallel implementation을 연결한다. Chinchilla의 최적 비율을 LLaMA가 그대로 사용했다고 단정하지 않는다.
  - **원문에서 읽을 부분:** [LLaMA 1 §1, §2.1, §2.4, Table 2, Figure 1](https://arxiv.org/abs/2302.13971v1). 7B/13B의 1.0T와 33B/65B의 1.4T tokens, 대부분 token을 한 번만 사용한 data pass, attention weight 미저장·선택적 activation 저장·model/sequence parallelism을 읽고, architecture 부품이나 AdamW와 별개인 **budget과 실행**의 선택으로 분리한다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971v1)
