// 두 값으로 묶기 — _id에 객체를 주면 됩니다
db.access_logs.aggregate([
  { $group: { _id: { level: '$level', path: '$path' }, cnt: { $sum: 1 } } },
  { $sort: { cnt: -1, _id: 1 } },
  { $limit: 5 }
])

// 평균·최대도 같은 방식
db.access_logs.aggregate([
  { $group: { _id: '$path', avg_status: { $avg: '$status' }, cnt: { $sum: 1 } } },
  { $sort: { cnt: -1, _id: 1 } }
])
