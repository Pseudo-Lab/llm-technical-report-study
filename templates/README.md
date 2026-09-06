# 문서 템플릿

- [Awesome 목록 한 줄 추가](awesome-entry.md): 복사용 Markdown 표 행과 논문 추가 방법입니다.
- [주간 문서](week.md): 논문 정보, 학습목표, 다섯 팀의 분석과 토론을 한 문서에 담습니다.
- [배경 문서](background.md): 주차별 본문 구성요소와 필요한 선행 개념·원전 범위를 정리합니다.

주간 문서는 `docs/weeks/wNN/README.md`, 배경 문서는 `docs/background/wNN.md`에 작성합니다. NN을 실제 주차 번호로 바꾸며, 템플릿의 상대 링크는 복사한 위치를 기준으로 합니다. 주차 문서와 배경 문서의 번호를 맞추고, 팀별 본문은 소제목 아래에 자유롭게 작성합니다.

[16주 문서 목록](../docs/weeks/README.md) · [배경 자료](../docs/background/README.md)

## Issue 템플릿

- [Awesome 목록에 논문 추가](https://github.com/Pseudo-Lab/llm-technical-report-study/issues/new?template=technical-report.yml): Awesome LLM Technical Reports에 수록할 논문 제안용입니다. 정규 커리큘럼이나 시즌 이후 읽기 선정과는 구분합니다.

주차별 작업은 일반 Issue에 주차와 작업 범위를 적습니다. 실제 학습목표·분석·토론은 주간 문서에 작성하며, 별도 Issue 양식은 두지 않습니다.

## Markdown을 수정해 PR 보내기

1. 관련 Issue를 만들거나 기존 Issue에서 작업 범위를 확인합니다. 논문을 추천만 하려면 Awesome 추가 제안 Issue까지만 작성해도 됩니다.
2. 직접 반영할 때는 `feature/<issue-number>` 브랜치에서 작업합니다. 저장소 쓰기 권한이 없다면 fork한 저장소에서 같은 규칙으로 브랜치를 만듭니다.
3. 해당 템플릿을 참고해 문서를 작성하고, Markdown 미리보기와 링크를 확인합니다. 이미 있는 주간 문서는 덮어쓰지 않고 필요한 부분만 수정합니다.
4. `[#<issue-number>]`를 포함한 메시지로 커밋하고, 이 저장소의 `main`을 대상으로 PR을 올립니다. [PR 템플릿](../.github/PULL_REQUEST_TEMPLATE.md)에 관련 Issue와 변경 내용을 간단히 적습니다.
