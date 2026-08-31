# koreatech-db — 강의 슬라이드

경영데이터베이스및실습(CCT770) 학습사이트가 참조하는 강의 자료입니다.
사이트: <https://koreatech-db.dreamitbiz.com/bizdata>

## 파일 두 벌을 두는 이유

| 파일 | 용도 | 링크되는 곳 |
|---|---|---|
| `<제목>.pdf` | **원본 · 다운로드용** (전체 화질) | 사이트의 [⬇ 내려받기] |
| `<제목>_웹열람본.pdf` | **화면 재생용** (쪽당 1920×1080 이미지로 재구성) | 사이트의 슬라이드 화면 |

- 웹 재생은 jsDelivr CDN을 거치는데 **파일당 20MB 제한**이 있어(실측 403), 원본이 크면 그대로는 재생되지 않습니다.
- 원본 PDF를 Ghostscript로 압축하면 이 자료들은 **본문이 백지로 날아갑니다**(1~3쪽 실측). 압축 대신 **쪽을 이미지로 다시 그려** 열람본을 만듭니다.

## 열람본 만드는 법

```sh
pdftoppm -r 96 -jpeg -jpegopt quality=82 원본.pdf pg
python3 -c "
import glob; from PIL import Image
f=sorted(glob.glob('pg-*.jpg')); im=[Image.open(x).convert('RGB') for x in f]
im[0].save('원본_웹열람본.pdf', save_all=True, append_images=im[1:], resolution=96.0)"
```

만든 뒤 **아무 쪽이나 원본과 눈으로 비교**해 내용이 살아 있는지 확인합니다.
