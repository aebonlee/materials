// 필드 추가·변경 — $set
db.access_logs.updateOne({ user: 'u003' }, { $set: { reviewed: true } })
db.access_logs.find({ user: 'u003' })

// 숫자 증가 — $inc
db.access_logs.updateOne({ user: 'u003' }, { $inc: { elapsed_ms: 100 } })

// 여러 건 한꺼번에
db.access_logs.updateMany({ level: 'INFO' }, { $set: { checked: true } })

// 필드 제거 — $unset
db.access_logs.updateMany({}, { $unset: { checked: '' } })

// 삭제 (습관: 먼저 find로 대상을 확인)
db.access_logs.find({ user: 'u001' })
db.access_logs.deleteOne({ user: 'u001' })
db.access_logs.countDocuments()
