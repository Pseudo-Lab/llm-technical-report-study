# Qwen1.5 → Qwen2 → Qwen2.5: 구조·토크나이저·데이터

[W02 학습목표](../weeks/w02/README.md) · [배경 읽기 지도](README.md)

<a id="qwen-architecture"></a>
## Qwen1.5 → Qwen2 → Qwen2.5: 구조와 토크나이저

Qwen2 보고서가 Qwen1.5를 전작으로 직접 부르고, Qwen2.5가 Qwen2 dense decoder를 유지한다고 설명하므로, 자료 합성 목표에 앞서 **같은 크기의 공개 checkpoint를 대응시켜** 읽는다. Qwen1.5 비교에는 공식 출시 글과 고정 `config.json`을 쓴다. Qwen2·Qwen2.5는 각 기술 보고서의 본문을 먼저 읽는다. 아래 표의 `max_position_embeddings`는 공개 checkpoint의 configured maximum이며, 본문이 말하는 native pre-training 길이나 DCA+YaRN으로 확장한 처리 길이와 같은 말이 아니다.

| 대응 7B model | 고정 config에서 확인 | 보고서가 말하는 핵심 | 점검할 차이 |
| --- | --- | --- | --- |
| [Qwen1.5-7B](https://huggingface.co/Qwen/Qwen1.5-7B/blob/831096e3a59a0789a541415da25ef195ceb802fe/config.json) | 32 layers, Q/KV heads = 32/32, `rope_theta=1,000,000`, maximum=32,768, `vocab_size=151,936` | [공식 출시 글](https://qwenlm.github.io/blog/qwen1.5/)은 32K 지원과 PPO/DPO 정렬을 공개한다. | `Q=KV=32`는 MHA다. token 하나의 KV cache에 32개의 K/V head가 든다. |
| [Qwen2-7B](https://huggingface.co/Qwen/Qwen2-7B/blob/453ed1575b739b5b03ce3758b23befdb0967f40e/config.json) | 28 layers, Q/KV=28/4, `rope_theta=1,000,000`, configured maximum=131,072, `vocab_size=152,064` | [Qwen2 v4 §2.2.1](https://arxiv.org/abs/2407.10671v4)은 MHA 대신 GQA, DCA+YaRN을 명시한다. §3.2의 **학습** 길이는 4,096→32,768이고, DCA+YaRN으로 최대 131,072 처리 주장을 덧붙인다. | `28/4`는 7개의 query head가 한 KV head를 공유하는 GQA다. 따라서 대응 7B에서만 MHA→GQA와 KV cache 축소를 말한다. |
| [Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B/blob/d149729398750b98c0af14eb82c78cfe92750796/config.json) | 28 layers, Q/KV=28/4, `rope_theta=1,000,000`, configured maximum=131,072, `vocab_size=152,064` | [Qwen2.5 v2 §2](https://arxiv.org/abs/2412.15115v2)는 Qwen2 dense decoder/GQA/RoPE/RMSNorm pre-norm을 유지한다. §3.3의 학습 길이는 4,096→32,768이고, DCA+YaRN으로 다른 open model은 128K까지 처리한다고 쓴다. | 7B의 core decoder 수치는 Qwen2와 같다. Qwen2.5의 새 질문은 구조 교체가 아니라 자료 품질·합성·후학습, 그리고 BBPE control-token interface다. |

**범위 주의.** Qwen1.5-7B를 계열 전체로 일반화하지 않는다. [Qwen1.5-110B의 고정 config](https://huggingface.co/Qwen/Qwen1.5-110B/blob/16659038ecdcc771c1293cf47020fa7cc2750ee8/config.json)는 Q/KV=64/8이고, [Qwen1.5-MoE-A2.7B의 고정 config](https://huggingface.co/Qwen/Qwen1.5-MoE-A2.7B/blob/1a758c50ecb6350748b9ce0a99d2352fd9fc11c9/config.json)는 60 experts와 token당 top-4를 둔다. Qwen2 v4 §2.2.2도 Qwen2 MoE가 이 별도 MoE 계열을 닮았다고 쓴다. 그러므로 MoE는 Qwen1.5-7B의 구조 변경이 아니라 Qwen2-57B-A14B의 별도 분기로 읽는다.

### 이 표 다음에 읽을 원전

| Qwen 본문 근거 | 함께 읽을 자료와 범위 | 짚고 갈 개념 |
| --- | --- | --- |
| [Qwen2 v4 §2.2.1](https://arxiv.org/abs/2407.10671v4)의 GQA | [GQA v3 §2–§3](https://arxiv.org/abs/2305.13245v3) | MHA는 `Q=KV`, MQA는 `KV=1`, GQA는 그 중간이다. Qwen2-7B의 `Q/KV=28/4`로 직접 확인한다. |
| Qwen2 v4 §2.2.1·§3.2와 [Qwen2.5 v2 §3.3](https://arxiv.org/abs/2412.15115v2)의 DCA+YaRN | [DCA v2 §1·§3.1–§3.4](https://arxiv.org/abs/2402.17463v2), [YaRN v3 §2–§4](https://arxiv.org/abs/2309.00071v3) | DCA는 chunk 안/사이/인접 chunk의 attention 위치를 다루고, YaRN은 RoPE context extension 방법이다. 두 방법과 pre-training 32K를 한 숫자로 합치지 않는다. |
| Qwen2.5 v2 §2의 tokenizer 문단 | [Byte-Level Subwords v2 “Byte Level Text Representation”](https://arxiv.org/abs/1909.03341v2) → [BPE v1 §3.2](https://arxiv.org/abs/1508.07909v1) | BBPE는 Qwen2.5의 신규 구조가 아니라 Qwen tokenizer의 계승이다. regular 151,643개는 유지하고, control token을 3→22로 늘렸다. config `152,064`은 embedding padding도 포함하므로 보고서의 논리 vocabulary 수와 직접 빼지 않는다. |

### Dense checkpoint를 Qwen2 MoE로 옮기는 초기화

Qwen2 [v4 §2.2.2](https://arxiv.org/abs/2407.10671v4)의 Eq. (1)–(2)와 Table 1을 먼저 읽는다. 그 뒤 [DeepSeekMoE v1 §3.1–§3.2, Fig. 2](https://arxiv.org/abs/2401.06066v1)에서 fine-grained expert와 shared/routed expert를, [Sparse Upcycling v2 §3, §3.1, §4.2.2](https://arxiv.org/abs/2212.05055v2)에서 dense MLP 복제와 router 초기화 기반의 upcycling을 읽는다. Qwen2의 intermediate-dimension shuffle과 50% random re-initialization은 Qwen2 §2.2.2에만 귀속한다. W02에서는 이 초기화 절차를, W04에서는 V2의 expert 분할·공유와 통신 균형을 다룬다.

<a id="bbpe"></a>
**BBPE 작은 점검.** `UTF-8 bytes → 빈번한 인접 pair 병합 → 길이가 다른 byte token`을 따라간다. 한글처럼 한 문자가 여러 UTF-8 byte를 쓰면 token 하나가 문자 일부일 수도 있다. regular token의 merge vocabulary와 대화·도구 경계를 나타내는 control token은 역할이 다르다. Qwen2.5 본문은 BBPE 유형·token 수·control-token 확장을 공개하며, 새 merge 학습 자료나 새 regular vocabulary를 제안했다고 말하지 않는다.

<a id="instruction-pool"></a>
## Instruction pool의 선별과 확장

본문 [Qwen2 §4.1.1](https://arxiv.org/abs/2407.10671v4)의 흐름은 `open-set ontology 추출 → tag 부여·대표 instruction 선별 → 제약 추가로 evolution → 여러 응답의 사람 순위 → demonstration·preference 자료`다. Ontology extraction은 instruction evolution에 들어가기 전에 instruction pool을 이해하고 선별하는 단계다. §4.1.2의 automated synthesis는 다음 절에서 별도로 다룬다.

| Qwen 본문 근거 | 필요한 읽기와 범위 | 배경 개념·점검 |
| --- | --- | --- |
| [Qwen2 v4 §4.1.1](https://arxiv.org/abs/2407.10671v4)는 InsTag로 대규모 instruction corpus의 open-set fine-grained ontology를 추출한 뒤 수동으로 다듬고, tag가 붙은 instruction을 고른다고 설명한다. | [InsTag arXiv v2 §3.1–§3.4, §4–§4.1](https://arxiv.org/abs/2308.07074v2) | predefined label set 없이 intent tag를 붙인 뒤 lexical/semantic/association noise를 정리한다. diversity는 tag coverage, complexity는 instruction당 tag 수로 읽는다. Qwen은 여기에 semantic richness·intent completeness도 썼다고 말하지만, **selection score/threshold는 공개하지 않았다.** |
| 같은 [Qwen2 §4.1.1](https://arxiv.org/abs/2407.10671v4)은 representative instruction selection에 Dong et al.을 인용한다. | [SFT Data Composition arXiv v4 §2–§3](https://arxiv.org/abs/2310.05492v4) | data amount·domain composition·SFT strategy가 능력에 주는 영향을 읽고, specialised math/code를 먼저 익힌 뒤 general data와 일부 섞는 DMT를 확인한다. 이 원전에는 Qwen이 적은 네 selection criterion의 알고리즘이 없으므로 그 알고리즘을 Dong/InsTag에 귀속하지 않는다. |
| [Qwen2 v4 §4.1.1](https://arxiv.org/abs/2407.10671v4)은 기존 instruction에 constraint/requirement를 더하는 self-evolution을 설명하고 Zhao et al.을 인용한다. | [Tree-Instruct §3·Fig. 2](https://aclanthology.org/2024.lrec-main.1460/) | `instruction → semantic tree → meaningful noun/verb node 추가 → 새 instruction`은 Tree-Instruct의 구체적 방법이다. 작은 점검: `“cache를 설명하라”`에 `“두 labelled section으로 read-through/write-through를 비교하라”`를 더했을 때 원래 과제가 유지되는지 본다. **Qwen은 semantic tree/node count를 썼다고 보고하지 않았다.** |
| [Qwen2 v4 §4.1.1–§4.1.2](https://arxiv.org/abs/2407.10671v4)는 tag·selection·evolution·human ranking을 collaborative annotation으로, rejection/execution/role-play 등을 automated synthesis로 분리한다. | Qwen2 §4.1.1–§4.1.2 | ontology extraction은 evolution 안의 단계가 아니다. `ontology → tag/selection → constraint addition → human-ranked D/P`가 annotation 흐름이고, 수학·코드·role-play 합성은 별도 경로다. |

**작게 따라 읽기.** “JSON API 예제와 오류 처리를 설명하라”에 API 작성·JSON 형식·오류 처리 같은 intent tag를 붙여 본다. 새 tag가 전체 coverage를 늘리는지와 한 instruction에 intent가 몇 개 있는지는 다른 질문이다. 이후 “두 개의 이름 붙인 절로 정상·실패 응답을 비교하라”를 추가하면 instruction evolution이 된다. 이는 학습용 예이며 Qwen의 비공개 점수식이나 tag 목록을 재현한 것은 아니다.

<a id="task-synthesis"></a>
## 과제별 합성·검증 자료

아래 순서는 학습을 위해 편집한 것이며, 저자가 선수 학습 순서를 제시했다는 뜻은 아니다. 각 연결은 Qwen 보고서 **본문의 인용**에서 시작한다.

| Qwen 본문 근거 | 필요한 배경 원전과 범위 | 개념·작은 점검 |
| --- | --- | --- |
| [Qwen2 v4 §4.1.2 “Data Repurposing”](https://arxiv.org/abs/2407.10671v4)는 Wikipedia 같은 지식원에서 자세한 인물 profile을 얻고, LLM으로 instruction/response를 만들어 role-play demonstration을 구성한다. 이를 reading comprehension과 유사하다고 설명한다. | [Ditto v1 §3.2–§3.4](https://arxiv.org/abs/2401.12474v1) | profile → 역할에 맞는 질문/대조 질문 → profile을 조건으로 한 응답 → SFT의 흐름을 확인한다. 예를 들어 “Alice” profile 밖의 시대·작품을 묻는 대조 질문은 모른다고 말해야 한다. **범위:** Qwen2는 이 profile 기반 구성을 인용한다. Qwen2가 Ditto의 모든 데이터베이스·template를 그대로 채택했다고 쓰면 안 된다. |
| [Qwen2.5 v2 §4.1(8)](https://arxiv.org/abs/2412.15115v2)는 수백 개 일반 system prompt와 prompt–conversation consistency를 설명하고, Lu et al.을 인용한다. | Ditto v1 §3.1–§3.4 | role identity/profile와 그것을 따르는 대화의 구분을 먼저 잡는다. Qwen2.5의 주장은 **일반 system prompt 다양화와 일관성**이며, Ditto의 Wikipedia 인물 profile 생성 절차를 채택했다는 주장이 아니다. |
| [Qwen2 v4 §4.1.2](https://arxiv.org/abs/2407.10671v4)는 제약 instruction에 대한 Python verifier를, [Qwen2.5 v2 §4.1(4)·§4.2](https://arxiv.org/abs/2412.15115v2)는 instruction·verification code·unit test 생성/교차검증과 pass/fail의 SFT/DPO 재사용을 설명한다. | [AutoIF v1 §3.2–§3.4](https://arxiv.org/abs/2406.13542v1) | `“두 단어로 답하라” → checker/test 생성 → 실행 → 통과 응답 보존`처럼 실행 가능한 제약을 걸러 낸다. §3.2의 back-translation은 checker가 뜻하는 제약과 원 instruction의 의미가 맞는지 확인하는 단계다. **범위:** 이는 Qwen2.5 §4.1(1)의 긴 응답 query back-translation과 다른 용례다. |
| [Qwen2 v4 §5.2.1](https://arxiv.org/abs/2407.10671v4)과 [Qwen2.5 v2 §5.2.1](https://arxiv.org/abs/2412.15115v2)는 IFEval을 instruction-following 평가에 쓴다. Qwen2.5 §5.2는 언어 의존 사례를 빼서 다국어 평가도 만든다. | [IFEval v1 §2.1–§2.2](https://arxiv.org/abs/2311.07911v1); AutoIF §4.1의 evaluation | IFEval은 Qwen의 관점에서 **평가 benchmark**다. 원전은 평가 prompt를 few-shot 생성·수동 검수해 만들지만, AutoIF/Qwen의 checker·unit test로 생성한 SFT 자료와 같은 것이 아니다. 학습–평가 오염을 따로 점검해야 하는 이유를 한 문장으로 설명한다. |
| [Qwen2 v4 §4.1.2](https://arxiv.org/abs/2407.10671v4)는 수학의 정확한/부정확한 reasoning path로 demonstration·preference를 만들고, [Qwen2.5 v2 §4.1(2)·§3.1](https://arxiv.org/abs/2412.15115v2)는 Qwen2.5-Math CoT, rejection sampling, reward model, annotated answer를 사용한다. | [Qwen2.5-Math v1 §3.1.1–§3.2.1](https://arxiv.org/abs/2409.12122v1) | 같은 문제에서 여러 reasoning path를 낸 뒤, 정답이 있으면 final answer로, 합성 문제면 majority vote와 reward score로 top-k를 고른다. 따라서 “정답 검증”과 “RM의 과정 품질 판단”이 같은 신호가 아님을 구분한다. |
| [Qwen2.5 v2 §4.1(3)·§3.1·§4.1(9)](https://arxiv.org/abs/2412.15115v2)는 Qwen2.5-Coder, 언어별 agent, GitHub/Q&A 원천, sandbox의 static check/unit test, critic·multi-agent 응답 필터를 설명한다. | [Qwen2.5-Coder v1 §4.1](https://arxiv.org/abs/2409.12186v1) | code snippet → instruction/response → scorer, 또는 AST parse·unit test 실행으로 증거를 얻는다. 실행 결과와 critic agreement는 서로 다른 품질 신호이며, 보고서는 critic/다중 채점의 오류율을 제시하지 않는다. |
