# 16주 기술 보고서 배경 읽기 지도

이 문서의 출발점은 **각 주차 보고서 본문에서 설명·사용하거나 선행 연구로 인용한 개념**이다. 아래 표에서 보고서의 본문 절을 먼저 확인한 뒤 필요한 배경으로 이동한다. 참고문헌 목록에만 있거나, 이해에 도움이 될 것 같다는 이유만으로 추가한 자료는 필수 경로에 넣지 않는다.

**본문 직접 연결**과 **인용 논문에서 이어지는 배경**을 구분한다. 후자는 보고서 본문 → 인용 논문의 본문 → 선행 개념의 연결을 함께 적는다. 읽는 순서와 작은 숫자 예시는 본문을 이해하도록 편집한 학습 보조이며, 저자가 제시한 선수 학습 순서나 논문에 실린 예시라는 뜻은 아니다. 배경 원전은 명시한 절을 확인했으며, 각 주차 보고서는 해당 README의 고정 판본을 기준으로 한다.

## 본문 수식을 읽기 위한 네 가지 수학 도구

1. **내적과 softmax — [DeepSeek-V2 §2.1.1](https://arxiv.org/abs/2405.04434v5).** query `q`와 key `k`의 내적은 관련성 점수이고, `softmax`는 후보 점수를 합이 1인 가중치로 바꾼다. `softmax(QKᵀ/√d)V`에서 K/V를 과거 token마다 남기는 이유를 확인한다.
2. **외적·저랭크·상태 — [DeepSeek-V2 §2.1.2](https://arxiv.org/abs/2405.04434v5), [Qwen3.8 §2.1.1](https://arxiv.org/abs/2608.30320v1).** `v kᵀ`는 key 방향에서 value를 꺼낼 수 있는 연관 행렬을 쓴다. 저랭크 압축은 `c=W_Dh`처럼 작은 latent를 남긴다. 두 보고서의 수식에서 행렬 차원과 보관하는 상태가 무엇인지 각각 써 본다.
3. **확률비·advantage·KL — [DeepSeek-R1 §2.1](https://arxiv.org/abs/2501.12948v2), [GLM-5 §4.1.2](https://arxiv.org/abs/2602.15763v2).** `r=π_θ(a|s)/π_old(a|s)`는 새 정책과 수집 정책의 action 확률비다. advantage는 기준보다 좋은 action인지의 신호, KL은 두 분포의 **비대칭 분포 차이 척도**다. 각 보고서에서 ratio·KL·mask가 들어가는 위치를 확인한다.
4. **부동소수점 범위·정밀도 — [DeepSeek-V3 §3.3](https://arxiv.org/abs/2412.19437v2).** exponent bit는 크기 범위, mantissa bit는 그 범위 안의 정밀도와 관련된다. 본문의 FP8 format·scale·고정밀 누적을 이 관점으로 읽는다.

<a id="week-map"></a>
## 주차별 본문 근거와 읽기 위치

표의 개념은 해당 보고서 본문에서 확인한 항목이다. 가이드의 공통 장 전체를 모든 주차의 필수 선수 지식으로 읽지 않고, 이 행에 적힌 개념만 찾아 읽는다.

| 주차 | 본문에서 잡을 개념 | 보고서 본문 근거 | 가이드에서 읽을 부분 |
| --- | --- | --- | --- |
| [W01](../weeks/w01/README.md) | BPE·pre-norm/SwiGLU/RoPE/AdamW, Llama 2 구조 변경·선호 ranking | [LLaMA §1–§2.2](https://arxiv.org/abs/2302.13971v1); [Llama 2 §2.2·§3.1–§3.2.3](https://arxiv.org/abs/2307.09288v2) | [구성요소·구조 비교·ranking](llama.md), [학습 예산](#data-context) |
| [W02](../weeks/w02/README.md) | Qwen1.5 대비 구조·BBPE, instruction pool, 과제별 합성·검증 | [Qwen2 §2·§3.2·§4.1–§4.3](https://arxiv.org/abs/2407.10671v4); [Qwen2.5 §2·§3.3·§4.1–§4.2](https://arxiv.org/abs/2412.15115v2) | [구조·토크나이저·데이터](qwen.md), [DPO 보충](#data-context) |
| [W03](../weeks/w03/README.md) | thinking/non-thinking fusion, 생각 예산, teacher-logit KL | [Qwen3 §4.1–§4.3·§4.5·§4.7](https://arxiv.org/abs/2505.09388v1) | [Qwen3 본문 안의 경로](#qwen3-internal) |
| [W04](../weeks/w04/README.md) | latent KV·decoupled RoPE, fine-grained/shared expert, device routing | [DeepSeek-V2 §2.1–§2.2](https://arxiv.org/abs/2405.04434v5) | [attention/cache](#attention-cache), [MoE 분할·공유](#moe-precision) |
| [W05](../weeks/w05/README.md) | MoE balance, sequential MTP, speculative decoding, FP8 | [DeepSeek-V3 §2.1.2·§2.2·§3.3·§5.4.3](https://arxiv.org/abs/2412.19437v2) | [MoE·MTP·정밀도](#moe-precision) |
| [W06](../weeks/w06/README.md) | GRPO, accuracy/format reward, cold start | [DeepSeek-R1 §2.1–§2.2·§3](https://arxiv.org/abs/2501.12948v2) | [GRPO·검증 보상](#grpo) |
| [W07](../weeks/w07/README.md) | MTP, SWA/GA, sink logit, MOPD | [MiMo §2.2](https://arxiv.org/abs/2505.07608v2); [Flash §2.1–§2.3·§4.1·§4.4](https://arxiv.org/abs/2601.02780v2) | [MTP](#moe-precision), [SWA/sink](#sparse-hybrid), [MOPD](#mopd) |
| [W08](../weeks/w08/README.md) | MLA의 MQA mode, DSA 선택·학습, agent 과제 합성 | [DeepSeek-V3.2 §2.1–§2.1.1·§3.2.3](https://arxiv.org/abs/2512.02556v1) | [MLA → DSA](#attention-cache), [W08의 과제 합성 절](../weeks/w08/README.md) |
| [W09](../weeks/w09/README.md) | CSA/HCA의 sequence 압축, specialist OPD·full-vocabulary scheduling | [DeepSeek-V4 §2.3·§5.1–§5.2](https://arxiv.org/abs/2606.19348v1) | [CSA/HCA 본문](../weeks/w09/README.md), [교사 신호·비용](#specialist-opd) |
| [W10](../weeks/w10/README.md) | GDN, MQA indexer·DSA/QSA, HC/mHC·GR, n-gram, Muon | [Qwen3.8 §2.1.1–§2.3·§3.1](https://arxiv.org/abs/2608.30320v1) | [Qwen 경로와 인용 논문 속 MLA](#qwen38-route) |
| [W11](../weeks/w11/README.md) | expert 통합, difficulty·64K RL, agent SFT 합성·XML | [GLM-4.5 §3.1–§3.5](https://arxiv.org/abs/2508.06471v1) | [전문가 생성·통합](#expert-integration), [agent 자료·환경](#evaluation-systems) |
| [W12](../weeks/w12/README.md) | rollout 분리·TITO·importance mask, 네 종류 검증 환경 | [GLM-5 §3.2·§3.6·§4.1–§4.2](https://arxiv.org/abs/2602.15763v2) | [비동기 RL 본문 식](#async-rl), [agent 자료·환경](#evaluation-systems) |
| [W13](../weeks/w13/README.md) | SSP·Pass@K, seed→trace curriculum, MGPO·Long2Short | [VibeThinker-1.5B §2–§3.4](https://arxiv.org/abs/2511.06221v1); [3B §2.1–§2.2](https://arxiv.org/abs/2606.16140v1) | [VibeThinker 본문 경로](#vibe-diversity) |
| [W14](../weeks/w14/README.md) | STAR·기기 탐색, short convolution, tempered decoupled Top-K KD | [LFM2 §2.1–§2.2·§3.3·§8.2](https://arxiv.org/abs/2511.23404v1) | [convolution/hybrid](#sparse-hybrid), [Top-K KD](#topk-kd), [기기 검색](#evaluation-systems) |
| [W15](../weeks/w15/README.md) | GDA→GDLA, Parallel Muon, seven-teacher MOPD의 domain별 신호 | [Motif 2 §2·§4.3](https://arxiv.org/abs/2511.07464v1); [Motif 3 §2.2·§5.1–§5.2](https://arxiv.org/abs/2608.09119v1) | [differential·optimizer](#residual-optimizer), [교사 신호·비용](#specialist-opd) |
| [W16](../weeks/w16/README.md) | tokenizer·한국어 데이터, KDA·NoPE·음의 고유값, selective transfer | [Solar Open §2.1·§3.1–§3.2·§6.1](https://arxiv.org/abs/2601.07022v1); [Solar Open 2 §2.2·§3.1](https://arxiv.org/abs/2607.20062v2) | [KDA/NoPE](#sparse-hybrid), [전이의 본문 비교](#residual-optimizer) |

<a id="qwen-data"></a>
## W02 — 구성요소에서 합성 데이터까지

[Qwen 계열 상세 가이드](qwen.md)에서 Qwen1.5→Qwen2→Qwen2.5의 대응 7B 구조, GQA·MoE·DCA/YaRN·BBPE, instruction pool의 선별·확장, 과제별 합성·검증을 함께 읽는다. 모든 항목에 보고서 본문 또는 Qwen1.5 공식 자료의 출발점과 선행 원전 범위를 연결했다.

<a id="data-context"></a>
## 0. 학습 예산, 긴 문맥, 선호 자료: W01–W03

[LLaMA §1–§2](https://arxiv.org/abs/2302.13971v1)가 직접 인용한 [Chinchilla v1](https://arxiv.org/abs/2203.15556v1) §1·§3을 읽는다. 고정 FLOPs에서 parameter 수와 학습 token 수를 함께 정하는 관계가 W01의 출발점이다. W02에서 이 논문은 [Qwen2.5 §3.2](https://arxiv.org/abs/2412.15115v2)의 hyperparameter scaling과 대비할 때만 읽는다. 데이터 품질·혼합의 근거는 Qwen2 §3.1과 Qwen2.5 §3.1 자체에 있다.

[W02 긴 문맥 보충](#qwen-data)의 YaRN은 위치/attention scaling을, DCA는 chunk 안·먼 chunk·인접 chunk의 상대 위치 구성을 조절한다. RoPE 기본식이 낯설면 [attention/cache](#attention-cache)에서 먼저 확인한다.

W02의 [Qwen2 §4.1–§4.3](https://arxiv.org/abs/2407.10671v4), [Qwen2.5 §4.2](https://arxiv.org/abs/2412.15115v2)가 직접 사용하는 [DPO v3](https://arxiv.org/abs/2305.18290v3) §3–§4를 읽는다. DPO는 `(prompt, 선호 응답, 비선호 응답)`과 reference policy에서 선호를 직접 최적화한다. **점검:** 고정된 선호쌍과 reference policy가 목적식에서 하는 일을 설명한다.

<a id="qwen3-internal"></a>
**W03은 Qwen3 본문 안에서 준비한다.** [Qwen3 §4.1–§4.3 → §4.5 → §4.7](https://arxiv.org/abs/2505.09388v1)의 post-training 단계·thinking/non-thinking fusion을 먼저 읽고, student가 생성한 sequence에서 teacher logits와 KL을 맞추는 증류를 확인한다. 마지막으로 thinking budget과 direct RL 비교를 읽는다. §4.3에서는 Stage-2의 self-rejection-sampled thinking 자료와 지시 수행·역할극을 포함한 non-thinking 자료를 합친다. `/think`·`/no think`와 빈 `<think>` block이 데이터와 template를 어떻게 연결하는지 확인하고, §4.5에서는 두 모드가 teacher output과 student-generated sequence의 logit alignment로 유지되는지 따라간다.

**W01 점검.** 고정 FLOPs에서 parameter와 token 수가 함께 바뀌는 간단한 선택을 써 보고, 2차원 RoPE에서는 벡터 `(x₁,x₂)`를 위치 `p`의 각도로 회전한 뒤 query·key의 내적이 `p−q`에 의존함을 계산한다. 이 상대 위치 성질이 GQA의 KV 공유와 별개라는 점도 확인한다.

<a id="attention-cache"></a>
## 1. Attention, 위치, cache: W01·W02·W04에서 W08·W10으로

**W04의 본문 직접 경로.** [DeepSeek-V2 §2.1.1–§2.1.4](https://arxiv.org/abs/2405.04434v5)가 설명·인용한 [Transformer v7](https://arxiv.org/abs/1706.03762v7) §3.2.1–§3.2.2 → [MQA v1](https://arxiv.org/abs/1911.02150v1) §2.4·§3–§3.1 → [GQA v3](https://arxiv.org/abs/2305.13245v3) §2.1–§2.2 → [RoFormer v5](https://arxiv.org/abs/2104.09864v5) §3.2·§3.4.2 순으로 읽는다. W01에서는 LLaMA/Llama 2 §2.2의 MHA·RoPE·GQA만, W02에서는 Qwen2 §2.2의 RoPE를 이곳에서 확인한다.

MHA는 각 query head가 과거의 K/V를 읽으므로 decoding 때 K/V cache가 자란다. MQA는 모든 query head가 하나의 K/V head를 공유하고, GQA는 몇 개 query head씩 공유한다. RoPE는 query·key를 위치별로 회전시켜 두 위치의 관계가 내적에 남게 한다. **MLA는 head 수를 줄이는 MQA/GQA와 달리, K/V 내용을 저차원 latent로 압축한다.** `c_t=W_Dh_t`를 cache하고 고정 projection은 query 쪽으로 결합할 수 있다. 다만 위치 회전 성분은 그렇게 단순히 흡수되지 않으므로 별도 RoPE key를 둔다.

**학습 점검.** 길이 `L`, head 수 `h`, head 차원 `d_h`, latent 차원 `d_c`를 두고, MHA가 대략 `L×h×d_h` 규모의 K/V를 남기는 반면 MLA가 어떤 `c_t`와 위치 성분을 남기는지 써 본다. “저랭크 latent KV”는 **저장 표현**이고, 뒤의 DSA/QSA는 **어디를 읽을지 고르는 index**라는 차이를 말할 수 있어야 한다.

**W08의 본문 직접 경로.** [DeepSeek-V3.2 §2.1–§2.1.1](https://arxiv.org/abs/2512.02556v1)은 MLA와 MQA를 인용하고, DSA를 MLA 위에 구성한다. 따라서 V2의 MLA·decoupled RoPE를 읽고 DSA의 indexer·token Top-k로 돌아온다. MQA mode에서 latent KV entry를 query head 사이에 공유하는 것과, indexer가 읽을 entry를 Top-k로 고르는 것은 별도 단계다. Qwen3.8에서 DSA와 MLA로 이어지는 연결은 아래 [Qwen 경로](#qwen38-route)에서 직접 인용과 후속 배경을 나눠 확인한다.

<a id="moe-precision"></a>
## 2. MoE, multi-token prediction, FP8: W04·W05·W07

**본문 연결.** W05의 [DeepSeek-V3 §2.1.2](https://arxiv.org/abs/2412.19437v2)는 DeepSeekMoE·Loss-Free Balancing을, §2.2는 Gloeckle 등의 MTP를, §5.4.3은 speculative decoding을, §1·§3.3은 FP8·mixed precision 원전을 직접 인용한다. 아래 외부 읽기는 이 절들에 대응한다. W07의 MTP는 MiMo §2.2와 Flash §2.1·§2.3이 인용한 V3 §2.2로 이어진다. W09·W10의 구체적 MoE/정밀도 설정은 각 보고서 본문에서 읽는다.

**W04의 MoE 분할과 공유.** [DeepSeek-V2 §2.2.1–§2.2.3](https://arxiv.org/abs/2405.04434v5)가 직접 인용한 [DeepSeekMoE v1 §2–§3.3](https://arxiv.org/abs/2401.06066v1)을 먼저 읽는다. 하나의 큰 expert를 작은 expert들로 나누면 조합 수가 어떻게 달라지는지, shared expert가 공통 지식을 맡으면 routed expert가 무엇에 특화할 수 있는지 설명한다. V2의 device-limited routing과 expert/device/communication balance loss는 본문 Fig. 4·식 (20)–(31)에서 확인한다.

**W05의 MoE 균형.** [DeepSeekMoE v1](https://arxiv.org/abs/2401.06066v1) §2·§3.1–§3.3 → [Loss-Free Balancing v1](https://arxiv.org/abs/2408.15664v1) §2–§3 → [DeepSeek-V3 v2](https://arxiv.org/abs/2412.19437v2) §2.1.2로 간다. router는 token마다 top-k expert를 고른다. 일부 expert에 token이 몰리면 계산·통신이 병목이 된다. Loss-Free Balancing은 auxiliary loss gradient로 본 모델을 밀기보다, 최근 load로 expert별 routing bias를 조정한다. 이는 V3가 대규모로 **채택·검증한 선행 방법**이며 V3가 새로 발명한 기법으로 읽지 않는다.

**MTP 읽기.** [Multi-token Prediction v1](https://arxiv.org/abs/2404.19737v1) §2 “Method”의 inference → [Speculative Decoding v2](https://arxiv.org/abs/2211.17192v2) §2.1–§2.3 → V3 §2.2 순서다. MTP는 다음 한 token만 맞히는 loss보다 먼 token에도 학습 신호를 준다. speculative decoding은 draft 후보를 target model이 검증·수정해 분포를 보존한다. V3의 sequential MTP는 병렬 head가 독립적으로 먼 token을 맞히는 설정과 달리 앞선 예측을 뒤 예측의 조건으로 연결한다.

**FP8 읽기.** V3 §3.3이 직접 인용한 [FP8 Formats v2 §2–§3.2](https://arxiv.org/abs/2209.05433v2)와 [FP8-LM v2 §2.1–§2.2·Appendix A.2](https://arxiv.org/abs/2310.18313v2)를 읽고, V3 §3.3.1–§3.3.3·Fig. 6–7·Appendix B.1로 돌아온다. FP8-LM의 per-tensor scaling·distributed FP8 all-reduce/optimizer와 V3의 tile/block scaling·FP32 accumulation을 대비한다. master weight와 loss scaling은 본문이 인용한 [Mixed Precision Training v3 §3.1–§3.3](https://arxiv.org/abs/1710.03740v3)에서 보충한다. E4M3/E5M2는 exponent/mantissa 배분이 다르다. scale은 값 묶음을 FP8이 표현 가능한 범위로 옮기고, master weight·gradient·accumulation처럼 오차가 누적되는 곳은 높은 정밀도로 둔다. 따라서 “FP8 학습”은 모든 tensor를 같은 8비트 형식으로 저장한다는 뜻이 아니다.

**학습 점검.** top-k router가 고르는 expert와 DSA/QSA가 고르는 KV entry를 구분한다. 또한 FP8에서 “range를 넘는 overflow”와 “mantissa가 짧아 생기는 quantization error”가 서로 다른 문제이고, scale·고정밀 누적이 각각 어디에 개입하는지 설명한다.

<a id="rl-distillation"></a>
## 3. 본문별 정렬·증류·비동기 RL 경로

같은 RL 용어가 나와도 아래 자료를 모든 주차에 반복해서 읽지 않는다. 각 항목은 해당 보고서가 설명하는 방법과 연결한 범위다.

<a id="sft-ppo"></a>
**W01 — Llama 2의 선호 순위와 정책 학습.** [LLaMA 계열 가이드](llama.md#preference-ranking)에서 chosen/rejected ranking → helpfulness/safety reward model → rejection sampling/PPO를 읽는다. InstructGPT와 PPO 원전 범위도 이 W01 경로에 모아 둔다.

<a id="grpo"></a>
**W06 — critic을 생략한 GRPO와 검증 보상.** [DeepSeek-R1 §2.1](https://arxiv.org/abs/2501.12948v2)이 직접 비교·인용한 PPO와 [DeepSeekMath v3](https://arxiv.org/abs/2402.03300v3) §4.1.1–§4.1.3을 연결한다. GRPO는 같은 prompt의 여러 rollout reward로 상대 advantage를 만든다. R1 §2.2는 수학 정답 비교와 코드의 compiler/test-case 검증을 accuracy reward의 예로 들고, format reward를 별도로 둔다. **학습 예시:** reward `[0, 1, 1, 0]`에서 상대 advantage의 부호를 구한 뒤, 논문 목적식의 확률비와 KL이 어디에 들어가는지 설명한다. 이어서 R1 §3.1–§3.2.2·Supplementary B.3.2–B.3.3에서 cold-start와 language-consistency reward, 추론·비추론 자료를 함께 쓰는 두 번째 SFT, 두 번째 RL이 각각 어떤 문제를 다루는지 나눈다.

<a id="mopd"></a>
**W07 — 학생이 생성한 경로 위에서의 MOPD.** [MiMo-V2-Flash §4.1 Stage 3·§4.4](https://arxiv.org/abs/2601.02780v2)가 직접 인용한 [On-Policy Distillation / GKD v3](https://arxiv.org/abs/2306.13649v3) §2–§3·Algorithm 1을 읽는다. teacher가 완성한 답변을 모으는 경우와 student가 생성한 prefix에서 teacher 분포를 조회하는 경우를 대비한다. Flash §4.4 식 (5)–(9)에서는 domain teacher가 준 reverse-KL advantage와 ORM advantage를 결합한다. teacher 분포와 정답 여부가 다른 신호를 주는 짧은 응답 예를 만들어, domain별 teacher 선택과 ORM의 역할을 따로 설명한다.

<a id="expert-integration"></a>
**W11 — 전문가 학습 후 단일 모델로 통합.** [GLM-4.5 §3.1·§3.2·§3.3.2–§3.5](https://arxiv.org/abs/2508.06471v1)를 먼저 읽는다. §3.2가 직접 인용한 DeepSeekMath의 GRPO 목적식과 KL 제거를 복습하고, 그 뒤의 cold-start → RL → self-distillation → RL 및 Overall SFT/unified training은 GLM-4.5 본문에서 확인한다. Reasoning RL의 difficulty 전환·single-stage 64K·token-weighted loss는 §3.2·Fig. 5–7에서, agent의 terminal-state 보상은 §3.3에서 읽는다.

<a id="async-rl"></a>
**W12 — 비동기 rollout의 token·확률 보존.** [GLM-5 §1·§3.2·§4.1.1–§4.1.2](https://arxiv.org/abs/2602.15763v2)가 직접 연결한 GLM-4.5의 rollout 시스템과 DeepSeekMath의 GRPO를 배경으로 읽는다. 본문이 새로 정의하는 TITO, old rollout log-probability, importance ratio와 mask는 GLM-5 식 (3)–(5)로 확인한다. PPO는 여기서 비교 대상이며, 이 비동기 보정의 정의는 GLM-5 본문에 있다.

<a id="vibe-diversity"></a>
**W13 — 해법 다양성에서 선택 압력으로.** [VibeThinker-1.5B §2·§3.1–§3.4](https://arxiv.org/abs/2511.06221v1)의 SSP·Pass@K·MGPO를 읽고, [VibeThinker-3B §2.1.1–§2.1.2·Fig. 3](https://arxiv.org/abs/2606.16140v1)으로 이어 간다. trusted seed에서 query expansion·multiple teacher trace·majority vote·verification을 거쳐 broad SFT와 hard/long SFT로 옮기는 기준이 배경이다. **점검:** stage 2의 짧은 trace 제거와 쉬운 query 제거가 각각 길이와 난이도 중 무엇을 거르는지 나눈다. 1.5B §2가 직접 인용한 [DeepSeekMath §4.1](https://arxiv.org/abs/2402.03300v3)의 group-relative 목적식에 돌아가, MGPO의 능력 경계 가중과 3B §2.2의 정답 trajectory 내 Long2Short 길이 재가중을 대조한다.

<a id="specialist-opd"></a>
**W09·W15 — 공유하는 OPD 배경과 서로 다른 문제.** [DeepSeek-V4 §5.1.1–§5.1.2·식 (29)·§5.2.2](https://arxiv.org/abs/2606.19348v1)는 specialist RL 뒤 mixed RL을 OPD로 바꾸고 full-vocabulary teacher 신호의 비용을 줄이는 scheduling을 다룬다. 본문이 인용한 [MiniLLM v1 §2.1–§2.2·식 (1)–(7)](https://arxiv.org/abs/2306.08543v1)의 reverse-KL과 student-sampled optimization을 배경으로 읽는다. **W09 점검:** student prefix에서 전체 어휘 분포를 조회하는 과정의 어느 단계가 계산·메모리를 쓰는지 그리고 scheduling과 연결한다.

[Motif 3 §5.1·§5.2.2–§5.2.4·Table 5](https://arxiv.org/abs/2608.09119v1)가 직접 인용한 [MiMo-V2-Flash §4.1·§4.4·식 (5)–(9)](https://arxiv.org/abs/2601.02780v2)를 배경으로 읽는다. W15의 질문은 13개 verifier domain을 다루는 6개 GRPO teacher와 1개 SWE SFT teacher의 서로 다른 학습 신호·latency를 어떻게 다루는가다. agent tool-use의 outcome verifier, professional-work의 judge, software-engineering의 successful-trajectory SFT를 나누고, token importance correction과 teacher routing이 각각 어느 학습 단계에 들어가는지 표시한다. W07에서 다룬 reverse-KL advantage와 ORM 결합 식을 다시 유도하는 목표로 삼지 않는다.

<a id="topk-kd"></a>
**W14 — 저장하지 않은 teacher tail을 다루는 KD.** [LFM2 §3.3·식 (1)–(2)·Appendix A](https://arxiv.org/abs/2511.23404v1)가 직접 인용한 [Hinton et al. v1 §2](https://arxiv.org/abs/1503.02531v1)에서 temperature soft target을, [Decoupled Knowledge Distillation v2 §3.1–§3.3](https://arxiv.org/abs/2203.08679v2)에서 target/non-target KL 분해를 읽는다. LFM2는 Top-K membership mass와 그 안의 conditional distribution을 따로 맞춘다. DKD의 class 분해와 동일한 식은 아니다. **점검:** K=2에서 관찰 가능한 teacher top-2와 저장되지 않은 tail을 표시하고, temperature가 어느 항에 들어가는지 확인한다.

<a id="solar-posttraining"></a>
**W16 보충 — 데이터·구조 목표를 읽은 뒤의 후학습.** [Solar Open §6–§6.1.1](https://arxiv.org/abs/2601.07022v1)은 SnapPO에서 generation·reward computation·training을 cache로 분리하고 behavior-policy log probability를 저장한다. 직접 채택한 [GSPO v1 §1–§4.1](https://arxiv.org/abs/2507.18071v1)의 sequence likelihood ratio·sequence-level clipping을 읽고, response pool의 reward만 다시 계산할 때 재생성할 필요가 없는 항목을 적는다.

[Solar Open 2 §4.2.2](https://arxiv.org/abs/2607.20062v2)는 12개 specialist를 독립 RL한 뒤 prompt 하나를 한 teacher에 route해 통합한다. 본문이 직접 인용한 [MOPD v1 §3.1–§3.2·식 (1)–(5)](https://arxiv.org/abs/2606.30406v1)에서 teacher routing·on-policy consolidation을 확인하고, 여기서는 250B 규모의 full-vocabulary 신호 비용과 CPU snapshot swap에 집중한다. 12개 teacher를 평균내는 것과 prompt별 한 teacher 분포를 distill하는 것을 구분한다.

<a id="sparse-hybrid"></a>
## 4. 긴 문맥과 hybrid token mixing: W07·W08·W10·W14·W16

W07의 [MiMo-V2-Flash §2.2](https://arxiv.org/abs/2601.02780v2)가 직접 인용한 [Longformer v2](https://arxiv.org/abs/2004.05150v2) §3–§3.1에서 local window와 global position을 읽는다. 이어서 Flash가 배치한 SWA/GA의 역할을 확인한다. Flash §2.2가 구현 출처로 밝힌 [gpt-oss model card v1 §2.2](https://arxiv.org/abs/2508.10925v1)를 이어 읽는다. learnable sink는 각 head의 softmax 분모에 더하는 bias로, 어느 token에도 attention을 배정하지 않을 여지를 만든다. Flash 식 (1)–(4)에서 이 항을 찾고, 초기 token의 KV를 cache하는 sink token 정책과 구분한다. Flash §2.3.1–§2.3.2의 lightweight MTP는 KV I/O·작은 batch의 RL rollout·straggler 문제에 맞춘 구조다. 같은 MTP라도 W05의 학습 보조 loss와 W07의 rollout 병목이라는 질문을 나눈다.

Qwen3.8 §2.1.1이 직접 인용한 [Linear Transformers Are Secretly Fast Weight Programmers v3](https://arxiv.org/abs/2102.11174v3) §2·§3.1–§4.2에서는 선형 attention을 `S_t=S_{t-1}+v_tk_t^T`, `o_t=S_tq_t` 같은 fixed-size outer-product state로 해석한다. [Gated Delta Networks v3](https://arxiv.org/abs/2412.06464v3) §2.1–§2.2·§3.1–§3.3은 같은 key에 새 value를 덮어쓸 수 있도록 delta rule·gate·decay를 둔다. W14에서는 LFM2 §8.2가 직접 대조하는 [Hyena v3 §2.1·§3.1–§3.4](https://arxiv.org/abs/2302.10866v3)의 long implicit convolution을 읽는다. LFM2는 이를 통째로 채택하지 않은 gated short convolution + 소수 GQA 설계다([LFM2 v1](https://arxiv.org/abs/2511.23404v1) §2.2).

W16의 Solar Open 2 §2.2는 [Kimi Linear v2 §2.2·§3](https://arxiv.org/abs/2510.26692v2)와 [Unlocking State-Tracking in Linear RNNs v5 §3.1·§4.1–§4.2](https://arxiv.org/abs/2411.12537v5)를 직접 인용한다. NoPE 자체는 [The Impact of Positional Encoding on Length Generalization in Transformers v2](https://arxiv.org/abs/2305.19466v2) §4 “What Is The Effect of Positional Encoding?”·§5 “How Does NoPE Represent Positions?”에서 위치 정보를 표현하는 방식을 확인한다. sequence 순서는 position embedding만이 아니라 recurrent state를 update한 **순서**에도 남는다. 음의 고유값은 단순 감쇠만 가능한 state가 parity 같은 교대 상태를 표현하게 하는 배경이다.

**학습 점검.** local attention은 어느 KV를 직접 다시 읽는지, recurrent state는 어느 정보를 고정 크기로 요약하는지 한 문장씩 대비한다. Hybrid model은 둘 중 하나가 다른 하나를 대체한다는 주장이 아니라, exact retrieval과 fixed-state memory의 약점을 보완하는 층 배치라는 점을 확인한다.

<a id="qwen38-route"></a>
## 5. Qwen3.8-Next 집중 읽기 경로

아래는 [Qwen3.8-Next v1](https://arxiv.org/abs/2608.30320v1) §2.1.1–§2.3·§3.1–§3.3을 읽기 위한 경로다. 기술 사실과 절 범위는 원문을 기준으로 한다.

### 5.1 본문 직접 경로: attention·MQA → DSA → QSA

**본문 직접 연결:** Qwen §2.1.1은 Transformer의 전역 attention을, §2.1.2는 MQA와 DSA를 직접 인용한다. [MQA §2.4·§3](https://arxiv.org/abs/1911.02150v1)와 [DeepSeek-V3.2 §2.1](https://arxiv.org/abs/2512.02556v1)을 읽고 Qwen의 QSA로 돌아온다. QSA의 **MQA indexer**가 micro-block을 점수화하고, 펼친 선택 mask가 별도 sparse core attention의 범위를 정한다. indexer 비용은 `O(L²)`에서 `O(L²/r)`로 줄지만 고정 `r`에서는 여전히 quadratic이고, sparse core 비용은 별도로 남는다. GQA는 이 절에서 dense 성능 baseline으로 읽는다.

**인용 논문에서 이어지는 MLA 배경:** Qwen 본문은 MLA를 직접 언급하지 않는다. 연결은 [Qwen §2.1.2](https://arxiv.org/abs/2608.30320v1) → [V3.2 §2.1–§2.1.1의 MLA 기반 DSA](https://arxiv.org/abs/2512.02556v1) → [V2 §2.1의 MLA](https://arxiv.org/abs/2405.04434v5)다. DSA의 구현을 이해할 때 이 경로로 latent KV 저장을 확인한다. QSA가 MLA를 사용하거나, 이 읽기 순서가 동일한 구현의 계보라는 뜻은 아니다.

작은 예로 과거 key 16개와 micro-block 크기 `r=4`를 둔다. 먼저 16 key를 순서를 보존한 4개 complete block key로 압축한다. 각 query가 4 block을 score한 뒤 `Top-K^B`에서 두 block을 고르면, 그 block의 원래 token index 8개로 다시 펼쳐 main attention이 읽는다. block을 아직 채우지 못한 최신 tail token은 block index에 맡기지 않고 항상 후보에 넣는다. 이때 `16 → 4 → Top-K^B → token expansion + tail`은 **indexing 절차**다. MLA의 latent KV cache와 같은 연산이라고 부르지 않는다.

Qwen §2.1.2 식 (12)–(20)에서는 dense teacher의 token attention을 block별 max-pool해 teacher distribution을 만들고, block indexer를 KL로 학습한 뒤 sparse continued pre-training으로 옮긴다. 선택 단위가 token에서 block으로 바뀌면 teacher 신호도 같은 단위로 맞춰야 하는 이유를 확인한다.

**점검:** “MLA에서 작아진 것은 저장되는 K/V 표현, QSA에서 먼저 작아진 것은 score할 후보 수”라고 말하고, causal block이 미래 token을 섞지 않아야 하는 이유를 설명한다.

### 5.2 Linear attention → DeltaNet → GDN

GDN의 state를 한 head 기준 `S_t∈R^{d_v×d_k}`라고 둔다. 이전 state를 먼저 `S_decay = α_t S_{t-1}`로 감쇠하면, `S_decay k_t`가 correction 전에 현재 key가 기존 memory에서 읽어낸 value 방향이다. 직관적 1차원 축약에서 이전 state가 `S=2`, `k=1`, 목표 value `v=5`, decay `α=0.5`, write gate `β=0.5`라고 하자. 먼저 decay로 남는 state는 1, 현재 key가 읽은 값도 1, correction error는 `5−1=4`다. β만큼 residual을 쓰면 state는 `1+0.5×4×1=3`이 된다. 이는 원문 식 전체를 대체하지 않는 작은 그림이지만, **α는 기존 연합을 얼마나 남길지, correction은 이미 key에 연결된 값을 왜 뺄지, β는 새 오차를 얼마나 쓸지**를 보여 준다.

Qwen §2.1.1은 Schlag 등의 fast-weight 해석과 [Gated Delta Networks v3](https://arxiv.org/abs/2412.06464v3)를 직접 인용한다. 이 절의 식 (1)–(11)에서 short convolution, L2 normalization, output gate와 recurrent update를 확인한다. 위 숫자는 이 식의 학습용 축약이다. GDN은 fixed-size state라 모든 token을 정확히 재생하지 못하고, Qwen은 주기적 sparse global attention으로 이를 보완한다.

### 5.3 residual → HC/mHC → GR

Qwen §2.2가 직접 비교하는 [Hyper-Connections v3](https://arxiv.org/abs/2409.19606v3) §2.1–§2.2와 [mHC v2](https://arxiv.org/abs/2512.24880v2) §3·§4.1–§4.2를 먼저 읽는다. HC는 여러 residual stream을 read·write·residual map으로 섞고, mHC는 residual map을 doubly stochastic manifold에 가깝게 둔다. 이어서 Qwen §2.2·식 (29)–(34)의 GR이 read/write traffic을 어떻게 줄이는지 읽는다.

branch가 4개이고 hidden channel이 `d`라면, GR read gate는 branch·channel마다 다른 `g_read∈R^{4×d}`로 어떤 channel을 어느 branch에서 읽을지 정한다. write gate는 branch마다 하나 `g_write∈R^4`인 scalar라 다음 residual을 branch 단위로 쓴다. 즉 **channel별 read, branch별 scalar write**다. 이 차원 차이와 H-res mix 생략은 품질 이름이 아니라 full-state read를 하나 줄이려는 memory-traffic 선택이라는 점을 점검한다.

### 5.4 MoE·FP8·n-gram·Muon을 함께 분류하기

Qwen의 MoE는 router/top-k와 expert capacity라는 [MoE 경로](#moe-precision)를 따른다. Qwen §2.3이 직접 인용한 [N-Grammer v1 §3.1–§3.4](https://arxiv.org/abs/2207.06366v1)에서 latent n-gram lookup이 token representation을 보강하는 방식을 먼저 읽는다. Qwen의 n-gram memory는 token n-gram을 deterministic multi-head hash lookup으로 주소화하고 host memory에서 비동기 prefetch한다. 이는 context에 따라 attention으로 찾는 KV cache와 다르며, host offload는 “GPU에서 계산하지 않는다”가 아니라 lookup latency를 layer 배치와 겹치려는 시스템 설계다.

Qwen §3.1이 직접 인용하는 [Muon author note](https://kellerjordan.github.io/posts/muon/) “Definition”·“The design of Muon”·“Proving that NS iteration orthogonalizes the update”와 [Muon is Scalable for LLM Training v1](https://arxiv.org/abs/2502.16982v1) §2.1–§2.3·Algorithm 1을 함께 읽는다. 전자는 제안자 설명문이고, 후자는 분산 학습으로 확장한 원전이다. Qwen이 Muon에 맡기는 대상은 **genuine 2D linear map**의 momentum update다. Q/K/V나 MLP projection은 논리적으로 독립 2D 행렬이면 Muon/Newton–Schulz 직교화 대상이다. 반면 embedding, output head, router, GR low-rank projection 등은 AdamW/Adam으로 남긴다. 물리 저장이 fused tensor여도 의미상 Q·K·V가 다른 map이면 먼저 논리적으로 나누고, tensor-parallel shard에서도 full logical matrix의 update 기하를 보존하는 gather–orthogonalize–shard 순서를 확인한다.

<a id="residual-optimizer"></a>
## 6. Residual, manifold, optimizer와 전이: W09·W10·W15·W16

DeepSeek-V4 §2.2·§2.4, Motif 3 §2.3·§3.3이 직접 다루는 mHC의 Sinkhorn–Knopp projection은 모든 row/column 합이 1인 nonnegative map을 향하게 해 residual mixing의 안정성을 노린다. Muon의 Newton–Schulz는 momentum matrix를 semi-orthogonal update에 가깝게 만드는 다른 문제다. 둘 다 행렬을 다뤄도 mHC는 residual **경로**, Muon은 optimizer **update geometry**를 다룬다. Motif 3의 수정 mHC·QK-Clip·MoE stabilization과 Parallel Muon도 이 층위를 분리해 읽는다.

W15의 Motif 3 §1·§2.1–§2.3이 직접 연결한 [Differential Transformer v2](https://arxiv.org/abs/2410.05258v2) §2.1의 두 attention map 차분과 [Grouped Differential Attention v1](https://arxiv.org/abs/2510.06949v1) §2.2의 비대칭 signal/noise head grouping을 먼저 읽는다. GDLA는 이 분리와 MLA식 latent KV를 결합한다. **점검:** `λ=1`이고 두 map이 한 token에 똑같이 `0.6`을 둘 때 차분이 `0`임을 계산한다. 실제 모델의 학습된 `λ`와 map은 달라 취소가 보장되지는 않으며, 잡음 억제는 이 구조가 노리는 해석이지 문자 그대로의 보장은 아니라는 점을 말한다. KV 압축과 이 차분은 서로 다른 병목을 푼다.

Solar Open 2 §3.1이 직접 비교한 전이 방법은 [Sparse Upcycling v2](https://arxiv.org/abs/2212.05055v2) §3–§3.1의 dense checkpoint→expert 복제와, [Priming v1](https://arxiv.org/abs/2605.08301v1) §2.2·§3.2.2–§3.2.4의 attention→hybrid alignment를 대비한다. Solar Open 2의 selective transfer는 shape·의미가 유지된 module만 옮기는 partial warm start다. expert를 복제하는 upcycling이나 alignment를 포함하는 hybrid priming과 같은 절차라고 부르지 않는다.

**학습 점검.** 2×2 nonnegative matrix에 row/column normalization을 번갈아 해 보는 것과, 2D momentum matrix의 update를 Newton–Schulz로 직교화하는 것을 그림으로 분리한다. 이어서 “저장 형상, 논리적 module 경계, transfer 가능한 표현”이 각각 왜 다른 판단 기준인지 설명한다.

<a id="evaluation-systems"></a>
## 7. Agent 자료·환경과 기기 검색: W08·W11·W12·W14

**W08 — 도구로 풀 수 있는 과제 합성.** [DeepSeek-V3.2 §3.2.3·Table 1](https://arxiv.org/abs/2512.02556v1)에서 environment·toolset·task·solution·verifier를 함께 만드는 loop를 읽는다. solution 함수가 도구 호출 또는 논리 계산만 수행하며 DB에 직접 접근하지 못하도록 제한하고, verifier를 통과한 풀이와 non-zero pass@100으로 과제를 거르는 과정을 그린다. §4.3·Fig. 5에서 난도를 높이는 것과 새로운 domain으로 transfer되는 것은 별도 질문임을 확인한다.

**W11 — RL 이전의 agent SFT 합성.** [GLM-4.5 §3.1·Fig. 4](https://arxiv.org/abs/2508.06471v1)의 tool/framework 수집 → task 합성 → user-simulator trajectory → terminal-state judge/filter 네 단계를 읽는다. XML function-call template과 rejection sampling도 같은 절의 설계다. **점검:** 잘못된 escaping과 잘못된 도구 실행 결과가 어느 단계에서 각각 걸러지는지 표시한다.

**W12 — 실행 가능한 네 종류의 환경.** [GLM-5 §4.2.1–§4.2.5·§6.2·Appendix B.4.1](https://arxiv.org/abs/2602.15763v2)은 SWE·terminal·search·slide 환경의 생성과 검증을 구체적으로 설명한다. 직접 인용한 [SWE-bench Goes Live! v1 §3.3–§3.4](https://arxiv.org/abs/2505.23419v1)의 live issue 재현·RepoLaunch 경로와 [Harbor task tutorial](https://harborframework.com/docs/tasks/task-tutorial)의 task 구성·검증 범위를 읽는다. SWE의 F2P/P2P, terminal의 self-validation, search의 WKG·양방향 검증, slide의 static/runtime/perceptual reward를 각기 그린다. **점검:** 한 환경을 골라 action → observable state → verifier result를 쓰고, 검증기가 놓칠 수 있는 실패도 하나 적는다.

**W14 — 기기에서 재는 architecture search.** LFM2 §2.1이 직접 대조한 [STAR v1 §4–§4.1·§5.3–§5.4](https://arxiv.org/abs/2411.17800v1)를 읽는다. STAR는 quality/parameter/cache proxy를 대상으로 여러 목적을 함께 탐색하고, LFM2는 실제 기기 latency·memory를 반영하는 hardware-in-the-loop search를 다룬다.

**W14 점검.** 폭 3의 short convolution은 각 위치에서 이웃 세 token을 직접 섞는다고 써 본다. gate가 있더라도 이는 장거리 implicit convolution을 뜻하지 않는다. 후보 A와 B의 품질·latency·memory를 함께 놓고, 한 지표가 더 좋아도 다른 지표에서 열세면 Pareto 우위가 아닐 수 있음을 판단한다.

**점검:** benchmark 점수, pass@k, verifier 통과, device latency는 서로 같은 종류의 지표가 아니다. 어떤 지표가 모델의 어떤 단계에서 실패를 발견하는지 먼저 말한 뒤, 해당 보고서의 주장 범위를 판단한다.

## 원전 사용 원칙

- 판본 없는 링크 대신 위에 적은 arXiv revision을 우선 사용한다. 이후 개정이 있으면 절 제목과 수식·그림 번호를 다시 대조한다.
- Qwen3.8의 QSA·GDN·GR·n-gram·Muon은 원문 §2–§3이 1차 근거다. 이 문서의 작은 예제는 학습용 축약이며, 구현 수식·성능 수치는 원문으로 확인한다.
- LFM2는 Hyena를, KDA는 GDN을, QSA는 MLA를 각각 그대로 재명명한 것이 아니다. 연결은 전제 또는 대비일 수 있고, 곧 계보·동일 구현을 뜻하지 않는다.
- 배경 원전은 필요한 절만 읽는다. 주차별 보고서의 새 주장, 실험 조건, 한계는 각 주차 README의 고정 원문에서 확인한다.

새 배경 문서를 추가할 때는 [배경 문서 템플릿](../../templates/background.md)을 사용한다.
