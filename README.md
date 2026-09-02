# materials — DreamIT Biz 강의자료 배포 리포

DreamIT Biz 학습사이트에서 내려받는 **강의자료 정본 보관소**입니다.
사이트 소스는 비공개로 두고, **수강생에게 나눠줄 자료만 이 리포에서 공개로 제공**합니다.

> ⚠️ **이 리포는 반드시 public으로 유지해야 합니다.**
> 각 학습사이트가 여기의 `raw.githubusercontent.com` 주소를 직접 참조합니다.
> private으로 바꾸면 토큰 없는 요청이 404가 되어 **전 사이트의 자료 링크가 한꺼번에 끊깁니다.**

## 왜 분리했나

자료가 사이트 빌드 산출물(`public/`)에 들어 있으면 **사이트를 통째로 긁을 때 자료 53.5MB가 같이 딸려갑니다.**
자료를 이 리포로 빼면 사이트를 복제해도 껍데기만 남습니다. (전역 CLAUDE.md §3.8 자산 보호 원칙 2층)

자료 자체는 수강생에게 줘야 하므로 공개입니다. 보호 대상은 **사이트 본체와 Supabase 데이터**이지 배포용 자료가 아닙니다.

## 링크 거는 법 — 저장용과 재생용은 주소가 다릅니다

**이 절을 건너뛰면 사이트에 빈 박스가 뜹니다.** 실제로 두 사이트(contents·seoultech)가
같은 함정에 빠져 몇 주간 강의안이 안 보였습니다.

| 용도 | 주소 | 왜 |
|---|---|---|
| **내려받기** | `https://raw.githubusercontent.com/aebonlee/materials/main/<사이트>/<파일명>` | raw는 `application/octet-stream`이라 클릭하면 저장됩니다 |
| **사이트 안에서 재생**(PDF) | `https://cdn.jsdelivr.net/gh/aebonlee/materials@main/<사이트>/<파일명>` | jsDelivr는 `application/pdf` + CORS라 인라인 렌더가 됩니다 |
| **사이트 안에서 재생**(PPTX) | `https://view.officeapps.live.com/op/embed.aspx?src=<raw 주소를 URL 인코딩>` | Office 온라인 뷰어. 원본이 공개 위치여야 합니다 |

한글 파일명은 URL 인코딩이 필요합니다.

### raw 주소를 미리보기에 쓰면 안 되는 이유 (실측)

```
content-type: application/octet-stream      ← application/pdf 가 아님
x-content-type-options: nosniff             ← 스니핑으로 PDF 판정도 막힘
content-security-policy: default-src 'none'; sandbox
access-control-allow-origin: *              ← fetch 는 됨
```

`<object type="application/pdf">`의 `type` 속성은 힌트일 뿐이고, 실제 판정은 응답
Content-Type이 합니다. `nosniff`까지 붙어 있어 브라우저는 이 응답을 문서로 렌더하지
않습니다. 더 나쁜 건, `<object>` 입장에서는 리소스를 "받기는 한" 것이라 **폴백 자식도
표시되지 않습니다** — 안내문 없는 빈 박스만 남습니다. 새 탭으로 열어도 재생 대신 저장됩니다.

`github.com/.../blob/...` 주소도 미리보기용이 아닙니다. GitHub이 `X-Frame-Options`로
iframe 임베드를 막기 때문에 새 탭으로 여는 용도로만 씁니다.

### 참조 구현

- `koreatech-db` — `src/data/bizdata/slides.ts`의 `toJsDelivr()` / `toEmbed()`.
  구글 슬라이드·PPTX·PDF를 형식별로 분기하는 가장 완성된 형태입니다.
- `build` — `src/data/decks.js`. jsDelivr를 베이스 주소로 고정한 단순한 형태.
- `contents` — `src/pages/DocView.jsx`. jsDelivr를 못 쓰는 상황(20MB 초과 등)에서
  raw를 CORS로 fetch해 `application/pdf` blob URL로 바꾸는 방식. blob은 같은 출처라
  `<a download>`의 파일명도 지켜집니다.

### 크기 제한

jsDelivr는 **파일당 20MB**를 넘으면 403입니다(실측). 원본이 크면 `koreatech-db`처럼
**경량 웹열람본**을 따로 만들어 재생용으로 쓰고, 원본은 내려받기 전용으로 둡니다
(만드는 법: [`koreatech-db/README.md`](koreatech-db/)).

### 교차 출처 `download` 속성

