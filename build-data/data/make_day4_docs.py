# -*- coding: utf-8 -*-
"""
DAY 4 지식베이스 — 매뉴얼 4종 생성기

교재 PART 04 는 지식베이스에 문서 10건을 올려 놓고 검색을 실습한다.
그 가운데 **절차서 5종과 트러블슈팅 사례 120건은 교재 저장소 원본을 쓴다**
(2026-09-09 저자 수령). 여기서 만드는 것은 원본에도 담기지 못한 **매뉴얼 4종**뿐이다 —
제조사 저작물이라 저자도 배포할 수 없어 빈자리로 남아 있던 부분이다.

만들어지는 것 (docs/ 아래 5개)
  밥캣 E32 · 캐터필러 304 CR(영문) · 구보타 U27-4(영문) · 리파 R10-5 · 문서_메타데이터.csv

기종 넷은 교재 [4-2] 및 부품마스터의 적용기종과 같다. 이 이름이 어긋나면
메타데이터 필터 실습이 성립하지 않는다(2026-09-09 에 볼보 EC55 로 잘못 만든 것을 바로잡았다).

메타데이터표는 **원본 절차서·사례를 포함한 10건 전체**를 적는다 — Dify 에 입력할 값이다.
"""
import os, csv, glob, shutil, subprocess, urllib.request, random

random.seed(20260928)
OUT = "docs"
os.makedirs(OUT, exist_ok=True)

# ── 한글 폰트 ─────────────────────────────────────────────────
FONT_URL = ("https://raw.githubusercontent.com/aebonlee/materials/main/"
            "build-data/data/NanumGothic-Regular.ttf")
FONT = "fonts/NanumGothic-Regular.ttf"
os.makedirs("fonts", exist_ok=True)
if not os.path.exists(FONT):
    found = glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
    if not found:
        subprocess.run("apt-get -qq install -y fonts-nanum", shell=True, check=False)
        found = glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
    shutil.copy(found[0], FONT) if found else urllib.request.urlretrieve(FONT_URL, FONT)

try:
    from fpdf import FPDF
except ImportError:
    subprocess.run(["pip", "-q", "install", "fpdf2"], check=True)
    from fpdf import FPDF

def pdf(path, title, sections, code=None):
    """sections = [(소제목, [문단…])]"""
    d = FPDF(format="A4")
    d.add_font("N", "", FONT)
    d.set_auto_page_break(True, margin=18)
    d.add_page()
    d.set_font("N", size=17); d.multi_cell(0, 10, title); d.ln(2)
    if code:
        d.set_font("N", size=9); d.set_text_color(110)
        d.multi_cell(0, 6, code); d.set_text_color(0); d.ln(1)
    for head, paras in sections:
        d.set_font("N", size=12.5); d.ln(3); d.multi_cell(0, 8, head); d.ln(1)
        d.set_font("N", size=10)
        for p in paras:
            d.multi_cell(0, 6.4, p); d.ln(1)
    d.output(os.path.join(OUT, path))

