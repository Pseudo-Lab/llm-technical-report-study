# W04 — Qwen2.5 → Qwen3

[주차 목록](../README.md) · [W04 Background](../../background/w04.md) · [주간 템플릿](../../../templates/week.md)

## 논문 정보

- 논문: Qwen2.5 → Qwen3
- arXiv: [Qwen2.5](https://arxiv.org/abs/2412.15115v2) → [Qwen3](https://arxiv.org/abs/2505.09388v1)
- 핵심 주제: Qwen2.5 합성·검증과 계승 경계 · 생각/비생각 모드 통합 · 생각 예산 · strong-to-weak distillation
- 모임 날짜: 추후 안내
- 주간 편집자: 추후 안내

## 학습목표

- [ ] Qwen2.5가 유지한 dense decoder·BBPE·long-context recipe와 Qwen3의 QKV-bias 제거·QK-Norm·shared-expert 제거·global-batch load balance를 구분해 설명할 수 있다.
  - **짚고 갈 개념:** GQA · KV cache · SwiGLU · RoPE · pre-RMSNorm · BBPE regular/control token · DCA · YaRN · QK-Norm · fine-grained/shared-routed expert · global-batch load-balancing loss
  - **함께 읽을 자료와 범위:** [Qwen2.5 handoff와 Qwen3 architecture](../../background/w04.md#qwen25-handoff)를 먼저 읽고, GQA §2.1–§2.2, DCA §1·§3.1–§3.4, YaRN §2–§4, DeepSeekMoE §3.1–§3.2·Fig.2, Demons in the Detail §2–§3·Eq. (3)–(6)·Algorithm 1을 따른다.
  - **원문에서 읽을 부분:** [Qwen2.5 §2·§3.3](https://arxiv.org/abs/2412.15115v2), [Qwen3 §2·§3.2, Table 1–2](https://arxiv.org/abs/2505.09388v1). Qwen3이 Qwen2.5의 22 control token이나 Turbo 1M recipe를 그대로 채택했다고 쓰지 않는다.
- [ ] Qwen2.5의 합성 응답 검증·system-prompt consistency와 Qwen3의 thinking/non-thinking 통합이 각각 어떤 데이터를 만들고 어떤 행동을 학습시키는지 설명할 수 있다.
  - **짚고 갈 개념:** Math/Coder 합성 · rejection sampling·reward model · sandbox 실행 · verification code·unit test · pass/fail의 SFT/DPO 재사용 · system-prompt consistency · self-rejection sampling · thinking/non-thinking SFT data · quality checklist · `/think`·`/no think` · 빈 생각 블록 · 다회차 전환 · 추론 토큰 예산 · 강제 중단 · 테스트 시 계산량 · 긴 문맥 검색 · 추론 간섭
  - **함께 읽을 자료와 범위:** [합성·검증 가이드](../../background/w04.md#qwen25-synthesis)에서 Qwen2.5 §3.1·§4.1(2)–(4)·(8)–(9)·§4.2를 확인한다. 담당 심화는 Math/Coder, AutoIF, Ditto 중 한 갈래로 나누며, 각각 [Qwen2.5-Math §3.1.1–§3.2.1](https://arxiv.org/abs/2409.12122v1)·[Qwen2.5-Coder §4.1](https://arxiv.org/abs/2409.12186v1), AutoIF §3.2–§3.4, Ditto §3.1–§3.4의 지정 범위를 읽는다. 이어 Qwen3 §4.1–§4.3의 reasoning data·non-thinking data·chat template을 비교한다. 생각 예산의 강제 중단·긴 문맥 한계는 담당 심화로 §4.7과 Appendix A.1.1을 읽는다.
  - **원문에서 읽을 부분:** [Qwen2.5 §3.1·§4.1(2)–(4)·(8)–(9)·§4.2](https://arxiv.org/abs/2412.15115v2), [Qwen3 §4.1–§4.3·§4.7, Table 9, Appendix A.1.1](https://arxiv.org/abs/2505.09388v1). Qwen2.5의 검증·system-prompt pipeline을 Qwen3가 그대로 채택했다고 가정하지 않고, 입력 문맥과 출력 생각 예산도 구분한다.
- [ ] Qwen3의 strong-to-weak distillation이 생각·비생각 두 모드의 교사 출력을 옮긴 뒤, 학생이 생성한 같은 모드 prefix에서 logit을 맞추는 이유를 직접 강화학습과 비교해 설명할 수 있다.
  - **짚고 갈 개념:** mode-conditioned teacher distribution · off-policy response distillation · on-policy logit alignment · KL divergence · exploration
  - **함께 읽을 자료와 범위:** [Qwen3 §4.5](https://arxiv.org/abs/2505.09388v1)에서 `/think`·`/no think` teacher response를 모두 쓰는 off-policy 단계와 학생 생성 sequence에서 logit을 맞추는 on-policy 단계를 읽고, §4.7 Table 21의 동일 checkpoint 직접 RL 비교로 이어 간다.
  - **원문에서 읽을 부분:** [Qwen3 §4.5·§4.7, Table 21](https://arxiv.org/abs/2505.09388v1). Qwen2.5의 offline DPO/online GRPO는 배경 recipe이지만 Qwen3 strong-to-weak two-phase loss와 같은 방법으로 합치지 않는다.

## 팀별 분석

### Architecture & Pre-training

### Data & Synthesis

### Post-training

### Alignment & RL

### Background

## 토론과 남은 질문

## 참고 자료

- [Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115v2)
- [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388v1)
