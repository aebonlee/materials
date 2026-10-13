"""python-docx 로 만든 .docx 는 settings.xml 의 compatibilityMode 가 14(Word 2010)라 Word 가 「호환성 모드」로 연다.
그 상태에서는 Word 데스크톱에 Copilot 단추가 나오지 않는다(2026-10-13 애본님 화면에서 확인).
→ <w:compat><w:compatSetting compatibilityMode=15/></w:compat> 를 넣어 현재 형식(Word 2013 이후)으로 표시한다. 본문은 건드리지 않는다.
실행: python3 scripts/fix-docx-compat.py *.docx   (두 생성기 끝에서도 부른다)
"""
import os, re, shutil, sys, tempfile, zipfile
TAG = ('<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
       '<w:compatSetting w:name="overrideTableStyleFontSizeAndJustification" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
       '<w:compatSetting w:name="enableOpenTypeFeatures" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
       '<w:compatSetting w:name="doNotFlipMirrorIndents" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/></w:compat>')

def fix(path):
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    out = []
    changed = False
    for info, data in items:
        if info.filename == 'word/settings.xml':
            s = data.decode('utf-8')
            if 'compatibilityMode' in s:
                s2 = re.sub(r'(w:name="compatibilityMode"[^>]*?w:val=")1[0-4](")', r'\g<1>15\2', s)
                if s2 != s: s, changed = s2, True
                data = s.encode('utf-8')
            else:
                s = re.sub(r'<w:compat\s*/>|<w:compat>.*?</w:compat>', '', s, flags=re.S)
                # 스키마 순서상 compat 은 rsids 앞, 없으면 맨 끝
                s = s.replace('<w:rsids>', TAG + '<w:rsids>', 1) if '<w:rsids>' in s else s.replace('</w:settings>', TAG + '</w:settings>', 1)
                data = s.encode('utf-8'); changed = True
        out.append((info, data))
    if changed:
        fd, tmp = tempfile.mkstemp(suffix='.docx', dir=os.path.dirname(os.path.abspath(path))); os.close(fd)
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            for info, data in out: z.writestr(info, data)
        shutil.move(tmp, path)
    return changed

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(('고침 ' if fix(p) else '그대로 ') + p)
