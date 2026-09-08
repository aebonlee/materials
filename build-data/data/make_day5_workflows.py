# -*- coding: utf-8 -*-
"""
DAY 5 n8n 워크플로 생성기 (대체 자료)

교재 PART 05 가 쓰는 두 파일을 만든다.
  sheet_prep.json        교재 8절 「제공된 준비용 워크플로 파일」 — 시트 저장소를 마련한다
  checklist_intake.json  교재 10절 「배포된 checklist_intake.json」 — 완성본(노드 7개)

불러오기: n8n 화면 오른쪽 위 … → Import from File

노드 구성 (수집 → 가공 → 출력)
  ① 점검표 제출 폼 (Form)   ② 사진 준비 (Code)      ③ Gemini 호출 (HTTP Request)
  ④ 응답 정리 (Code)        ⑤ 시트 적재 (Sheets)     ⑥ 불량 있음? (IF)   ⑦ Slack 알림 (Slack)

자격증명은 파일에 담기지 않는다. 불러온 뒤 각자 만들어 둔 것을 고르면 된다.
"""
import json, os

def node(name, ntype, ver, pos, params, **extra):
    n = {"parameters": params, "name": name, "type": ntype,
         "typeVersion": ver, "position": pos, "id": name}
    n.update(extra)
    return n

def conn(pairs):
    """pairs = [(from, to, outputIndex)]"""
    c = {}
    for src, dst, idx in pairs:
        c.setdefault(src, {"main": []})
        while len(c[src]["main"]) <= idx:
            c[src]["main"].append([])
        c[src]["main"][idx].append({"node": dst, "type": "main", "index": 0})
    return c

CODE_PREP = """// 폼으로 올라온 사진을 Gemini 가 받는 형태(base64)로 바꿉니다.
const item = $input.first();
const key = Object.keys(item.binary || {})[0];
if (!key) { throw new Error('사진이 없습니다. 폼에서 점검표 사진을 첨부했는지 확인하세요.'); }
const bin = item.binary[key];
const buf = await this.helpers.getBinaryDataBuffer(0, key);
// 프롬프트도 여기서 함께 내보냅니다.
// (HTTP 노드 표현식 안에 중괄호가 든 글을 그대로 적으면 n8n 표현식이 중간에서 끊깁니다)
const prompt = [
  '이 사진은 굴착기 일일점검표입니다. 아래 형식의 JSON 으로만 답하세요.',
  '{"장비ID": "", "점검일자": "YYYY-MM-DD", "점검자": "",',
  ' "항목": {"<항목명>": {"판정": "양호|불량", "비고": ""}}, "특이사항": ""}',
  '항목명은 사진에 적힌 그대로 쓰고, JSON 외의 말은 쓰지 마세요.'
].join(String.fromCharCode(10));
return [{ json: { mime: bin.mimeType || 'image/jpeg', data: buf.toString('base64'), prompt } }];"""

CODE_CLEAN = """// 모델 응답에서 값만 꺼내 시트·알림이 쓸 일곱 항목으로 정리합니다.
const raw = $json.candidates[0].content.parts[0].text;      // ① 모델이 쓴 글만 꺼낸다
const clean = raw.replace(/```json|```/g, '').trim();        // ② 코드펜스를 걷어낸다
const ext = JSON.parse(clean);                               // ③ JSON 으로 바꾼다
const bad = Object.entries(ext['항목'] || {})                 // ④ 불량 항목만 고른다
  .filter(([k, v]) => v['판정'] === '불량')
  .map(([k, v]) => k + (v['비고'] ? ` (${v['비고']})` : ''));
return [{ json: {                                            // ⑤ 일곱 항목으로 내보낸다
  제출시각: $now.toFormat('yyyy-MM-dd HH:mm'),
  장비ID: ext['장비ID'] || '',
  점검일자: ext['점검일자'] || '',
  점검자: ext['점검자'] || '',
  불량수: bad.length,
  불량항목: bad.join(', '),
  특이사항: ext['특이사항'] || ''
} }];"""

# 프롬프트는 앞 노드(사진 준비)가 $json.prompt 로 넘긴다 — 표현식 안에 중괄호를 두지 않기 위함
BODY = ('={{ JSON.stringify({ contents: [{ parts: ['
        '{ inline_data: { mime_type: $json.mime, data: $json.data } }, '
        '{ text: $json.prompt } ] }], '
        'generationConfig: { temperature: 0 } }) }}')

