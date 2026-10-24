// 정답 예시
db.access_logs.aggregate([
  { $group: { _id: '$user', cnt: { $sum: 1 } } },
  { $sort: { cnt: -1, _id: 1 } },
  { $limit: 5 }
])

db.access_logs.aggregate([
  { $match: { level: 'ERROR' } },
  { $group: { _id: '$error.code', cnt: { $sum: 1 } } },
  { $sort: { cnt: -1, _id: 1 } },
  { $limit: 5 }
])

// 셋째 — $match를 뒤로 옮기면
db.access_logs.aggregate([
  { $group: { _id: '$path', errors: { $sum: 1 } } },
  { $match: { level: 'ERROR' } }
])
