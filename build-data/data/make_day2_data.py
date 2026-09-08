# -*- coding: utf-8 -*-
"""
DAY 2 실습 데이터 생성기 (data_day2.zip 대체본)

원본 실습 데이터를 받지 못한 상황에서, 교재 [2-8] 이후의 모든 코드가
그대로 돌아가도록 같은 폴더·같은 컬럼·같은 성격의 데이터를 만든다.

  records/maintenance_2024_2025.csv   정비 이력 500행
  kpi/operation_2024_2025.csv         가동 기록 9,812행
  parts/parts_usage_hq.xlsx           본사 2,000행
  parts/parts_usage_busan.xlsx        부산 1,300행
  parts/parts_issue_gwangju.csv       광주 1,000행
  parts/parts_usage_dealer.csv        딜러 700행 (영문 스키마)
  parts/parts_master.csv              부품 마스터
  fonts/NanumGothic-Regular.ttf       그래프 한글 폰트 (교재 [2-1] 이 이 경로를 직접 읽는다)

수치는 난수라 교재에 인쇄된 출력과 똑같지 않다. 대신 분석의 결론은 같게 심어 두었다.
  · 리파 R10-5 의 정비시간이 다른 기종보다 유의하게 길다
  · 겨울에 저온성 증상(시동 불량·예열 등)이 몰린다
  · 정비기사 표기가 흔들린다 (김반장 / 박 기사님 / 최주임)
  · 완전 중복 4행, 30분 이내 유사 중복 4쌍
  · 다운타임이 계획가동시간을 넘는 예외 20건
"""
import os, glob, shutil, subprocess, sys, urllib.request
import numpy as np, pandas as pd

SEED = 20260908
rng = np.random.default_rng(SEED)

# ── 장비와 기종 ────────────────────────────────────────────────
EQ_MODEL = {
    "EX-101": "밥캣 E32",     "EX-102": "캐터필러 304 CR", "EX-103": "구보타 U27-4",
    "EX-104": "리파 R10-5",   "EX-201": "밥캣 E32",        "EX-202": "캐터필러 304 CR",
    "EX-203": "구보타 U27-4", "EX-204": "밥캣 E32",        "EX-205": "리파 R10-5",
    "EX-206": "구보타 U27-4", "EX-301": "캐터필러 304 CR", "EX-302": "밥캣 E32",
    "EX-303": "구보타 U27-4", "EX-304": "리파 R10-5",      "EX-305": "밥캣 E32",
}
EQS = list(EQ_MODEL)
SITE = {"1": "본사", "2": "부산", "3": "광주"}          # 장비ID 세 번째 글자
site_of = lambda eq: SITE[eq[3]]

# ── 증상·조치 사전 ─────────────────────────────────────────────
# (증상, 원인부품, 조치방법, 기준 정비시간(분))
BREAK = [
    ("시동 불량",            "연료 필터",        "배터리 충전 후 시동 확인, 단자 청소·조임", 80),
    ("예열 지연",            "예열 플러그",      "예열 플러그 교체, 배선 점검",              70),
    ("한파 중 동작 지연",    "유압유",           "유압유 교환, 예열 시간 연장 안내",         95),
    ("조작 반응 둔함",       "파일럿 밸브",      "파일럿 압력 재조정, 밸브 청소",           110),
    ("연료계통 수분 검출",   "연료 필터",        "연료 필터 교체, 워터세퍼레이터 배출",      75),
    ("배터리 방전",          "배터리",           "배터리 교체, 충전계통 점검",               60),
    ("유압 작동 시 이상음",  "유압펌프",         "유압펌프 압력 점검, 오일 보충",           185),
    ("유압 압력 저하로 작업 불가", "유압펌프",   "유압펌프 탈거·교체, 계통 플러싱 후 압력 재측정", 480),
    ("붐 실린더 누유",       "붐 실린더 씰",     "씰 키트 교체, 로드 상태 확인",            295),
    ("트랙 장력 이완",       "트랙 조정 실린더", "트랙 장력 재조정, 그리스 주입",           100),
    ("트랙 롤러 누유",       "트랙 롤러",        "롤러 교체, 인접 롤러 상태 확인",          160),
    ("아이들러 유격",        "아이들러",         "아이들러 교체, 트랙 장력 재조정",         180),
    ("좌측 주행 불가",       "주행모터",         "주행모터 탈거·교체, 파이널 드라이브 오일 교환", 420),
    ("과열 후 엔진 출력 상실", "헤드 개스킷",    "실린더 헤드 탈거 점검, 헤드 개스킷 교체 및 냉각계통 세척", 460),
    ("엔진오일 누유",        "오일 필터",        "오일 필터 재체결, 누유 부위 확인",        160),
    ("하부주행체 전반 마모", "고무 트랙",        "고무 트랙 좌·우, 트랙 롤러 4개, 아이들러 일괄 교체", 345),
    ("냉각수 온도 상승",     "라디에이터",       "라디에이터 청소, 냉각수 교환",            140),
    ("작업등 점등 불량",     "작업등",           "작업등 교체, 배선 접점 정비",              45),
]
COLD_KW = {"시동 불량", "예열 지연", "한파 중 동작 지연", "조작 반응 둔함",
           "연료계통 수분 검출", "배터리 방전"}          # 저온성 증상
