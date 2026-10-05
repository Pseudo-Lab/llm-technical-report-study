# 보충 세션

[주차 목록](README.md) · [16주 읽기 가이드](../background/workload.md)

정규 16주 사이에 계열의 이전 보고서와 후속 버전을 함께 보는 보충 세션입니다. MiMo·DeepSeek처럼 후속 보고서가 이어지고, 스터디를 진행하는 동안에도 새로운 자료가 나올 수 있어 보충 주제는 유연하게 조정합니다.

보충 세션은 필요할 때 **수요일 저녁**에 여는 것으로 예정하고 있습니다. 매주 고정하지 않으며, 구체적인 날짜와 시간은 별도로 안내합니다. **참여는 자유**이고 주간 문서 작성 의무는 없습니다.

- **선행**: 다음 정규 주차 전에 읽어 두면 좋은 자료입니다.
- **비교**: 방금 읽은 정규 보고서와 이전·후속 버전을 비교하는 자료입니다.
- 📄는 arXiv가 아닌 공식 PDF입니다.

## 보충 주제와 시점 초안

아래 자료와 시점은 초안입니다. 후속 보고서와 팀원 제안에 따라 조정합니다.

| 보충 | 여는 시점 | 자료 | 연결 주차 | 성격 |
| --- | --- | --- | --- | --- |
| [S1](#s1) | W02 다음 주 | Llama 3 Herd | W02 | 비교 |
| [S2](#s2) | W04 다음 주 | DeepSeekMoE | W05 | 선행 |
| [S3](#s3) | W05 다음 주 | DeepSeek LLM | W05 | 비교 |
| [S4](#s4) | W06 다음 주 | DeepSeekMath | W07 | 선행 |
| [S5](#s5) | W09 다음 주 | MiMo-V2.6 📄 | W08 | 비교 |
| [S6](#s6) | W11 다음 주 | ChatGLM | W12 | 선행 |

<a id="s1"></a>

## S1 — W02 다음 주: Llama 3 Herd

- 자료: [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783v3)
- W02 정규 모임에서는 Llama 2의 RLHF를 핵심 흐름(§3.2의 RM → rejection sampling → PPO) 위주로 발췌해 읽고, 세부 비교는 이 세션에서 Llama 3의 SFT·rejection sampling·DPO 후학습과 함께 다룹니다.

<a id="s2"></a>

## S2 — W04 다음 주: DeepSeekMoE

- 자료: [DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066v1)
- W05 DeepSeek-V2가 쓰는 MoE 구조의 출발점입니다.

<a id="s3"></a>

## S3 — W05 다음 주: DeepSeek LLM

- 자료: [DeepSeek LLM: Scaling Open-Source Language Models with Longtermism](https://arxiv.org/abs/2401.02954v1)
- DeepSeek 계열의 초기 설계를 요약하고, W05에서 읽은 V2의 MoE·MLA 설계와 비교합니다.

<a id="s4"></a>

## S4 — W06 다음 주: DeepSeekMath

- 자료: [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300v3)
- W07에서 R1의 GRPO를 읽기 전에, GRPO의 원전과 수학 데이터 선별 파이프라인을 먼저 확인합니다.

<a id="s5"></a>

## S5 — W09 다음 주: MiMo-V2.6

- 자료: 📄 [MiMo-V2.6 Technical Report](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL/blob/main/MiMo_V2_6_technical_report.pdf)
- W08에서 읽은 MiMo·MiMo-V2-Flash와 비교하며 후속 보고서의 변경점을 살펴봅니다.

<a id="s6"></a>

## S6 — W11 다음 주: ChatGLM

- 자료: [ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools](https://arxiv.org/abs/2406.12793v2)
- W12 GLM-4.5 이전의 GLM 계열 역사를 정리합니다.

<a id="self-study"></a>

## 자율 참고 (세션 없음)

보충 세션은 열지 않지만, 관심 있는 참여자가 자유롭게 참고할 자료입니다.

| 자료 | 연결 주차 |
| --- | --- |
| [Qwen Technical Report](https://arxiv.org/abs/2309.16609v1) | W03 |
| [Qwen2.5-Math Technical Report](https://arxiv.org/abs/2409.12122v1) | W04 |