`<a href="https://raw.githubusercontent.com/..." download="한글이름.pdf">`의 파일명은
**무시됩니다.** `download`는 같은 출처에서만 동작합니다. 파일명을 지켜야 하면
`contents`처럼 blob으로 받거나, 애초에 리포의 파일명을 그대로 쓰세요.

## 목차

| 사이트 | 개수 | 자료 |
|---|---|---|
| [dsu](dsu/) | 16 | 동신대 교수자 AI 연수 — `cover`·`day1`~`day3` × 국문·영문 × PDF·Word |
| [koreatech](koreatech/) | 15 | 한국기술교육대 컴퓨팅사고 — 주차별 강의안 `week01`~`week12`, 과제 2종, 중간 이후 계획 |
| [kdt-ai](kdt-ai/) | 11 | Attention 논문, 실습 노트북 6종, 실습 데이터·requirements |
| [build](build/) | 6 | 건설기계 6일 과정 강의안 `DAY_1`~`DAY_6` — 사이트는 [`aebonlee/build`](https://github.com/aebonlee/build) |
| [koreatech-db](koreatech-db/) | 3 | 경영데이터베이스및실습 — 1장 원본 + 웹열람본, 폴더 안내 |
| [contents](contents/) | 3 | 휴넷 AI 홍보 실무 — 이미지 가이드, 강의노트, 마케팅 덱 |
| [nonghyupsaryo](nonghyupsaryo/) | 3 | 농협사료 실습 샘플 CSV 3종 |
| [chosun](chosun/) | 2 | 조선대 교원 교육 — Day1·Day2 |
| [seoultech](seoultech/) | 1 | 서울과기대 강의안 (2026-06-16) |
| [pytorch26](pytorch26/) | 1 | 프레임워크 비교 |
| [hufs](hufs/) | 1 | 한국외대 설치 가이드 (zip) |
| [data](data/) | 1 | 데이터 분석·시각화 강의안 |

총 **64개 파일 / 93MB** · 12개 폴더. (2026-09-02 실측)

### 여기 두지 않는 것 — 런타임 데이터

`koreatech/public/py/weather.csv`는 옮기지 않았습니다.
Pyodide 실습 코드가 `open('weather.csv')`로 **상대경로로 여는 런타임 데이터**라, 이 리포로 옮기면 실습이 깨집니다.
배포용 자료가 아니라 실습 환경의 일부로 봅니다. 같은 성격의 파일은 사이트에 남겨 둡니다.

### 중복 통합

`data/강의안_데이터분석_시각화.pptx`와 `unist/`의 같은 이름 파일이 md5 동일(`7a46258f…`)이라 **정본 하나로 합쳤습니다.**

> 2026-09-02 정정 — "unist 사이트도 `data/` 경로를 참조한다"고 적혀 있었으나, 실제
> `aebonlee/unist` 소스에는 이 리포를 가리키는 링크가 **한 건도 없습니다**. 파일이
> 같았을 뿐 참조 관계는 없습니다. unist에 자료 링크를 붙일 때 `data/` 정본을 쓰면 됩니다.

## 자료를 추가할 때

1. **사이트 리포 이름과 같은 폴더**에 넣습니다. 폴더가 없으면 만듭니다.
   폴더명이 사이트 이름과 다르면 나중에 어느 사이트 자료인지 추적이 안 됩니다.
   (예외 두 곳 — `hufs/`는 사이트가 `hufs26`, `build/`는 사이트가 `build`로 이름이 같습니다.)
2. **사이트 리포의 `public/`에는 두지 않습니다.** 넣으면 다시 번들에 섞여 분리한 의미가 없어집니다.
3. 위 목차 표를 갱신합니다. — 최근 두 번(`build`·`koreatech-db`)이 누락돼 표가 10개 파일만큼
   실제와 어긋나 있었습니다.
4. 파일명은 가급적 영문으로 — 한글이면 링크마다 URL 인코딩이 필요합니다.
5. 사이트에서 **미리보기로 띄울 자료**라면 위 "링크 거는 법"의 재생용 주소를 씁니다.
   raw 주소를 `<object>`·`<iframe>`에 그대로 물리면 빈 박스가 됩니다.

## 관련

- 전역 규칙: CLAUDE.md §3.8 자산 보호 원칙
- 전수 감사 기록: [`aebonlee/dreamit-1000`](https://github.com/aebonlee/dreamit-1000)
- 실시간 배포·수강생 작품 수집은 패들렛(`padlet.com/dreamitbiz`)에서 계속합니다. 이 리포는 **정본 보관**이 역할입니다.

---

*DreamIT Biz · 이애본*
