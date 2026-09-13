# daegu — 대구광역시 공무원 AI 실무 교육

사이트: <https://daegu.dreamitbiz.com/automation>

| 파일 | 내용 |
|---|---|
| `daegu-automation-lecture_v1.1_20260913.pptx` | 행정업무 자동화 1~8교시 강의교안 97장 (강사 정동엽) |

## 내려받기 주소

```
https://raw.githubusercontent.com/aebonlee/materials/main/daegu/daegu-automation-lecture_v1.1_20260913.pptx
```

## 판본

| 판 | 날짜 | 바뀐 것 |
|---|---|---|
| **v1.1** | 2026-09-13 | 사이트 컬러 통합(다크블루 `#0B2447` · 로열블루 `#2E52E0`)에 맞춰 다시 구움. 화면 그림의 주석(점선·번호)이 주황 → 남색. 본문의 "주황 번호" 표현도 "남색 번호"로 정정. |
| v1.0 | 2026-09-09 | 최초. 옛 하늘 청색 팔레트 + 주황 주석. **v1.1 로 교체되어 더 이상 제공하지 않는다.** |

## 다시 구우려면

이 교안은 손으로 만든 파일이 아니라 **생성기 산출물**이다. 내용을 고칠 일이 있으면
PPTX 를 직접 고치지 말고 사이트 저장소(`aebonlee/daegu`)의 `ppt/` 에서 다시 굽는다.

```bash
cd ppt
npm install
npm install --no-save sharp   # 크롬이 없는 환경에서만 (맥 등)
node render-svg.mjs           # SVG → PNG. 그림이 바뀔 때만
node build.mjs                # PPTX → ppt/dist/
```

판본(`v1.1`·`20260913`)은 `ppt/theme.mjs` 의 `VERSION`·`STAMP` **한 곳에서** 정한다.
파일명과 표지 꼬리말이 같은 값을 받아 쓴다.

구운 뒤에는 **이 리포에 커밋·푸시해야** 내려받기 주소에 반영된다 (전역 CLAUDE.md §3.8 2층).
