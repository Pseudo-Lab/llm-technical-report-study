# Phase 4 합격 기준 (v2 스킬을 만들기 전에 미리 정함 · 2026-10-31)

v2 스킬로 같은 범위를 다시 만든 덱(`baseline-v2`)을 아래 기준으로 판정한다. 측정 도구는 `.local/w03-arch-skill-compare/tools/deck_metrics.cjs`, `check_deck.cjs`, 비교 Workflow의 퀴즈 · 판정 · 수치 감사다. v1 · 팀원 덱의 측정값은 `.local/w03-arch-skill-compare/metrics/`에 있다.

## 반드시 (하나라도 못 미치면 불합격)
1. `check_deck.cjs` 1440×900 · 860×760 · 390×844 실패 0 (깨진 로컬 링크 포함), 페이지 JS 오류 0
2. 수치 감사: 틀린 수치 0, 계산 · 추정값인데 표시가 없는 것 0
3. 대본 있는 장 ≥ 95%, 출처 줄이 보이는 장 = 100%
4. 범위 주제 13개 모두 본편에 있음 (untied embedding · QKV bias · pre-norm/RMSNorm · SwiGLU 8/3 · 학습 설정(AdamW · cosine · 2,048) · Qwen Table 1 · 2 · MHA→GQA · KV cache · MoE Eq.(1)–(2) · fine-grained/shared expert · upcycling 초기화 · Qwen2 Table 1 · Qwen2 Table 2–5), 범위 밖(RoPE 상세 · DCA · YaRN · Qwen Table 3)은 본편에 없음
5. 유도 · 계산을 단계로 보여 줌: 8/3, token당 KV cache, Eq.(1)–(2) 수치 예시, upcycling 복제 수
6. 수식은 KaTeX로 렌더된 것(수식 이미지 crop만으로 대신하지 않음)
7. shell 회귀: W01 · W03 덱의 shell을 v2로 바꾼 사본의 전 장 픽셀 차이 0 또는 차이마다 이유 기록

## 개선 목표 (v1 대비, 팀원 덱 기준선)
8. 밀도: 장당 본문 + 시각 산문 글자 수 중앙값이 v1(680)보다 낮고 팀원(290)의 2배 이하 (≤ 580). p90 ≤ 800
9. 제목: 렌더된 제목 줄 수 3줄 이상인 장 비율이 v1보다 낮음
10. 퀴즈("장만 보기" 조건): v2 정답률 ≥ v1, 그리고 팀원 덱과의 차이를 절반 이상 줄임 (팀원이 v1보다 낮으면 v2 ≥ 팀원)
11. 주제별 쌍대 판정(v2 vs 팀원): 13개 주제 중 v2가 지거나 비기는 주제가 v1 vs 팀원보다 적음
12. 우리 강점 유지: 미기술 · 해석 · 계산 표시와 출처 표시가 v1 수준(장당 표시 수 중앙값이 v1의 50% 이상)

## 판정 방법
- 1 · 3 · 6 · 8 · 9 · 12: `deck_metrics.cjs` · `check_deck.cjs`
- 2 · 4 · 5 · 10 · 11: 비교 Workflow(퀴즈 · 판정 · 수치 감사 · 반박 검증)
- 7: shell 교체 사본 스크린샷 픽셀 비교
- LLM 실행 편차를 보기 위해 v1을 3개 섹션만 한 번 더 만들어 범위를 함께 적는다.
