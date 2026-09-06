# LLaMA 1 → Llama 2: 구성요소와 변경점

[W01 학습목표](../weeks/w01/README.md) · [배경 읽기 지도](README.md)

<a id="llama1-recipe"></a>
## LLaMA 1의 구성요소

LLaMA 1은 [§2.1–§2.3](https://arxiv.org/abs/2302.13971v1)에서 공개 데이터·BPE tokenizer·기존 Transformer 개선·AdamW를 어떤 recipe로 묶었는지를, Llama 2는 [§2.2와 Appendix A.2.1](https://arxiv.org/abs/2307.09288v2)에서 그중 무엇을 유지하고 무엇을 바꾸었는지를 직접 적고 있다. 다음 순서는 그 본문을 읽기 위한 편집 순서다.

| 대상 본문에서 먼저 확인할 것 | 필요한 배경 읽기와 범위 | 읽고 나서 확인할 질문 |
| --- | --- | --- |
| LLaMA 1 §2.1의 BPE/SentencePiece, 숫자 분리, unknown UTF-8 byte decomposition | [BPE v1 §3.2](https://arxiv.org/abs/1508.07909v1) | BPE vocabulary 구성과 LLaMA가 말한 unknown 문자 byte 분해를 구분할 수 있는가? Llama 2 §2.2는 **같은 tokenizer**를 썼다고만 말한다. |
| LLaMA 1 §2.2의 pre-normalization과 RMSNorm | [GPT-3 v1 §2.1](https://arxiv.org/abs/2005.14165v1)의 pre-norm 선례 → [RMSNorm v1 §3–§4](https://arxiv.org/abs/1910.07467v1)의 정규화 함수 | attention과 FFN의 입력에 norm을 둔다는 것이 무엇인지, RMSNorm이 mean-centering을 생략한다는 점을 블록 그림으로 설명할 수 있는가? |
| LLaMA 1 §2.2의 SwiGLU [PaLM] | [GLU Variants v1 §2–§3.1](https://arxiv.org/abs/2002.05202v1) → [PaLM v1 §2](https://arxiv.org/abs/2204.02311v1) | SwiGLU의 원 제안은 Shazeer (2020)이고 PaLM은 이를 채택한 선례임을 구분할 수 있는가? `Swish(xW) ⊙ xV`와 LLaMA의 `2/3·4d` FFN dimension을 함께 확인한다. |
| LLaMA 1 §2.2의 absolute position 제거와 RoPE | [RoFormer v5 §3.2](https://arxiv.org/abs/2104.09864v5) | position vector를 더하는 방식과 Q/K에 회전을 적용하는 방식을 구분할 수 있는가? |
| LLaMA 1 §2.3의 AdamW와 cosine schedule | [AdamW v3 §2](https://arxiv.org/abs/1711.05101v3) | Adam의 L2 penalty와 decoupled weight decay를 구분한 뒤, LLaMA가 공개한 β·weight decay·warmup만 기록할 수 있는가? |
| LLaMA 1 §1의 Chinchilla 참고와 inference budget 언급 | [Chinchilla v1 §1·§3](https://arxiv.org/abs/2203.15556v1) | fixed training FLOPs에서 parameter/token을 배분하는 주장과 LLaMA가 덧붙인 serving inference cost를 분리할 수 있는가? |

## 원 Transformer 블록과 LLaMA의 차이

[LLaMA §2.2](https://arxiv.org/abs/2302.13971v1)가 비교 기준으로 삼는 [Transformer v7 §3.1·§3.3·§3.5](https://arxiv.org/abs/1706.03762v7)를 옆에 둔다. norm을 **어디에 적용하는가**와 **무슨 함수로 계산하는가**는 별개의 선택이다.

| 구성요소 | 원 Transformer | LLaMA §2.2 |
| --- | --- | --- |
| norm 위치 | `LayerNorm(x + Sublayer(x))`의 post-norm | `x + Sublayer(RMSNorm(x))`의 pre-norm |
| FFN | 두 linear map 사이 ReLU | gate와 value projection을 곱하는 SwiGLU; parameter 수를 고려한 중간 폭 |
| 위치 정보 | 입력 embedding에 position encoding을 더함 | 각 layer의 Q/K에 RoPE 적용 |

위 식은 블록을 비교하기 위한 축약이다. 구현에서도 [attention/MLP 앞 RMSNorm](https://github.com/huggingface/transformers/blob/e42587f596181396e1c4b63660abf0c736b10dae/src/transformers/models/llama/modeling_llama.py#L403-L422)과 [gate/up/down projection](https://github.com/huggingface/transformers/blob/e42587f596181396e1c4b63660abf0c736b10dae/src/transformers/models/llama/modeling_llama.py#L191-L218)을 찾아 대조한다. Transformers 코드는 고정 판본의 구현 보조 근거다. 논문이 설명하지 않은 학습 설정을 코드의 기본값에서 추정하지 않는다.

<a id="llama2-delta"></a>
## Llama 1 → Llama 2: 유지와 변경

[Llama 2 §2.2](https://arxiv.org/abs/2307.09288v2)는 standard Transformer, pre-norm RMSNorm, SwiGLU, RoPE, AdamW를 LLaMA 1에서 **대부분 계승**했다고 명시한다. tokenizer도 LLaMA 1과 동일하다. 반대로 실제 primary architecture difference는 context 2K→4K와 GQA다. [Table 1과 Appendix A.2.1](https://arxiv.org/abs/2307.09288v2)을 통해 7B·13B는 GQA를 쓰지 않고 34B·70B에만 쓴 사실, MQA의 한 KV head와 달리 GQA ablation에서는 8 KV projections를 쓴 사실을 확인한다.

| 항목 | LLaMA 1 본문 | Llama 2 본문 | W01에서 말해야 할 결론 |
| --- | --- | --- | --- |
| tokenizer | §2.1 BPE/SentencePiece, 숫자 분리, byte decomposition | §2.2: **same tokenizer as Llama 1**, 32k | Llama 2의 차이가 아니다. |
| block recipe | §2.2 pre-norm RMSNorm, SwiGLU, RoPE | §2.2가 같은 네 요소를 다시 명시 | Llama 2가 RMSNorm/SwiGLU/RoPE를 새로 도입했다는 식으로 말하지 않는다. |
| optimizer | §2.3 AdamW | §2.2 AdamW | Llama 2의 primary architecture difference가 아니다. |
| context | Table 2: 2K | Table 1/A.2.1: 4K | 명시적 architecture change다. A.2.1은 150B-token 통제 비교도 제공한다. |
| attention/KV | ordinary causal MHA | Table 1/A.2.1: 34B·70B GQA; 8 KV projections 비교 | 큰 모델에서 KV-cache/throughput 병목을 겨냥한 명시적 변화다. |
| data/tokens | 1.0T 또는 1.4T | 2.0T, new public-data mix | 구조 차이와 data-scale 차이를 같은 칸에 넣지 않는다. |


GQA의 정의는 [GQA v3 §2.1–§2.2](https://arxiv.org/abs/2305.13245v3)에서 읽는다. 이어 Llama 2 Appendix A.2.1의 MHA/MQA/GQA 비교와 Figure 24로 KV cache가 문맥·batch가 커질수록 병목이 되는 이유를 확인한다. 구현은 [Transformers v4.31.0의 `num_key_value_heads`](https://github.com/huggingface/transformers/blob/e42587f596181396e1c4b63660abf0c736b10dae/src/transformers/models/llama/configuration_llama.py#L53-L60)와 [KV head 반복](https://github.com/huggingface/transformers/blob/e42587f596181396e1c4b63660abf0c736b10dae/src/transformers/models/llama/modeling_llama.py#L233-L328)을 보조로만 대조한다. 이 구현은 논문별 모든 체크포인트 설정을 대신하지 않는다.

<a id="preference-ranking"></a>
## 사람 선호를 ranking과 PPO로 잇는 경로

[§3.2.1–§3.2.3과 Eq. (1)–(4)](https://arxiv.org/abs/2307.09288v2)에서 사람의 chosen/rejected 응답을 ranking loss로 바꾸고, helpfulness와 safety reward model을 분리하며, 최신 모델의 응답을 다시 수집해 RM의 분포 이탈을 줄이려 한 과정을 읽는다. [InstructGPT v1 §3.1–§3.2](https://arxiv.org/abs/2203.02155v1)로 공통 골격을, [PPO v2 §3](https://arxiv.org/abs/1707.06347v2)로 clipped update의 목적을 확인한 뒤 Llama 2로 돌아온다.

마지막으로 Llama 2 [§3.2.3과 Figure 7–8](https://arxiv.org/abs/2307.09288v2)을 읽어, K개를 생성·보상으로 고른 뒤 재학습하는 rejection sampling과 policy가 매 update 달라지는 PPO를 구분한다. 저자들은 V4 전에는 rejection sampling만 쓰고 이후 PPO를 순차 결합했다. 이 구분이 보상 해킹·RM 분포 이탈·도움됨/안전성 trade-off라는 [§5.1–§5.2](https://arxiv.org/abs/2307.09288v2)의 한계를 읽는 출발점이다.
