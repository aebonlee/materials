# -*- coding: utf-8 -*-
"""
DAY 3 실습 데이터 생성기 (data_day3_audio.zip · data_day3_docs.zip 대체본)

원본 실습 데이터를 받지 못한 상황에서, 교재 PART 03 의 코드가 그대로 돌아가도록
같은 폴더·같은 파일 이름의 데이터를 만든다.

  audio/normal/*.wav          정상 펌프 100개
  audio/abnormal/*.wav        이상 펌프 100개 (2~4kHz 대역이 약 +6dB 높다)
  audio/call1_engine_start.wav / .txt   상담 녹음과 정답 전사
  checklists/daily_001~005.png          일일점검표 사진 5장
  checklists/checklists_ground_truth.json  채점용 정답지
  drawings/drawing_R-DWG-001.png        도면(표제란 + BOM)
  parts/parts_master.csv                부품 마스터 ([3-50] 대조용)
  fonts/NanumGothic-Regular.ttf         그래프·이미지용 한글 폰트

비전 실습(주조품 사진)은 교재대로 공개 데이터셋을 원 배포처에서 내려받는다.
내려받기가 막히면 casting_local/ 에 대체 이미지를 만들어 둔다.
"""
import os, glob, json, wave, shutil, subprocess, sys, urllib.request
import numpy as np

SEED = 20260909
rng = np.random.default_rng(SEED)
SR = 16000

# ── 한글 폰트 ─────────────────────────────────────────────────
FONT_URL = ("https://raw.githubusercontent.com/aebonlee/materials/main/"
            "build-data/data/NanumGothic-Regular.ttf")
os.makedirs("fonts", exist_ok=True)
FONT = "fonts/NanumGothic-Regular.ttf"
if not os.path.exists(FONT):
    found = glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
    if not found:
        try:
            subprocess.run("apt-get -qq install -y fonts-nanum", shell=True, check=False, timeout=180)
            found = glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
        except Exception:
            found = []
    try:
        shutil.copy(found[0], FONT) if found else urllib.request.urlretrieve(FONT_URL, FONT)
    except Exception as e:
        print("  ! 한글 폰트를 준비하지 못했습니다:", e)

# ══════════════════════════════════════════════════════════════
# 1) 음향 — 정상 100 / 이상 100
# ══════════════════════════════════════════════════════════════
def write_wav(path, sig):
    x = np.clip(sig / (np.abs(sig).max() + 1e-9) * 0.85, -1, 1)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())