CHECK = [
    ("200시간 정기점검",  "엔진오일 필터",      "엔진오일·오일필터 교환, 벨트 장력 점검",              105),
    ("500시간 정기점검",  "유압 리턴 필터",     "유압 리턴 필터 교환, 각부 그리스 주입",              140),
    ("1000시간 정기점검", "에어클리너 엘리먼트","에어클리너 엘리먼트 교환, 필터류 일괄 교체, 트랙 조정", 205),
    ("일상 점검",         "그리스",             "그리스 주입, 육안 점검",                              40),
]
MECH = ["오 기사", "정 기사", "유 기사", "최 주임", "김 반장", "한 기사", "박 기사"]
MECH_P = [0.35, 0.24, 0.19, 0.06, 0.06, 0.05, 0.05]
# 기종별 정비시간 배율 — 리파 R10-5 를 확실히 길게 둔다(교재의 결론)
MODEL_K = {"리파 R10-5": 1.55, "밥캣 E32": 1.10, "구보타 U27-4": 0.95, "캐터필러 304 CR": 0.88}

# ── 달력 ──────────────────────────────────────────────────────
days = pd.date_range("2024-01-01", "2025-11-30", freq="D")
DAYS = list(days[days.dayofweek != 6])                # 정비·부품 기록은 평일·토요일에만
ALL_DAYS = list(days)                                 # 가동 기록은 일요일 특근도 일부 있다

# ══════════════════════════════════════════════════════════════
# 1) 가동 기록 (kpi)
# ══════════════════════════════════════════════════════════════
rows = []
for eq in EQS:
    model = EQ_MODEL[eq]
    for d in ALL_DAYS:
        plan = float(rng.choice([3.0, 3.5, 4.0, 6.0, 8.0], p=[.10, .10, .20, .35, .25]))
        rows.append((d.strftime("%Y-%m-%d"), eq, site_of(eq), plan, d.dayofweek))
kpi = pd.DataFrame(rows, columns=["일자", "장비ID", "거점", "계획가동시간", "_dow"])
w = np.where(kpi["_dow"] == 6, 0.12, 1.0); w = w / w.sum()     # 일요일은 드물게
kpi = (kpi.iloc[rng.choice(len(kpi), 9812, replace=False, p=w)]
          .drop(columns="_dow").sort_values(["일자", "장비ID"]).reset_index(drop=True))

# 기종별 가동률 — 밥캣이 가장 높고 구보타가 가장 낮게
UTIL = {"밥캣 E32": .748, "캐터필러 304 CR": .715, "리파 R10-5": .695, "구보타 U27-4": .686}
kpi["기종_"] = kpi["장비ID"].map(EQ_MODEL)
u = kpi["기종_"].map(UTIL).to_numpy()
noise = rng.normal(0, .12, len(kpi))
ratio = np.clip(u + noise, 0.0, 1.0)
kpi["실제가동시간"] = (kpi["계획가동시간"] * ratio).round(1)
kpi["다운타임(분)"] = 0                                        # 고장이 난 날에만 뒤에서 채운다
kpi["고장건수"] = 0
kpi["비고"] = pd.Series(np.nan, index=kpi.index, dtype=object)