# ══════════════════════════════════════════════════════════════
# 절차서 5종 — v1/v2 는 「기록 방법」 항목만 다르다(판본 실습의 핵심)
# ══════════════════════════════════════════════════════════════
COMMON = [
    ("1. 목적", ["이 절차서는 굴착기 일일 점검의 수행 방법과 기록 방법을 정한다. "
                 "적용 범위는 정비 1팀이 관리하는 전 장비이며, 교대 전 점검에 적용한다."]),
    ("2. 점검 항목", ["점검 항목은 여덟 가지다. 엔진오일 레벨, 냉각수 레벨, 유압유 누유, 트랙 장력, "
                     "그리스 주입, 작업등 점등, 계기판 경고등, 안전벨트 상태를 순서대로 확인한다.",
                     "항목마다 양호 또는 불량으로 판정한다. 판단이 애매하면 불량으로 적고 비고에 근거를 남긴다."]),
    ("3. 점검 순서", ["시동 전 육안 점검을 먼저 하고, 시동 후 계기판과 작동부를 확인한다. "
                     "시동 전 점검에서 불량이 나오면 시동을 걸지 않고 정비 담당자에게 알린다."]),
]
AFTER = [
    ("5. 불량 발견 시 조치", ["불량 항목이 하나라도 있으면 장비를 사용하지 않고 정비 담당자에게 즉시 알린다. "
                            "안전과 관련된 항목(안전벨트, 계기판 경고등, 유압 누유)은 예외 없이 사용 중지 대상이다.",
                            "조치가 끝나면 재점검을 실시하고 그 결과를 같은 방법으로 기록한다."]),
    ("6. 보관", ["점검 기록은 3년간 보관한다. 보관 책임자는 정비 1팀 반장이다."]),
]
pdf("Kubota_U27-4_Operator_Manual_EN.pdf", "KUBOTA U27-4 OPERATOR'S MANUAL (EXCERPT)",
    [("SAFE OPERATION -13",
      ["Before starting the engine, make sure the safety lever is in the LOCK position. "
       "The engine will not crank while the safety lever is released. This is a designed interlock, not a fault.",
       "Do not attempt to bypass the interlock. If the engine does not crank with the lever locked, "
       "inspect the battery terminals and the starter relay before further troubleshooting."]),
     ("PERIODIC SERVICE",
      ["Service intervals are counted in engine service hours shown on the hour meter, not in calendar days. "
       "Perform the daily checks before every shift regardless of the hour meter reading.",
       "Every 50 hours: grease all pivot points, check track tension, drain water from the fuel filter separator.",
       "Every 200 hours: replace engine oil and engine oil filter, inspect the fan belt tension, "
       "check coolant level and hoses for cracks.",
       "Every 500 hours: replace the hydraulic return filter, replace the fuel filter element, "
       "inspect the travel motor for oil leakage.",
       "Every 1000 hours: replace the air cleaner element, replace all filters as a set, "
       "adjust the track and inspect idlers and rollers for wear.",
       "In cold weather below -5 degrees Celsius, extend the glow plug preheat time and idle the machine "
       "for at least three minutes before operation. Low hydraulic oil temperature slows the control response."]),
     ("MAINTENANCE RECORD",
      ["Record every service in the maintenance logbook with the hour meter reading, the date, "
       "the parts replaced and the name of the technician. Keep the record for the life of the machine."])],
    code="Code No. RH418-8193-1  /  Issued 2024-08  /  KUBOTA Corporation (excerpt for training)")
pdf("Caterpillar_304CR_Service_Excerpt_EN.pdf", "CATERPILLAR 304 CR SERVICE MANUAL (EXCERPT)",
    [("SEAT BELT INSPECTION",
      ["Inspect the seat belt and the attaching hardware before each shift. "
       "Replace the seat belt within three years of the date on the belt tag, regardless of appearance.",
       "The tag is attached to the belt webbing near the buckle and shows the month and year of manufacture."]),
     ("TRACK ADJUSTMENT",
      ["Measure the track sag at the midpoint between the carrier roller and the idler. "
       "The specified sag is 10 to 15 mm. Adjust with grease through the track adjuster fitting."])],
    code="Code No. SEBU8407-05  /  Issued 2023-05  /  Caterpillar Inc. (excerpt for training)")
pdf("Bobcat_E32_취급설명서_발췌.pdf", "밥캣 E32 취급설명서 (발췌)",
    [("정기 점검 주기", ["점검 주기는 계기판의 가동 시간을 기준으로 센다. 달력 날짜가 아니라 실제로 돌아간 시간이다.",
                      "50시간마다 각 회전부에 그리스를 주입하고 트랙 장력을 확인한다. 연료 필터의 수분 분리기를 배출한다.",
                      "200시간마다 엔진오일과 엔진오일 필터를 교환하고, 팬 벨트 장력과 냉각수 상태를 함께 확인한다.",
                      "500시간마다 유압 리턴 필터와 연료 필터 엘리먼트를 교환하고 주행모터의 누유를 점검한다.",
                      "1000시간마다 에어클리너 엘리먼트를 교환하고 필터류를 일괄 교체한다. 트랙을 조정하고 아이들러와 롤러의 마모를 확인한다."]),
     ("안전 장치", ["안전 레버가 잠김 위치에 있어야 시동이 걸린다. 레버가 풀려 있으면 크랭킹이 되지 않는다.",
                  "이는 고장이 아니라 설계된 안전 장치다. 어떤 경우에도 이 장치를 우회하지 않는다.",
                  "레버를 잠근 상태에서도 크랭킹이 되지 않으면 배터리 단자와 시동 릴레이를 먼저 확인한다."]),
     ("저온 시 취급", ["외기 온도가 낮으면 유압유의 점도가 올라가 조작 반응이 느려진다.",
                    "영하에서는 예열 시간을 평소보다 길게 주고, 무부하로 3분 이상 돌린 뒤 작업을 시작한다."]),
     ("정비 기록", ["정비를 마칠 때마다 가동 시간, 날짜, 교체한 부품, 작업자 이름을 기록에 남긴다."])],
    code="문서번호 B32-OM-KR-2024 / 발행 2024-06 / 두산밥캣 (교육용 발췌)")
