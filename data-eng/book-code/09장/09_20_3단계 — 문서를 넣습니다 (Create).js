db.access_logs.insertMany([
  { ts: ISODate('2026-08-31T09:00:00Z'), level: 'INFO',  path: '/',        status: 200, user: 'u001' },
  { ts: ISODate('2026-08-31T09:01:10Z'), level: 'INFO',  path: '/login',   status: 200, user: 'u002' },
  { ts: ISODate('2026-08-31T09:02:30Z'), level: 'ERROR', path: '/api/pay', status: 500, user: 'u002',
    error: { code: 'PAY-42', message: 'timeout' } },
  { ts: ISODate('2026-08-31T09:03:00Z'), level: 'WARN',  path: '/search',  status: 200, user: 'u003',
    elapsed_ms: 3200 }
])

db.access_logs.countDocuments()
db.access_logs.findOne()