# ── ① 준비용 워크플로 — 시트 저장소 마련 ──────────────────────
prep = {
    "name": "sheet_prep",
    "nodes": [
        node("수동 실행", "n8n-nodes-base.manualTrigger", 1, [-60, 300], {}),
        node("헤더 한 줄 만들기", "n8n-nodes-base.code", 2, [180, 300], {"jsCode":
             "// 시트의 첫 줄(열 이름)을 만들기 위한 한 건입니다.\n"
             "// 한 번 실행해 열이 생기면 이 워크플로는 더 쓰지 않습니다.\n"
             "return [{ json: {\n"
             "  제출시각: '2026-01-01 09:00', 장비ID: 'EX-000', 점검일자: '2026-01-01',\n"
             "  점검자: '(예시)', 불량수: 0, 불량항목: '', 특이사항: '열 생성용 예시 행 — 확인 후 지우세요'\n"
             "} }];"}),
        node("시트 만들기", "n8n-nodes-base.googleSheets", 4.5, [420, 300], {
            "operation": "append",
            "documentId": {"__rl": True, "mode": "list", "value": "",
                           "cachedResultName": "점검표_자동수집"},
            "sheetName": {"__rl": True, "mode": "list", "value": "",
                          "cachedResultName": "수집"},
            "columns": {"mappingMode": "autoMapInputData", "value": {}},
            "options": {}}),
    ],
    "connections": conn([("수동 실행", "헤더 한 줄 만들기", 0),
                         ("헤더 한 줄 만들기", "시트 만들기", 0)]),
    "settings": {"executionOrder": "v1"}, "pinData": {},
}

# ── ② 완성본 — 노드 7개 ───────────────────────────────────────
intake = {
    "name": "checklist_intake",
    "nodes": [
        node("점검표 제출 폼", "n8n-nodes-base.formTrigger", 2.2, [-140, 300], {
            "formTitle": "굴착기 일일점검표 제출",
            "formDescription": "점검을 마친 점검표를 정면에서 찍어 올려 주세요.",
            "formFields": {"values": [
                {"fieldLabel": "점검표 사진", "fieldType": "file",
                 "acceptFileTypes": ".jpg,.jpeg,.png", "requiredField": True}]},
            "options": {}}, webhookId="checklist-intake-form"),
        node("사진 준비", "n8n-nodes-base.code", 2, [100, 300], {"jsCode": CODE_PREP}),
        node("Gemini 호출", "n8n-nodes-base.httpRequest", 4.2, [340, 300], {
            "method": "POST",
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
            "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth",
            "sendBody": True, "specifyBody": "json", "jsonBody": BODY,
            "options": {}}),
        node("응답 정리", "n8n-nodes-base.code", 2, [580, 300], {"jsCode": CODE_CLEAN}),
        node("시트 적재", "n8n-nodes-base.googleSheets", 4.5, [820, 300], {
            "operation": "append",
            "documentId": {"__rl": True, "mode": "list", "value": "",
                           "cachedResultName": "점검표_자동수집"},
            "sheetName": {"__rl": True, "mode": "list", "value": "",
                          "cachedResultName": "수집"},
            "columns": {"mappingMode": "autoMapInputData", "value": {}},
            "options": {}}),
        node("불량 있음?", "n8n-nodes-base.if", 2.2, [1060, 300], {
            "conditions": {"options": {"caseSensitive": True, "leftValue": "",
                                       "typeValidation": "strict", "version": 2},
                           "combinator": "and",
                           "conditions": [{"id": "bad-gt-0",
                                           "leftValue": "={{ $json['불량수'] }}",
                                           "rightValue": 0,
                                           "operator": {"type": "number", "operation": "gt"}}]},
            "options": {}}),
        node("Slack 알림", "n8n-nodes-base.slack", 2.3, [1320, 220], {
            "resource": "message", "operation": "post", "select": "channel",
            "channelId": {"__rl": True, "mode": "name", "value": "정비-알림"},
            "text": ("=:rotating_light: 점검표 불량 발견\n"
                     "장비: {{ $json['장비ID'] }} / 점검일자: {{ $json['점검일자'] }}\n"
                     "불량 {{ $json['불량수'] }}건 — {{ $json['불량항목'] }}\n"
                     "점검자: {{ $json['점검자'] }} / 특이사항: {{ $json['특이사항'] }}"),
            "otherOptions": {}}),
    ],
    "connections": conn([("점검표 제출 폼", "사진 준비", 0), ("사진 준비", "Gemini 호출", 0),
                         ("Gemini 호출", "응답 정리", 0), ("응답 정리", "시트 적재", 0),
                         ("시트 적재", "불량 있음?", 0), ("불량 있음?", "Slack 알림", 0)]),
    "settings": {"executionOrder": "v1"}, "pinData": {},
}

os.makedirs("workflows", exist_ok=True)
for name, wf in (("sheet_prep.json", prep), ("checklist_intake.json", intake)):
    json.dump(wf, open(f"workflows/{name}", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  workflows/{name:<24} 노드 {len(wf['nodes'])}개")
print("\n※ 자격증명(Gemini 키·구글 계정·Slack 봇 토큰)은 파일에 담기지 않습니다.")
print("   불러온 뒤 각 노드에서 각자 만들어 둔 자격증명을 고르세요.")
