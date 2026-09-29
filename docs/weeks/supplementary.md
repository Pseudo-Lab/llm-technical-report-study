# 보충 세션

[주차 목록](README.md) · [16주 읽기 가이드](../background/workload.md)

정규 16주 사이에 계열의 이전 보고서나 후속 버전을 함께 보는 보충 세션입니다. 정규 모임은 매주 토요일이므로 보충 세션은 **정규 모임 다음 주**에 열고, 구체적인 요일과 시간은 추후 안내합니다. 참여는 자유이며, 주간 문서 작성 의무는 없습니다.

- **선행**: 다음 정규 주차 전에 읽어 두면 좋은 자료입니다. 해당 주차 **직전 주**의 보충 세션에 둡니다.
- **비교**: 방금 읽은 정규 보고서와 이전·후속 버전을 비교하는 자료입니다. 해당 주차 **직후 주**의 보충 세션에 둡니다.
- 📝는 논문이 없어 공식 블로그·발표 자료로 읽는 항목, 📄는 arXiv가 아닌 공식 PDF입니다.

## 일정 한눈에 보기

| 보충 | 여는 시점 | 연결 주차 | 자료 | 성격 |
| --- | --- | --- | --- | --- |
| [S1](#s1) | W02 다음 주 | W02 · W03 | Llama 3 Herd · Qwen Technical Report | 비교 · 선행 |
| [S2](#s2) | W04 다음 주 | W04 · W05 | Qwen2.5-Math · QwQ-32B 📝 · DeepSeek LLM · DeepSeekMoE | 비교 · 선행 |
| [S3](#s3) | W06 다음 주 | W07 | DeepSeekMath | 선행 |
| [S4](#s4) | W08 다음 주 | W08 · W09 | MiMo-V2-Pro 📝 · MiMo-V2.5-Pro 📝 · MiMo-V2.6 📄 · DeepSeek-V3.1 📝 | 비교 · 선행 |
| [S5](#s5) | W10 다음 주 | W11 | Qwen3-Next 📝 · Qwen3.5 📝 | 선행 |
| [S6](#s6) | W11 다음 주 | W12 | ChatGLM | 선행 |
| [S7](#s7) | W12 다음 주 | W12 → W13 | GLM-4.7 📝 | 비교 |
| [S8](#s8) | W14 다음 주 | W15 | Motif 2.6B | 선행 |

<a id="s1"></a>

## S1 — W02 다음 주: Llama 3 비교와 Qwen 계열 소개

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783v3) | W02 비교 | §3.1 Pre-Training Data, §4.1–§4.2 Post-training Modeling·Data | Data & Synthesis · Post-training |
| [Qwen Technical Report](https://arxiv.org/abs/2309.16609v1) | W03 선행 | §2 Pretraining 개요, §3 Alignment, §4–§5 Code-Qwen·Math-Qwen 분화는 훑어보기 | Background |

- W02 정규 모임에서는 Llama 2의 RLHF를 핵심 흐름(§3.2의 RM → rejection sampling → PPO) 위주로 발췌해 읽고, 세부 비교는 이 세션에서 Llama 3의 SFT·rejection sampling·DPO 후학습과 함께 다룹니다.
- Qwen 1은 W03의 Qwen1.5 → Qwen2 이전 계보를 소개하는 자료로 짧게 요약합니다.

<a id="s2"></a>

## S2 — W04 다음 주: Qwen 특화 모델 비교와 DeepSeek 선행

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| [Qwen2.5-Math Technical Report](https://arxiv.org/abs/2409.12122v1) | W04 비교 | §2 Pre-training, §3.1–§3.3 SFT·Reward Model·RL | Data & Synthesis · Post-training |
| 📝 [QwQ-32B: Embracing the Power of Reinforcement Learning](https://qwenlm.github.io/blog/qwq-32b/) | W04 비교 | 블로그 전문. Qwen3의 thinking/non-thinking 통합과 RL 구성 비교 | Alignment & RL |
| [DeepSeek LLM](https://arxiv.org/abs/2401.02954v1) | W05 선행 (요약) | §2.1 Data, §3 Scaling Laws, §4 Alignment | Background |
| [DeepSeekMoE](https://arxiv.org/abs/2401.06066v1) | W05 선행 (**구조팀 필독**) | §3.1–§3.3 Fine-Grained Expert Segmentation·Shared Expert Isolation·Load Balance, §4.4–§4.5 Ablation·Expert Specialization | Architecture & Pre-training |

<a id="s3"></a>

## S3 — W06 다음 주: DeepSeekMath 선행

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| [DeepSeekMath](https://arxiv.org/abs/2402.03300v3) | W07 선행 | §2.1 Data Collection and Decontamination, §4.1 Group Relative Policy Optimization, §5.2 Insights of Reinforcement Learning | Data & Synthesis · Alignment & RL |

- W07에서 R1의 GRPO를 읽기 전에, GRPO의 원전과 수학 데이터 선별 파이프라인을 먼저 확인합니다.

<a id="s4"></a>

## S4 — W08 다음 주: MiMo 후속 버전과 DeepSeek-V3.1

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| 📝 [Xiaomi MiMo-V2-Pro](https://mimo.xiaomi.com/mimo-v2-pro) | W08 비교 | V2-Flash 대비 변경점을 표로 정리 | 전체 |
| 📝 [Xiaomi MiMo-V2.5-Pro](https://mimo.xiaomi.com/mimo-v2-5-pro/) | W08 비교 | V2-Pro 대비 변경점을 표로 정리. 학습 파이프라인과 MOPD 부분 중심 | Post-training |
| 📄 [MiMo-V2.6 Technical Report](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL/blob/main/MiMo_V2_6_technical_report.pdf) | W08 비교 | RL 설계 부분 발췌. V2.5-Pro의 교사 통합 방식과 비교 | Alignment & RL |
| 📝 [DeepSeek-V3.1 Release](https://api-docs.deepseek.com/news/news250821/) | W09 선행 | Think/Non-Think 하이브리드 추론과 agent 후학습 변경점 | Post-training |

- MiMo 읽기 순서는 MiMo → V2-Flash(W08 정규) → V2-Pro → V2.5-Pro → V2.6입니다. 읽기 순서일 뿐, 모든 단계가 앞 모델의 가중치를 이어받았다는 뜻은 아닙니다.

<a id="s5"></a>

## S5 — W10 다음 주: Qwen3-Next와 Qwen3.5

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| 📝 [Qwen3-Next: Towards Ultimate Training & Inference Efficiency](https://qwen.ai/blog?id=qwen3-next) | W11 선행 | hybrid attention, 고희소성 MoE, 학습 안정화, MTP 구성 | Architecture & Pre-training |
| 📝 [Qwen3.5: Towards Native Multimodal Agents](https://qwen.ai/blog?id=qwen3.5) | W11 선행 | Qwen3-Next 이후 hybrid 구조와 학습 부분. 텍스트 스터디이므로 vision 부분은 제외 | Architecture & Pre-training |

- W11의 Qwen3.8-Next를 읽기 전에 Qwen3-Next → Qwen3.5로 이어지는 hybrid 구조를 비교 기준으로 잡습니다.

<a id="s6"></a>

## S6 — W11 다음 주: ChatGLM 계열 선행

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| [ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools](https://arxiv.org/abs/2406.12793v2) | W12 선행 | §1 Introduction(세대별 변화), §2 ChatGLM Techniques | Background |

<a id="s7"></a>

## S7 — W12 다음 주: GLM-4.7

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| 📝 [GLM-4.7: Advancing the Coding Capability](https://z.ai/blog/glm-4.7) | W12 → W13 비교 | interleaved·preserved thinking과 턴별 thinking 제어. GLM-4.6 대비 변경점 | Post-training · Alignment & RL |

- GLM-4.7 블로그의 Tech Report 링크는 W12에서 읽은 GLM-4.5 보고서로 연결됩니다. GLM-4.7만 다루는 별도 보고서는 없습니다.

<a id="s8"></a>

## S8 — W14 다음 주: Motif 2.6B 선행

| 자료 | 성격 | 읽을 범위 | 맡을 팀 |
| --- | --- | --- | --- |
| [Motif 2.6B Technical Report](https://arxiv.org/abs/2508.09148v1) | W15 선행 | §2 Architecture(2.1 Design Decision, 2.2 Tokenizer), §3 Pre-training | Architecture & Pre-training |

- 2.6B는 버전이 아니라 파라미터 규모입니다. W15의 Motif 2 → Motif 3 이전 구조 탐색을 확인합니다.