def band_noise(n, lo, hi, rms):
    """lo~hi Hz 대역만 남긴 잡음"""
    spec = np.fft.rfft(rng.normal(0, 1, n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(spec, n)
    return y / (y.std() + 1e-9) * rms

def pump(abnormal):
    """유압 펌프 소리 — 기본 회전음 + 하모닉 + 잡음. 이상이면 2~4kHz 가 커진다."""
    dur = 3.0
    n = int(SR * dur)
    t = np.arange(n) / SR
    f0 = 58 + rng.normal(0, 2.0)                      # 회전 기본 주파수
    y = np.zeros(n)
    for k, a in enumerate([1.0, 0.55, 0.32, 0.2, 0.12], start=1):
        y += a * np.sin(2 * np.pi * f0 * k * t + rng.uniform(0, 6.3))
    y *= 1 + 0.06 * np.sin(2 * np.pi * 1.7 * t)       # 완만한 부하 변동
    y += band_noise(n, 100, 8000, 0.10)               # 배경 잡음
    # ← 여기서 갈린다. 이상음은 2~4kHz 대역이 약 +6dB 높다(교재 [3-24] 그림).
    # 개체마다 편차를 둬서 완전히 갈리지는 않게 한다 — 그래야 혼동 행렬을 볼 일이 생긴다.
    band = (0.035 if not abnormal else 0.115) * rng.uniform(0.75, 1.3)
    y += band_noise(n, 2000, 4000, band)
    if abnormal:                                      # 캐비테이션 — 불규칙한 충격음
        for _ in range(rng.integers(6, 14)):
            i = rng.integers(0, n - 600)
            env = np.exp(-np.arange(600) / 90)
            y[i:i + 600] += 0.28 * env * np.sin(2 * np.pi * rng.uniform(2400, 3800) * np.arange(600) / SR)
    return y * rng.uniform(0.85, 1.15)

for tag, ab in (("normal", False), ("abnormal", True)):
    os.makedirs(f"audio/{tag}", exist_ok=True)
    for i in range(1, 101):
        write_wav(f"audio/{tag}/{tag}_{i:03d}.wav", pump(ab))

# ── 상담 녹음 (전사 실습용) ────────────────────────────────────
CALL = """상담원: 네, 고객센터입니다. 무엇을 도와드릴까요?
고객: 굴착기 시동이 안 걸려서요. 아침부터 계속 그럽니다.
상담원: 장비 번호를 알려 주시겠어요?
고객: 이엑스 이공오번입니다.
상담원: 계기판에 경고등이 들어와 있습니까?
고객: 배터리 표시등이 깜빡입니다.
상담원: 어제 작업 마치고 시동을 껐을 때 이상은 없었습니까?
고객: 없었습니다. 오늘 아침에만 그렇습니다.
상담원: 배터리 방전으로 보입니다. 단자 상태를 먼저 확인해 주시고, 정비 기사 배정해 드리겠습니다.
고객: 네, 부탁드립니다."""
open("audio/call1_engine_start.txt", "w", encoding="utf-8").write(CALL)

tts_ok = False
try:
    try:
        from gtts import gTTS
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "-q", "install", "gTTS"], check=True, timeout=300)
        from gtts import gTTS
    body = "\n".join(l.split(":", 1)[1].strip() for l in CALL.splitlines())
    gTTS(text=body, lang="ko").save("audio/_call1.mp3")
    try:                                             # ① ffmpeg 이 있으면 그걸로
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "audio/_call1.mp3",
                        "-ar", str(SR), "-ac", "1", "audio/call1_engine_start.wav"],
                       check=True, timeout=300)
    except Exception:                                # ② 없으면 librosa 로 읽어 직접 쓴다
        import librosa
        sig, _ = librosa.load("audio/_call1.mp3", sr=SR, mono=True)
        write_wav("audio/call1_engine_start.wav", sig)
    os.remove("audio/_call1.mp3")
    tts_ok = os.path.exists("audio/call1_engine_start.wav")
except Exception as e:
    print("  ! 상담 녹음(음성 합성)을 만들지 못했습니다:", type(e).__name__)
    print("    [3-44] 전사 실습은 스마트폰으로 30초쯤 직접 녹음해 audio/ 에 올려 쓰세요.")

# ══════════════════════════════════════════════════════════════
# 2) 점검표 사진 5장 + 채점용 정답지
# ══════════════════════════════════════════════════════════════
from PIL import Image, ImageDraw, ImageFont

def font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()

ITEMS = ["엔진오일 레벨", "냉각수 레벨", "유압유 누유", "트랙 장력",
         "그리스 주입", "작업등 점등", "계기판 경고등", "안전벨트"]
INSPECTORS = ["김 반장", "박 기사", "최 주임", "오 기사", "정 기사"]
BAD_MEMO = {"엔진오일 레벨": "하한선 근접, 보충 요청", "냉각수 레벨": "소량 부족",
            "유압유 누유": "붐 실린더 하단 유막", "트랙 장력": "좌측 처짐",
            "그리스 주입": "미주입 구간 있음", "작업등 점등": "우측 미점등",
            "계기판 경고등": "배터리 경고등 점등", "안전벨트": "버클 마모"}

