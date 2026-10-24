// 분 단위로 묶어 요청 수 추이 보기
db.access_logs.aggregate([
  { $group: {
      _id: { $dateToString: { format: '%Y-%m-%d %H:%M', date: '$ts' } },
      cnt: { $sum: 1 },
      errors: { $sum: { $cond: [{ $eq: ['$level', 'ERROR'] }, 1, 0] } }
  } },
  { $sort: { _id: 1 } },
  { $limit: 10 }
])
