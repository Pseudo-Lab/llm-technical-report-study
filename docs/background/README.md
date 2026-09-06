# 16주 기술 보고서 배경 읽기 지도

**읽기 분담:** [개인 준비 3–4시간 기준의 공통 읽기와 팀별 심화](workload.md)를 따른다. 아래 전체 목록은 필요한 개념을 찾아 쓰는 지도이며, 개인별 전원 정독 과제가 아니다.

각 주차 상세 가이드는 **보고서 본문에서 설명·사용하거나 선행 연구로 인용한 구성요소**에서 출발한다. 구조·토크나이저·데이터·학습 방법·실행 시스템을 본문 순서에 따라 살펴보고, 필요한 개념의 작동 방식, 선행 원전과 읽을 범위, 해당 보고서의 변경점을 연결한다. 개인 준비에서는 공통 범위와 담당 갈래에 필요한 개념을 읽고, 세 학습목표는 모임 후 함께 설명할 수 있도록 정리한다.

**본문의 직접 연결**과 **인용 논문을 거치는 배경**을 구분한다. 후자는 `보고서 본문 → 인용 논문의 본문 → 필요한 개념`이라는 경로를 적는다. 참고문헌 목록에만 등장한 자료는 필수 경로로 넣지 않는다. 보고서가 이름을 사용하지만 원전을 인용하지 않은 개념은 원전 보충임을 표시한다. 보고서 자체가 정의한 방법은 해당 본문을 읽고, 세부 절차가 공개되지 않은 경우에는 공개 범위를 표시한다.

읽는 순서와 작은 숫자 예시는 이해를 돕기 위한 편집이다. 저자가 제시한 선수 학습 순서나 논문 속 실험 수치와 구분해 읽는다. 주 보고서는 각 주차 README의 고정 판본을, 배경 원전은 가이드에 적힌 판본과 범위를 기준으로 한다.

<a id="week-map"></a>
## 주차별 구성요소와 상세 가이드

아래에는 대표 구성요소를 적었다. 상세 가이드에서 각 항목의 **본문 근거 → 필요한 개념 → 원전 범위 → 작동 확인과 변경점**을 따라간다. 이미 배운 개념은 공통 경로로 복습하고, 각 주차에서는 그 보고서가 사용한 방식과 달라진 조건을 확인한다.

