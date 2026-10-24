// 조건 일치
db.access_logs.find({ level: 'ERROR' })

// 중첩 필드는 점 표기법으로
db.access_logs.find({ 'error.code': 'PAY-42' })

// 비교 연산자 ($gt $gte $lt $lte $ne $in)
db.access_logs.find({ status: { $gte: 400 } })
db.access_logs.find({ level: { $in: ['WARN', 'ERROR'] } })

// 필드가 있는 문서만
db.access_logs.find({ elapsed_ms: { $exists: true } })

// 보여 줄 필드 고르기 (1=보임, 0=숨김)
db.access_logs.find({}, { _id: 0, level: 1, path: 1 })

// 정렬·개수 제한 (1=오름차순, -1=내림차순)
db.access_logs.find().sort({ ts: -1 }).limit(2)
