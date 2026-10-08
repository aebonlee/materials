"""
클레임 리뷰 실습 파일 2종 (2차수 교육생 질문 반영, 2026-10-08)

  haleon-광고가이드라인-발췌.docx  — 식약처 「의약외품 표시·광고 가이드라인」(2025-04-14) 중
                                     III. 광고 가이드라인 장만 발췌. 원본 PDF 52쪽은 Copilot 참조에
                                     너무 길어 광고 장(약 17쪽)만 떼어 둔다.
  haleon-광고문안-샘플.docx         — 가상 의약외품(손소독제) 광고 문안. 가이드라인 3.2 절의
                                     부적합 유형을 일부러 섞어 두었다. 실제 제품·브랜드가 아니다.

실행: materials/haleon 폴더에서  python3 scripts/make-claim-review-files.py
원본 PDF: haleon-의약외품-표시광고-가이드라인.pdf (식약처 민원인 안내서, 공개 자료)
"""
import os, re, subprocess
from docx import Document
from docx.shared import Pt

PDF = 'haleon-의약외품-표시광고-가이드라인.pdf'
EXCERPT = 'haleon-광고가이드라인-발췌.docx'
SAMPLE = 'haleon-광고문안-샘플.docx'


def pdf_pages(path):
    txt = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, check=True).stdout
    return txt.split('\f')


def build_excerpt():
    pages = pdf_pages(PDF)
    # 인쇄 쪽 번호(- 19 - … - 35 -)로 장 경계를 잡는다. 목차가 III장을 19~35쪽이라 한다.
    foot = lambda n: re.compile(r'-\s*%d\s*-' % n)
    start = next(i for i, p in enumerate(pages) if foot(19).search(p))
    end = next(i for i, p in enumerate(pages) if foot(35).search(p)) + 1
    doc = Document()
    st = doc.styles['Normal']; st.font.name = 'Malgun Gothic'; st.font.size = Pt(10)
    doc.add_heading('의약외품 표시·광고 가이드라인 — III. 광고 가이드라인 (발췌)', 0)
    doc.add_paragraph('출처: 식품의약품안전처 바이오생약국 의약외품정책과, 「의약외품 표시·광고 가이드라인(민원인 안내서)」 2025. 4. 14. '
                      '원본 PDF 중 III장(광고 가이드라인)만 Copilot 참조용으로 떼어 낸 것입니다. '
                      '안내서는 법적 효력을 갖지 않는 참고 자료이며, 최종 판단은 최신 법령과 담당 부서 확인에 따릅니다.')
    doc.add_paragraph(f'원본 PDF 쪽: {start + 1} ~ {end} (인쇄 쪽 번호 19 ~ 35)')
    for i in range(start, end):
        for line in pages[i].split('\n'):
            s = line.strip()
            if not s or re.fullmatch(r'-\s*\d+\s*-', s):
                continue
            if re.match(r'^3\.\d\.\d\.?\s', s):
                doc.add_heading(s, 2)
            elif re.match(r'^3\.\d\.?\s', s):
                doc.add_heading(s, 1)
            else:
                doc.add_paragraph(re.sub(r'\s{2,}', ' ', s))
    doc.save(EXCERPT)
    return start, end


# 가상 제품. 가이드라인 3.2 절의 부적합 유형을 문장마다 하나씩 심었다 (정답표는 사이트 2교시 자료).
SAMPLE_LINES = [
    ('제목', '[광고 문안 초안] 클린핸드 겔 — 손소독제 (가상 제품)'),
    ('안내', '매체: 사내 뉴스레터 · 온라인몰 상세페이지 / 작성: 마케팅팀 / 상태: 내부 리뷰 전'),
    ('본문', '① 클린핸드 겔은 99.9% 세균 제거는 물론, 피부염과 아토피까지 진정시켜 주는 손소독제입니다.'),
    ('본문', '② 임상시험으로 효능이 입증된 제품이라 믿고 쓰실 수 있습니다.'),
    ('본문', '③ 피부과 전문의가 추천하는 손소독제, 약사들이 먼저 찾는 제품입니다.'),
    ('본문', '④ 부작용이 전혀 없어 아이에게도 100% 안전합니다.'),
    ('본문', '⑤ 국내 최고의 살균력, 타사 제품보다 2배 강력합니다.'),
    ('본문', '⑥ 100% 천연·유기농 성분으로 만들어 피부에 순합니다.'),
    ('본문', '⑦ 식약처가 추천하는 프리미엄 손소독제입니다.'),
    ('본문', '⑧ 물과 비누로 손을 씻기 어려울 때 적당량을 손에 덜어 마를 때까지 문질러 주세요.'),
    ('본문', '⑨ 눈에 들어갔을 때는 즉시 물로 씻어 내고, 이상이 있으면 의사·약사와 상담하세요.'),
    ('본문', '⑩ 어린이의 손이 닿지 않는 곳에 보관하고, 사용 후 뚜껑을 닫아 주세요.'),
    ('안내', '※ 이 문안은 교육용 가상 사례입니다. 실제 제품·브랜드·허가사항과 무관합니다.'),
]


def build_sample():
    doc = Document()
    st = doc.styles['Normal']; st.font.name = 'Malgun Gothic'; st.font.size = Pt(11)
    for kind, text in SAMPLE_LINES:
        if kind == '제목':
            doc.add_heading(text, 0)
        elif kind == '안내':
            p = doc.add_paragraph(); r = p.add_run(text); r.italic = True
        else:
            doc.add_paragraph(text)
    doc.save(SAMPLE)


if __name__ == '__main__':
    if os.path.basename(os.getcwd()) != 'haleon':
        raise SystemExit('materials/haleon 폴더에서 실행하세요')
    if not os.path.exists(PDF):
        raise SystemExit(f'{PDF} 없음')
    s, e = build_excerpt()
    build_sample()
    d = Document(EXCERPT)
    n = len([p for p in d.paragraphs if p.text.strip()])
    assert n > 150, f'발췌본 문단이 {n}개뿐 — 장 경계를 잘못 잡았다'
    assert any('3.2.4' in p.text for p in d.paragraphs), '3.2.4 절이 발췌본에 없다'
    assert not any('질의응답' in p.text and p.style.name.startswith('Heading') for p in d.paragraphs), 'IV장이 섞여 들어갔다'
    print(f'  {EXCERPT}: PDF {s+1}~{e}쪽, 문단 {n}개')
    print(f'  {SAMPLE}: 문장 {len([l for l in SAMPLE_LINES if l[0]=="본문"])}개')