# 기종별 가동률을 목표에 맞춘다 (합계 기준 보정)
for m, target in UTIL.items():
    idx = kpi.index[kpi["기종_"] == m]
    cur = kpi.loc[idx, "실제가동시간"].sum() / kpi.loc[idx, "계획가동시간"].sum()
    kpi.loc[idx, "실제가동시간"] = (kpi.loc[idx, "실제가동시간"] * target / cur).round(1)
    kpi.loc[idx, "실제가동시간"] = np.minimum(kpi.loc[idx, "실제가동시간"], kpi.loc[idx, "계획가동시간"])

# ══════════════════════════════════════════════════════════════
# 2) 정비 이력 (records)
# ══════════════════════════════════════════════════════════════
key = kpi.set_index(["장비ID", "일자"]).index                  # 가동 기록이 있는 (장비, 일자)
avail = {}                                                     # 장비별 가능 일자
for eq, d in key:
    avail.setdefault(eq, []).append(d)

# 유사 중복 4쌍이 뒤에서 더해져 최종 고장수리는 268건이 된다
BREAK_BY_MODEL = {"구보타 U27-4": 65, "리파 R10-5": 68, "밥캣 E32": 87, "캐터필러 304 CR": 44}
WINTER_COLD, WINTER_OTHER, NONWINTER = 41, 51, 172             # 겨울×저온성 교차표 목표(+유사중복 4)

is_winter = lambda ds: int(ds[5:7]) in (11, 12, 1, 2)
cold  = [s for s in BREAK if s[0] in COLD_KW]
warm  = [s for s in BREAK if s[0] not in COLD_KW]

# 기종별 배정량을 겨울저온 / 겨울일반 / 비겨울 세 칸에 비례 배분
plan_cells = []
tot = sum(BREAK_BY_MODEL.values())
for m, n in BREAK_BY_MODEL.items():
    a = round(WINTER_COLD * n / tot); b = round(WINTER_OTHER * n / tot)
    plan_cells.append([m, a, b, n - a - b])
# 반올림 오차를 첫 기종에서 보정
for j, target in enumerate([WINTER_COLD, WINTER_OTHER, NONWINTER], start=1):
    plan_cells[0][j] += target - sum(c[j] for c in plan_cells)

recs, used = [], set()
taken = {}                                                     # 장비별 기록 시각
def pick_day(eq, winter):
    pool = [d for d in avail[eq] if is_winter(d) == winter]
    for _ in range(400):
        d = pool[rng.integers(len(pool))]
        h, mi = int(rng.integers(8, 17)), int(rng.choice([0, 10, 20, 30, 40, 50]))
        t0 = h * 60 + mi
        near = [x for x in taken.get((eq, d), []) if abs(x - t0) <= 40]   # 40분 안에는 다른 기록을 두지 않는다
        if not near:
            taken.setdefault((eq, d), []).append(t0)
            return d, f"{h:02d}:{mi:02d}"
    raise RuntimeError("기록 시각을 잡지 못했습니다")

def add(eq, winter, sym_pool, gubun):
    d, t = pick_day(eq, winter)
    wts = np.array([1.0 if b <= 120 else 0.45 if b <= 220 else 0.12 for *_, b in sym_pool])
    s, part, act, base = sym_pool[rng.choice(len(sym_pool), p=wts / wts.sum())]
    mins = round(base * MODEL_K[EQ_MODEL[eq]] * rng.normal(1.0, .18) / 5) * 5
    recs.append({"장비ID": eq, "고장일시": f"{d} {t}", "구분": gubun, "증상": s,
                 "원인부품": part, "조치방법": act, "정비시간(분)": float(max(20, mins)),
                 "정비기사": rng.choice(MECH, p=MECH_P)})

for m, n_wc, n_wo, n_nw in plan_cells:
    eqs = [e for e in EQS if EQ_MODEL[e] == m]
    for n, winter, pool in [(n_wc, True, cold), (n_wo, True, warm), (n_nw, False, warm)]:
        for _ in range(n):
            add(eqs[rng.integers(len(eqs))], winter, pool, "고장수리")

for _ in range(228):                                            # 정기점검
    eq = EQS[rng.integers(len(EQS))]
    add(eq, bool(rng.integers(2)), CHECK, "정기점검")

df = pd.DataFrame(recs).sort_values("고장일시").reset_index(drop=True)
df.insert(0, "record_id", [f"MR-{i:05d}" for i in range(1, len(df) + 1)])

