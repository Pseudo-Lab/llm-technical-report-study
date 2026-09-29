# 보충 세션

[주차 목록](README.md) · [16주 읽기 가이드](../background/workload.md)

정규 16주 사이에 계열의 이전 보고서나 후속 버전을 함께 보는 보충 세션입니다. 정규 모임은 매주 토요일이므로 보충 세션은 **정규 모임 다음 주**에 열고, 구체적인 요일과 시간은 추후 안내합니다. 보충은 **1주에 1편**이며, 참여는 자유이고 주간 문서 작성 의무는 없습니다.

- **선행**: 다음 정규 주차 전에 읽어 두면 좋은 자료입니다.
- **비교**: 방금 읽은 정규 보고서와 이전·후속 버전을 비교하는 자료입니다.
- 📝는 논문이 없어 공식 블로그로 읽는 항목, 📄는 arXiv가 아닌 공식 PDF입니다.

## 일정 한눈에 보기

| 보충 | 여는 시점 | 자료 | 연결 주차 | 성격 |
| --- | --- | --- | --- | --- |
| [S1](#s1) | W02 다음 주 | Llama 3 Herd | W02 | 비교 |
| [S2](#s2) | W03 다음 주 | QwQ-32B 📝 | W04 | 선행 |
| [S3](#s3) | W04 다음 주 | DeepSeekMoE | W05 | 선행 · 구조팀 필독 |
| [S4](#s4) | W05 다음 주 | DeepSeek LLM | W05 | 비교 |
| [S5](#s5) | W06 다음 주 | DeepSeekMath | W07 | 선행 |
| [S6](#s6) | W08 다음 주 | MiMo-V2.5-Pro 📝 | W08 | 비교 |
| [S7](#s7) | W09 다음 주 | MiMo-V2.6 📄 | W08 | 비교 |
| [S8](#s8) | W10 다음 주 | Qwen3-Next 📝 | W11 | 선행 |
| [S9](#s9) | W11 다음 주 | ChatGLM | W12 | 선행 |
| [S10](#s10) | W12 다음 주 | GLM-4.7 📝 | W13 | 선행 |

<a id="s1"></a>

## S1 — W02 다음 주: Llama 3 Herd

- 자료: [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783v3)
- 읽을 범위: §3.1 Pre-Training Data, §4.1–§4.2 Post-training Modeling·Data
- 맡을 팀: Data & Synthesis · Post-training
- W02 정규 모임에서는 Llama 2의 RLHF를 핵심 흐름(§3.2의 RM → rejection sampling → PPO) 위주로 발췌해 읽고, 세부 비교는 이 세션에서 Llama 3의 SFT·rejection sampling·DPO 후학습과 함께 다룹니다.

<a id="s2"></a>

## S2 — W03 다음 주: QwQ-32B

- 자료: 📝 [QwQ-32B: Embracing the Power of Reinforcement Learning](https://qwenlm.github.io/blog/qwq-32b/)
- 읽을 범위: 블로그 전문
- 맡을 팀: Alignment & RL
- W04에서 Qwen3의 thinking/non-thinking 통합을 읽기 전에, Qwen 계열의 reasoning 특화 RL 모델을 먼저 확인합니다.

<a id="s3"></a>

## S3 — W04 다음 주: DeepSeekMoE

- 자료: [DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066v1)
- 읽을 범위: §3.1–§3.3 Fine-Grained Expert Segmentation·Shared Expert Isolation·Load Balance, §4.4–§4.5 Ablation·Expert Specialization
- 맡을 팀: **Architecture & Pre-training 필독**
- W05 DeepSeek-V2가 쓰는 MoE 구조의 출발점입니다.

<a id="s4"></a>

## S4 — W05 다음 주: DeepSeek LLM

- 자료: [DeepSeek LLM: Scaling Open-Source Language Models with Longtermism](https://arxiv.org/abs/2401.02954v1)
- 읽을 범위: §2.1 Data, §3 Scaling Laws, §4 Alignment
- 맡을 팀: Background
- DeepSeek 계열의 초기 설계를 요약하고, W05에서 읽은 V2의 MoE·MLA 설계와 비교합니다.

<a id="s5"></a>

## S5 — W06 다음 주: DeepSeekMath

- 자료: [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300v3)
- 읽을 범위: §2.1 Data Collection and Decontamination, §4.1 Group Relative Policy Optimization, §5.2 Insights of Reinforcement Learning
- 맡을 팀: Data & Synthesis · Alignment & RL
- W07에서 R1의 GRPO를 읽기 전에, GRPO의 원전과 수학 데이터 선별 파이프라인을 먼저 확인합니다.

<a id="s6"></a>

## S6 — W08 다음 주: MiMo-V2.5-Pro

- 자료: 📝 [Xiaomi MiMo-V2.5-Pro](https://mimo.xiaomi.com/mimo-v2-5-pro/)
- 읽을 범위: 학습 파이프라인과 MOPD 부분 중심
- 맡을 팀: Post-training
- 중간 단계인 📝 [MiMo-V2-Pro](https://mimo.xiaomi.com/mimo-v2-pro)는 따로 읽지 않고, V2-Flash → V2-Pro → V2.5-Pro 변경점 표로 정리합니다.

<a id="s7"></a>

## S7 — W09 다음 주: MiMo-V2.6

- 자료: 📄 [MiMo-V2.6 Technical Report](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL/blob/main/MiMo_V2_6_technical_report.pdf)
- 읽을 범위: RL 설계 부분 발췌
- 맡을 팀: Alignment & RL
- S6의 V2.5-Pro 교사 통합 방식과 비교합니다. MiMo 읽기 순서는 MiMo → V2-Flash(W08) → V2-Pro → V2.5-Pro(S6) → V2.6(S7)이며, 모든 단계가 앞 모델의 가중치를 이어받았다는 뜻은 아닙니다.

<a id="s8"></a>

## S8 — W10 다음 주: Qwen3-Next

- 자료: 📝 [Qwen3-Next: Towards Ultimate Training & Inference Efficiency](https://qwen.ai/blog?id=qwen3-next)
- 읽을 범위: hybrid attention, 고희소성 MoE, 학습 안정화, MTP 구성
- 맡을 팀: Architecture & Pre-training
- W11의 Qwen3.8-Next를 읽기 전에 비교 기준이 되는 hybrid 구조를 잡습니다.

<a id="s9"></a>

## S9 — W11 다음 주: ChatGLM

- 자료: [ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools](https://arxiv.org/abs/2406.12793v2)
- 읽을 범위: §1 Introduction(세대별 변화), §2 ChatGLM Techniques
- 맡을 팀: Background
- W12 GLM-4.5 이전의 GLM 계열 역사를 정리합니다.

<a id="s10"></a>

## S10 — W12 다음 주: GLM-4.7

- 자료: 📝 [GLM-4.7: Advancing the Coding Capability](https://z.ai/blog/glm-4.7)
- 읽을 범위: interleaved·preserved thinking과 턴별 thinking 제어, GLM-4.6 대비 변경점
- 맡을 팀: Post-training · Alignment & RL
- W12 GLM-4.5에서 W13 GLM-5로 넘어가기 전의 변경점을 봅니다. 블로그의 Tech Report 링크는 GLM-4.5 보고서로 연결되며, GLM-4.7만 다루는 별도 보고서는 없습니다.

<a id="self-study"></a>

## 자율 참고 (세션 없음)

보충 세션은 열지 않지만, 관심 있는 팀이 필요한 부분만 참고할 자료입니다.

| 자료 | 연결 주차 | 볼 부분 |
| --- | --- | --- |
| [Qwen Technical Report](https://arxiv.org/abs/2309.16609v1) | W03 | Qwen1.5 이전 계보 소개. §2 Pretraining, §3 Alignment |
| [Qwen2.5-Math Technical Report](https://arxiv.org/abs/2409.12122v1) | W04 | §2 Pre-training, §3.1–§3.3 SFT·Reward Model·RL |
| 📝 [DeepSeek-V3.1 Release](https://api-docs.deepseek.com/news/news250821/) | W09 | Think/Non-Think 하이브리드 추론과 agent 후학습 |
| 📝 [Qwen3.5: Towards Native Multimodal Agents](https://qwen.ai/blog?id=qwen3.5) | W11 | Qwen3-Next 이후 hybrid 구조. vision 부분은 제외 |
