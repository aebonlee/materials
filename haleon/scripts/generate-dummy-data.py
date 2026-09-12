#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
헤일리온코리아 Copilot 실무과정 — 실습용 더미 데이터 생성기

  pip3 install openpyxl python-docx
  python3 scripts/generate-dummy-data.py     # materials/haleon 에서 실행

만드는 것 (순서 중요):
  1) haleon-판매데이터-더미.xlsx
  2) haleon-설문원시데이터-더미.xlsx
  3) haleon-회의메모-더미.docx
  4) haleon-보고서샘플-더미.docx   ← 1) 을 읽어 수치를 채운다

4) 가 1) 을 읽는 이유: 2교시 실습이 "요약본의 숫자가 원본과 맞는지 대조"하는 것이라,
보고서에 적힌 값이 엑셀에서 실제로 집계된 값이어야 실습이 성립한다.
난수 시드를 고정해 두었으므로 다시 돌려도 같은 값이 나온다.

모든 값은 가공한 것이며 헤일리온코리아의 실제 데이터가 아니다.
"""
import os
import random
from datetime import datetime

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

SEED = 20260922
FONT = '맑은 고딕'

CHANNELS = ['약국', '이커머스', '대형마트', 'H&B스토어']
CATEGORIES = ['구강케어', '진통·해열', '비타민·보충제', '소화·위장', '호흡기케어']
MONTHS = [f'{m}월' for m in range(1, 13)]
QUARTER = {**{f'{m}월': 'Q1' for m in (1, 2, 3)}, **{f'{m}월': 'Q2' for m in (4, 5, 6)},
           **{f'{m}월': 'Q3' for m in (7, 8, 9)}, **{f'{m}월': 'Q4' for m in (10, 11, 12)}}

BASE = {
    ('약국', '구강케어'): 3200, ('약국', '진통·해열'): 5400, ('약국', '비타민·보충제'): 2600,
    ('약국', '소화·위장'): 3900, ('약국', '호흡기케어'): 3100,
    ('이커머스', '구강케어'): 4100, ('이커머스', '진통·해열'): 2200, ('이커머스', '비타민·보충제'): 6800,
    ('이커머스', '소화·위장'): 1900, ('이커머스', '호흡기케어'): 1700,
    ('대형마트', '구강케어'): 5200, ('대형마트', '진통·해열'): 1800, ('대형마트', '비타민·보충제'): 3400,
    ('대형마트', '소화·위장'): 2100, ('대형마트', '호흡기케어'): 1400,
    ('H&B스토어', '구강케어'): 2900, ('H&B스토어', '진통·해열'): 900, ('H&B스토어', '비타민·보충제'): 4300,
    ('H&B스토어', '소화·위장'): 700, ('H&B스토어', '호흡기케어'): 800,
}
# 계절성 — 호흡기는 겨울, 비타민은 연초에 크다. 5장 '계절성 반영 부족' 서술의 근거가 된다.
SEASON = {
    '호흡기케어':   [1.9, 1.7, 1.2, 0.8, 0.6, 0.5, 0.5, 0.6, 0.9, 1.3, 1.7, 2.0],
    '비타민·보충제': [1.4, 1.2, 1.0, 1.0, 1.0, 0.9, 0.9, 0.9, 1.0, 1.1, 1.2, 1.3],
    '진통·해열':    [1.2, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.1, 1.1, 1.2],
    '구강케어':     [1.0, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.1],
    '소화·위장':    [1.1, 1.0, 1.0, 1.0, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0, 1.2],
}


# ────────────────────────── 공통 헬퍼 ──────────────────────────
def xl_header(ws, cols):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF')
        c.alignment = Alignment(horizontal='center')
        c.fill = PatternFill('solid', fgColor='16202B')


def xl_notice(wb, title, lines, after=-1):
    ws = wb.create_sheet('읽어주세요')
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, size=14)
    for i, line in enumerate(lines, start=2):
        ws.cell(row=i, column=1, value=line)
    ws.column_dimensions['A'].width = 95
    wb.move_sheet('읽어주세요', offset=after)


def setfont(run, size=10.5, bold=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    rf.set(qn('w:eastAsia'), FONT)


def new_doc():
    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.5)
    return d


# ────────────────────────── ① 판매데이터 ──────────────────────────
def build_sales():
    random.seed(SEED)
    wb = Workbook()
    ws = wb.active
    ws.title = '월별판매'
    xl_header(ws, ['연도', '월', '분기', '채널', '카테고리', '매출(만원)', '판매수량'])

    rows = []
    for mi, month in enumerate(MONTHS):
        for ch in CHANNELS:
            for cat in CATEGORIES:
                base = BASE[(ch, cat)] * SEASON[cat][mi]
                sales = int(base * random.uniform(0.85, 1.15))
                qty = int(sales * random.uniform(0.8, 1.3))
                rows.append([2025, month, QUARTER[month], ch, cat, sales, qty])
    for r in rows:
        ws.append(r)
    for col, w in zip('ABCDEFG', [8, 8, 8, 14, 16, 14, 12]):
        ws.column_dimensions[col].width = w

    ws2 = wb.create_sheet('목표대비실적')
    xl_header(ws2, ['월', '채널', '목표(만원)', '실적(만원)'])
    agg = {}
    for r in rows:
        agg[(r[1], r[3])] = agg.get((r[1], r[3]), 0) + r[5]
    for month in MONTHS:
        for ch in CHANNELS:
            actual = agg[(month, ch)]
            ws2.append([month, ch, int(actual * random.uniform(0.82, 1.18)), actual])
    # 목표가 비어 있는 행 2건 — 0 나누기 처리를 사람이 정하게 만드는 장치 (1교시 시연 2)
    # ⚠ ws2.cell(row, column, value=None) 로 쓰면 안 된다.
    #   openpyxl 은 value=None 을 "값 인자를 주지 않았다"로 보고 셀을 건드리지 않는다.
    #   실제로 이걸로 빈칸이 하나도 안 만들어진 채 배포될 뻔했다.
    ws2.cell(row=6, column=3).value = None
    ws2.cell(row=27, column=3).value = None
    for col, w in zip('ABCD', [8, 14, 14, 14]):
        ws2.column_dimensions[col].width = w

    xl_notice(wb, '헤일리온코리아 Copilot 실무과정 — 실습용 더미 데이터', [
        '',
        '이 파일의 모든 숫자는 실습을 위해 만들어 낸 가공 데이터입니다. 실제 매출이 아닙니다.',
        '',
        '[시트 안내]',
        '  월별판매      2025년 채널 × 카테고리 × 월별 매출·수량 (240행)',
        '  목표대비실적  월 × 채널 목표와 실적 (48행). 목표가 비어 있는 행이 2개 섞여 있습니다.',
        '',
        '[Copilot을 쓰기 전에]',
        '  1) 이 파일을 OneDrive 또는 SharePoint에 저장하고 자동 저장을 켜세요.',
        '  2) 데이터 안 아무 셀을 클릭하고 Ctrl + T 를 눌러 표로 지정하세요.',
        '     두 시트 모두 각각 표로 지정해야 합니다.',
        '',
        '자세한 절차는 학습사이트 → 교시별 학습자료 → 1교시 Excel 을 보세요.',
        'https://haleon.dreamitbiz.com/lessons',
    ], after=-2)

    wb.save('haleon-판매데이터-더미.xlsx')
    print(f'  haleon-판매데이터-더미.xlsx  월별판매 {len(rows)}행 / 목표대비실적 48행')


# ────────────────────────── ② 설문 원시데이터 ──────────────────────────
DEPT_VARIANTS = ['영업본부', '영업 본부', '영업본부 ', ' 영업본부', '영업',
                 '마케팅팀', '마케팅 팀', '마케팅팀 ', '마케팅',
                 '재무팀', '재무 팀', '재무팀 ',
                 '인사팀', '인사 팀', 'HR팀',
                 '연구개발본부', '연구개발 본부', 'R&D본부',
                 '생산관리팀', '생산관리 팀']
GRADES = ['사원', '대리', '과장', '차장', '부장']
SUGGEST = [
    '점심시간에 스트레칭 프로그램이 있으면 좋겠습니다',
    '헬스장 제휴 확대 요청드립니다',
    '', '', '',
    '재택 근무일에도 참여할 수 있는 온라인 프로그램을 원합니다',
    '건강검진 항목을 늘려주세요',
    '', '',
    '사내 계단 이용 캠페인 좋았습니다',
    '금연 지원 프로그램이 있으면 합니다',
    '',
    '수면 관리 관련 특강을 듣고 싶습니다',
    '', '',
    '부서별 걷기 대회를 제안합니다',
]


def build_survey():
    random.seed(SEED)
    # 판매데이터와 같은 시드를 쓰되 소비 순서가 다르므로 값은 겹치지 않는다.
    wb = Workbook()
    ws = wb.active
    ws.title = '설문응답'
    xl_header(ws, ['응답ID', '사번', '부서', '직급', '응답일시', '만족도(1-5)', '운동빈도(주)', '건의사항'])

    emp_numbers = [f'H{n:05d}' for n in random.sample(range(10000, 99999), 118)]
    data = []
    for i in range(118):
        day = random.randint(1, 12)
        hour = random.randint(9, 18)
        minute = random.choice([0, 7, 13, 22, 31, 45, 58])
        # 응답일시를 텍스트/날짜 두 형식으로 섞는다 (1교시 시연 3 ④)
        when = (f'2026-09-{day:02d} {hour:02d}:{minute:02d}' if i % 3 == 0
                else datetime(2026, 9, day, hour, minute))
        data.append([f'R{i+1:04d}', emp_numbers[i], random.choice(DEPT_VARIANTS),
                     random.choice(GRADES), when,
                     random.choice([1, 2, 3, 3, 4, 4, 4, 5, 5, None, None]),
                     random.choice([0, 0, 1, 1, 2, 2, 3, 3, 4, 5]),
                     random.choice(SUGGEST)])

    # 중복 응답 6건 — 클라이언트가 아니라 사람이 눈으로 확인하게 만드는 장치
    for src in random.sample(range(len(data)), 6):
        dup = list(data[src])
        dup[0] = f'R{len(data)+1:04d}'
        dup[5] = random.choice([1, 2, 3, 4, 5])
        data.append(dup)
    random.shuffle(data)
    for r in data:
        ws.append(r)
    for col, w in zip('ABCDEFGH', [10, 10, 16, 8, 20, 14, 13, 46]):
        ws.column_dimensions[col].width = w

    xl_notice(wb, '헤일리온코리아 Copilot 실무과정 — 설문 원시데이터 (실습용)', [
        '',
        '가상의 사내 웰빙 설문을 시스템에서 내려받은 형태 그대로 만든 파일입니다.',
        '실제 응답이 아니며 사번·부서·건의사항 모두 가공한 값입니다.',
        '',
        '[일부러 심어 둔 지저분함 — 1교시 시연 3에서 정리합니다]',
        '  · 같은 사번이 두 번 응답한 행이 6건 있습니다',
        '  · 부서명 표기가 제각각입니다 (영업본부 / 영업 본부 / 영업본부_뒤에공백 / 영업)',
        '  · 만족도 열에 빈 값이 섞여 있습니다',
        '  · 응답일시에 텍스트와 날짜 값이 섞여 있습니다',
        '',
        '[중요] 정리 작업은 반드시 사본에서 하세요.',
        '  [파일] → [사본 저장] 으로 원본을 남겨 두고 시작합니다.',
        '',
        '자세한 절차는 학습사이트 → 교시별 학습자료 → 1교시 Excel → 시연 3 을 보세요.',
    ], after=-1)

    wb.save('haleon-설문원시데이터-더미.xlsx')
    print(f'  haleon-설문원시데이터-더미.xlsx  설문응답 {len(data)}행 (중복 6건 포함)')


# ────────────────────────── ③ 회의 메모 ──────────────────────────
MEMO = """9/15 월 14시~15시10분 3층 회의실
참석 - 인사팀 김OO 팀장, 인사팀 박OO, 마케팅 이OO, 총무 정OO, 안전보건 최OO (연구개발본부 담당자는 불참, 나중에 공유하기로)

