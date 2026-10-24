// 필드 이름을 일부러 틀리게 넣어 봅니다 (오류 없이 들어갑니다)
db.access_logs.insertOne({ Level: 'ERROR', path: '/oops' })

// level로 찾으면 안 나옵니다 — 오류도 없이 그냥 빠집니다
db.access_logs.countDocuments({ level: 'ERROR' })

// 실제 필드 이름을 확인하는 습관
db.access_logs.find({ path: '/oops' })

// 정리
db.access_logs.deleteOne({ path: '/oops' })
