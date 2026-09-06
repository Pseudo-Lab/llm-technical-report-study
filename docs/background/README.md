# 16주 기술 보고서 배경 읽기 지도

이 문서는 각 주차 보고서가 이미 안다고 가정하는 개념을, 먼저 읽을 순서와 최소 원전으로 연결한다. 주차의 Action Item을 대신하는 요약이 아니다. 배경 원전은 아래에 적은 절만 확인했으며, 별도 표기가 없는 한 논문 전체를 읽었다는 뜻이 아니다. 각 주차 원문은 해당 주차 문서의 고정 판본을 기준으로 한다.

## 먼저 잡을 네 가지 수학 도구

1. **내적과 softmax.** query `q`와 key `k`의 내적은 관련성 점수이고, `softmax`는 후보 점수를 합이 1인 가중치로 바꾼다. `softmax(QKᵀ/√d)V`에서 K/V를 과거 token마다 남기는 이유와, score 하나를 더하는 것과 value를 하나 더 쓰는 것이 다른 이유를 구분한다.
2. **외적·저랭크·상태.** `v kᵀ`는 key 방향에서 value를 꺼낼 수 있는 작은 연관 행렬을 쓴다. 저랭크 압축은 `c=W_Dh`처럼 작은 latent `c`만 보관하고 필요한 선형 변환을 나중에 결합하는 방법이다. 행렬 차원과 저장하는 상태의 차원을 먼저 써 보는 습관이 MLA·linear attention·GDN에 공통으로 필요하다.
3. **확률비·advantage·KL.** importance ratio `r=π_θ(a|s)/π_old(a|s)`는 새 정책이 이미 수집한 action을 얼마나 더 선호하는지 나타낸다. advantage는 기준보다 좋은 action인지의 신호, KL은 두 분포가 어긋난 정도를 재는 **비대칭 분포 차이 척도**다. PPO와 GRPO, 비동기 RL의 보정은 이 세 기호를 공유한다.
4. **부동소수점 범위·정밀도.** exponent bit는 다룰 수 있는 크기 범위, mantissa bit는 그 범위 안의 촘촘함을 정한다. 작은 format일수록 scale을 정하고 민감한 누적·optimizer 상태를 높은 정밀도로 남겨야 한다. FP8, loss scaling, residual-state 저장을 이 관점으로 읽는다.

<a id="week-map"></a>
## 주차별 진입표