def draw_checklist(path, eq, date, who, verdicts, note):
    W, H = 1000, 1320
    im = Image.new("RGB", (W, H), (252, 251, 247))
    d = ImageDraw.Draw(im)
    d.rectangle([30, 30, W - 30, H - 30], outline=(60, 60, 60), width=3)
    d.text((W // 2, 80), "굴착기 일일점검표", font=font(46), fill=(20, 20, 20), anchor="mm")
    y = 140
    for label, val in (("장비ID", eq), ("점검일자", date), ("점검자", who)):
        d.text((70, y), f"{label}", font=font(28), fill=(70, 70, 70))
        d.line([(210, y + 36), (520, y + 36)], fill=(120, 120, 120), width=2)
        d.text((225, y), val, font=font(30), fill=(15, 15, 15))
        y += 62
    y += 20
    cols = [70, 470, 640, W - 70]
    d.rectangle([cols[0], y, cols[3], y + 52], fill=(232, 230, 222))
    for x, t in ((cols[0] + 16, "점검 항목"), (cols[1] + 30, "판정"), (cols[2] + 30, "비고")):
        d.text((x, y + 12), t, font=font(28), fill=(30, 30, 30))
    y += 52
    for it in ITEMS:
        v = verdicts[it]
        d.rectangle([cols[0], y, cols[3], y + 64], outline=(150, 150, 150), width=1)
        d.line([(cols[1], y), (cols[1], y + 64)], fill=(150, 150, 150), width=1)
        d.line([(cols[2], y), (cols[2], y + 64)], fill=(150, 150, 150), width=1)
        d.text((cols[0] + 16, y + 16), it, font=font(28), fill=(20, 20, 20))
        d.text((cols[1] + 46, y + 14), v["판정"], font=font(30),
               fill=(20, 20, 20) if v["판정"] == "양호" else (185, 30, 30))
        if v["비고"]:
            d.text((cols[2] + 14, y + 20), v["비고"], font=font(22), fill=(70, 70, 70))
        y += 64
    y += 26
    d.text((70, y), "특이사항", font=font(28), fill=(70, 70, 70))
    d.rectangle([70, y + 42, W - 70, y + 150], outline=(150, 150, 150), width=1)
    d.text((86, y + 60), note or "없음", font=font(26), fill=(20, 20, 20))
    d.text((W - 70, H - 60), "DreamIT Biz 실습용 양식", font=font(20), fill=(160, 160, 160), anchor="rs")
    im.save(path)

os.makedirs("checklists", exist_ok=True)
gt = {"사진": []}
for i in range(1, 6):
    eq = f"EX-{rng.choice([101, 103, 203, 205, 302])}"
    date = f"2025-11-{rng.integers(3, 26):02d}"
    who = INSPECTORS[rng.integers(len(INSPECTORS))]
    bad = list(rng.choice(len(ITEMS), rng.integers(1, 3), replace=False))
    verdicts = {it: {"판정": "불량" if j in bad else "양호",
                     "비고": BAD_MEMO[it] if j in bad else ""}
                for j, it in enumerate(ITEMS)}
    note = "정비팀 점검 요청" if bad else "없음"
    name = f"daily_{i:03d}.png"
    draw_checklist(f"checklists/{name}", eq, date, who, verdicts, note)
    gt["사진"].append({"파일": name, "장비ID": eq, "점검일자": date, "점검자": who,
                       "항목": verdicts, "특이사항": note})
json.dump(gt, open("checklists/checklists_ground_truth.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ══════════════════════════════════════════════════════════════
# 3) 도면 1장 (표제란 + BOM)
# ══════════════════════════════════════════════════════════════
BOM = [("R10-10510", "유압호스(붐 실린더)", "2"), ("R10-10260", "붐 실린더 씰킷", "1"),
       ("GEN-10030", "리튬 그리스 (400g)", "1"), ("R10-10270", "아이들러", "2"),
       ("", "고정 브래킷", "4")]                     # 품번 없는 행 — 교재가 짚는 자리
os.makedirs("drawings", exist_ok=True)
W, H = 1400, 990
im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)
d.rectangle([20, 20, W - 20, H - 20], outline=(40, 40, 40), width=3)
d.rectangle([60, 70, 700, 560], outline=(90, 90, 90), width=2)
d.line([(60, 315), (700, 315)], fill=(190, 190, 190), width=1)
d.line([(380, 70), (380, 560)], fill=(190, 190, 190), width=1)
d.ellipse([300, 240, 460, 400], outline=(40, 40, 40), width=3)
d.rectangle([150, 150, 300, 250], outline=(40, 40, 40), width=3)
d.text((80, 90), "BOOM CYLINDER ASSY", font=font(24), fill=(40, 40, 40))
tx, ty = 760, 70
d.rectangle([tx, ty, W - 60, ty + 44 * (len(BOM) + 1)], outline=(60, 60, 60), width=2)
d.text((tx + 14, ty + 10), "품번", font=font(24), fill=(20, 20, 20))
d.text((tx + 210, ty + 10), "명칭", font=font(24), fill=(20, 20, 20))
d.text((tx + 480, ty + 10), "수량", font=font(24), fill=(20, 20, 20))
for k, (pn, nm, q) in enumerate(BOM, start=1):
    yy = ty + 44 * k
    d.line([(tx, yy), (W - 60, yy)], fill=(150, 150, 150), width=1)
    d.text((tx + 14, yy + 10), pn or "—", font=font(22), fill=(20, 20, 20))
    d.text((tx + 210, yy + 10), nm, font=font(22), fill=(20, 20, 20))
    d.text((tx + 495, yy + 10), q, font=font(22), fill=(20, 20, 20))
bx, by = 760, H - 250
d.rectangle([bx, by, W - 60, H - 60], outline=(60, 60, 60), width=2)
for k, (label, val) in enumerate([("도면번호", "R-DWG-001"), ("도면명", "붐 실린더 조립도"),
                                  ("적용기종", "리파 R10-5"), ("일자", "2025-10-14")]):
    yy = by + 46 * k
    d.line([(bx, yy), (W - 60, yy)], fill=(150, 150, 150), width=1)
    d.text((bx + 14, yy + 12), label, font=font(22), fill=(90, 90, 90))
    d.text((bx + 170, yy + 10), val, font=font(24), fill=(15, 15, 15))
im.save("drawings/drawing_R-DWG-001.png")

# ══════════════════════════════════════════════════════════════
# 4) 부품 마스터 ([3-50] BOM 대조용 — DAY 2 와 같은 표)
# ══════════════════════════════════════════════════════════════
import csv
MASTER = [
    ("GEN-10010", "엔진오일 15W-40 (20L)", "공통"), ("GEN-10020", "엔진오일 필터", "공통"),
    ("GEN-10030", "리튬 그리스 (400g)", "공통"),    ("GEN-10040", "연료 필터", "공통"),
    ("GEN-10050", "에어클리너 엘리먼트", "공통"),   ("GEN-10060", "유압 리턴 필터", "공통"),
    ("GEN-10070", "냉각수 (4L)", "공통"),           ("GEN-10080", "작업등 LED", "공통"),
    ("B32-10210", "고무 트랙 (320mm)", "밥캣 E32"), ("B32-10230", "트랙 롤러", "밥캣 E32"),
    ("B32-10410", "안전벨트", "밥캣 E32"),          ("B32-10510", "유압호스(암 실린더)", "밥캣 E32"),
    ("C304-10220", "고무 트랙 (300mm)", "캐터필러 304 CR"), ("C304-10240", "아이들러", "캐터필러 304 CR"),
    ("C304-10410", "안전벨트", "캐터필러 304 CR"),  ("C304-10520", "파일럿 밸브", "캐터필러 304 CR"),
    ("U27-10230", "트랙 롤러", "구보타 U27-4"),     ("U27-10250", "예열 플러그", "구보타 U27-4"),
    ("U27-10410", "안전벨트", "구보타 U27-4"),      ("U27-10530", "주행모터 씰킷", "구보타 U27-4"),
    ("R10-10260", "붐 실린더 씰킷", "리파 R10-5"),  ("R10-10270", "아이들러", "리파 R10-5"),
    ("R10-10410", "안전벨트", "리파 R10-5"),        ("R10-10510", "유압호스(붐 실린더)", "리파 R10-5"),
]
os.makedirs("parts", exist_ok=True)
with open("parts/parts_master.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["부품번호", "부품명", "적용기종", "단가(원)"])
    for pn, nm, m in MASTER:
        w.writerow([pn, nm, m, int(rng.integers(8, 260)) * 1000])

# ══════════════════════════════════════════════════════════════
# 5) 비전 실습 대비 — 공개 데이터셋을 못 받을 때 쓸 대체 이미지
# ══════════════════════════════════════════════════════════════
def casting(defect):
    im = Image.new("RGB", (512, 512), (16, 16, 18))
    d = ImageDraw.Draw(im)
    cx, cy, r = 256, 256, 190
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 155), outline=(210, 210, 215), width=6)
    d.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=(16, 16, 18), outline=(200, 200, 205), width=5)
    for a in range(0, 360, 45):                      # 볼트 구멍
        bx = cx + int(140 * np.cos(np.radians(a))); by = cy + int(140 * np.sin(np.radians(a)))
        d.ellipse([bx - 17, by - 17, bx + 17, by + 17], fill=(30, 30, 34), outline=(190, 190, 195), width=3)
    px = np.array(im, dtype=float)
    px += rng.normal(0, 5, px.shape)                 # 촬영 잡음
    im = Image.fromarray(np.clip(px, 0, 255).astype("uint8"))
    if defect:                                       # 결함 — 표면 결손·기공
        d = ImageDraw.Draw(im)
        for _ in range(rng.integers(2, 5)):
            a = rng.uniform(0, 6.28); rr = rng.uniform(80, 175)
            ex = cx + rr * np.cos(a); ey = cy + rr * np.sin(a); s = rng.integers(9, 24)
            d.ellipse([ex - s, ey - s, ex + s, ey + s], fill=(60, 58, 62))
    return im

for tag, defect in (("def_front", True), ("ok_front", False)):
    os.makedirs(f"casting_local/{tag}", exist_ok=True)
    for i in range(1, 31):
        casting(defect).save(f"casting_local/{tag}/{'def' if defect else 'ok'}_{i:03d}.jpeg", quality=92)

# ══════════════════════════════════════════════════════════════
print("실습 데이터를 만들었습니다.")
print(f"  audio/normal · abnormal            {len(glob.glob('audio/normal/*.wav'))} · {len(glob.glob('audio/abnormal/*.wav'))}개")
print(f"  audio/call1_engine_start.wav/.txt  {'준비됨' if tts_ok else '전사용 녹음 없음 — 직접 녹음해 올리세요'}")
print(f"  checklists/daily_001~005.png       5장 + 정답지")
print(f"  drawings/drawing_R-DWG-001.png     1장")
print(f"  parts/parts_master.csv             {len(MASTER)}행")
print(f"  casting_local/                     결함 30 · 정상 30 (공개 데이터셋을 못 받을 때만 씁니다)")
print(f"  fonts/NanumGothic-Regular.ttf      {'준비됨' if os.path.exists(FONT) else '없음'}")
print("\n※ 원본 실습 데이터를 대신해 만든 것이라 교재에 인쇄된 숫자·사진과는 다릅니다.")
print("   실습의 흐름과 결론(이상음은 2~4kHz 가 높다, 추출 결과를 정답지로 채점한다)은 같습니다.")
