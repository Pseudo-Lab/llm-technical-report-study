# W02 — Llama 2

[주차 목록](../README.md) · [W02 Background](../../background/w02.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Llama 2
- arXiv: [Llama 2](https://arxiv.org/abs/2307.09288v2)
- 핵심 주제: LLaMA 1 recipe의 유지와 구조 변화 · preference reward model · iterative RLHF
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

> RLHF 두 목표는 정규 모임에서 §3.2의 RM → rejection sampling → PPO 흐름 위주로 핵심만 발췌해 읽고, 세부 비교는 [보충 S1](../supplementary.md#s1)에서 Llama 3의 후학습과 함께 다룹니다.

- [ ] **Llama 2에서 유지된 LLaMA 1 recipe와 실제 구조 변화인 2K→4K context 및 large-model GQA를 분리하여, GQA가 KV cache와 inference scalability를 어떻게 바꾸는지 설명할 수 있다.**
  - **짚고 갈 개념:** causal MHA, KV cache, MQA, GQA, KV head 수, context length, inference throughput, retained BPE/RMSNorm/SwiGLU/RoPE/AdamW. context length·GQA는 Llama 2의 명시적 변화지만 tokenizer와 기본 block recipe는 계승 항목이다.
  - **함께 읽을 자료와 범위:** [LLaMA 가이드의 Llama 2 delta](../../background/w02.md#llama2-delta)에서 유지/변경/data-scale을 먼저 나눈다. 이어 [GQA §2.1–§2.2](https://arxiv.org/abs/2305.13245v3)와 Llama 2 Appendix A.2.1의 MHA·MQA·8-KV-projection GQA 비교, Figure 24만 읽는다. LLaMA 1의 BPE·RMSNorm·SwiGLU·RoPE 원전은 W01에서 읽었으므로 여기서는 “유지”를 확인하는 데만 재방문한다.
  - **원문에서 읽을 부분:** [Llama 2 §2.1–§2.2, Table 1, Appendix A.2.1, Tables 16–18, Figure 24](https://arxiv.org/abs/2307.09288v2). 7B·13B가 아니라 34B·70B에 GQA를 사용한 적용 범위, 2T pretraining token과 new public-data mixture를 architecture difference와 분리해 기록한다.

- [ ] **사람의 선호 쌍과 4단계 preference rating을 helpfulness/safety reward model의 ranking loss와 margin으로 바꾸는 과정을 수식으로 설명할 수 있다.**
  - **짚고 갈 개념:** chosen/rejected pair, scalar reward head, pairwise ranking loss, preference-rating margin, helpfulness/safety reward model, reward-model distribution shift. reward model은 다음-token head 대신 prompt–response에 scalar를 내며, pair를 학습할 때만 chosen/rejected 순서를 쓴다.
  - **함께 읽을 자료와 범위:** [InstructGPT §3.1–§3.2](https://arxiv.org/abs/2203.02155v1)로 SFT→human preference→reward model이라는 공통 골격만 확인한다. 이후 Llama 2 §3.2.1–§3.2.2와 Eq. (1)–(2), Appendix A.3.2–A.3.4에서 Meta의 rating·margin·도움됨/안전성 분리를 읽는다. InstructGPT의 dataset 수치나 training recipe를 Llama 2의 사실로 반복하지 않는다.
  - **원문에서 읽을 부분:** [Llama 2 §3.2.1–§3.2.2, Eq. (1)–(2), Tables 7–8, Figure 6](https://arxiv.org/abs/2307.09288v2). `-log σ(rθ(x,yc)-rθ(x,yr))`와 rating-based margin을 추적하고, 왜 safety/helpfulness를 separate RM으로 둬야 하는지와 preference pair가 비슷해질수록 ranking이 어려워지는 한계를 구분한다.

- [ ] **Llama 2가 rejection sampling과 PPO를 어떤 순서로 iterative RLHF에 결합하며, KL penalty가 reward hacking과 policy drift를 왜 제한하는지 설명할 수 있다.**
  - **짚고 갈 개념:** K candidate generation, reward re-ranking, rejection-sampled SFT, PPO, policy objective, reference-policy KL penalty, reward hacking, iterative data refresh. K개 중 최고 reward 응답으로 재학습하는 rejection sampling은 PPO policy update와 같은 연산이 아니다.
  - **함께 읽을 자료와 범위:** [PPO §3](https://arxiv.org/abs/1707.06347v2)에서 clipped policy update의 목적만 확인한다. 이어 Llama 2 §3.2.3와 Eq. (3)–(4), Figures 7–8을 읽어 K-sample selection, 이전 version sample을 함께 보존한 변화, PPO reward objective와 KL penalty를 순서대로 연결한다. 이 주차에서는 reward-model ranking loss를 다시 유도하지 않고, 앞 목표의 RM을 fixed reward estimator로 받아 쓴다.
  - **원문에서 읽을 부분:** [Llama 2 §3.2.3, Eq. (3)–(4), Figures 7–8, §5.1–§5.2](https://arxiv.org/abs/2307.09288v2). RLHF V4 이전의 rejection sampling과 이후 PPO 결합, safety prompt에서 safety RM 우선 사용, reference-policy KL이 높은 RM score와 낮은 human evaluation으로 나타나는 reward hacking을 완화하려는 경계를 확인한다.

## 발표자료

- [통합 발표자료](index.html): 팀원 자료를 [#180](https://github.com/Pseudo-Lab/llm-technical-report-study/issues/180) 분담 순서로 묶은 98장입니다. 장마다 근거 줄에 Llama 2 원문 쪽과 팀원 자료 쪽 링크가 있습니다.
- 파트별 원본(`slides/`, 받은 그대로):
  - 사전학습 & 아키텍처 · 이경민: [슬라이드](slides/w02-llama2-pretraining-architecture.html)
  - Data · 정호찬: [슬라이드](slides/llama2_data.html)
  - 데이터 & Post-training · 송용우: [§3–§3.2.1 SFT와 선호 데이터](slides/llama2_sft_preference_data.html) · 원본 [JSON](slides/llama2_sft_preference_data.json) — 덱에서 `N` 키로 대본을 봅니다 · [§3–§3.2 SFT와 RLHF](slides/llama2_sft_rlhf.html)
  - 데이터 & Post-training · 임병극: [§3.3–§3.4 GAtt와 평가](slides/W02_Llama2_GAtt_Evaluation.html)
  - Alignment & RL · 김민제: [RLHF 개요 · §3.2.1–§3.2.2 Reward Model](slides/llama2_rl_part1.html)
  - Background · 이정민: [Tokenizer · BPE · Byte Fallback](slides/tokenizer-bpe.html)
  - Background · 김민선: [위치 인코딩: Transformer → GPT-3 → RoPE](slides/llama2-background-RoPE.html)
- [Llama 2 읽기 지도](llama2-reading-map.html) · [Markdown](llama2-reading-map.md): 다섯 파트의 범위 · 질문 · 개념 설명 페이지입니다. 발표자료의 근거 링크가 이 페이지를 가리킵니다. 파트별 범위는 2026-10-24 스터디 배정을 따릅니다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- 보충: [S1 — Llama 3 Herd 비교 (W02 다음 주)](../supplementary.md#s1)
- [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288v2)
