<h1 align="center">LLM Technical Report Study</h1>

> 최신 LLM 기술보고서를 함께 읽고, 모델의 구조와 학습 방법을 이해하는 스터디입니다.

<div align="center">
  <a href="https://pseudo-lab.com"><img src="https://img.shields.io/badge/PseudoLab-S13-3776AB" alt="PseudoLab 13th season" /></a>
  <a href="https://discord.gg/EPurkHVtp2"><img src="https://img.shields.io/badge/Discord-BF40BF" alt="Discord Community" /></a>
  <a href="https://github.com/Pseudo-Lab/llm-technical-report-study/stargazers"><img src="https://img.shields.io/github/stars/Pseudo-Lab/llm-technical-report-study" alt="Stars" /></a>
  <a href="https://github.com/Pseudo-Lab/llm-technical-report-study/network/members"><img src="https://img.shields.io/github/forks/Pseudo-Lab/llm-technical-report-study" alt="Forks" /></a>
  <a href="https://github.com/Pseudo-Lab/llm-technical-report-study/pulls"><img src="https://img.shields.io/github/issues-pr/Pseudo-Lab/llm-technical-report-study" alt="Pull requests" /></a>
  <a href="https://github.com/Pseudo-Lab/llm-technical-report-study/issues"><img src="https://img.shields.io/github/issues/Pseudo-Lab/llm-technical-report-study" alt="Issues" /></a>
</div>

## ✨ 스터디 소개

최신 LLM 기술보고서를 읽으며 필요한 배경지식을 함께 공부하고, 각 모델의 특징과 기술의 변화를 토론합니다. 학습한 내용은 GitHub 공동 문서에 기록합니다.

## 🎯 학습 목표

- 핵심 기법이 해결하려는 문제와 이전 방법과의 차이를 설명합니다.
- 모델의 구조·데이터·학습 과정을 이해하고, 논문의 주요 주장과 근거를 검토합니다.
- 학습한 내용과 토론을 공동 문서로 정리하고 공유합니다.
- 16주차의 13기가 끝나면, LLM Technical Report에 대한 Survey Paper를 같이 작성해보려고합니다. 

## 🧭 Study Overview

| 항목 | 내용 |
| --- | --- |
| 운영 기간 | 16주, 방학 제외 |
| 세부 일정 | 첫 정기 모임일, 종료일과 방학 배치는 추후 안내 |
| 정기 모임 | 매주 토요일 오전 9시 |
| 진행 시간 | 주차별 논문과 토론 내용에 따라 1시간 30분~3시간 |
| 진행 방식 | 가짜연구소 Discord 온라인 모임, 세부 채널 추후 안내 |
| 정규 참여자 | 약 10명 |
| 분석팀 | 5개 팀, 팀당 2명 기본 |
| 주간 기록 | 주차별 Markdown 문서 1개 |
| 시즌 이후 (선택) | LLM 계보·기술 변화와 모델 비교 자료 정리 |

### 모집 및 가짜연구소 공통 일정

| 일정 | 날짜 |
| --- | --- |
| 모집 시작 | 2026년 9월 18일 |
| 모집 마감 | 2026년 9월 28일 |
| 선정 발표 | 2026년 10월 1일 |
| 가짜연구소 공식 활동 시작 | 2026년 10월 4일 |
| 가짜연구소 공식 활동 종료 | 2027년 1월 9일 |
| Grand Gathering | 2027년 1월 9일 |

위 날짜는 가짜연구소 공통 일정이며, 우리 스터디의 16주 운영 일정은 별도로 안내합니다.

## 🙋 Who Can Join?

### 정규 참여자

Transformer와 LLM의 기본적인 학습 과정을 이해하고, 기술보고서를 함께 읽고 토론하고 싶은 분을 모집합니다. 관심 있는 분석팀을 선택해 발표·토론과 공동 문서 정리에 참여합니다.

### 청강자

정규 참여자 외에도 청강자는 Discord 공개 세션의 발표와 토론에 참여할 수 있습니다. 청강자에게는 주간 문서 작성 의무가 없습니다.

