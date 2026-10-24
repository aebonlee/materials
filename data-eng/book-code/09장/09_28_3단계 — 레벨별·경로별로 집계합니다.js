// 레벨별 건수
db.access_logs.aggregate([
  { $group: { _id: '$level', count: { $sum: 1 } } },
  { $sort: { count: -1, _id: 1 } }
])

// ERROR가 많이 난 경로 순위
db.access_logs.aggregate([
  { $match: { level: 'ERROR' } },
  { $group: { _id: '$path', errors: { $sum: 1 } } },
  { $sort: { errors: -1, _id: 1 } }   // 건수가 같으면 이름순 — 순서를 고정한다
])
