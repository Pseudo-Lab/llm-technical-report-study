# 논문 읽기·발표 스킬

| 순서 | 스킬 | 결과 |
| --- | --- | --- |
| Skills 1 · [#170](https://github.com/Pseudo-Lab/llm-technical-report-study/issues/170) | [extract-paper-parts](extract-paper-parts/SKILL.md) | 다섯 파트 개요·협업 제안·파트별 질문·개념별 페이지로 된 Markdown·HTML 읽기 지도 |
| Skills 2 · [#169](https://github.com/Pseudo-Lab/llm-technical-report-study/issues/169) | [create-paper-presentation](create-paper-presentation/SKILL.md) | 검토된 분석에서 구성한 HTML 발표자료와 화면 검토 피드백 |

추출 → 사람의 범위·근거 검토 → 발표자료 제작 순으로 사용한다. 검토 전 초안을 요청받으면 검토 상태를 명시한다. 두 스킬은 원래 파트와 목차, 원문 근거, 실험 조건과 불확실성을 유지하며 담당 범위나 공식 학습목표를 임의로 확정하지 않는다.

읽기 지도의 첫 페이지는 다섯 파트가 다루는 내용과 분량, 둘째 페이지는 함께 준비할 파트 조합이다. 이어서 파트마다 질문(RQ) 한 페이지와 개념당 한 페이지가 나오고, Background에는 이번 논문에서 새로 채울 빈 영역 표가 있다. 개념 링크는 해당 파트 탭과 페이지를 함께 연다. [읽기 화면 양식](extract-paper-parts/assets/reading-map-shell.html)을 브라우저에서 직접 열면 동작하는 미리보기를 볼 수 있다.

W01 LLaMA 1 발표자료를 만들며 받은 피드백은 [W01 회고](../docs/weeks/w01/notes/retrospective.md)에 있고, 두 스킬에 다음처럼 반영했다.

- 설계 선택은 대안 → 고른 것 → 원문 이유(없으면 미기술) → 외부 근거와 인용 여부로 쓴다.
- 원문이 넘어간 배경 주제는 담당 파트와 로드맵을 붙여 Background로 묶고, 발표자료에서는 부록과 본편의 “다음 주 깊게 다시 다룰 내용” 표시로 옮긴다.
- 수치 · 인용은 원문을 다시 열어 확인하고, 직접 돌릴 수 있는 것은 돌린 결과를 쓴다.
- 개념 장은 펼친 식 · 숫자 예시 · 되는 예와 예외로 만든다. 발표자료의 대본은 `N` 키로 띄운다.

## 실행

아래 명령은 저장소 루트에서 실행한다. Markdown 렌더러에는 Node.js와 `marked`, 발표자료 생성기에는 Python 3, 브라우저 검사기에는 Node.js와 Playwright 및 Chromium이 필요하다. 생성된 HTML은 별도 서버 없이 브라우저에서 열 수 있다.

```sh
# Skills 1: 작성한 Markdown으로 읽기 화면 생성
node skills/extract-paper-parts/scripts/render_reading_map.mjs input.md output.html
node skills/extract-paper-parts/scripts/test_render_reading_map.mjs

# Skills 2: 포함된 3장 예시로 발표자료 생성·검사
python3 skills/create-paper-presentation/scripts/build_deck.py \
  skills/create-paper-presentation/assets/example-slides.json /tmp/paper-example.html
node skills/create-paper-presentation/scripts/check_deck.cjs \
  /tmp/paper-example.html /tmp/paper-example-check
```

기본 모듈 탐색이 안 되면 `MARKED_MODULE` 또는 `PLAYWRIGHT_MODULE`에 설치된 모듈 경로를 지정한다. Playwright의 기본 브라우저가 없으면 `CHROME_PATH`에 Chrome 실행 파일 경로를 지정할 수 있다. 구체적인 입력 양식과 검토 절차는 각 `SKILL.md`를 따른다. 브라우저 검사는 화면·이동·로컬 링크를 확인하며 원문 사실성이나 사람의 이해도를 대신 검증하지 않는다.