# 정비기사 표기 흔들림 — 같은 사람을 다르게 적은 기록
for name, alt, n in [("김 반장", "김반장", 7), ("박 기사", "박 기사님", 5), ("최 주임", "최주임", 4)]:
    idx = df.index[df["정비기사"] == name]
    if len(idx) >= n:
        df.loc[rng.choice(idx, n, replace=False), "정비기사"] = alt

# 유사 중복 4쌍 — 같은 장비, 10분 뒤, 표현만 다른 증상
SIM = {"유압 작동 시 이상음": "유압 소리 이상", "트랙 장력 이완": "트랙 헐거움",
       "붐 실린더 누유": "붐실린더 누유", "아이들러 유격": "아이들러 유격 재확인"}
cand = df.index[df["증상"].isin(SIM) & ~df["고장일시"].str[5:7].isin(["11", "12", "01", "02"])]
near = []
for i in rng.choice(cand, 4, replace=False):
    r = df.loc[i].copy()
    ts = pd.to_datetime(r["고장일시"]) + pd.Timedelta(minutes=10)
    r["고장일시"] = ts.strftime("%Y-%m-%d %H:%M")
    r["증상"] = SIM[r["증상"]]
    r["정비시간(분)"] = r["정비시간(분)"] + 10
    near.append(r)
df = pd.concat([df, pd.DataFrame(near)], ignore_index=True)

# 결측 — 원인부품 45칸
df.loc[rng.choice(df.index, 45, replace=False), "원인부품"] = np.nan

# 결측 — 정비시간 20칸 (19건은 그날 정비가 1건뿐이라 다운타임으로 복원된다)
df["_일자"] = df["고장일시"].str[:10]
cnt = df.groupby(["장비ID", "_일자"])["record_id"].transform("count")
solo  = df.index[cnt == 1]
multi = df.index[cnt > 1]
miss = list(rng.choice(solo, 19, replace=False)) + list(rng.choice(multi, 1, replace=False))
df.loc[miss, "정비시간(분)"] = np.nan
df = df.drop(columns="_일자")

# 완전 중복 4행
okd = df["정비시간(분)"].notna() & df["원인부품"].notna()
dup = pd.concat([
    df.loc[rng.choice(df.index[okd & (df["구분"] == "고장수리")], 2, replace=False)],
    df.loc[rng.choice(df.index[okd & (df["구분"] == "정기점검")], 2, replace=False)]])
df = pd.concat([df, dup], ignore_index=True).sort_values("고장일시").reset_index(drop=True)
df["record_id"] = df["record_id"]                               # 중복 행은 record_id 도 같다
COLS = ["record_id", "장비ID", "고장일시", "구분", "증상", "원인부품",
        "조치방법", "정비시간(분)", "정비기사"]
df = df[COLS]

# 가동 기록의 고장건수를 정비 이력과 맞춘다
bd_days = (df[df["구분"] == "고장수리"].assign(일자=lambda x: x["고장일시"].str[:10])
             .groupby(["장비ID", "일자"]).size())
kpi = kpi.set_index(["장비ID", "일자"])
kpi["고장건수"] = bd_days.reindex(kpi.index).fillna(0).astype(int)
kpi = kpi.reset_index()

# 고장이 난 날에는 그만큼 멈춰 있었다 — 다운타임과 실제가동시간을 함께 맞춘다
fault = kpi.index[kpi["고장건수"] > 0]
dt = np.minimum(rng.gamma(2.0, 90, len(fault)) + 30, kpi.loc[fault, "계획가동시간"] * 60).round().astype(int)
kpi.loc[fault, "다운타임(분)"] = dt
kpi.loc[fault, "실제가동시간"] = np.minimum(
    kpi.loc[fault, "실제가동시간"], (kpi.loc[fault, "계획가동시간"] - dt / 60).clip(lower=0)).round(1)

# 예외 20건 — 다운타임이 계획가동시간을 넘는다(하루 종일 멈춰 있던 날)
pool = kpi.index[kpi["고장건수"] > 0]
exc = rng.choice(pool, 20, replace=False)
kpi.loc[exc, "실제가동시간"] = 0.0
kpi.loc[exc, "다운타임(분)"] = (kpi.loc[exc, "계획가동시간"] * 60 + rng.integers(20, 300, 20)).round().astype(int)
kpi.loc[exc[:18], "비고"] = "고장 정지"
kpi.loc[exc[18:], "비고"] = "정기점검"
kpi = kpi[["일자", "장비ID", "거점", "계획가동시간", "실제가동시간", "다운타임(분)", "고장건수", "비고"]]