| 주차 | 상세 Background | 본문에서 함께 읽을 구성요소 |
| --- | --- | --- |
| [W01](../weeks/w01/README.md) | [LLaMA 1](w01.md#llama1-recipe) | BPE, pre-norm/RMSNorm, SwiGLU·PaLM, RoPE, AdamW, 학습·추론 예산 |
| [W02](../weeks/w02/README.md) | [Llama 2](w02.md#llama2-delta) | 유지된 recipe와 문맥·GQA 변경, 선호 ranking·RM·rejection sampling·PPO |
| [W03](../weeks/w03/README.md) | [Qwen1.5 → Qwen2](w03.md) | checkpoint 비교, GQA·DCA·YaRN·MoE 초기화, ontology·instruction 선별/확장, profile 역할극·실행 검증 |
| [W04](../weeks/w04/README.md) | [Qwen2.5 → Qwen3](w04.md) | BBPE·control token, Math/Coder·AutoIF·system prompt, QK-Norm·global-batch balance, mixture·mode fusion·생각 예산·증류 |
| [W05](../weeks/w05/README.md) | [DeepSeek-V2](w05.md) | MHA/MQA/GQA→MLA, decoupled RoPE, expert 분할·공유·routing, tokenizer, 분산 학습·recompute, YaRN, SFT·reward·RL |
| [W06](../weeks/w06/README.md) | [DeepSeek-V3](w06.md) | loss-free balance, MTP, packing·FIM·token boundary, PP/EP/DP·DualPipe, FP8 format/scale/누적/state, R1 trace·RM·GRPO |
| [W07](../weeks/w07/README.md) | [DeepSeek-R1](w07.md) | GRPO 목적식, verifier와 reward, cold start·rejection sampling, 일반/안전 정렬, 긴 rollout 시스템, teacher trace 증류 |
| [W08](../weeks/w08/README.md) | [MiMo → MiMo-V2-Flash](w08.md) | parser·중복 제거·태깅·mixture, MTP 학습/추론, 난도별 reward·resampling, rollout scheduling, SWA/GA·sink·MOPD |
| [W09](../weeks/w09/README.md) | [DeepSeek-V3.2](w09.md) | DSA indexer와 학습, KL·off-policy mask·routing/sampling 일치, thinking context, agent cold start·환경 합성, test-time context 관리 |
| [W10](../weeks/w10/README.md) | [DeepSeek-V4](w10.md) | MoE·MTP 계승, mHC, CSA/HCA, Muon·분산/cache 시스템, FIM·packing·문맥 curriculum, 안정화, GRM·OPD·FP4 학습 |
| [W11](../weeks/w11/README.md) | [Qwen3.8-Next](w11.md) | GDN·global attention·QSA, norm/gate, HC/mHC→GR, n-gram memory, FP8, 논리 행렬별 Muon·Polar Express·분산 실행·FlashQLA, scaling·stress test |
| [W12](../weeks/w12/README.md) | [GLM-4.5](w12.md) | MoE·attention·MTP, 데이터 처리와 mid-training, agent SFT 합성, specialist RL·reward·self-distillation·통합 |
| [W13](../weeks/w13/README.md) | [GLM-5](w13.md) | 기반 구조와 문맥 확장, 데이터/학습 시스템, 비동기 rollout·TITO·importance correction, 실행 환경과 verifier |
| [W14](../weeks/w14/README.md) | [VibeThinker 1.5B → 3B](w14.md) | base model, solution spectrum·Pass@K, seed→trace 생성·선별, MGPO·Long2Short, 통합·정렬·test-time 검증 |
| [W15](../weeks/w15/README.md) | [Motif 2 → Motif 3](w15.md) | width/depth 확장, GDA→GDLA, mHC·PolyNorm, MoE 안정화, Parallel Muon·문맥 병렬화, SuperBPE·mixture, SFT·specialist·MOPD |
| [W16](../weeks/w16/README.md) | [Solar Open → Solar Open 2](w16.md) | tokenizer·chat protocol, 데이터/curriculum·MoE, SFT 합성·SnapPO, KDA·NoPE·상태 추적, 선택적 전이, 장문맥·agent 후학습 |

## 본문 수식을 읽기 위한 네 가지 도구

1. **내적과 softmax — [W05 attention](w05.md).** `softmax(QKᵀ/√d)V`에서 내적은 관련성 점수, softmax는 이를 합이 1인 가중치로 바꾼다. 과거 token의 K/V를 남기는 이유와 head 공유 방식을 확인한다.
2. **외적·저랭크·상태 — [W05 MLA](w05.md), [W11 GDN](w11.md).** `c=W_Dh`는 저차원 표현을 만들고, `v kᵀ`는 key 방향에서 value를 읽을 수 있는 연관 행렬을 쓴다. 압축된 token별 cache와 계속 갱신되는 고정 크기 state의 차원을 각각 적는다.
3. **확률비·advantage·KL — [W07 GRPO](w07.md), [W13 비동기 RL](w13.md).** `π_θ(a|s)/π_old(a|s)`는 현재 정책과 수집 정책의 action 확률비다. 상대 reward로 만든 advantage와 비대칭 분포 차이인 KL이 목적식의 어느 위치에 들어가는지 구분한다.
4. **부동소수점 범위·정밀도 — [W06 FP8](w06.md).** exponent/mantissa, quantization scale, 누적 정밀도, optimizer state 정밀도를 나눠 읽는다. 같은 FP8 입력을 쓰더라도 scale을 공유하는 묶음과 누적 방식에 따라 오차가 달라진다.

## 공통 개념을 다시 만났을 때

<a id="qwen-data"></a>
<a id="data-context"></a>
### 토크나이저, 데이터와 학습 예산

[W01](w01.md)에서 BPE·compute/token budget을, [W03](w03.md)에서 instruction 선별·합성·검증을 배운다. [W04](w04.md)의 BBPE/control token·과제별 합성 확장·instance-level mixture, [W06](w06.md)의 packing·FIM·token-boundary 처리, [W15](w15.md)의 SuperBPE와 [W16](w16.md)의 언어별 pre-tokenization은 각 보고서가 바꾼 부분이다. tokenizer 학습 corpus, pre-training mixture, 후학습 instruction pool은 목적과 처리 단계가 다르다.

W03·W04의 선호 최적화를 읽을 때는 [Qwen2 §4.3](https://arxiv.org/abs/2407.10671v4)·[Qwen2.5 §4.2](https://arxiv.org/abs/2412.15115v2)가 사용하는 [DPO v3 §3–§4](https://arxiv.org/abs/2305.18290v3)를 함께 읽는다. 고정된 chosen/rejected 쌍과 reference-relative log probability의 역할을 확인하고, 뒤의 rollout 기반 RL과 구분한다.

<a id="qwen3-internal"></a>
Qwen3의 계승 블록, 데이터 단계, thinking/non-thinking과 증류는 [W04 상세 가이드](w04.md)에서 본문 순서대로 읽는다.

<a id="attention-cache"></a>
### Attention의 공유·압축·선택

[W02](w02.md#llama2-delta)·[W03](w03.md)의 MHA/MQA/GQA는 **head 사이 K/V 공유**, [W05](w05.md)의 MLA는 **token별 저장 표현의 저랭크 압축**, [W09](w09.md)의 DSA는 **읽을 token 선택**이다. [W10](w10.md)의 CSA/HCA는 sequence block의 내용을 압축하며, [W11](w11.md)의 QSA는 block을 점수화한 뒤 선택한 block을 token index로 펼친다. 어느 축을 바꾸는지 먼저 확인해야 cache 절감과 attention 연산 절감을 비교할 수 있다.

<a id="moe-precision"></a>
### MoE, MTP와 분산·정밀도

MoE의 expert 분할·공유와 routing balance는 [W05](w05.md), selection bias와 작은 sequence loss의 결합은 [W06](w06.md)에서 읽는다. [W04](w04.md)의 global-batch balance와 [W15](w15.md)의 expert 기능 다양성 점검은 balance를 측정하는 단위와 대상을 바꾼다. expert에 token이 균등하게 가는 것과 서로 다른 함수를 배우는 것은 별도 질문이다.

MTP의 보조 학습 목적은 [W06](w06.md), 학습용 module을 decoding draft에 쓰는 조건과 rollout 병목은 [W08](w08.md)에서 연결한다. FP8의 format·scale·누적·저장 구분과 PP/EP/DP·통신 overlap도 [W06](w06.md)에서 준비하고, [W10](w10.md)·[W15](w15.md)·[W16](w16.md)의 구체적 시스템 선택으로 돌아간다.

<a id="rl-distillation"></a>
### 선호·보상·정책·교사 신호

<a id="sft-ppo"></a>
**선호 ranking → RM → PPO:** [W02 Llama 2](w02.md#preference-ranking). chosen/rejected 자료, reward model, policy update를 구분한다. InstructGPT·PPO의 기본 읽기 범위는 이곳에 모아 둔다.

<a id="grpo"></a>
**Group-relative RL:** [W07 R1](w07.md). verifier가 만든 reward, group advantage, policy ratio/KL을 각각 읽는다.

<a id="mopd"></a>
**학생 prefix의 교사 신호와 outcome reward 결합:** [W08 Flash](w08.md). teacher trace SFT와 student-generated-prefix distillation의 차이를 확인한다.

<a id="expert-integration"></a>
**Specialist 학습과 통합:** [W12 GLM-4.5](w12.md). domain별 생성·검증·학습 뒤 단일 모델로 옮기는 단계를 따라간다.

<a id="async-rl"></a>
**Policy lag와 token metadata:** [W13 GLM-5](w13.md). 비동기 수집에서 probability·mask·token 경계를 보존하는 이유를 확인한다.

<a id="vibe-diversity"></a>
**해법 다양성·난도·길이:** [W14 VibeThinker](w14.md). Pass@K, seed/trace 선별, MGPO와 Long2Short가 서로 다른 선택 압력을 만드는지 확인한다.

<a id="solar-posttraining"></a>
**Generation/reward/train cache와 agent 통합:** [W16 Solar](w16.md). SnapPO와 Solar Open 2의 비동기 RL·MOPD를 단계와 신호별로 비교한다.

<a id="specialist-opd"></a>
OPD를 다시 만날 때에는 student가 생성한 prefix에서 무엇을 조회하는지부터 확인한다. [W10 V4](w10.md)는 full-vocabulary 신호와 teacher scheduling, [W15 Motif 3](w15.md)는 domain별 teacher와 sampled-token log probability, [W16 Solar Open 2](w16.md)는 다수 교사의 serving·재구성 비용을 함께 다룬다. 같은 용어가 나와도 목적식과 실행 방식은 각 본문에서 확인한다.

<a id="sparse-hybrid"></a>
### Local mixing, global retrieval와 고정 크기 memory

[W08](w08.md)의 SWA/GA, [W11](w11.md)의 GDN/global attention, [W16](w16.md)의 KDA/softmax는 local 정보와 장거리 정보를 결합하는 서로 다른 구성이다. local KV 직접 조회, fixed-size recurrent state, 전역 attention이 보관하고 다시 읽는 정보를 비교한다. GDN과 KDA를 동일 구현으로 취급하지 않는다.

<a id="qwen38-route"></a>
### Qwen3.8의 수식·차원·작은 계산

[W11 상세 가이드](w11.md)에 GDN 상태 갱신, QSA의 `16 token → 4 block → 2 block → 8 token + tail`, GR의 read/write 차원, n-gram lookup, 논리적 행렬별 Muon 적용을 모았다. Qwen3.8이 직접 인용한 DSA에서 V3.2의 MLA 구현을 더 이해하려면 `Qwen §2.1.2 → V3.2 §2.1 → V2 §2.1`로 이어진다. 이 간접 비교 경로가 QSA의 MLA 채택을 뜻하지는 않는다.

<a id="residual-optimizer"></a>
### Residual, optimizer와 전이에서 다루는 행렬

[W10](w10.md)의 mHC는 residual stream 사이의 전달, [W11](w11.md)의 GR은 branch/channel별 read와 write, [W15](w15.md)의 differential attention은 attention 출력의 차분을 다룬다. Muon은 parameter update 행렬을, [W16](w16.md)의 selective transfer는 이전 model과 대응 가능한 module을 다룬다. 행렬 연산이라는 공통점만으로 같은 안정화 기법이나 같은 전이 절차로 묶지 않는다.

<a id="evaluation-systems"></a>
### 합성 자료, 실행 환경과 검증

[W03](w03.md)는 instruction 선별·합성의 기본 경로를, [W04](w04.md)는 Qwen2.5의 수학·코드 합성 및 검증 확장을, [W09](w09.md)는 environment/tool/task/solution/verifier의 공동 합성을, [W12](w12.md)는 agent SFT trajectory 생성을, [W13](w13.md)는 실행 환경별 검증을 다룬다. 학습 자료의 verifier 통과와 평가 benchmark의 점수는 다른 증거다.

각 원전의 판본·범위는 주차별 상세 가이드에서 확인한다. 새 배경 문서를 추가할 때는 [배경 문서 템플릿](../../templates/background.md)을 참고하고, 필요한 개념의 본문 출발점과 원전 연결을 함께 기록한다.