| 주차 | 먼저 필요한 경로 | 본문에서 이어 읽을 보고서·절 |
| --- | --- | --- |
| [W01](../weeks/w01/README.md) | compute-optimal 학습 → RoPE·GQA → SFT/PPO | [학습·문맥·정렬](#data-context) → [attention/cache](#attention-cache) → [GRPO](#rl-distillation) |
| [W02](../weeks/w02/README.md) | RoPE → YaRN/DCA, SFT → DPO | [학습·문맥·정렬](#data-context) → [attention/cache](#attention-cache) |
| [W03](../weeks/w03/README.md) | teacher/student, on-policy KL | [학습·문맥·정렬](#data-context) → [GRPO](#rl-distillation) |
| [W04](../weeks/w04/README.md) | MHA → MQA/GQA → latent KV·RoPE | [attention/cache](#attention-cache) |
| [W05](../weeks/w05/README.md) | MoE router → balance, MTP → speculative decoding, FP8 | [MoE·정밀도](#moe-precision) |
| [W06](../weeks/w06/README.md) | PPO → GRPO → verifier | [GRPO·증류](#rl-distillation) |
| [W07](../weeks/w07/README.md) | local/global attention, sink logit, on-policy distillation | [긴 문맥·hybrid](#sparse-hybrid) → [GRPO·증류](#rl-distillation) |
| [W08](../weeks/w08/README.md) | MLA latent KV → DSA token selection | [attention/cache](#attention-cache) |
| [W09](../weeks/w09/README.md) | block compression, residual stream, matrix optimizer | [residual·optimizer](#residual-optimizer) |
| [W10](../weeks/w10/README.md) | GDN/QSA/GR/n-gram/Muon 통합 경로 | [Qwen3.8-Next 경로](#qwen38-route) |
| [W11](../weeks/w11/README.md) | cold-start SFT, domain RL, distillation | [GRPO·증류](#rl-distillation) → [평가·시스템](#evaluation-systems) |
| [W12](../weeks/w12/README.md) | importance ratio → policy lag·token alignment | [GRPO·증류](#rl-distillation) |
| [W13](../weeks/w13/README.md) | pass@k, GRPO, distillation | [GRPO·증류](#rl-distillation) → [평가·시스템](#evaluation-systems) |
| [W14](../weeks/w14/README.md) | local convolution·gate, architecture search | [긴 문맥·hybrid](#sparse-hybrid) → [평가·시스템](#evaluation-systems) |
| [W15](../weeks/w15/README.md) | differential attention → GDA → latent KV | [residual·optimizer](#residual-optimizer) |
| [W16](../weeks/w16/README.md) | delta state, negative eigenvalue, partial transfer | [긴 문맥·hybrid](#sparse-hybrid) → [residual·optimizer](#residual-optimizer) |

<a id="data-context"></a>
## 0. 학습 예산, 긴 문맥, 선호 자료: W01–W03

[Chinchilla v1](https://arxiv.org/abs/2203.15556v1) §1·§3은 고정 FLOPs에서 parameter 수와 학습 token 수를 함께 정하는 경험적 관계를 다룬다. 이는 데이터 품질·후학습·아키텍처까지 결정하는 법칙이 아니라, W01의 “작게 만들고 오래 학습” 선택을 읽는 출발점이다.

긴 문맥에서는 RoPE 기본식을 안 뒤 [YaRN v3](https://arxiv.org/abs/2309.00071v3) §2·§3.1–§3.3과 [DCA v2](https://arxiv.org/abs/2402.17463v2) §2.1–§2.2·§3–§3.4를 대비한다. YaRN은 위치/attention scaling으로 RoPE 외삽을 조절하고, DCA는 chunk 안·먼 chunk·인접 chunk의 상대 위치 행렬을 다르게 구성한다.

선호 학습에서는 [DPO v3](https://arxiv.org/abs/2305.18290v3) §3–§4를 읽는다. DPO는 `(prompt, 선호 응답, 비선호 응답)`과 reference policy에서 명시적 reward-model RL loop 없이 선호를 직접 최적화한다. **점검:** KL의 방향을 바꾸면 목적이 바뀌는 이유와, on-policy teacher KL이 고정된 선호쌍 학습과 다른 이유를 설명한다.

**W01 점검.** 고정 FLOPs에서 parameter와 token 수가 함께 바뀌는 간단한 선택을 써 보고, 2차원 RoPE에서는 벡터 `(x₁,x₂)`를 위치 `p`의 각도로 회전한 뒤 query·key의 내적이 `p−q`에 의존함을 계산한다. 이 상대 위치 성질이 GQA의 KV 공유와 별개라는 점도 확인한다.

<a id="attention-cache"></a>
## 1. Attention, 위치, cache: W01·W02·W04에서 W08·W10으로

**읽는 순서.** [Transformer v7](https://arxiv.org/abs/1706.03762v7) §3.2.1–§3.2.2 → [MQA v1](https://arxiv.org/abs/1911.02150v1) §2.4·§3–§3.1 → [GQA v3](https://arxiv.org/abs/2305.13245v3) §2.1–§2.2 → [RoFormer v5](https://arxiv.org/abs/2104.09864v5) §3.2·§3.4.2 → [DeepSeek-V2 v5](https://arxiv.org/abs/2405.04434v5) §2.1.1–§2.1.4이다. 이들은 각각 MHA, 하나의 KV 공유, group별 KV 공유, 상대 위치 회전, latent KV cache를 설명하는 원전이다.

MHA는 각 query head가 과거의 K/V를 읽으므로 decoding 때 K/V cache가 자란다. MQA는 모든 query head가 하나의 K/V head를 공유하고, GQA는 몇 개 query head씩 공유한다. RoPE는 query·key를 위치별로 회전시켜 두 위치의 관계가 내적에 남게 한다. **MLA는 head 수를 줄이는 MQA/GQA와 달리, K/V 내용을 저차원 latent로 압축한다.** `c_t=W_Dh_t`를 cache하고 고정 projection은 query 쪽으로 결합할 수 있다. 다만 위치 회전 성분은 그렇게 단순히 흡수되지 않으므로 별도 RoPE key를 둔다.

**학습 점검.** 길이 `L`, head 수 `h`, head 차원 `d_h`, latent 차원 `d_c`를 두고, MHA가 대략 `L×h×d_h` 규모의 K/V를 남기는 반면 MLA가 어떤 `c_t`와 위치 성분을 남기는지 써 본다. “저랭크 latent KV”는 **저장 표현**이고, 뒤의 DSA/QSA는 **어디를 읽을지 고르는 index**라는 차이를 말할 수 있어야 한다.

DSA는 [DeepSeek-V3.2 v1](https://arxiv.org/abs/2512.02556v1) §2.1–§2.1.1에서 lightweight indexer가 historical KV를 점수화하고 token Top-k를 선택하는 방법이다. QSA는 [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.1.2에서 **MQA indexer**가 압축한 key block을 점수화해 top-k를 고르고, 펼친 mask가 별도 sparse core attention을 이끈다. indexer는 길이 `L`과 block 크기 `r`에서 `O(L²)`를 `O(L²/r)`로 낮추며, 고정 `r`에서는 선형이 아니고 sparse core 비용은 따로 남는다. MLA와 QSA는 모두 긴 문맥 비용을 낮추지만, 전자는 latent 차원의 저장 축, 후자는 sequence block의 index·선택 축이라는 대비로 읽는다.

<a id="moe-precision"></a>
## 2. MoE, multi-token prediction, FP8: W05·W07·W09·W10

**MoE 읽기.** [DeepSeekMoE v1](https://arxiv.org/abs/2401.06066v1) §2·§3.1–§3.3 → [Loss-Free Balancing v1](https://arxiv.org/abs/2408.15664v1) §2–§3 → [DeepSeek-V3 v2](https://arxiv.org/abs/2412.19437v2) §2.1.2로 간다. router는 token마다 top-k expert를 고른다. 일부 expert에 token이 몰리면 계산·통신이 병목이 된다. Loss-Free Balancing은 auxiliary loss gradient로 본 모델을 밀기보다, 최근 load로 expert별 routing bias를 조정한다. 이는 V3가 대규모로 **채택·검증한 선행 방법**이며 V3가 새로 발명한 기법으로 읽지 않는다.

**MTP 읽기.** [Multi-token Prediction v1](https://arxiv.org/abs/2404.19737v1) §2 “Method”의 inference → [Speculative Decoding v2](https://arxiv.org/abs/2211.17192v2) §2.1–§2.3 → V3 §2.2 순서다. MTP는 다음 한 token만 맞히는 loss보다 먼 token에도 학습 신호를 준다. speculative decoding은 draft 후보를 target model이 검증·수정해 분포를 보존한다. V3의 sequential MTP는 병렬 head가 독립적으로 먼 token을 맞히는 설정과 달리 앞선 예측을 뒤 예측의 조건으로 연결한다.

**FP8 읽기.** [FP8 Formats v2](https://arxiv.org/abs/2209.05433v2) §2·§3–§3.2 → [Mixed Precision Training v3](https://arxiv.org/abs/1710.03740v3) §3.1–§3.3 → V3 §3.3.1–§3.3.3이다. E4M3/E5M2는 exponent/mantissa 배분이 다르다. scale은 값 묶음을 FP8이 표현 가능한 범위로 옮기고, master weight·gradient·accumulation처럼 오차가 누적되는 곳은 높은 정밀도로 둔다. 따라서 “FP8 학습”은 모든 tensor를 같은 8비트 형식으로 저장한다는 뜻이 아니다.

**학습 점검.** top-k router가 고르는 expert와 DSA/QSA가 고르는 KV entry를 구분한다. 또한 FP8에서 “range를 넘는 overflow”와 “mantissa가 짧아 생기는 quantization error”가 서로 다른 문제이고, scale·고정밀 누적이 각각 어디에 개입하는지 설명한다.

<a id="rl-distillation"></a>
## 3. 정렬, GRPO, 증류, 비동기 RL: W01–W03·W06·W07·W11–W13

**읽는 순서.** [InstructGPT v1](https://arxiv.org/abs/2203.02155v1) §3.1–§3.2·§3.5 → [PPO v2](https://arxiv.org/abs/1707.06347v2) §3–§4 → [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3 → [On-Policy Distillation v3](https://arxiv.org/abs/2306.13649v3) §2·§3·Algorithm 1을 권한다. SFT·보상 모델·PPO의 기본 흐름에서 PPO는 ratio를 clip하거나 KL penalty를 둬 update 폭을 제한한다. GRPO는 같은 prompt의 여러 rollout reward로 상대 advantage를 만들고 critic을 생략한다. GRPO 자체는 R1·GLM의 신규 알고리즘이 아니다.

R1-Zero는 정답 비교처럼 검증 가능한 **outcome reward**와 응답 구조를 위한 별도 **format reward**를 사용한다([DeepSeek-R1 v2](https://arxiv.org/abs/2501.12948v2) §2.1–§2.3). compiler 실행은 일반적인 verifier의 예이지만, R1의 보상 항목으로 단정하지 않는다. verifier가 약한 글쓰기·일반 대화에서는 model reward를 과도하게 최적화할 때 reward hacking이 생길 수 있어 SFT·preference reward를 섞는다(§3, Supplementary B.5). GLM-5의 TITO와 importance masking은 [GLM-5 v2](https://arxiv.org/abs/2602.15763v2) §4.1.1–§4.1.2에서 비동기 rollout의 old log-probability와 token identity를 보존해 policy lag를 다루는 별도 문제다.

증류는 [Hinton et al. v1](https://arxiv.org/abs/1503.02531v1) §2–§2.1의 teacher soft target에서 시작하지만, Qwen3·MOPD는 student가 실제 생성한 prefix 위에서 teacher distribution을 맞추는 on-policy 변형이다. W13에서는 [Evaluating LLMs Trained on Code v2](https://arxiv.org/abs/2107.03374v2) §2–§2.1·Appendix A의 pass@k도 읽는다. 여러 sample 중 하나라도 맞힐 가능성은 단일 sample 정확도와 다른 신호다.

**학습 점검.** 같은 prompt에서 reward가 `[0, 1, 1, 0]`인 네 rollout을 생각해 평균보다 좋은 응답이 양의 relative advantage를 받는다고 말한다. 이어서 그 rollout이 old policy에서 나왔다면 `r`와 KL이 필요한 이유, 그리고 teacher가 만든 정답 prefix와 student가 이미 만든 prefix가 왜 다른지를 설명한다.

<a id="sparse-hybrid"></a>
## 4. 긴 문맥과 hybrid token mixing: W07·W08·W10·W14·W16

[Longformer v2](https://arxiv.org/abs/2004.05150v2) §3–§3.1은 local window와 일부 global position을 분리한다. 이를 통해 W07의 SWA/GA를 “전 token 전역 attention”으로 오해하지 않는다. MiMo-V2-Flash의 learnable sink는 [MiMo-V2-Flash v2](https://arxiv.org/abs/2601.02780v2) §2.2·식 (1)–(4)에서 softmax 분모에 더하는 logit이며, 초기 token의 KV를 cache하는 sink token 정책과 다르다.

선형 attention은 [Linear Transformers Are Secretly Fast Weight Programmers v3](https://arxiv.org/abs/2102.11174v3) §2·§3.1–§4.2에서 `S_t=S_{t-1}+v_tk_t^T`, `o_t=S_tq_t`처럼 fixed-size outer-product state를 쓴다. [Gated Delta Networks v3](https://arxiv.org/abs/2412.06464v3) §2.1–§2.2·§3.1–§3.3은 같은 key에 새 value를 덮어쓸 수 있도록 delta rule·gate·decay를 둔다. 이 경로는 LFM2의 Hyena와 동일하지 않다. [Hyena v3](https://arxiv.org/abs/2302.10866v3) §2.1·§3.1–§3.4은 long implicit convolution 계열이고, LFM2는 이를 통째로 채택하지 않은 gated short convolution + 소수 GQA 설계다([LFM2 v1](https://arxiv.org/abs/2511.23404v1) §2.2).

Solar Open 2의 KDA/NoPE는 [Kimi Linear v2](https://arxiv.org/abs/2510.26692v2) §2.2·§3, [Unlocking State-Tracking in Linear RNNs v5](https://arxiv.org/abs/2411.12537v5) §3.1·§4.1–§4.2와 연결한다. NoPE 자체는 [The Impact of Positional Encoding on Length Generalization in Transformers v2](https://arxiv.org/abs/2305.19466v2) §4 “What Is The Effect of Positional Encoding?”·§5 “How Does NoPE Represent Positions?”에서 위치 정보를 표현하는 방식을 확인한다. sequence 순서는 position embedding만이 아니라 recurrent state를 update한 **순서**에도 남는다. 음의 고유값은 단순 감쇠만 가능한 state가 parity 같은 교대 상태를 표현하게 하는 배경이다.

**학습 점검.** local attention은 어느 KV를 직접 다시 읽는지, recurrent state는 어느 정보를 고정 크기로 요약하는지 한 문장씩 대비한다. Hybrid model은 둘 중 하나가 다른 하나를 대체한다는 주장이 아니라, exact retrieval과 fixed-state memory의 약점을 보완하는 층 배치라는 점을 확인한다.

<a id="qwen38-route"></a>
## 5. Qwen3.8-Next 집중 읽기 경로

아래는 [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.1.1–§2.3·§3.1–§3.3을 읽기 위한 경로다. 기술 사실과 절 범위는 원문을 기준으로 한다.

### 5.1 MHA/MQA/GQA → MLA → DSA → QSA

위 [attention/cache 경로](#attention-cache)를 끝낸 뒤 Qwen §2.1.2를 읽는다. **MLA**는 token마다 보관할 KV 내용을 latent로 압축한다. **DSA**는 indexer로 token 후보를 Top-k 선택한다. **QSA**는 MQA indexer가 micro-block을 점수화하고, 선택 mask가 별도 sparse core attention의 범위를 정해 score 비용을 낮춘다. 따라서 이 순서는 역사적 동일 계보가 아니라, 긴 문맥 비용을 줄이는 서로 다른 축을 비교하는 읽기 경로다.

작은 예로 과거 key 16개와 micro-block 크기 `r=4`를 둔다. 먼저 16 key를 순서를 보존한 4개 complete block key로 압축한다. 각 query가 4 block을 score한 뒤 `Top-K^B`에서 두 block을 고르면, 그 block의 원래 token index 8개로 다시 펼쳐 main attention이 읽는다. block을 아직 채우지 못한 최신 tail token은 block index에 맡기지 않고 항상 후보에 넣는다. 이때 `16 → 4 → Top-K^B → token expansion + tail`은 **indexing 절차**다. MLA의 latent KV cache와 같은 연산이라고 부르지 않는다.

**점검:** “MLA에서 작아진 것은 저장되는 K/V 표현, QSA에서 먼저 작아진 것은 score할 후보 수”라고 말하고, causal block이 미래 token을 섞지 않아야 하는 이유를 설명한다.

### 5.2 Linear attention → DeltaNet → GDN

GDN의 state를 한 head 기준 `S_t∈R^{d_v×d_k}`라고 둔다. 이전 state를 먼저 `S_decay = α_t S_{t-1}`로 감쇠하면, `S_decay k_t`가 correction 전에 현재 key가 기존 memory에서 읽어낸 value 방향이다. 직관적 1차원 축약에서 이전 state가 `S=2`, `k=1`, 목표 value `v=5`, decay `α=0.5`, write gate `β=0.5`라고 하자. 먼저 decay로 남는 state는 1, 현재 key가 읽은 값도 1, correction error는 `5−1=4`다. β만큼 residual을 쓰면 state는 `1+0.5×4×1=3`이 된다. 이는 원문 식 전체를 대체하지 않는 작은 그림이지만, **α는 기존 연합을 얼마나 남길지, correction은 이미 key에 연결된 값을 왜 뺄지, β는 새 오차를 얼마나 쓸지**를 보여 준다.

Qwen의 GDN은 [Gated Delta Networks v3](https://arxiv.org/abs/2412.06464v3) 위에서 short convolution, L2 normalization, output gate를 결합한 hybrid branch다(Qwen §2.1.1·식 (1)–(11)). GDN은 fixed-size state라 모든 token을 정확히 재생하지 못하고, Qwen은 주기적 sparse global attention으로 그 약점을 보완한다.

### 5.3 residual → HC/mHC → GR

[Hyper-Connections v3](https://arxiv.org/abs/2409.19606v3) §2.1–§2.2는 여러 residual stream을 read map·write map·residual map으로 섞는다. [mHC v2](https://arxiv.org/abs/2512.24880v2) §3·§4.1–§4.2는 residual map을 doubly stochastic manifold에 가깝게 두어 수치 안정성을 노린다. Qwen의 **GR은 HC/mHC를 그대로 재사용한 이름이 아니다.** Qwen §2.2·식 (29)–(34)은 residual branch의 read/write traffic을 줄이는 별도 설계다.

branch가 4개이고 hidden channel이 `d`라면, GR read gate는 branch·channel마다 다른 `g_read∈R^{4×d}`로 어떤 channel을 어느 branch에서 읽을지 정한다. write gate는 branch마다 하나 `g_write∈R^4`인 scalar라 다음 residual을 branch 단위로 쓴다. 즉 **channel별 read, branch별 scalar write**다. 이 차원 차이와 H-res mix 생략은 품질 이름이 아니라 full-state read를 하나 줄이려는 memory-traffic 선택이라는 점을 점검한다.

### 5.4 MoE·FP8·n-gram·Muon을 함께 분류하기

Qwen의 MoE는 router/top-k와 expert capacity라는 [MoE 경로](#moe-precision)를 따른다. n-gram memory는 Qwen §2.3에서 token n-gram을 deterministic multi-head hash lookup으로 주소화하고 host memory에서 비동기 prefetch한다. 이는 context에 따라 attention으로 찾는 KV cache와 다르며, host offload는 “GPU에서 계산하지 않는다”가 아니라 lookup latency를 layer 배치와 겹치려는 시스템 설계다.

Muon은 제안자의 [Muon author note](https://kellerjordan.github.io/posts/muon/) “Definition”·“The design of Muon”·“Proving that NS iteration orthogonalizes the update”와 [Muon is Scalable for LLM Training v1](https://arxiv.org/abs/2502.16982v1) §2.1–§2.3·Algorithm 1을 함께 읽는다. 전자는 판본이 붙은 논문이 아닌 제안자 설명문이고, 후자는 분산 학습으로 확장한 원전이다. 대상은 **genuine 2D linear map**의 momentum update다. Q/K/V나 MLP projection은 논리적으로 독립 2D 행렬이면 Muon/Newton–Schulz 직교화 대상이다. 반면 embedding, output head, router, GR low-rank projection처럼 그 matrix geometry가 맞지 않는 parameter는 AdamW/Adam으로 남는다. 물리 저장이 fused tensor여도 의미상 Q·K·V가 다른 map이면 먼저 논리적으로 나누고, tensor-parallel shard여도 full logical matrix의 update 기하를 보존하도록 gather–orthogonalize–shard 순서를 생각한다. “저장 tensor가 2차원인가”만으로 Muon 대상을 정하면 안 된다.

<a id="residual-optimizer"></a>
## 6. Residual, manifold, optimizer와 전이: W09·W10·W15·W16

mHC의 Sinkhorn–Knopp projection은 모든 row/column 합이 1인 nonnegative map을 향하게 해 residual mixing의 안정성을 노린다. Muon의 Newton–Schulz는 momentum matrix를 semi-orthogonal update에 가깝게 만드는 다른 문제다. 둘 다 행렬을 다뤄도 mHC는 residual **경로**, Muon은 optimizer **update geometry**를 다룬다. Motif 3의 수정 mHC·QK-Clip·MoE stabilization과 Parallel Muon도 이 층위를 분리해 읽는다.

W15에서는 [Differential Transformer v2](https://arxiv.org/abs/2410.05258v2) §2.1의 두 attention map 차분과 [Grouped Differential Attention v1](https://arxiv.org/abs/2510.06949v1) §2.2의 비대칭 signal/noise head grouping을 먼저 읽는다. GDLA는 이 분리와 MLA식 latent KV를 결합한다. **점검:** `λ=1`이고 두 map이 한 token에 똑같이 `0.6`을 둘 때 차분이 `0`임을 계산한다. 실제 모델의 학습된 `λ`와 map은 달라 취소가 보장되지는 않으며, 잡음 억제는 이 구조가 노리는 해석이지 문자 그대로의 보장은 아니라는 점을 말한다. KV 압축과 이 차분은 서로 다른 병목을 푼다.

전이는 [Sparse Upcycling v2](https://arxiv.org/abs/2212.05055v2) §3–§3.1의 dense checkpoint→expert 복제와, [Priming v1](https://arxiv.org/abs/2605.08301v1) §2.2·§3.2.2–§3.2.4의 attention→hybrid alignment를 대비한다. Solar Open 2의 selective transfer는 shape·의미가 유지된 module만 옮기는 partial warm start다. expert를 복제하는 upcycling이나 alignment를 포함하는 hybrid priming과 같은 절차라고 부르지 않는다.

**학습 점검.** 2×2 nonnegative matrix에 row/column normalization을 번갈아 해 보는 것과, 2D momentum matrix의 update를 Newton–Schulz로 직교화하는 것을 그림으로 분리한다. 이어서 “저장 형상, 논리적 module 경계, transfer 가능한 표현”이 각각 왜 다른 판단 기준인지 설명한다.

<a id="evaluation-systems"></a>
## 7. 평가·검색·agent 시스템: W11–W14

W11은 전문가 모델의 SFT/RL 출력을 Overall SFT와 unified training으로 합치는 문제다([GLM-4.5 v1](https://arxiv.org/abs/2508.06471v1) §2.3·§3–§3.5). W12는 그 policy를 오래 실행되는 agent environment에서 비동기로 rollout하는 문제다. W13의 pass@k는 여러 sample의 해법 다양성, W14의 [STAR v1](https://arxiv.org/abs/2411.17800v1) §4–§4.1·§5.3–§5.4는 quality/parameter/cache proxy의 multi-objective search, LFM2는 실제 기기 latency·memory를 목적에 넣은 hardware-in-the-loop search를 다룬다.

**W14 점검.** 폭 3의 short convolution은 각 위치에서 이웃 세 token을 직접 섞는다고 써 본다. gate가 있더라도 이는 장거리 implicit convolution을 뜻하지 않는다. 후보 A와 B의 품질·latency·memory를 함께 놓고, 한 지표가 더 좋아도 다른 지표에서 열세면 Pareto 우위가 아닐 수 있음을 판단한다.

**점검:** benchmark 점수, pass@k, verifier 통과, device latency는 서로 같은 종류의 지표가 아니다. 어떤 지표가 모델의 어떤 단계에서 실패를 발견하는지 먼저 말한 뒤, 해당 보고서의 주장 범위를 판단한다.

## 원전 사용 원칙

- 판본 없는 링크 대신 위에 적은 arXiv revision을 우선 사용한다. 이후 개정이 있으면 절 제목과 수식·그림 번호를 다시 대조한다.
- Qwen3.8의 QSA·GDN·GR·n-gram·Muon은 원문 §2–§3이 1차 근거다. 이 문서의 작은 예제는 학습용 축약이며, 구현 수식·성능 수치는 원문으로 확인한다.
- LFM2는 Hyena를, KDA는 GDN을, QSA는 MLA를 각각 그대로 재명명한 것이 아니다. 연결은 전제 또는 대비일 수 있고, 곧 계보·동일 구현을 뜻하지 않는다.
- 배경 원전은 필요한 절만 읽는다. 주차별 보고서의 새 주장, 실험 조건, 한계는 각 주차 README의 고정 원문에서 확인한다.

새 배경 문서를 추가할 때는 [배경 문서 템플릿](../../templates/background.md)을 사용한다.
