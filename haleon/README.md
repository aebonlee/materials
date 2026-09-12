# haleon — 헤일리온코리아 Copilot 실무과정 실습 데이터

학습사이트 <https://haleon.dreamitbiz.com> 의 **실습 데이터** 메뉴에서 내려받는 파일들입니다.

**모두 실습을 위해 만들어 낸 가공 데이터입니다. 헤일리온코리아의 실제 데이터가 아닙니다.**

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `haleon-판매데이터-더미.xlsx` | 1교시 Excel 시연 1·2, 실습 | 월별판매 240행 / 목표대비실적 48행 (목표 빈 값 2건 포함) |
| `haleon-설문원시데이터-더미.xlsx` | 1교시 Excel 시연 3 | 설문응답 124행. 중복 사번 6건·부서 표기 흔들림·빈 값·날짜 형식 혼재를 일부러 남김 |
| `haleon-회의메모-더미.docx` | 2교시 Word 시연 1 | 정리 안 된 회의 메모. 담당·기한이 미정인 항목이 여럿 |
| `haleon-보고서샘플-더미.docx` | 2교시 Word 시연 2·실습 / 4교시 PowerPoint | 10개 절 보고서. **본문 수치는 판매데이터 xlsx 에서 실제로 집계한 값** |

## 다시 만들려면

`scripts/generate-dummy-data.py` 로 재생성합니다. 난수 시드를 `20260922` 로 고정해 두어
다시 돌려도 같은 값이 나옵니다.

보고서 docx 는 판매데이터 xlsx 를 읽어 수치를 채우므로 **xlsx 를 먼저 만들어야** 합니다.
이 순서를 지켜야 "요약본의 숫자가 원본과 맞는지 대조하는" 2교시 실습이 성립합니다.

```sh
pip3 install openpyxl python-docx
python3 scripts/generate-dummy-data.py      # 이 폴더에서 실행
```

## 링크 형태

사이트는 `src/config/site.ts` 의 `MATERIALS_BASE` 를 통해 아래 주소를 참조합니다.
한글 파일명이라 URL 인코딩이 필요합니다 (사이트 쪽에서 `encodeURIComponent` 로 처리).

```
https://raw.githubusercontent.com/aebonlee/materials/main/haleon/<파일명>
```
