# -*- coding: utf-8 -*-
"""
DAY 4 지식베이스 문서 생성기 (RAG 실습용 대체 자료)

교재 PART 04 는 지식베이스에 문서 10건을 올려 놓고 검색을 실습한다.
원본 자료를 받지 못해, 실습이 겨냥하는 네 가지 상황이 그대로 재현되도록 만든다.

  ① 같은 주제 다른 판본   일일점검_및_기록_SOP v1(개정 전) · v2(개정 후, 개정일 2025-11)
  ② 유사 증상 다른 원인   시동 불량 사례 — 안전 레버 / 배터리 방전 / 연료 필터
  ③ 다국어 질문          구보타 U27-4 영문 매뉴얼 (Code No. RH418-8193-1)
  ④ 지식베이스 외 주제    타워크레인·용접은 일부러 넣지 않는다

만들어지는 것 (docs/ 아래 10건 + 메타데이터표)
  절차서 5 · 매뉴얼 4 · 트러블슈팅 사례 120건 1 · 문서_메타데이터.csv
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
pdf("일일점검_및_기록_SOP_v1.pdf", "일일 점검 및 기록 표준 작업 절차서 (v1)",
    COMMON + [("4. 기록 방법",
               ["점검 결과는 종이 일일 점검표에 볼펜으로 기입한다. 연필로 적지 않는다.",
                "점검자는 이름을 자필로 적고 날짜를 함께 기입한다. "
                "작성한 점검표는 정비고 캐비닛의 당월 바인더에 철한다.",
                "수정이 필요하면 두 줄을 긋고 옆에 다시 적은 뒤 서명한다. 지우거나 덧쓰지 않는다."])] + AFTER,
    code="문서번호 SOP-MNT-001 / 작성일 2024-03-15 / 작성 정비1팀 / 판본 v1")
pdf("일일점검_및_기록_SOP_v2.pdf", "일일 점검 및 기록 표준 작업 절차서 (v2)",
    COMMON + [("4. 기록 방법 (개정)",
               ["점검 결과는 개정된 전자 양식에 기입한다. 스마트폰으로 사내 점검 폼을 열어 항목별 판정을 선택한다.",
                "종이 점검표는 통신이 되지 않는 현장에서만 예비로 사용하고, 복귀 후 같은 날 안에 전자 양식으로 옮겨 적는다.",
                "사진 첨부는 불량 항목에 대해 필수다. 정면에서 문서 전체가 들어오게 찍는다.",
                "제출한 기록은 수정할 수 없다. 잘못 제출했으면 정정 사유를 적어 다시 제출한다."])] + AFTER,
    code="문서번호 SOP-MNT-001 / 개정일 2025-11-04 / 작성 정비1팀 / 판본 v2 (v1 대체)")
pdf("겨울철_저온시동_점검지침.pdf", "겨울철 저온 시동 점검 지침",
    [("1. 적용", ["외기 온도 영하 5도 이하인 날의 시동 전 점검에 적용한다."]),
     ("2. 시동 전 확인", ["배터리 단자의 부식과 조임 상태를 확인한다. 저온에서는 배터리 용량이 크게 줄어든다.",
                        "연료 필터의 수분 분리기를 배출한다. 수분이 얼면 연료 공급이 끊긴다.",
                        "유압유 온도가 낮으면 조작 반응이 느려진다. 무부하로 3분 이상 예열한 뒤 작업한다."]),
     ("3. 시동이 걸리지 않을 때", ["예열 플러그 작동을 확인하고, 예열 시간을 평소보다 길게 준다.",
                                "크랭킹은 10초를 넘기지 않고 30초 쉬었다가 다시 시도한다.",
                                "세 번 시도해도 걸리지 않으면 중단하고 정비 담당자에게 알린다."]),
     ("4. 자주 나오는 원인", ["저온기 시동 불량의 상당수는 배터리 방전과 연료 계통 수분이다. "
                            "다만 안전 레버가 해제되어 있으면 크랭킹 자체가 되지 않으므로 이것부터 확인한다."])],
    code="문서번호 SOP-MNT-014 / 작성일 2024-11-20 / 작성 정비1팀")
pdf("유압계통_누유_점검절차.pdf", "유압 계통 누유 점검 절차",
    [("1. 목적", ["유압 누유의 발견과 초기 조치 방법을 정한다."]),
     ("2. 점검 위치", ["붐 실린더, 암 실린더, 버킷 실린더의 로드 표면과 씰 부위를 확인한다.",
                     "유압호스의 이음부와 꺾임부를 확인한다. 트랙 롤러와 아이들러의 씰 부위도 함께 본다."]),
     ("3. 판정 기준", ["로드 표면의 얇은 유막은 정상 범위로 본다. 방울이 맺히거나 흘러내리면 불량으로 판정한다.",
                     "바닥에 유압유가 고여 있으면 즉시 사용을 중지한다."]),
     ("4. 조치", ["씰 키트 교체 후 압력을 재측정한다. 교체 이력은 부품 사용 이력에 남긴다."])],
    code="문서번호 SOP-MNT-021 / 작성일 2025-03-06 / 작성 정비1팀")
pdf("정비_안전수칙_및_작업중지_절차.pdf", "정비 안전 수칙 및 작업 중지 절차",
    [("1. 기본 수칙", ["정비 전 시동을 끄고 열쇠를 뽑아 담당자가 보관한다. 붐은 지면에 내려 둔다."]),
     ("2. 작업 중지 표시", ["작업 중지 표시를 조작부에 걸고, 표시를 건 사람만 제거한다."]),
     ("3. 안전벨트", ["안전벨트는 장비 사용 중 반드시 착용한다. 벨트와 태그가 손상되면 즉시 교체한다."]),
     ("4. 중지 기준", ["안전 관련 항목이 불량이면 작업을 중지한다. 판단이 어려우면 중지 쪽을 택한다.",
                     "중지 대상은 안전벨트 손상, 계기판 경고등 점등, 유압 누유, 제동 이상 네 가지를 기본으로 한다.",
                     "중지 결정은 현장에서 즉시 하고, 사후에 담당자가 기록으로 남긴다. 결정을 미루지 않는다."]),
     ("5. 재개 절차", ["조치가 끝나면 조치 내용과 확인자를 기록하고, 안전 담당자의 확인을 받은 뒤 작업을 재개한다.",
                    "재개 전 재점검에서 같은 항목이 다시 불량으로 나오면 재개하지 않는다."])],
    code="문서번호 SOP-SAF-003 / 작성일 2025-06-11 / 작성 안전관리팀")

# ══════════════════════════════════════════════════════════════
# 매뉴얼 4종 — 영문 2종(다국어 검색 실습) · 국문 2종
# ══════════════════════════════════════════════════════════════
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
pdf("Volvo_EC55_정비지침_발췌.pdf", "볼보 EC55 정비 지침 (발췌)",
    [("유압 계통", ["유압유는 2000시간 또는 2년 중 빠른 쪽에 교환한다. 사용 환경이 험하면 주기를 앞당긴다.",
                  "누유가 확인되면 압력을 측정하고 규정값과 대조한다. 압력이 규정값 안이어도 누유는 별개로 조치한다.",
                  "유압호스는 이음부의 조임 상태와 꺾임부의 균열을 함께 본다. 표면이 부풀어 오른 호스는 교체 대상이다."]),
     ("전기 계통", ["배터리는 3년마다 교체를 검토한다. 저온기에는 시동 전 전압을 확인한다.",
                  "발전기 출력 전압이 규정값에 못 미치면 주행 중 정지로 이어질 수 있으므로 즉시 조치한다.",
                  "배선 커넥터의 접점 부식은 작업등 미점등과 계기판 오작동의 흔한 원인이다."]),
     ("하부 주행체", ["트랙 처짐량은 캐리어 롤러와 아이들러의 중간에서 잰다. 규정값은 10~15mm 다.",
                   "과도하게 당기면 롤러와 아이들러가 빨리 닳는다. 느슨하면 트랙이 이탈한다."])],
    code="문서번호 EC55-SM-KR-2025 / 발행 2025-02 / 볼보건설기계 (교육용 발췌)")

# ══════════════════════════════════════════════════════════════
# 트러블슈팅 사례 120건 — 유사 증상 다른 원인이 섞이게
# ══════════════════════════════════════════════════════════════
CASES = [
    ("시동 불량 — 크랭킹이 되지 않음", "안전 레버 해제 상태",
     "계기판은 들어오나 크랭킹이 되지 않음. 안전 레버 위치 확인.",
     "안전 레버를 잠김 위치로 되돌린 뒤 정상 시동.",
     "저온기에 배터리를 먼저 의심하기 쉬우나, 크랭킹 자체가 안 되면 안전 레버부터 본다."),
    ("시동 불량 — 크랭킹은 되나 걸리지 않음", "연료 계통 수분",
     "연료 필터 수분 분리기 확인. 물이 차 있음.",
     "수분 배출 후 필터 교체, 시동 정상.",
     "한파 뒤 첫 시동에서 반복된다. 겨울에는 매일 배출한다."),
    ("시동 불량 — 크랭킹이 약함", "배터리 방전",
     "배터리 전압 측정 11.4V. 단자 부식 확인.",
     "충전 후 단자 청소·조임. 3일 뒤 재방전으로 배터리 교체.",
     "전압만 보고 넘기면 재발한다. 충전 후 이틀은 지켜본다."),
    ("유압 작동 시 이상음", "유압펌프 압력 저하",
     "무부하 압력 측정, 규정값 미달.",
     "펌프 탈거·교체, 계통 플러싱 후 압력 재측정.",
     "소리가 커지기 전에 압력이 먼저 떨어진다."),
    ("붐 실린더 누유", "씰 손상",
     "로드 표면 흠집과 유막 확인.",
     "씰 키트 교체, 로드 연마.",
     "로드에 흠이 있으면 씰만 갈아도 다시 샌다."),
    ("트랙 헐거움", "트랙 장력 이완",
     "캐리어 롤러와 아이들러 중간 처짐량 측정 22mm.",
     "그리스 주입으로 장력 조정, 처짐 12mm.",
     "규정 처짐은 10~15mm. 과도하게 당기면 롤러가 빨리 닳는다."),
    ("과열", "냉각수 부족과 라디에이터 막힘",
     "냉각수 레벨 하한, 라디에이터 핀에 분진.",
     "냉각수 보충, 라디에이터 세척.",
     "분진 현장은 주 1회 세척으로 재발이 줄었다."),
    ("작업등 미점등", "접점 부식",
     "커넥터 분리 후 접점 확인.",
     "접점 청소·조임 후 정상.",
     "전구부터 갈면 원인을 못 찾는다. 접점을 먼저 본다."),
    ("조작 반응 둔함", "저온에 의한 유압유 점도 상승",
     "외기 영하 8도. 예열 없이 작업 시작한 것 확인.",
     "무부하 3분 예열 후 정상.",
     "고장으로 접수되는 건 중 겨울에 이 유형이 가장 많다."),
    ("계기판 경고등 점등", "충전 계통 이상",
     "발전기 출력 전압 측정, 규정값 미달.",
     "발전기 교체.",
     "경고등을 무시하고 운행하면 주행 중 정지로 이어진다."),
]
EQ = ["EX-101", "EX-103", "EX-201", "EX-203", "EX-205", "EX-302", "EX-304"]
WHO = ["오 기사", "정 기사", "유 기사", "최 주임", "김 반장", "한 기사", "박 기사"]
lines = ["트러블슈팅 사례 통합 (교육용 대체 자료)",
         "형식: 사례번호 / 증상 / 확인 절차 / 원인 / 조치 / 결과 / 노하우 메모", ""]
for i in range(1, 121):
    sym, cause, check, act, memo = CASES[(i - 1) % len(CASES)]
    eq, who = EQ[(i * 3) % len(EQ)], WHO[(i * 5) % len(WHO)]
    d = f"202{4 + (i % 2)}-{((i % 12) + 1):02d}-{((i % 27) + 1):02d}"
    lines += [f"[사례 {i:03d}] {d} / 장비 {eq} / 담당 {who}",
              f"  증상     : {sym}", f"  확인 절차 : {check}", f"  원인     : {cause}",
              f"  조치     : {act}", f"  결과     : 조치 후 정상 작동 확인",
              f"  노하우   : {memo}", ""]
open(os.path.join(OUT, "트러블슈팅_통합_120건.txt"), "w", encoding="utf-8").write("\n".join(lines))

# ══════════════════════════════════════════════════════════════
# 메타데이터 표 — Dify 에 입력할 값 (표기는 반드시 통일)
# ══════════════════════════════════════════════════════════════
META = [
    ("일일점검_및_기록_SOP_v1.pdf", "절차서", "공통", "2024-03", "개정 전 판본 — 필터 실습용으로 함께 올린다"),
    ("일일점검_및_기록_SOP_v2.pdf", "절차서", "공통", "2025-11", "현재 유효 판본"),
    ("겨울철_저온시동_점검지침.pdf", "절차서", "공통", "2024-11", ""),
    ("유압계통_누유_점검절차.pdf", "절차서", "공통", "2025-03", ""),
    ("정비_안전수칙_및_작업중지_절차.pdf", "절차서", "공통", "2025-06", ""),
    ("Kubota_U27-4_Operator_Manual_EN.pdf", "매뉴얼", "구보타 U27-4", "2024-08", "영문 — 다국어 검색 실습용"),
    ("Caterpillar_304CR_Service_Excerpt_EN.pdf", "매뉴얼", "캐터필러 304 CR", "2023-05", "영문"),
    ("Bobcat_E32_취급설명서_발췌.pdf", "매뉴얼", "밥캣 E32", "2024-06", ""),
    ("Volvo_EC55_정비지침_발췌.pdf", "매뉴얼", "볼보 EC55", "2025-02", ""),
    ("트러블슈팅_통합_120건.txt", "사례기록", "공통", "2025-12", "사례 120건"),
]
with open(os.path.join(OUT, "문서_메타데이터.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["문서명", "문서 종류", "대상 기종", "개정일", "비고"])
    w.writerows(META)

n = len(glob.glob(f"{OUT}/*"))
print(f"지식베이스 문서를 만들었습니다 — docs/ 아래 {n}개")
for p in sorted(glob.glob(f"{OUT}/*")):
    print(f"  {os.path.basename(p):<44}{os.path.getsize(p)/1024:>7.0f} KB")
print("\n※ 원본 자료를 대신해 만든 교육용 문서입니다. 제조사 실제 매뉴얼이 아닙니다.")
print("   실습이 겨냥하는 네 상황(판본·유사증상·다국어·지식베이스 외)은 그대로 재현됩니다.")
