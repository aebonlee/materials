// chatbot-lab — 문서 청크 임베딩 프록시
// OPENAI_API_KEY는 이 함수 안(서버)에서만 쓰이고 클라이언트로는 절대 내려가지 않는다.
// Supabase 대시보드(웹) 에디터에서 파일 하나만 붙여넣어 배포할 수 있도록 공용 헬퍼를 인라인했다
// (bot-chat/index.ts에도 동일한 블록이 중복되어 있음 — 웹 배포 편의 목적의 의도적 중복).

const ALLOWED_ORIGINS = new Set([
  'https://aebonlee.github.io',
  'http://localhost:5173',
  'http://127.0.0.1:5173',
])

function corsHeaders(origin: string | null): HeadersInit {
  const allowOrigin = origin && ALLOWED_ORIGINS.has(origin) ? origin : 'https://aebonlee.github.io'
  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-bot-token',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    Vary: 'Origin',
  }
}

// 진짜 비밀은 아님(빌드 번들에 그대로 들어감) — URL을 우연히 발견한 봇/스캐너를 걸러내는 약한 방어선.
function checkClientToken(req: Request): boolean {
  const expected = Deno.env.get('BOT_CLIENT_TOKEN')
  if (!expected) return true // 토큰을 설정 안 했으면 검사 생략(개발 편의)
  return req.headers.get('x-bot-token') === expected
}

const OPENAI_API_KEY = Deno.env.get('OPENAI_API_KEY')
const EMBEDDING_MODEL = 'text-embedding-3-small'
const MAX_TEXTS_PER_CALL = 64

Deno.serve(async (req) => {
  const origin = req.headers.get('origin')
  const headers = corsHeaders(origin)

  if (req.method === 'OPTIONS') {
    return new Response(null, { headers })
  }
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'method not allowed' }), { status: 405, headers })
  }
  if (!checkClientToken(req)) {
    return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers })
  }
  if (!OPENAI_API_KEY) {
    return new Response(JSON.stringify({ error: 'OPENAI_API_KEY not configured on server' }), {
      status: 500,
      headers,
    })
  }

  let body: { texts?: string[] }
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'invalid json body' }), { status: 400, headers })
  }

  const texts = (body.texts ?? []).filter((t) => typeof t === 'string' && t.trim().length > 0)
  if (texts.length === 0) {
    return new Response(JSON.stringify({ error: 'texts is empty' }), { status: 400, headers })
  }
  if (texts.length > MAX_TEXTS_PER_CALL) {
    return new Response(
      JSON.stringify({ error: `too many texts, max ${MAX_TEXTS_PER_CALL} per call` }),
      { status: 400, headers },
    )
  }

  const res = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model: EMBEDDING_MODEL, input: texts }),
  })

  if (!res.ok) {
    const errText = await res.text()
    return new Response(JSON.stringify({ error: 'openai embeddings failed', detail: errText }), {
      status: 502,
      headers,
    })
  }

  const json = await res.json()
  const embeddings: number[][] = json.data
    .sort((a: { index: number }, b: { index: number }) => a.index - b.index)
    .map((d: { embedding: number[] }) => d.embedding)

  return new Response(JSON.stringify({ embeddings, model: EMBEDDING_MODEL }), {
    headers: { ...headers, 'Content-Type': 'application/json' },
  })
})