- 올해 웰빙 프로그램 참여율이 낮다는 얘기 나옴. 작년보다 떨어졌다고 함. 정확한 수치는 인사팀에서 다시 뽑기로
- 이OO: 홍보가 부족했던 것 같다. 사내 게시판만 썼는데 아무도 안 본다고
- 정OO: 엘리베이터 모니터 활용 가능. 총무팀에서 슬롯 확보 가능한지 확인해본다고 함
- 최OO: 안전보건 쪽 캠페인이랑 묶으면 예산 같이 쓸 수 있을듯. 근데 예산 승인은 아직

*** 숏폼 영상 만들자는 얘기 (이OO 제안) ***
- 30초 정도. 엘리베이터 모니터랑 사내 게시판 동시 게시
- 주제는 점심시간 걷기. 15분만 걸어도 오후 집중력 달라진다는 내용
- 톤은 가볍게. 훈계하는 느낌 나면 역효과라고 다들 동의함

- 김팀장: 제품 관련 내용은 절대 넣지 말 것. 심의 이슈. 사내 캠페인 소재만
- 박OO: 설문 결과 보니까 스트레칭 프로그램 요청이 제일 많았음. 걷기랑 같이 갈 수 있는지 검토

일정 관련
- 10월 중 런칭 목표인데 확정 아님
- 영상 시안은 9월말까지 보기로? (이OO가 만들어오기로 한 것 같은데 확실치 않음)
- 예산은 다음 회의 전까지 최OO가 안전보건 예산 항목 확인