# ══════════════════════════════════════════════════════════════
# 3) 부품 사용 이력 (parts)
# ══════════════════════════════════════════════════════════════
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
master = pd.DataFrame(MASTER, columns=["부품번호", "부품명", "적용기종"])
master["단가(원)"] = (rng.integers(8, 260, len(master)) * 1000).astype(int)

REASON  = ["소모품 보충", "마모교체", "정기교체", "고장수리"]
REASON_P = [.547, .248, .127, .078]

def parts_for(eq):
    m = EQ_MODEL[eq]
    ok = master[master["적용기종"].isin(["공통", m])]
    return ok.iloc[rng.integers(len(ok))]

def draw(n, eq_weights):
    out = []
    eqs = list(eq_weights); w = np.array([eq_weights[e] for e in eqs], dtype=float); w /= w.sum()
    for _ in range(n):
        eq = rng.choice(eqs, p=w)
        p = parts_for(eq)
        d = DAYS[rng.integers(len(DAYS))]
        out.append((d, eq, p["부품번호"], p["부품명"],
                    int(rng.choice([1, 1, 1, 2, 2, 3, 4])), rng.choice(REASON, p=REASON_P)))
    return pd.DataFrame(out, columns=["일자", "장비ID", "부품번호", "부품명", "수량", "교체사유"]) \
             .sort_values("일자").reset_index(drop=True)

# 본사 2,000행 — 전 거점 장비가 섞여 있고 부산 장비가 가장 많다
w_hq = {e: (3.4 if e[3] == "2" else 3.0 if e[3] == "3" else 1.9) for e in EQS}
hq = draw(2000, w_hq)
hq_out = hq.rename(columns={"일자": "사용일자", "수량": "수량(EA)"}).copy()
hq_out["사용일자"] = hq_out["사용일자"].dt.strftime("%Y-%m-%d")
hq_out = hq_out[["사용일자", "장비ID", "부품번호", "부품명", "수량(EA)", "교체사유"]]

# 부산 1,300행 — 컬럼명이 다르고 날짜는 점 구분, 수량에 '개'가 섞인다
bs = draw(1300, {e: 1.0 for e in EQS if e[3] == "2"})
bs_out = bs.rename(columns={"일자": "일자", "장비ID": "장비", "부품번호": "품번",
                            "부품명": "품명", "수량": "개수", "교체사유": "사유"}).copy()