❗ 참여 링크: [가짜연구소 Discord](https://discord.gg/EPurkHVtp2)<br>
❗ 첫 정기 모임과 세부 채널: 추후 안내

<a id="weekly-roadmap"></a>

## 🗺️ 16주 커리큘럼과 핵심 주제

16주 동안 읽을 보고서와 핵심 주제입니다. 자세한 학습목표와 읽기 자료는 [주차별 문서](docs/weeks/README.md)에서 확인할 수 있습니다.

| 주차 | Technical Report | 핵심 주제 |
| --- | --- | --- |
| W01 | [LLaMA 1](https://arxiv.org/abs/2302.13971v1) | 기존 Transformer 개선의 recipe · optimizer · compute/token budget |
| W02 | [Llama 2](https://arxiv.org/abs/2307.09288v2) | LLaMA 1 recipe의 유지와 구조 변화 · preference reward model · iterative RLHF |
| W03 | [Qwen1.5 공식 자료](https://qwenlm.github.io/blog/qwen1.5/) → [Qwen2](https://arxiv.org/abs/2407.10671v4) | 7B MHA→GQA · long-context 처리 · dense-to-MoE initialization · instruction pool과 scalable synthesis |
| W04 | [Qwen2.5](https://arxiv.org/abs/2412.15115v2) → [Qwen3](https://arxiv.org/abs/2505.09388v1) | Qwen2.5 합성·검증과 계승 경계 · 생각/비생각 모드 통합 · 생각 예산 · strong-to-weak distillation |
| W05 | [DeepSeek-V2](https://arxiv.org/abs/2405.04434v5) | MLA의 KV 압축·위치 분리 · DeepSeekMoE의 expert 분할·공유와 통신 균형 |
| W06 | [DeepSeek-V3](https://arxiv.org/abs/2412.19437v2) | 채택한 auxiliary-loss-free MoE 균형 · sequential MTP · FP8 mixed-precision 학습 |
| W07 | [DeepSeek-R1](https://arxiv.org/abs/2501.12948v2) | R1-Zero의 pure RL · readable reasoning을 위한 다단계 post-training · 증류와 직접 RL의 조건부 비교 |
| W08 | [MiMo](https://arxiv.org/abs/2505.07608v2) → [MiMo-V2-Flash](https://arxiv.org/abs/2601.02780v2) | MiMo의 reasoning data·verifier-RL → Flash의 hybrid SWA/GA·deployment MTP·MOPD |
| W09 | [DeepSeek-V3.2](https://arxiv.org/abs/2512.02556v1) | MLA 위 DSA indexer·top-k KV 선택 · scalable GRPO · thinking agent context·환경 합성 |
| W10 | [DeepSeek-V4](https://arxiv.org/abs/2606.19348v1) | CSA의 block compression+DSA · HCA의 강한 dense compression · specialist→OPD 통합 |
| W11 | [Qwen3.8-Next](https://arxiv.org/abs/2608.30320v1) | GDN·전역 주의·QSA의 역할 분담, GR·n-gram memory, TP 환경의 Muon 적용 |
| W12 | [GLM-4.5](https://arxiv.org/abs/2508.06471v1) | 전문 모델의 SFT·RL과 능력 통합, reasoning/agent RL의 국소 설계, agent SFT 합성 |
| W13 | [GLM-5](https://arxiv.org/abs/2602.15763v2) | 비동기 agent RL의 안정화, token-정렬 최적화, 검증 가능한 장기 agent 환경 |
| W14 | [VibeThinker-1.5B](https://arxiv.org/abs/2511.06221v1) → [VibeThinker-3B](https://arxiv.org/abs/2606.16140v1) | SSP의 다양성 우선 증류 · 3B의 seed-to-trace curriculum · MGPO와 Long2Short |
| W15 | [Motif 2](https://arxiv.org/abs/2511.07464v1) → [Motif 3](https://arxiv.org/abs/2608.09119v1) | GDA→GDLA의 신호·잡음 분리와 latent KV · Parallel Muon · seven-teacher MOPD |
| W16 | [Solar Open](https://arxiv.org/abs/2601.07022v1) → [Solar Open 2](https://arxiv.org/abs/2607.20062v2) | 저자원 언어 데이터·tokenizer·curriculum · NoPE 상태 · 선택적 weight transfer |

## 👥 분석팀

관심 분야에 따라 다섯 팀으로 나누어 참여합니다. 팀당 2명을 기본으로 하며, 모집 상황에 따라 조정할 수 있습니다.

| 팀 | 함께 살펴볼 내용 |
| --- | --- |
| Architecture & Pre-training | 모델 구조와 사전학습 |
| Data & Synthesis | 데이터 구성·선별·합성 |
| Post-training | 지도 미세조정과 증류 |
| Alignment & RL | 선호 학습·보상·강화학습 |
| Background | 배경 개념과 선행 연구 |

## 🧑‍🤝‍🧑 진행 방식

1. **모임 전:** 해당 주차의 보고서를 읽고, 팀에서 맡은 관점의 내용과 질문을 정리합니다. 필요한 배경 개념은 [읽기 가이드](docs/background/workload.md)를 참고합니다.
2. **모임:** 팀별 발표와 토론으로 모델의 특징과 주요 설계 선택을 함께 살펴봅니다.
3. **모임 후:** 배운 내용과 남은 질문을 주차별 공동 문서에 기록합니다. 주간 편집자는 돌아가며 맡습니다.

## 🔭 결과물과 시즌 이후 활동

매주 학습 내용과 토론을 정리한 공동 문서를 만듭니다. 시즌 이후에는 희망자들이 모델 계보와 기술 변화를 연결한 서베이형 문서로 발전시킬 수 있습니다.

구성 방향은 [LLM Internals: 언어 모델의 계보와 알고리즘 진화](https://speakerdeck.com/inureyes/llm-internals-language-model-genealogy-and-algorithm-evolution-2023-2026)를 참고합니다.

## 📚 참고 자료

- [주차별 논문과 공동 문서](docs/weeks/README.md): 16주 학습목표와 읽기 범위를 확인하고, 매주 분석과 토론 내용을 채워갑니다.
- [읽기 가이드](docs/background/workload.md): 주차별 읽기 범위와 팀별 분담을 참고합니다.
- [주차별 Background 읽기 지도](docs/background/README.md#week-map): 본문 구성요소별 필요한 개념, 배경 원전과 읽을 범위, 이전 방법과의 차이를 확인합니다.
- [Awesome LLM Technical Reports](docs/awesome-technical-reports.md): 함께 읽는 보고서와 추가 읽기 후보를 모은 목록입니다.

## 🤝 GitHub Collaboration

- 논문 제안, 문서 개선과 논의가 필요한 내용은 Issue로 관리합니다.
- 주차별 문서는 각각의 Issue에서 작업합니다.
- 작업 브랜치는 `feature/<issue-number>` 형식을 사용합니다.
- 커밋 메시지에는 `[#<issue-number>]`를 포함합니다.
- 변경 사항은 Pull Request에서 검토한 뒤 기본 브랜치에 반영합니다.

처음 기여한다면 [Markdown 템플릿과 PR 작성 방법](templates/README.md#markdown을-수정해-pr-보내기)을 참고해주세요. 논문은 복사용 표 행으로 추가하고, 주간 문서는 준비된 소제목 아래에 자유롭게 작성하면 됩니다.

## Acknowledgement 🙏

이 프로젝트는 가짜연구소 Open Academy로 진행됩니다. 참여자들이 나눈 질문, 설명과 기록이 더 많은 사람의 학습으로 이어지기를 바랍니다.

LLM Technical Report Study is developed as part of Pseudo-Lab's Open Research Initiative. Special thanks to all participants and the open-source research community.

## About Pseudo Lab 👋🏼

[Pseudo-Lab](https://pseudo-lab.com/)은 머신러닝과 AI 기술의 발전을 위해 함께 연구하고 지식을 공유하는 비영리 커뮤니티입니다. Sharing, Motivation, Collaborative Joy를 핵심 가치로 오픈소스 프로젝트와 연구 활동을 이어가고 있습니다.

## Contributors 😃

<a href="https://github.com/Pseudo-Lab/llm-technical-report-study/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Pseudo-Lab/llm-technical-report-study" alt="Contributors" />
</a>

## License 🗞

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