기타
- 부서별 걷기 대회 아이디어 나왔는데 이번엔 안 하기로. 인원 관리가 어렵다고
- 재택근무자 참여 방법 논의 필요. 결론 안 남
- 다음 회의 9/22 같은 시간 (변경될 수 있음)

--- 메모 끝 ---
※ 참석자 이름/부서는 확인 필요. 급하게 적어서 직급 틀렸을 수 있음"""


def build_memo():
    d = new_doc()

    def para(text, size=10.5, bold=False, after=6):
        p = d.add_paragraph()
        setfont(p.add_run(text), size, bold)
        p.paragraph_format.space_after = Pt(after)

    para('웰빙캠페인 킥오프 회의 메모', 14, True)
    para('(회의 중 받아적은 메모 — 정리 안 됨)', 9)
    d.add_paragraph()
    for line in MEMO.split('\n'):
        if line.strip() == '':
            d.add_paragraph()
        else:
            para(line, 10.5, after=2)
    d.save('haleon-회의메모-더미.docx')
    print('  haleon-회의메모-더미.docx')


# ────────────────────────── ④ 보고서 샘플 ──────────────────────────
def build_report():
    wb = load_workbook('haleon-판매데이터-더미.xlsx', data_only=True)
    rows = list(wb['월별판매'].iter_rows(min_row=2, values_only=True))
    by_ch, by_cat, by_q, by_cat_m = {}, {}, {}, {}
    for _, month, q, ch, cat, sales, _qty in rows:
        by_ch[ch] = by_ch.get(ch, 0) + sales
        by_cat[cat] = by_cat.get(cat, 0) + sales
        by_q[q] = by_q.get(q, 0) + sales
        by_cat_m[(cat, month)] = by_cat_m.get((cat, month), 0) + sales
    total = sum(by_ch.values())
    tgt = act = 0
    skipped = 0
    for _month, _ch, t, a in wb['목표대비실적'].iter_rows(min_row=2, values_only=True):
        if t:
            tgt += t
            act += a
        else:
            skipped += 1   # 목표가 빈 구간은 달성률 산정에서 제외 (보고서 6장 서술과 일치시킨다)
    rate = act / tgt * 100
    resp_jan, resp_jul = by_cat_m[('호흡기케어', '1월')], by_cat_m[('호흡기케어', '7월')]

    def eok(v):
        return f'{v/10000:.1f}억 원'

    r = new_doc()

    def para(text, size=10.5, bold=False, align=None, after=8):
        p = r.add_paragraph()
        setfont(p.add_run(text), size, bold)
        if align:
            p.alignment = align
        p.paragraph_format.space_after = Pt(after)

    def heading(text, level=1):
        p = r.add_paragraph()
        setfont(p.add_run(text), {1: 15, 2: 12.5}[level], True)
        p.paragraph_format.space_before = Pt(18 if level == 1 else 12)
        p.paragraph_format.space_after = Pt(6)

    def bullets(items):
        for it in items:
            p = r.add_paragraph(style='List Bullet')
            setfont(p.add_run(it), 10.5)
            p.paragraph_format.space_after = Pt(4)

    def table(cols, data):
        t = r.add_table(rows=1, cols=len(cols))
        t.style = 'Light Grid Accent 1'
        for i, c in enumerate(cols):
            setfont(t.rows[0].cells[i].paragraphs[0].add_run(c), 10, True)
        for row in data:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                setfont(cells[i].paragraphs[0].add_run(str(v)), 10)
        r.add_paragraph()

    para('2025년 채널별 판매 실적 분석 및\n2026년 운영 방향 보고', 18, True, WD_ALIGN_PARAGRAPH.CENTER)
    para('\n\n(실습용 가상 보고서 — 실제 데이터가 아닙니다)\n\n영업기획팀 · 2026. 09.', 10, align=WD_ALIGN_PARAGRAPH.CENTER)
    r.add_page_break()

    heading('1. 개요')
    para(f'본 보고서는 2025년 한 해 동안의 채널별·카테고리별 판매 실적을 정리하고, 이를 바탕으로 2026년 운영 방향을 '
         f'검토하기 위해 작성했다. 분석 대상 기간의 총 매출은 {eok(total)}이며, 4개 유통 채널(약국, 이커머스, '
         f'대형마트, H&B스토어)과 5개 카테고리(구강케어, 진통·해열, 비타민·보충제, 소화·위장, 호흡기케어)를 대상으로 한다.')
    para('보고서는 크게 세 부분으로 구성된다. 3장부터 5장까지는 실적 현황을 채널·카테고리·분기 관점에서 정리했고, '
         '6장과 7장은 목표 대비 달성 현황과 그 과정에서 확인된 문제를 다룬다. 8장 이후는 개선 방향과 2026년 계획, '
         '그리고 의사결정이 필요한 항목을 정리했다.')
    para('본 보고서의 모든 수치는 첨부한 「haleon-판매데이터-더미.xlsx」에서 집계한 값이다. 요약본을 만들 때 숫자가 '
         '정확히 옮겨졌는지 이 파일과 대조할 수 있다.')

    heading('2. 추진 배경')
    para('최근 2년간 유통 채널별 성과 편차가 확대되면서, 전 채널에 동일한 운영 기준을 적용하는 방식이 한계에 이르렀다는 '
         '문제 제기가 영업 현장에서 반복적으로 있었다. 특히 이커머스 채널의 비중이 빠르게 늘어나는 가운데, '
         '카테고리별로는 그 성장이 고르지 않다는 점이 확인되었다.')
    para('한편 목표 수립 방식이 채널의 특성을 충분히 반영하지 못한다는 지적도 있었다. 채널별로 목표를 세우는 기준이 '
         '서로 달라 달성률을 나란히 놓고 비교하기 어렵다는 것이다. 이 두 가지 문제의식이 본 분석의 출발점이다.')
    bullets([
        '유통 채널별 성과 편차 확대에 따른 채널별 운영 전략의 필요성',
        '이커머스 비중 확대에도 불구하고 카테고리별로 고르지 않은 성장',
        '채널 특성을 반영하지 못하는 목표 수립 방식에 대한 현장 의견',
        '판매 데이터와 목표 데이터의 관리 체계 분리로 인한 집계 부담',
    ])

    heading('3. 채널별 판매 현황')
    para(f'2025년 총 매출은 {eok(total)}이며, 채널별 구성은 다음과 같다.')
    table(['채널', '매출', '비중'],
          [[ch, eok(v), f'{v/total*100:.1f}%'] for ch, v in sorted(by_ch.items(), key=lambda x: -x[1])])
    top_ch, low_ch = max(by_ch, key=by_ch.get), min(by_ch, key=by_ch.get)
    para(f'{top_ch} 채널이 {eok(by_ch[top_ch])}으로 가장 큰 비중을 차지했고, {low_ch} 채널이 {eok(by_ch[low_ch])}으로 '
         f'가장 작았다. 두 채널의 격차는 {by_ch[top_ch]/by_ch[low_ch]:.2f}배다.')
    para('다만 채널별 절대 규모만으로 성과를 판단하기는 어렵다. 채널마다 취급 카테고리 구성이 다르고, 마진 구조도 '
         '동일하지 않기 때문이다. 예를 들어 H&B스토어는 매출 규모는 가장 작지만 비타민·보충제 카테고리의 비중이 높아 '
         '카테고리 전략 측면에서는 별도의 검토가 필요하다.')
    para('이커머스 채널은 비타민·보충제와 구강케어에 매출이 집중되어 있고, 진통·해열과 소화·위장 카테고리의 비중은 '
         '낮게 나타났다. 오프라인 구매가 여전히 우세한 카테고리가 존재한다는 뜻으로, 채널별로 밀어야 할 카테고리를 '
         '구분할 필요가 있음을 시사한다.')

    heading('4. 카테고리별 판매 현황')
    table(['카테고리', '매출', '비중'],
          [[c, eok(v), f'{v/total*100:.1f}%'] for c, v in sorted(by_cat.items(), key=lambda x: -x[1])])
    top_cat = max(by_cat, key=by_cat.get)
    para(f'{top_cat}가 {eok(by_cat[top_cat])}으로 가장 큰 비중을 차지했다. 카테고리 간 격차는 채널 간 격차보다 '
         '완만한 편이나, 이는 연간 합계 기준이라는 점을 감안해야 한다.')
    para(f'특히 호흡기케어는 연간 합계로는 중위권이지만 계절 편차가 가장 크다. 1월 매출이 {eok(resp_jan)}인 반면 '
         f'7월은 {eok(resp_jul)}으로 {resp_jan/resp_jul:.1f}배 차이가 난다. 연간 평균으로 재고와 목표를 운영하면 '
         '겨울에는 결품이, 여름에는 과잉 재고가 발생하는 구조다.')
    para('비타민·보충제는 연초에 매출이 집중되는 경향이 뚜렷하다. 새해 건강 관리 수요와 관련이 있는 것으로 보이며, '
         '이 시기에 맞춘 프로모션 설계가 효과적일 것으로 판단된다. 반면 구강케어와 소화·위장은 계절 편차가 작아 '
         '연중 고른 운영이 가능하다.')

    heading('5. 분기별 추이')
    table(['분기', '매출', '비중'], [[q, eok(by_q[q]), f'{by_q[q]/total*100:.1f}%'] for q in ['Q1', 'Q2', 'Q3', 'Q4']])
    para(f'Q1이 {eok(by_q["Q1"])}으로 가장 높고 Q3가 {eok(by_q["Q3"])}으로 가장 낮다. 호흡기케어와 비타민·보충제의 '
         '계절성이 이 편차를 대부분 설명한다. 두 카테고리를 제외하면 분기별 편차는 크게 줄어든다.')
    para('분기별 편차 자체가 문제는 아니다. 문제는 이 편차가 목표 배분에 반영되지 않는다는 점이다. 현재 월 목표는 '
         '연간 목표를 12로 나눈 균등 배분 방식이어서, 계절성이 큰 카테고리에서는 특정 월에 구조적인 미달 또는 초과가 '
         '반복적으로 발생한다.')

    heading('6. 목표 대비 달성 현황')
    para(f'2025년 전체 목표 대비 달성률은 {rate:.1f}%다. 전체 수치로는 목표에 근접했으나, 채널별·월별로 들어가면 '
         '편차가 크게 나타난다.')
    para('달성률을 해석할 때 주의할 점이 두 가지 있다. 첫째, 목표 수립 시점의 기준이 채널마다 달라 단순 비교에는 '
         '한계가 있다. 전년 실적을 기준으로 잡은 채널과 시장 성장률을 기준으로 잡은 채널이 섞여 있기 때문이다.')
    para(f'둘째, 원본 데이터의 목표 항목 중 {skipped}건이 비어 있다. 해당 구간은 이번 집계에서 달성률 산정 대상에서 제외했다. '
         '비어 있는 목표를 0으로 볼 것인지 제외할 것인지에 따라 전체 달성률이 달라지므로, 이 처리 방식을 그대로 '
         '유지할지 여부는 별도 결정이 필요하다.')

    heading('7. 주요 이슈')
    heading('7-1. 목표 설정 기준의 불일치', 2)
    para('채널별로 목표 수립 방식이 달라 달성률을 나란히 놓고 비교하기 어렵다. 전년 실적 기준으로 잡은 채널과 '
         '시장 성장률 기준으로 잡은 채널이 섞여 있어, 달성률이 높은 채널이 실제로 더 잘한 것인지 목표가 낮았던 것인지 '
         '구분되지 않는다. 이는 성과 평가와 자원 배분 모두에 영향을 미친다.')
    heading('7-2. 데이터 품질', 2)
    para('판매 데이터와 목표 데이터가 서로 다른 시스템에서 관리되어 채널명 표기가 통일되어 있지 않다. 집계할 때마다 '
         '수작업 대조가 발생하고, 그 과정에서 누락이나 중복이 생길 여지가 있다. 실제로 이번 분석에서도 채널명 매칭에 '
         '상당한 시간이 소요되었다.')
    heading('7-3. 계절성 반영 부족', 2)
    para('월 목표가 연간 목표의 1/12로 균등 배분되어 있어, 계절성이 큰 카테고리에서 특정 월에 과도한 미달 또는 초과가 '
         '나타난다. 현장에서는 이를 "달성 불가능한 여름 목표"로 인식하고 있으며, 목표에 대한 신뢰를 떨어뜨리는 요인이 되고 있다.')

    heading('8. 개선 방향')
    bullets([
        '목표 수립 기준을 채널 구분 없이 통일한다. 기준안은 영업기획팀에서 10월 중 제시한다.',
        '판매·목표 데이터의 채널명 표기 체계를 하나로 정리하고, 마스터 코드를 지정한다.',
        '계절성이 큰 카테고리는 월 목표를 계절 지수로 보정해 배분한다.',
        '달성률 산정에서 목표가 비어 있는 구간을 어떻게 처리할지 규칙을 문서화한다.',
        '채널별 카테고리 구성 차이를 반영한 보조 지표를 추가로 도입한다.',
    ])

    heading('9. 2026년 운영 계획')
    table(['구분', '내용', '시점'], [
        ['목표 기준 통일안 수립', '채널 공통 기준안 마련 및 관련 부서 협의', '2026년 10월'],
        ['채널 마스터 코드 정비', '판매·목표 시스템의 채널명 표기 통일', '2026년 11월'],
        ['계절 지수 반영', '카테고리별 월 배분 로직 설계 및 적용', '2026년 12월'],
        ['2026년 목표 확정', '신규 기준으로 채널별·카테고리별 목표 확정', '2026년 1월'],
        ['운영 결과 1차 점검', '신규 기준 적용 후 첫 분기 결과 검토', '2026년 4월'],
    ])

    heading('10. 결정이 필요한 사항')
    bullets([
        '목표 기준 통일안의 적용 시점 — 2026년 하반기부터인지 2026년 초부터인지',
        '목표가 비어 있는 구간의 달성률 처리 방식 — 제외할지 0으로 볼지',
        '채널 마스터 코드 정비의 주관 부서 — 영업기획팀인지 정보시스템팀인지',
        '계절 지수 산출에 사용할 기준 기간 — 최근 1년인지 3년 평균인지',
    ])
    para('')
    para('※ 본 문서는 Copilot 실습을 위해 작성한 가상 보고서다. 회사의 실제 실적·계획과 무관하다.', 9)

    r.save('haleon-보고서샘플-더미.docx')
    print(f'  haleon-보고서샘플-더미.docx  (총매출 {eok(total)} / 달성률 {rate:.1f}%)')


# ────────────────────────── 자체 검증 ──────────────────────────
def verify():
    """만든 파일이 의도한 모양인지 확인한다.
    '심어 둔 지저분함'은 실습의 재료다. 조용히 빠지면 시연이 성립하지 않는데
    파일은 멀쩡히 열리므로 눈으로는 안 잡힌다."""
    from collections import Counter
    bad = []

    wb = load_workbook('haleon-판매데이터-더미.xlsx')
    if wb.sheetnames != ['읽어주세요', '월별판매', '목표대비실적']:
        bad.append(f'판매 시트 구성이 다름: {wb.sheetnames}')
    if wb['월별판매'].max_row != 241:
        bad.append(f'월별판매 행 수: {wb["월별판매"].max_row - 1} (240 이어야 함)')
    tg = list(wb['목표대비실적'].iter_rows(min_row=2, values_only=True))
    if len(tg) != 48:
        bad.append(f'목표대비실적 행 수: {len(tg)} (48 이어야 함)')
    blanks = sum(1 for r in tg if r[2] is None)
    if blanks != 2:
        bad.append(f'목표 빈 값이 2건이 아님: {blanks}건')

    wb2 = load_workbook('haleon-설문원시데이터-더미.xlsx')
    rows = list(wb2['설문응답'].iter_rows(min_row=2, values_only=True))
    if len(rows) != 124:
        bad.append(f'설문 행 수: {len(rows)} (124 이어야 함)')
    dups = sum(v - 1 for v in Counter(r[1] for r in rows).values() if v > 1)
    if dups != 6:
        bad.append(f'중복 사번이 6건이 아님: {dups}건')
    if not any(r[5] is None for r in rows):
        bad.append('만족도 빈 값이 하나도 없음')
    kinds = {type(r[4]).__name__ for r in rows}
    if kinds != {'str', 'datetime'}:
        bad.append(f'응답일시 형식이 섞여 있지 않음: {kinds}')
    variants = {r[2] for r in rows if r[2].strip().startswith('영업')}
    if len(variants) < 3:
        bad.append(f'부서 표기 흔들림이 부족함: {variants}')

    for f, min_chars, min_tables in [('haleon-회의메모-더미.docx', 700, 0),
                                     ('haleon-보고서샘플-더미.docx', 3000, 4)]:
        d = Document(f)
        ps = [p.text for p in d.paragraphs if p.text.strip()]
        chars = sum(len(p) for p in ps)
        if chars < min_chars:
            bad.append(f'{f}: 본문 {chars}자 (최소 {min_chars}자)')
        if len(d.tables) < min_tables:
            bad.append(f'{f}: 표 {len(d.tables)}개 (최소 {min_tables}개)')

    if bad:
        print('\n✗ 검증 실패')
        for b in bad:
            print('  ·', b)
        raise SystemExit(1)
    # 사이트(datasets.ts)가 화면에 적어 둔 행 수·용량이 실물과 맞는지
    # 저쪽 검사기(npm run check)가 대조할 수 있도록 실측값을 남긴다.
    import json
    manifest = {
        'generatedBy': 'scripts/generate-dummy-data.py',
        'seed': SEED,
        'files': {
            'haleon-판매데이터-더미.xlsx': {
                'bytes': os.path.getsize('haleon-판매데이터-더미.xlsx'),
                'sheets': wb.sheetnames,
                'rows': {'월별판매': wb['월별판매'].max_row - 1, '목표대비실적': len(tg)},
                'emptyTargets': blanks,
            },
            'haleon-설문원시데이터-더미.xlsx': {
                'bytes': os.path.getsize('haleon-설문원시데이터-더미.xlsx'),
                'sheets': wb2.sheetnames,
                'rows': {'설문응답': len(rows)},
                'duplicateEmployees': dups,
            },
            'haleon-회의메모-더미.docx': {'bytes': os.path.getsize('haleon-회의메모-더미.docx')},
            'haleon-보고서샘플-더미.docx': {
                'bytes': os.path.getsize('haleon-보고서샘플-더미.docx'),
                'tables': len(Document('haleon-보고서샘플-더미.docx').tables),
            },
        },
    }
    with open('manifest.json', 'w', encoding='utf-8') as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2)

    print('  검증 통과 — 목표 빈 값 2건 / 중복 사번 6건 / 일시 형식 혼재 / 부서 표기 흔들림 확인')
    print('  manifest.json 갱신 (사이트 검사기가 화면 표기와 대조한다)')


if __name__ == '__main__':
    here = os.path.basename(os.getcwd())
    if here != 'haleon':
        raise SystemExit('materials/haleon 폴더에서 실행하세요. 현재: ' + os.getcwd())
    print('실습 데이터 생성 (시드 %d)' % SEED)
    build_sales()      # ① 먼저
    build_survey()
    build_memo()
    build_report()     # ④ 는 ① 을 읽는다
    verify()
    print('완료')
