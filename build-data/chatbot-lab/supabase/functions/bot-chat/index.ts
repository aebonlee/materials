// chatbot-lab — 채팅 프록시 (OpenAI / Solar 공용)
// - API 키(OPENAI_API_KEY, SOLAR_API_KEY)는 이 함수 안에서만 쓰이고 클라이언트로 내려가지 않는다.
// - RAG 사용 시: 사용자 메시지를 임베딩 → pgvector 유사도 검색(bot_match_chunks, service role) → 시스템 프롬프트에 발췌 삽입.
// - provider 응답을 정규화한 SSE(`data: {"delta":"..."}\n\n` ... `data: [DONE]\n\n`)로 그대로 스트리밍한다.
// Supabase 대시보드(웹) 에디터에서 파일 하나만 붙여넣어 배포할 수 있도록 공용 헬퍼를 인라인했다
// (bot-embed/index.ts에도 동일한 블록이 중복되어 있음 — 웹 배포 편의 목적의 의도적 중복).
import { createClient } from 'jsr:@supabase/supabase-js@2'

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
const SOLAR_API_KEY = Deno.env.get('SOLAR_API_KEY')
const ANTHROPIC_API_KEY = Deno.env.get('ANTHROPIC_API_KEY')
const GEMINI_API_KEY = Deno.env.get('GEMINI_API_KEY')
const SOLAR_API_BASE = Deno.env.get('SOLAR_API_BASE') ?? 'https://api.upstage.ai/v1'
// 구글이 제공하는 OpenAI 호환 창구 — 같은 형식으로 부를 수 있어 코드가 하나로 줄어든다.
const GEMINI_API_BASE = 'https://generativelanguage.googleapis.com/v1beta/openai'

const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!

const EMBEDDING_MODEL = 'text-embedding-3-small'

// 쓸 수 있는 서비스 네 가지. 키를 넣은 것만 쓰면 된다 — 넷 다 넣을 필요 없다.
type Provider = 'openai' | 'solar' | 'anthropic' | 'gemini'

const DEFAULT_MODEL: Record<Provider, string> = {
  openai: 'gpt-4.1-mini',
  // ⚠️ Upstage Solar 모델명은 바뀔 수 있음 — 실제 배포 전 https://console.upstage.ai 문서로 최신 모델 ID를 확인할 것.
  solar: 'solar-pro2',
  anthropic: 'claude-opus-5',
  gemini: 'gemini-2.5-flash',
}

const API_KEYS: Record<Provider, string | undefined> = {
  openai: OPENAI_API_KEY,
  solar: SOLAR_API_KEY,
  anthropic: ANTHROPIC_API_KEY,
  gemini: GEMINI_API_KEY,
}

const KEY_NAME: Record<Provider, string> = {
  openai: 'OPENAI_API_KEY',
  solar: 'SOLAR_API_KEY',
  anthropic: 'ANTHROPIC_API_KEY',
  gemini: 'GEMINI_API_KEY',
}

type ChatMessage = { role: 'system' | 'user' | 'assistant'; content: string }

interface ChatRequestBody {
  provider?: Provider
  model?: string
  systemPrompt?: string
  history?: ChatMessage[]
  userMessage: string
  ragDocumentIds?: string[]
  useRag?: boolean
}

async function embedQuery(text: string): Promise<number[] | null> {
  if (!OPENAI_API_KEY) return null
  const res = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: { Authorization: `Bearer ${OPENAI_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: EMBEDDING_MODEL, input: text }),
  })
  if (!res.ok) return null
  const json = await res.json()
  return json.data?.[0]?.embedding ?? null
}

async function retrieveContext(userMessage: string, ragDocumentIds: string[] | undefined) {
  const embedding = await embedQuery(userMessage)
  if (!embedding) return { snippet: '', chunks: [] as unknown[] }

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
  const { data, error } = await supabase.rpc('bot_match_chunks', {
    query_embedding: `[${embedding.join(',')}]`,
    match_count: 6,
    doc_ids: ragDocumentIds && ragDocumentIds.length > 0 ? ragDocumentIds : null,
  })
  if (error || !data) return { snippet: '', chunks: [] as unknown[] }

  const snippet = data
    .map(
      (c: { chunk_index: number; content: string }, i: number) =>
        `[발췌 ${i + 1} / 청크#${c.chunk_index}]\n${c.content}`,
    )
    .join('\n\n')
  return { snippet, chunks: data }
}

function sseLine(obj: unknown) {
  return `data: ${JSON.stringify(obj)}\n\n`
}

async function streamOpenAiCompatible(
  baseUrl: string,
  apiKey: string,
  model: string,
  messages: ChatMessage[],
) {
  const upstream = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, messages, stream: true }),
  })

  if (!upstream.ok || !upstream.body) {
    const detail = await upstream.text().catch(() => '')
    throw new Error(`upstream ${upstream.status}: ${detail}`)
  }

  const reader = upstream.body.getReader()
  const decoder = new TextDecoder()
  const encoder = new TextEncoder()

  return new ReadableStream<Uint8Array>({
    async start(controller) {
      let buffer = ''
      try {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() ?? ''
          for (const line of lines) {
            const trimmed = line.trim()
            if (!trimmed.startsWith('data:')) continue
            const payload = trimmed.slice(5).trim()
            if (payload === '[DONE]') {
              controller.enqueue(encoder.encode(sseLine({ done: true })))
              continue
            }
            try {
              const json = JSON.parse(payload)
              const delta = json.choices?.[0]?.delta?.content
              if (delta) controller.enqueue(encoder.encode(sseLine({ delta })))
            } catch {
              // 파싱 안 되는 라인은 무시(keep-alive 등)
            }
          }
        }
      } catch (err) {
        controller.enqueue(encoder.encode(sseLine({ error: String(err) })))
      } finally {
        controller.enqueue(encoder.encode('data: [DONE]\n\n'))
        controller.close()
      }
    },
  })
}

