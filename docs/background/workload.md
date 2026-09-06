# 16주 읽기 분량과 분담 — 개인 준비 3–4시간 기준

[주차 목록](../weeks/README.md) · [Background 지도](README.md)

LLaMA 1과 Llama 2는 각각 W01·W02에 읽는다. Qwen은 **W03: Qwen1.5 + Qwen2**, **W04: Qwen2.5 + Qwen3**로 나눈다. 전체는 **16주, 기술 보고서 21편과 Qwen1.5 공식 출시 자료**다.

Background 가이드는 본문을 이해하는 데 필요한 개념과 원전을 찾아 둔 지도다. 모든 참가자가 수록된 원전을 매주 전부 정독하는 과제가 아니다. 모두 주 자료의 흐름과 공통 핵심을 읽고, 소속 팀에서 맡은 한 갈래를 더 깊게 읽는다. 세 학습목표는 모임 후 함께 설명할 수 있어야 할 목표다.

## 개인 준비시간과 읽기 깊이

| 단계 | 시간 예산 | 준비 결과 |
| --- | ---: | --- |
| 주 자료 전체 흐름 확인 | 40분 | 배정된 두 자료가 있으면 둘 다 abstract·introduction·주요 그림·conclusion을 확인하고 각 절의 질문을 표시한다. |
| 공통 핵심 정독 | 90분 | 아래 공통 범위를 대상 본문과 연결된 배경 설명으로 읽는다. 작동 그림이나 작은 예시 하나를 따라간다. |
| 소속 팀 심화 | 60분 | 팀 안에서 고른 한 갈래와 필요한 원전의 지정 절을 읽는다. 공통으로 읽은 부분은 반복하지 않는다. |
| 발표·질문 메모 | 20분 | 원문 위치, 이해한 흐름, 미공개 범위와 질문을 공동 문서에 적는다. |

합계 **210분(3시간 30분)**은 준비 예산이다. 개인별 이해 속도를 측정한 예측은 아니다. 첫 1–2회 실제 준비시간을 확인하고 4시간을 넘으면 담당 원전·유도 범위를 줄인다. 별도 슬라이드 제작이나 실험 재현은 이 시간에 자동으로 추가하지 않는다.

## 16주 공통 읽기와 팀별 심화

PDF 쪽수는 **평가·참고문헌·부록을 포함한 고정 판본 전체**다. 모두 같은 깊이로 읽을 필수 쪽수와 다르며, 짧은 보고서도 새 수식이 많으면 부담이 크다. 본문의 정확한 절과 배경 원전 범위는 각 주차에 연결된 가이드에서 확인한다.

| 주차 | 주 자료와 PDF 전체 | 모두 읽을 공통 범위 | 팀 안에서 나눌 심화 갈래 |
| --- | --- | --- | --- |
| [W01](../weeks/w01/README.md) | LLaMA 1 **27쪽** | §2.1–§2.3의 tokenizer·block·optimizer와 §1의 학습/추론 예산 | BPE / norm·SwiGLU / RoPE / AdamW / 학습 예산 중 담당 개념 하나. Llama 2의 RLHF를 같은 주에 얹지 않는다. |
| [W02](../weeks/w02/README.md) | Llama 2 **77쪽** | §2.2의 전작 대비 변경과 §3.1–§3.2의 SFT→선호/RM→RLHF 흐름 | GQA·문맥 / 선호 데이터·ranking / rejection sampling·PPO / 안전성 중 한 갈래. LLaMA block 원전은 W01 설명을 재사용한다. |
| [W03](../weeks/w03/README.md) | Qwen1.5 공식 글 + Qwen2 **26쪽** | 같은 크기 checkpoint의 구조 차이, §4.1의 instruction 선별·확장·합성 흐름 | DCA+YaRN / MoE 초기화 / InsTag·evolution / profile 역할극·실행 검증 중 한 갈래. |
| [W04](../weeks/w04/README.md) | Qwen2.5 **26쪽** + Qwen3 **35쪽** = **61쪽** | Qwen2.5의 합성·검증과 Qwen3의 thinking/non-thinking 통합을 잇는 학습 흐름 | BBPE·QK-Norm·MoE / Math·Coder 합성 / system prompt·AutoIF / thinking budget·증류 중 한 갈래. 아래 공통 경로를 사용한다. |
| [W05](../weeks/w05/README.md) | DeepSeek-V2 **52쪽** | MLA 그림·KV cache 차원과 decoupled RoPE의 이유 | MLA 유도 / shared·routed expert / routing·통신 / 데이터·후학습 중 한 갈래. |
| [W06](../weeks/w06/README.md) | DeepSeek-V3 **53쪽** | loss-free balance와 MTP가 각각 바꾸는 학습 신호, FP8의 목적 | expert 균형 / MTP / FP8 수치 표현 / DualPipe·통신을 서로 나눠 맡는다. |
| [W07](../weeks/w07/README.md) | DeepSeek-R1 **86쪽** | R1-Zero→cold start→R1→학생 증류의 recipe와 GRPO 역할 | 목적식 / reward·데이터 / 긴 rollout 시스템 / 증류 비교 중 하나. 긴 사례·보충 평가는 담당 질문에 필요한 부분을 찾는다. |
| [W08](../weeks/w08/README.md) | MiMo **28쪽** + Flash **31쪽** = **59쪽** | MiMo의 MTP 활용과 Flash의 학생 trajectory 기반 MOPD | 두 보고서의 정독을 팀 안에서 나누고, architecture / data / rollout·teacher 신호 중 하나를 비교한다. |
| [W09](../weeks/w09/README.md) | DeepSeek-V3.2 **23쪽** | DSA 선택·학습 경로와 앞서 배운 MLA의 관계 | sparse 학습 / RL 안정화 / agent 환경 합성 중 하나. MLA·GRPO 원전 전체를 다시 읽지 않는다. |
| [W10](../weeks/w10/README.md) | DeepSeek-V4 **58쪽** | CSA/HCA가 압축하는 단위와 읽는 정보의 차이 | mHC / Muon / FP4·분산 실행 / OPD·teacher serving을 나눠 맡는다. |
| [W11](../weeks/w11/README.md) | Qwen3.8-Next **28쪽** | GDN state와 QSA retrieval의 역할·정보 보존 방식 | GR / n-gram / Muon·Polar Express / kernel·scaling 중 하나. 모든 수식 유도를 개인별 필수로 두지 않는다. |
| [W12](../weeks/w12/README.md) | GLM-4.5 **26쪽** | specialist 학습→expert-output SFT→통합의 흐름 | 데이터 합성 / reward / agent serialization / self-distillation 중 하나. |
| [W13](../weeks/w13/README.md) | GLM-5 **40쪽** | rollout→TITO→학습 신호, 비동기로 생기는 policy lag | MLA·DSA 변경 / deployment / SWE·search·slide 환경 / 중요도 보정 중 하나. |
| [W14](../weeks/w14/README.md) | VibeThinker 1.5B **13쪽** + 3B **14쪽** = **27쪽** | 두 모델의 SSP 계승과 데이터/RL 변경 | seed→trace / MGPO / Long2Short 중 하나. 두 기법을 모두 처음부터 유도하는 개인 과제로 만들지 않는다. |
| [W15](../weeks/w15/README.md) | Motif 2 **17쪽** + 3 **32쪽** = **49쪽** | GDA→GDLA와 domain별 teacher를 쓰는 목적 | optimizer·system / tokenizer·data / specialist·MOPD 중 하나. 전작·후속작의 깊은 읽기도 팀 안에서 나눈다. |
| [W16](../weeks/w16/README.md) | Solar Open **33쪽** + Open 2 **33쪽** = **66쪽** | 전작에서 옮긴 것·바꾼 것과 선택적 구조 전이의 이유 | 한국어·data / KDA·구조 전이 / SnapPO·후학습·agent 중 하나. 마지막 주에 앞선 모든 원전을 다시 요구하지 않는다. |

