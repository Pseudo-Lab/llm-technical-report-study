# 주차별 문서

기술 보고서 21편과 Qwen1.5 공식 출시 자료를 16주에 나누어 읽습니다. LLaMA 1·Llama 2는 각각 한 주로, Qwen1.5·Qwen2와 Qwen2.5·Qwen3는 두 모델씩 묶습니다.

[Background 읽기 지도](../background/README.md#week-map)는 본문 구성요소별 필요한 이유, 배경 원전과 읽을 범위, 해당 보고서의 변경점을 연결합니다. 전체 목록을 개인별 필수 정독 과제로 삼지 않으며, 앞 주차의 개념은 연결된 설명을 재사용합니다.

각 문서의 세 체크박스는 모임 후 함께 설명하거나 작은 예시로 확인할 Action Item입니다. 원문 위치와 주장이 성립하는 조건·한계를 학습 질문에서 확인하며, 실험 점수를 별도 필수 칸에 옮겨 적지는 않습니다.

| 주차 | 논문 | 이번 주에 잡을 개념 |
| --- | --- | --- |
| [W01](w01/README.md) | LLaMA 1 | 기존 Transformer 개선의 recipe · optimizer · compute/token budget |
| [W02](w02/README.md) | Llama 2 | LLaMA 1 recipe의 유지와 구조 변화 · preference reward model · iterative RLHF |
| [W03](w03/README.md) | Qwen1.5 → Qwen2 | 7B MHA→GQA · long-context 처리 · dense-to-MoE initialization · instruction pool과 scalable synthesis |
| [W04](w04/README.md) | Qwen2.5 → Qwen3 | Qwen2.5 합성·검증과 계승 경계 · 생각/비생각 모드 통합 · 생각 예산 · strong-to-weak distillation |
| [W05](w05/README.md) | DeepSeek-V2 | MLA의 KV 압축·위치 분리 · DeepSeekMoE의 expert 분할·공유와 통신 균형 |
| [W06](w06/README.md) | DeepSeek-V3 | 채택한 auxiliary-loss-free MoE 균형 · sequential MTP · FP8 mixed-precision 학습 |
| [W07](w07/README.md) | DeepSeek-R1 | R1-Zero의 pure RL · readable reasoning을 위한 다단계 post-training · 증류와 직접 RL의 조건부 비교 |
| [W08](w08/README.md) | MiMo → MiMo-V2-Flash | MiMo의 reasoning data·verifier-RL → Flash의 hybrid SWA/GA·deployment MTP·MOPD |
| [W09](w09/README.md) | DeepSeek-V3.2 | MLA 위 DSA indexer·top-k KV 선택 · scalable GRPO · thinking agent context·환경 합성 |
| [W10](w10/README.md) | DeepSeek-V4 | CSA의 block compression+DSA · HCA의 강한 dense compression · specialist→OPD 통합 |
| [W11](w11/README.md) | Qwen3.8-Next | GDN·전역 주의·QSA의 역할 분담, GR·n-gram memory, TP 환경의 Muon 적용 |
| [W12](w12/README.md) | GLM-4.5 | 전문 모델의 SFT·RL과 능력 통합, reasoning/agent RL의 국소 설계, agent SFT 합성 |
| [W13](w13/README.md) | GLM-5 | 비동기 agent RL의 안정화, token-정렬 최적화, 검증 가능한 장기 agent 환경 |
| [W14](w14/README.md) | VibeThinker-1.5B → VibeThinker-3B | SSP의 다양성 우선 증류 · 3B의 seed-to-trace curriculum · MGPO와 Long2Short |
| [W15](w15/README.md) | Motif 2 → Motif 3 | GDA→GDLA의 신호·잡음 분리와 latent KV · Parallel Muon · seven-teacher MOPD |
| [W16](w16/README.md) | Solar Open → Solar Open 2 | 저자원 언어 데이터·tokenizer·curriculum · NoPE 상태 · 선택적 weight transfer |

[주간 템플릿](../../templates/week.md) · [프로젝트 소개](../../README.md)