pdf("Rippa_R10-5_정비지침_발췌.pdf", "리파 R10-5 정비 지침 (발췌)",
    [("유압 계통", ["유압유는 2000시간 또는 2년 중 빠른 쪽에 교환한다. 사용 환경이 험하면 주기를 앞당긴다.",
                  "누유가 확인되면 압력을 측정하고 규정값과 대조한다. 압력이 규정값 안이어도 누유는 별개로 조치한다.",
                  "유압호스는 이음부의 조임 상태와 꺾임부의 균열을 함께 본다. 표면이 부풀어 오른 호스는 교체 대상이다."]),
     ("전기 계통", ["배터리는 3년마다 교체를 검토한다. 저온기에는 시동 전 전압을 확인한다.",
                  "발전기 출력 전압이 규정값에 못 미치면 주행 중 정지로 이어질 수 있으므로 즉시 조치한다.",
                  "배선 커넥터의 접점 부식은 작업등 미점등과 계기판 오작동의 흔한 원인이다."]),
     ("하부 주행체", ["트랙 처짐량은 캐리어 롤러와 아이들러의 중간에서 잰다. 규정값은 10~15mm 다.",
                   "과도하게 당기면 롤러와 아이들러가 빨리 닳는다. 느슨하면 트랙이 이탈한다."])],
    code="문서번호 R10-5-SM-KR-2025 / 발행 2025-02 / 리파 (교육용 발췌)")

# ══════════════════════════════════════════════════════════════
# 트러블슈팅 사례 120건 — 유사 증상 다른 원인이 섞이게
# ══════════════════════════════════════════════════════════════
META = [
    # 절차서 5종과 사례 파일은 교재 저장소 원본이다(2026-09-09 수령). 매뉴얼 4종만 우리가 만든 대체본이다
    # — 제조사 저작물이라 원본에도 담기지 않았다. 기종은 교재 [4-2]·부품마스터와 같은 넷이다.
    ("일일점검_및_기록_SOP_v1.pdf", "절차서", "공통", "2024-03", "개정 전 판본 — 필터 실습용으로 함께 올린다"),
    ("일일점검_및_기록_SOP_v2.pdf", "절차서", "공통", "2025-11", "현재 유효 판본"),
    ("겨울철_장비운용_지침.pdf", "절차서", "공통", "2024-11", ""),
    ("유압계통_이상음_점검_SOP.pdf", "절차서", "공통", "2025-03", ""),
    ("하부주행체_육안검사_가이드.pdf", "절차서", "공통", "2025-06", ""),
    ("Bobcat_E32_취급설명서_발췌.pdf", "매뉴얼", "밥캣 E32", "2024-06", "교육용 대체본"),
    ("Caterpillar_304CR_Service_Excerpt_EN.pdf", "매뉴얼", "캐터필러 304 CR", "2023-05", "영문 · 교육용 대체본"),
    ("Kubota_U27-4_Operator_Manual_EN.pdf", "매뉴얼", "구보타 U27-4", "2024-08", "영문 — 다국어 검색 실습용 · 교육용 대체본"),
    ("Rippa_R10-5_정비지침_발췌.pdf", "매뉴얼", "리파 R10-5", "2025-02", "교육용 대체본"),
    ("트러블슈팅_통합_120건.txt", "사례기록", "공통", "2025-12", "사례 120건 — 교재 저장소 원본"),
]
with open(os.path.join(OUT, "문서_메타데이터.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["문서명", "문서 종류", "대상 기종", "개정일", "비고"])
    w.writerows(META)

n = len(glob.glob(f"{OUT}/*"))
print(f"매뉴얼 대체본을 만들었습니다 — docs/ 아래 {n}개 (절차서·사례는 교재 저장소 원본을 쓰세요)")
for p in sorted(glob.glob(f"{OUT}/*")):
    print(f"  {os.path.basename(p):<44}{os.path.getsize(p)/1024:>7.0f} KB")
print("\n※ 원본 자료를 대신해 만든 교육용 문서입니다. 제조사 실제 매뉴얼이 아닙니다.")
print("   실습이 겨냥하는 네 상황(판본·유사증상·다국어·지식베이스 외)은 그대로 재현됩니다.")