## Qwen 두 주차의 읽기 경계

[W03 가이드](w03.md)는 **Qwen1.5 → Qwen2**의 실제 변경과 Qwen2 본문의 배경을 맡는다. Qwen1.5는 [공식 출시 글](https://qwenlm.github.io/blog/qwen1.5/)과 고정 config로 읽으며 별도 기술 보고서 한 편으로 세지 않는다.

[W04 가이드](w04.md)는 **Qwen2.5 → Qwen3**를 맡는다. Qwen2.5의 합성 pipeline을 Qwen3가 새로 제안한 방법처럼 옮기지 않는다. Qwen2.5 본문과 선행 원전의 설명을 유지한 채 같은 주에서 Qwen3의 계승·변경과 비교한다.

| 주차 | 공통으로 읽을 본문 | 읽고 연결할 것 |
| --- | --- | --- |
| W03 | Qwen1.5 공식 글의 Introduction·Aligning with Human Preference·Long Context Understanding, [Qwen2 v4 §2.1–§2.2.1·§4.1.1–§4.1.2](https://arxiv.org/abs/2407.10671v4), 가이드의 7B config 비교 | MHA/GQA 변경과 `ontology/tag → instruction 선별·확장 → 응답 합성·검증`. PPO/DPO 채택의 공개 범위도 확인한다. |
| W04 | [Qwen2.5 v2 §2·§4.1(4)·§4.1(8)·§4.2](https://arxiv.org/abs/2412.15115v2), [Qwen3 v1 §2·§4의 단계 개요·§4.3](https://arxiv.org/abs/2505.09388v1) | BBPE/control token, checker/test와 SFT/DPO 재사용, system-prompt consistency를 Qwen3의 thinking/non-thinking 데이터·chat template와 연결한다. |

Qwen2.5 + Qwen3는 두 편 합계 61쪽으로 여전히 무겁다. W03에서 익힌 GQA·DCA·YaRN·역할극 기본 원전은 반복 정독하지 않는다. W04의 Math/Coder 원전, AutoIF 세부, Qwen3 thinking budget·on-policy distillation은 담당 갈래에 나누고 해당 내용을 모임에서 공유한다.

## 다섯 팀의 분담 원칙

- **Architecture & Pre-training:** 공통 구조를 확인한 뒤 구조 유도 또는 학습/실행 시스템 중 한 갈래를 맡는다.
- **Data & Synthesis:** 데이터 생성·선별·검증 중 이번 보고서의 변경을 설명하는 경로를 고른다. 모든 합성 원전을 한 사람이 요약하지 않는다.
- **Post-training:** SFT·증류·통합 단계에서 옮기는 데이터 또는 교사 신호 하나를 따라간다.
- **Alignment & RL:** reward·선호·정책 갱신 중 담당 경로를 읽고, 공통 배경으로 이미 배운 PPO/GRPO를 반복 숙제로 쌓지 않는다.
- **Background:** 이번 주 선택한 심화 갈래에서 막히는 선수 개념 하나를 설명한다. 전체 배경 목록은 필요할 때 찾아 쓴다.

팀의 두 사람이 전작/후속작 또는 서로 다른 갈래를 맡으면 공동 문서에서 합친다. 배정하지 못한 심화 항목은 선택 읽기로 남긴다. 다섯 팀의 발표는 모임에서 듣고 토론하며, 그 준비량을 개인별 추가 숙제로 다시 더하지 않는다.