// Claude 는 메시지 형식이 다르다 — system 이 messages 안이 아니라 별도 항목이고,
// 응답도 형식이 달라 공식 SDK 로 부른 뒤 우리 형식(SSE)으로 바꿔 내보낸다.
async function streamAnthropic(
  apiKey: string,
  model: string,
  systemPrompt: string,
  messages: ChatMessage[],
) {
  const { default: Anthropic } = await import('npm:@anthropic-ai/sdk@0.71.0')
  const client = new Anthropic({ apiKey })

  const turns = messages
    .filter((m) => m.role !== 'system')
    .map((m) => ({ role: m.role as 'user' | 'assistant', content: m.content }))

  const encoder = new TextEncoder()
  return new ReadableStream<Uint8Array>({
    async start(controller) {
      try {
        const stream = client.messages.stream({
          model,
          max_tokens: 8000,
          system: systemPrompt,
          messages: turns,
        })
        for await (const event of stream) {
          if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
            controller.enqueue(encoder.encode(sseLine({ delta: event.delta.text })))
          }
        }
      } catch (err) {
        controller.enqueue(encoder.encode(sseLine({ error: String(err) })))
      } finally {
        controller.enqueue(encoder.encode('data: [DONE]\n\n'))
        controller.close()
      }
    },
  })
}

Deno.serve(async (req) => {
  const origin = req.headers.get('origin')
  const headers = corsHeaders(origin)

  if (req.method === 'OPTIONS') return new Response(null, { headers })
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'method not allowed' }), { status: 405, headers })
  }
  if (!checkClientToken(req)) {
    return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers })
  }

  let body: ChatRequestBody
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'invalid json body' }), { status: 400, headers })
  }

  const asked = body.provider ?? 'openai'
  const provider: Provider = (['openai', 'solar', 'anthropic', 'gemini'] as const).includes(
    asked as Provider,
  )
    ? (asked as Provider)
    : 'openai'
  const model = body.model?.trim() || DEFAULT_MODEL[provider]
  const apiKey = API_KEYS[provider]
  if (!apiKey) {
    return new Response(
      JSON.stringify({
        error: `${KEY_NAME[provider]} 가 서버에 없습니다. Supabase → Edge Functions → Secrets 에 넣으세요.`,
      }),
      { status: 500, headers },
    )
  }
  if (!body.userMessage?.trim()) {
    return new Response(JSON.stringify({ error: 'userMessage is required' }), { status: 400, headers })
  }

  let systemPrompt = body.systemPrompt?.trim() || '너는 유용한 개인 비서야.'
  let context: unknown[] = []

  if (body.useRag) {
    const result = await retrieveContext(body.userMessage, body.ragDocumentIds)
    context = result.chunks
    if (result.snippet) {
      systemPrompt = `${systemPrompt}\n\n다음은 사용자가 업로드한 문서에서 검색된 관련 발췌다. 이 내용을 근거로 답하고, 근거가 부족하면 솔직히 말해라.\n\n${result.snippet}`
    }
  }

  const messages: ChatMessage[] = [
    { role: 'system', content: systemPrompt },
    ...(body.history ?? []),
    { role: 'user', content: body.userMessage },
  ]

  try {
    // Claude 만 형식이 다르고, 나머지 셋은 OpenAI 형식이라 같은 함수로 처리한다.
    const BASE: Record<Exclude<Provider, 'anthropic'>, string> = {
      openai: 'https://api.openai.com/v1',
      solar: SOLAR_API_BASE,
      gemini: GEMINI_API_BASE,
    }
    const stream =
      provider === 'anthropic'
        ? await streamAnthropic(apiKey, model, systemPrompt, messages)
        : await streamOpenAiCompatible(BASE[provider], apiKey, model, messages)

    // 첫 이벤트로 RAG 컨텍스트(인용 표시용)를 먼저 흘려보낸다.
    const encoder = new TextEncoder()
    const prelude = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode(sseLine({ context })))
        controller.close()
      },
    })

    const combined = new ReadableStream<Uint8Array>({
      async start(controller) {
        const preludeReader = prelude.getReader()
        const streamReader = stream.getReader()
        while (true) {
          const { done, value } = await preludeReader.read()
          if (done) break
          controller.enqueue(value)
        }
        while (true) {
          const { done, value } = await streamReader.read()
          if (done) break
          controller.enqueue(value)
        }
        controller.close()
      },
    })

    return new Response(combined, {
      headers: {
        ...headers,
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        Connection: 'keep-alive',
      },
    })
  } catch (err) {
    return new Response(JSON.stringify({ error: String(err) }), { status: 502, headers })
  }
})