bs_out["일자"] = bs_out["일자"].dt.strftime("%Y.%m.%d")
mix = rng.choice(bs_out.index, len(bs_out) // 3, replace=False)
bs_out["개수"] = bs_out["개수"].astype(object)
bs_out.loc[mix, "개수"] = bs_out.loc[mix, "개수"].astype(str) + "개"
bs_out = bs_out[["일자", "장비", "품번", "품명", "개수", "사유"]]

# 광주 1,000행 — 영문 컬럼, 미국식 날짜, 사유 표기가 흔들리고 품명이 없다
GJ_MEMO = {"소모품 보충": ["출고", "보충", "소모품"], "마모교체": ["마모로 교체", "마모교체", "마모"],
           "정기교체": ["정기교체", "정기 교체", "주기 도래"], "고장수리": ["고장", "고장수리", "수리건"]}
gj = draw(1000, {e: 1.0 for e in EQS if e[3] == "3"})
gj_out = pd.DataFrame({
    "date": gj["일자"].dt.strftime("%m/%d/%Y"),
    "eq":   gj["장비ID"], "pn": gj["부품번호"], "qty": gj["수량"],
    "memo": [rng.choice(GJ_MEMO[r]) for r in gj["교체사유"]],
})

# 딜러 700행 — 장비ID가 아니라 기종명이고 전부 영문이다(그래서 표준화가 어렵다)
MODEL_SHORT = {"밥캣 E32": "E32", "캐터필러 304 CR": "304 CR",
               "구보타 U27-4": "U27-4", "리파 R10-5": "R10-5"}
EN_REASON = {"소모품 보충": "Stock replenishment", "마모교체": "Wear replacement",
             "정기교체": "Scheduled replacement", "고장수리": "Breakdown repair"}
EN_PART = {"안전벨트": "Seat Belt", "트랙 롤러": "Track Roller", "아이들러": "Idler",
           "엔진오일 필터": "Engine Oil Filter", "연료 필터": "Fuel Filter",
           "에어클리너 엘리먼트": "Air Cleaner Element", "유압 리턴 필터": "Hydraulic Return Filter",
           "냉각수 (4L)": "Coolant (4L)", "작업등 LED": "Work Lamp LED",
           "엔진오일 15W-40 (20L)": "Engine Oil 15W-40 (20L)", "리튬 그리스 (400g)": "Lithium Grease (400g)",
           "고무 트랙 (320mm)": "Rubber Track (320mm)", "고무 트랙 (300mm)": "Rubber Track (300mm)",
           "예열 플러그": "Glow Plug", "파일럿 밸브": "Pilot Valve", "붐 실린더 씰킷": "Boom Cylinder Seal Kit",
           "주행모터 씰킷": "Travel Motor Seal Kit", "유압호스(붐 실린더)": "Hydraulic Hose (Boom Cyl.)",
           "유압호스(암 실린더)": "Hydraulic Hose (Arm Cyl.)"}
dl = draw(700, {e: 1.0 for e in EQS})
dl_out = pd.DataFrame({
    "date": dl["일자"].dt.strftime("%Y-%m-%d"),
    "model": [MODEL_SHORT[EQ_MODEL[e]] for e in dl["장비ID"]],
    "part_no": dl["부품번호"].str.replace("-", "", regex=False),
    "part_name": [EN_PART[n] for n in dl["부품명"]],
    "qty": dl["수량"], "reason": [EN_REASON[r] for r in dl["교체사유"]],
})

# ══════════════════════════════════════════════════════════════
# 4) 저장
# ══════════════════════════════════════════════════════════════
for d in ("records", "kpi", "parts"):
    os.makedirs(d, exist_ok=True)
df.to_csv("records/maintenance_2024_2025.csv", index=False, encoding="utf-8-sig")
kpi.to_csv("kpi/operation_2024_2025.csv", index=False, encoding="utf-8-sig")
master.to_csv("parts/parts_master.csv", index=False, encoding="utf-8-sig")
gj_out.to_csv("parts/parts_issue_gwangju.csv", index=False, encoding="utf-8-sig")
dl_out.to_csv("parts/parts_usage_dealer.csv", index=False, encoding="utf-8-sig")
hq_out.to_excel("parts/parts_usage_hq.xlsx", index=False)
bs_out.to_excel("parts/parts_usage_busan.xlsx", index=False)

# ── 그래프 한글 폰트 ───────────────────────────────────────────
# 교재 [2-1] 이 fonts/NanumGothic-Regular.ttf 를 직접 읽으므로 그 경로에 둔다.
os.makedirs("fonts", exist_ok=True)
FONT_DST = "fonts/NanumGothic-Regular.ttf"
FONT_URL = ("https://raw.githubusercontent.com/aebonlee/materials/main/"
            "build-data/data/NanumGothic-Regular.ttf")
if not os.path.exists(FONT_DST):
    found = glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
    if not found:                                   # 코랩이면 설치해서 쓴다
        try:
            subprocess.run("apt-get -qq install -y fonts-nanum", shell=True,
                           check=False, timeout=180)
            found = glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
        except Exception:
            found = []
    try:
        if found:
            shutil.copy(found[0], FONT_DST)
        else:
            urllib.request.urlretrieve(FONT_URL, FONT_DST)
    except Exception as e:
        print("  ! 한글 폰트를 준비하지 못했습니다:", e)

print("실습 데이터를 만들었습니다.")
print(f"  records/maintenance_2024_2025.csv  {len(df):,}행")
print(f"  kpi/operation_2024_2025.csv        {len(kpi):,}행")
print(f"  parts/  본사 {len(hq_out):,} · 부산 {len(bs_out):,} · 광주 {len(gj_out):,} · 딜러 {len(dl_out):,} · 마스터 {len(master)}")
print(f"  fonts/NanumGothic-Regular.ttf      {'준비됨' if os.path.exists(FONT_DST) else '없음 — 노트북 맨 위 한글 폰트 칸을 실행하세요'}")
print("\n※ 원본 실습 데이터를 대신해 만든 것이라 교재에 인쇄된 숫자와는 다릅니다.")
print("   분석의 결론(리파 R10-5 정비시간이 길다, 겨울에 저온성 고장이 몰린다 등)은 같습니다.")
