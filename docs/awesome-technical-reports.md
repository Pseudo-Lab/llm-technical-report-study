# Awesome LLM Technical Reports

LLM의 구조·데이터·학습 기법을 이해하고 모델 간 변화를 비교하기 위한 논문 목록입니다. 정규 스터디 자료와 배경·비교 읽기를 함께 모았습니다.

arXiv 사전공개 논문과 저자·기관이 공개한 독립 논문 PDF를 수록합니다. 블로그·모델 카드·발표 자료만 공개된 항목은 포함하지 않습니다.

논문을 추가하려면 [복사용 Markdown 행](../templates/awesome-entry.md)을 사용해 PR을 올려주세요. 추천만 하고 싶다면 [Awesome 추가 제안 Issue](https://github.com/Pseudo-Lab/llm-technical-report-study/issues/new?template=technical-report.yml)만 작성해도 됩니다.

[배경·비교 읽기](#배경지식과-비교를-위한-technical-reports) · [학습 보충 논문](#모델-학습을-다룬-보충-논문) · [추가 비교 읽기](#추가-비교-읽기) · [정규 스터디와 후보](#technical-reports) · [참고한 공개 목록](#참고한-공개-목록) · [16주 스터디](weeks/README.md)

## 배경지식과 비교를 위한 Technical Reports

구조·데이터·학습 기법의 배경을 살펴볼 보고서입니다. 연결 주차는 비교해서 읽기 좋은 위치이며, 직접적인 기술 계승이나 필독 지정을 뜻하지 않습니다. 절 번호는 각 행에 표시한 arXiv 판본 기준입니다.

### 구조와 효율

| 보고서 | 먼저 볼 부분 | 확인할 질문 | 연결 주차 |
| --- | --- | --- | --- |
| [Mistral 7B](https://arxiv.org/abs/2310.06825) · v1 | [§2](https://arxiv.org/html/2310.06825v1) | GQA의 KV 공유와 sliding-window attention의 직접 주의 범위는 무엇이 다른가? 층을 거친 정보 전달 범위와 rolling-buffer cache 크기는 어떻게 구분하는가? | [W01](weeks/w01/README.md) · [W07](weeks/w07/README.md) · [W14](weeks/w14/README.md) |
| [Mixtral of Experts](https://arxiv.org/abs/2401.04088) · v1 | [§2–3](https://arxiv.org/html/2401.04088v1) | 토큰별 top-2 expert 선택에서 전체·활성 파라미터 수와 토큰당 연산량을 어떻게 구분하는가? | [W02](weeks/w02/README.md) · [W04](weeks/w04/README.md) · [W05](weeks/w05/README.md) |
| [Kimi Linear: An Expressive, Efficient Attention Architecture](https://arxiv.org/abs/2510.26692) · v2 | [§1, §6.3](https://arxiv.org/html/2510.26692v2) | KDA와 full attention을 섞었을 때 고정 상태·KV cache·장문 처리 비용의 관계는 어떻게 달라지는가? | [W10](weeks/w10/README.md) · [W16](weeks/w16/README.md) |

### 데이터와 사전학습

| 보고서 | 먼저 볼 부분 | 확인할 질문 | 연결 주차 |
| --- | --- | --- | --- |
| [Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone](https://arxiv.org/abs/2404.14219) · v4 | [§2](https://arxiv.org/html/2404.14219v4) | 소형 모델의 데이터 선별·합성 데이터·단계별 학습과 온디바이스 제약을 어떻게 함께 고려하는가? | [W13](weeks/w13/README.md) · [W14](weeks/w14/README.md) |
| [Phi-4 Technical Report](https://arxiv.org/abs/2412.08905) · v1 | [§2–4](https://arxiv.org/html/2412.08905v1) | 합성 데이터의 생성·선별·혼합과 사후학습은 각각 무엇을 바꾸는가? 구조 변경과 데이터 개선의 효과를 어떻게 구분하는가? | [W02](weeks/w02/README.md) · [W13](weeks/w13/README.md) |
| [OLMo: Accelerating the Science of Language Models](https://arxiv.org/abs/2402.00838) · v4 | [§2, §5](https://arxiv.org/html/2402.00838v4) | 가중치 외에 데이터·코드·체크포인트·로그를 공개하면 어떤 학습 가설을 검증할 수 있는가? | [W01](weeks/w01/README.md) · [W02](weeks/w02/README.md) |
| [2 OLMo 2 Furious](https://arxiv.org/abs/2501.00656) · v3 | [§3–4](https://arxiv.org/html/2501.00656v3) | 정규화와 학습 설정은 안정성에 어떤 영향을 주는가? Mid-training의 데이터 구성과 학습률 변화는 어떻게 비교하는가? | [W02](weeks/w02/README.md) · [W15](weeks/w15/README.md) |
| [DeepSeek LLM: Scaling Open-Source Language Models with Longtermism](https://arxiv.org/abs/2401.02954) · v1 | [§3](https://arxiv.org/html/2401.02954v1) | Batch size·learning rate의 경험식과 모델·데이터 배분은 어떻게 다른 문제인가? 데이터나 학습 조건이 달라져도 같은 scaling law를 쓸 수 있는가? | [W04](weeks/w04/README.md) · [W10](weeks/w10/README.md) |

### 사후학습과 RL

| 보고서 | 먼저 볼 부분 | 확인할 질문 | 연결 주차 |
| --- | --- | --- | --- |
| [Tülu 3: Pushing Frontiers in Open Language Model Post-Training](https://arxiv.org/abs/2411.15124) · v5 | [§4–7](https://arxiv.org/html/2411.15124v5) | SFT·DPO·RLVR은 어떤 데이터와 학습 신호를 쓰는가? 개발용 평가와 미지 평가를 왜 나누는가? | [W03](weeks/w03/README.md) · [W06](weeks/w06/README.md) |
| [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300) · v3 | [§2, §4.1](https://arxiv.org/html/2402.03300v3) | GRPO는 PPO의 critic을 무엇으로 대체하는가? 결과 단위 보상과 과정 단위 보상은 advantage 계산을 어떻게 바꾸는가? | [W04](weeks/w04/README.md) · [W06](weeks/w06/README.md) · [W07](weeks/w07/README.md) |
| [Nemotron-4 340B Technical Report](https://arxiv.org/abs/2406.11704) · v2 | [§3.1–3.3](https://arxiv.org/html/2406.11704v2) | 합성 prompt·응답 생성, 품질 필터링, 선호 순위화에서 생성 모델과 보상 모델은 각각 어떤 역할을 맡는가? | [W02](weeks/w02/README.md) · [W13](weeks/w13/README.md) |

## 모델 학습을 다룬 보충 논문

| 논문 | 먼저 볼 부분 | 확인할 질문 | 연결 주차 |
| --- | --- | --- | --- |
| [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982) · v1 | [§2.1–2.3, §3.2–3.3](https://arxiv.org/html/2502.16982v1) | Muon과 AdamW의 업데이트·스케일 조정은 어떻게 다른가? 분산 Muon의 연산·통신과 Moonlight 학습 실험은 무엇을 보여주는가? | [W09](weeks/w09/README.md) · [W10](weeks/w10/README.md) · [W15](weeks/w15/README.md) |

Moonlight를 실증 모델로 포함하는 옵티마이저 연구이므로 모델 보고서와 구분했습니다.

## 추가 비교 읽기

공개 GitHub 목록에서 찾고 논문 원문을 확인한 추가 후보입니다. 최신 보고서를 이해하는 데 도움이 되는 이전 세대도 포함하며, 이번 시즌의 필독 논문이나 주차 편성을 추가한 것은 아닙니다.

### 구조와 장문맥

| 논문 | 읽어볼 내용 |
| --- | --- |
| [Gemma: Open Models Based on Gemini Research and Technology](https://arxiv.org/abs/2403.08295) | 2B·7B 모델의 구조·학습·안전성 평가를 함께 읽고, 소형 범용 모델 보고서가 공개하는 설계 범위를 살펴봅니다. |
| [Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) | Local/global attention의 교차 배치, GQA, 2B·9B 모델의 증류를 통해 구조 선택과 교사 신호의 역할을 비교합니다. |
| [Jamba: A Hybrid Transformer-Mamba Language Model](https://arxiv.org/abs/2403.19887) | Transformer·Mamba·MoE를 결합한 구조와 ablation으로, attention-only 모델과 hybrid SSM 모델의 차이를 살펴봅니다. |
| [Jamba-1.5: Hybrid Transformer-Mamba Models at Scale](https://arxiv.org/abs/2408.12570) | Jamba의 규모 확장, 256K context와 ExpertsInt8을 함께 읽고 hybrid 구조의 장문맥 추론·메모리 제약을 살펴봅니다. |
| [MiniMax-01: Scaling Foundation Models with Lightning Attention](https://arxiv.org/abs/2501.08313) | 텍스트 모델의 Lightning Attention·MoE·병렬 학습을 중심으로, 장문맥 비용을 구조와 시스템에서 어떻게 줄이는지 살펴봅니다. |
| [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783) | Llama 1·2 이후의 데이터 구성, 규모 확장, 장문맥·사후학습을 비교할 때 필요한 부분을 골라 읽습니다. |

### 데이터와 학습 공개

| 논문 | 읽어볼 내용 |
| --- | --- |
| [Baichuan 2: Open Large-scale Language Models](https://arxiv.org/abs/2309.10305) | 데이터 clustering·중복 제거·샘플링과 PPO 정렬을 연결합니다. 처리 방식의 공개와 원시 학습 데이터 전체 공개는 구분합니다. |
| [BLOOM: A 176B-Parameter Open-Access Multilingual Language Model](https://arxiv.org/abs/2211.05100) | ROOTS의 다국어 데이터 구성, 거버넌스, 필터링·중복 제거·개인정보 처리를 통해 데이터 수집 단계의 선택을 살펴봅니다. |
| [OLMoE: Open Mixture-of-Experts Language Models](https://arxiv.org/abs/2409.02060v2) | 학습 데이터·코드·로그가 공개된 MoE의 routing, load balancing, expert specialization 실험을 읽습니다. 2024년 공개 모델을 다룬 보고서의 v2 기준입니다. |
| [OpenELM: An Efficient Language Model Family with Open Training and Inference Framework](https://arxiv.org/abs/2404.14619) | Layer-wise scaling과 공개 학습·추론 프레임워크, 로그·체크포인트를 통해 구조 효율과 재현 가능성을 함께 살펴봅니다. |
| [Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling](https://arxiv.org/abs/2304.01373) | 학습 데이터 순서를 통제한 모델군과 중간 체크포인트를 활용해 모델 크기·데이터 중복 제거·학습 진행에 따른 변화를 비교합니다. |
| [Yi: Open Foundation Models by 01.AI](https://arxiv.org/abs/2403.04652) | 영어·중국어 데이터의 필터링·중복 제거, 고품질 SFT와 장문맥 확장을 연결해 데이터 품질 중심의 개발 선택을 살펴봅니다. |

## Technical Reports

정규 스터디와 추가 읽기 후보를 모델명·보고서 제목 기준 알파벳순으로 정리했습니다. 이 표의 주차는 이번 시즌 편성입니다. arXiv 링크를 우선하고, 공식 PDF로 수집한 자료는 해당 링크를 유지합니다.

| 보고서 | 원문 | 스터디 |
| --- | --- | --- |
| A.X K1 Technical Report | [arXiv](https://arxiv.org/abs/2601.09200) | — |
| Apertus | [arXiv](https://arxiv.org/abs/2509.14233) | — |
| Apple Foundation Models 2025 | [arXiv](https://arxiv.org/abs/2507.13575) | — |
| Command A | [arXiv](https://arxiv.org/abs/2504.00698) | — |
| DeepSeek-R1 | [arXiv](https://arxiv.org/abs/2501.12948) | [W06](weeks/w06/README.md) |
| DeepSeek-V2 | [arXiv](https://arxiv.org/abs/2405.04434) | [W04](weeks/w04/README.md) |
| DeepSeek-V3 | [arXiv](https://arxiv.org/abs/2412.19437) | [W05](weeks/w05/README.md) |
| DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models | [arXiv](https://arxiv.org/abs/2512.02556) | [W08](weeks/w08/README.md) |
| DeepSeek-V4 | [arXiv](https://arxiv.org/abs/2606.19348) | [W09](weeks/w09/README.md) |
| DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning | [arXiv](https://arxiv.org/abs/2511.22570) | — |
| dots.llm1 Technical Report | [arXiv](https://arxiv.org/abs/2506.05767) | — |
| ERNIE 4.5 Technical Report | [공식 논문 PDF](https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf) | — |
| EuroLLM-22B: Technical Report | [arXiv](https://arxiv.org/abs/2602.05879) | — |
| EuroLLM-9B | [arXiv](https://arxiv.org/abs/2506.04079) | — |
| EXAONE 4.0: Unified Large Language Models Integrating Non-reasoning and Reasoning Modes | [arXiv](https://arxiv.org/abs/2507.11407) | — |
| EXAONE 4.5 Technical Report | [arXiv](https://arxiv.org/abs/2604.08644) | — |
| Falcon-H1 | [arXiv](https://arxiv.org/abs/2507.22448) | — |
| Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities | [arXiv](https://arxiv.org/abs/2507.06261) | — |
| Gemma 3 Technical Report | [arXiv](https://arxiv.org/abs/2503.19786) | — |
| GLM-4.5: Agentic, Reasoning, and Coding Foundation Models | [arXiv](https://arxiv.org/abs/2508.06471) | [W11](weeks/w11/README.md) |
| GLM-5: from Vibe Coding to Agentic Engineering | [arXiv](https://arxiv.org/abs/2602.15763) | [W12](weeks/w12/README.md) |
| Hermes 4 Technical Report | [arXiv](https://arxiv.org/abs/2508.18255) | — |
| Hunyuan-A13B Technical Report | [공식 논문 PDF](https://github.com/Tencent-Hunyuan/Hunyuan-A13B/blob/main/report/Hunyuan_A13B_Technical_Report.pdf) | — |
| Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent | [arXiv](https://arxiv.org/abs/2411.02265) | — |
| Hunyuan-TurboS: Advancing Large Language Models through Mamba-Transformer Synergy and Adaptive Chain-of-Thought | [arXiv](https://arxiv.org/abs/2505.15431) | — |
| Intern-S1 | [arXiv](https://arxiv.org/abs/2508.15763) | — |
| InternLM2 Technical Report | [arXiv](https://arxiv.org/abs/2403.17297) | — |
| K-EXAONE 2.0 Technical Report | [arXiv](https://arxiv.org/abs/2608.04505) | — |
| K-EXAONE Technical Report | [arXiv](https://arxiv.org/abs/2601.01739) | — |
| Kimi K2: Open Agentic Intelligence | [arXiv](https://arxiv.org/abs/2507.20534) | — |
| KORMo: Korean Open Reasoning Model for Everyone | [arXiv](https://arxiv.org/abs/2510.09426) | — |
| LFM2 Technical Report | [arXiv](https://arxiv.org/abs/2511.23404) | [W14](weeks/w14/README.md) |
| LLaMA 1 | [arXiv](https://arxiv.org/abs/2302.13971) | [W01](weeks/w01/README.md) |
| Llama 2 | [arXiv](https://arxiv.org/abs/2307.09288) | [W01](weeks/w01/README.md) |
| Magistral | [arXiv](https://arxiv.org/abs/2506.10910) | — |
| Mellum2 Technical Report | [arXiv](https://arxiv.org/abs/2605.31268) | — |
| MiMo | [arXiv](https://arxiv.org/abs/2505.07608) | [W07](weeks/w07/README.md) |
| MiMo-V2-Flash | [arXiv](https://arxiv.org/abs/2601.02780) | [W07](weeks/w07/README.md) |
| MiniCPM4 | [arXiv](https://arxiv.org/abs/2506.07900) | — |
| MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention | [arXiv](https://arxiv.org/abs/2506.13585) | — |
| MiniMax-M2 Series | [arXiv](https://arxiv.org/abs/2605.26494) | — |
| Ministral 3 | [arXiv](https://arxiv.org/abs/2601.08584) | — |
| Motif 2 12.7B technical report | [arXiv](https://arxiv.org/abs/2511.07464) | [W15](weeks/w15/README.md) |
| Motif 3: Technical Report | [arXiv](https://arxiv.org/abs/2608.09119) | [W15](weeks/w15/README.md) |
| NorwAI's Large Language Models: Technical Report | [arXiv](https://arxiv.org/abs/2601.03034) | — |
| NVIDIA Nemotron 3: Efficient and Open Intelligence | [arXiv](https://arxiv.org/abs/2512.20856) | — |
| OLMo 3 | [arXiv](https://arxiv.org/abs/2512.13961) | — |
| Pangu Ultra MoE: How to Train Your Big MoE on Ascend NPUs | [arXiv](https://arxiv.org/abs/2505.04519) | — |
| Phi-4-reasoning Technical Report | [arXiv](https://arxiv.org/abs/2504.21318) | — |
| PLaMo 2 | [arXiv](https://arxiv.org/abs/2509.04897) | — |
| Qwen Technical Report | [arXiv](https://arxiv.org/abs/2309.16609) | — |
| Qwen2 Technical Report | [arXiv](https://arxiv.org/abs/2407.10671) | [W02](weeks/w02/README.md) |
| Qwen2.5 Technical Report | [arXiv](https://arxiv.org/abs/2412.15115) | [W02](weeks/w02/README.md) |
| Qwen3 Technical Report | [arXiv](https://arxiv.org/abs/2505.09388) | [W03](weeks/w03/README.md) |
| Qwen3-Coder-Next Technical Report | [arXiv](https://arxiv.org/abs/2603.00729) | — |
| Qwen3.8-Next | [arXiv](https://arxiv.org/abs/2608.30320) | [W10](weeks/w10/README.md) |
| Ruyi2 Technical Report | [arXiv](https://arxiv.org/abs/2602.22543) | — |
| Salamandra | [arXiv](https://arxiv.org/abs/2502.08489) | — |
| Skywork-OR1 | [arXiv](https://arxiv.org/abs/2505.22312) | — |
| Skywork-R1V3 Technical Report | [arXiv](https://arxiv.org/abs/2507.06167) | — |
| SmolLM2 | [arXiv](https://arxiv.org/abs/2502.02737) | — |
| Solar Open 2 Technical Report | [arXiv](https://arxiv.org/abs/2607.20062) | [W16](weeks/w16/README.md) |
| Solar Open Technical Report | [arXiv](https://arxiv.org/abs/2601.07022) | [W16](weeks/w16/README.md) |
| Step 3.5 Flash: Open Frontier-Level Intelligence with 11B Active Parameters | [arXiv](https://arxiv.org/abs/2602.10604) | — |
| Technical Report of TeleChat2, TeleChat2.5 and T1 | [arXiv](https://arxiv.org/abs/2507.18013) | — |
| Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B | [arXiv](https://arxiv.org/abs/2511.06221) | [W13](weeks/w13/README.md) |
| VibeThinker-3B | [arXiv](https://arxiv.org/abs/2606.16140) | [W13](weeks/w13/README.md) |
| Yi-Lightning Technical Report | [arXiv](https://arxiv.org/abs/2412.01253) | — |

## 참고한 공개 목록

아래 목록은 후보를 찾는 데 사용했습니다. 논문 제목·링크·읽을 내용은 각 논문 원문에서 확인했습니다.

- [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM): Pythia·BLOOM·OLMoE.
- [ChenZiHong-Gavin/llm-tech-report](https://github.com/ChenZiHong-Gavin/llm-tech-report): Gemma·Gemma 2·Jamba·Jamba-1.5·MiniMax-01·Llama 3.
- [HqWu-HITCS/Awesome-Chinese-LLM](https://github.com/HqWu-HITCS/Awesome-Chinese-LLM): Baichuan 2·Yi·OpenELM.

배경·비교 읽기, 학습 보충 논문과 추가 비교 읽기는 2026-09-06에 초록과 관련 본문을 확인했습니다. ERNIE 4.5와 Hunyuan-A13B는 공식 PDF의 표지·초록·본문 구성을 확인했습니다. 기존 후보 전체를 다시 정독하거나 최신 판본까지 일괄 검증한 것은 아닙니다.
