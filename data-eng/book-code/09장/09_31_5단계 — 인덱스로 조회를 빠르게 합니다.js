// 인덱스 만들기 전 — 몇 개 문서를 훑는지
db.access_logs.find({ level: 'ERROR' }).explain('executionStats').executionStats.totalDocsExamined

// 인덱스 생성 (1=오름차순, -1=내림차순)
db.access_logs.createIndex({ level: 1, ts: -1 })
db.access_logs.getIndexes()

// 만든 뒤 다시 측정
db.access_logs.find({ level: 'ERROR' }).explain('executionStats').executionStats.totalDocsExamined

// 실제 조회도 해 봅니다
db.access_logs.find({ level: 'ERROR' }).sort({ ts: -1 }).limit(5)
