import type { ChatContextChunk, MessageRole, Provider } from './types'

// 값은 .env 에서 옵니다(supabaseClient.ts 가 없으면 먼저 멈춰 알려 줍니다).
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY
const CLIENT_TOKEN = import.meta.env.VITE_BOT_CLIENT_TOKEN || ''
const FUNCTIONS_BASE = `${SUPABASE_URL}/functions/v1`

function functionHeaders() {
  // Supabase Edge Function 게이트웨이가 기본적으로 자체 JWT 인증을 요구한다(Enforce JWT Verification).
  // 공용 anon 키를 Authorization/apikey로 실어 보내야 게이트웨이를 통과한다 — 우리 앱 자체 인증은
  // 별도인 x-bot-token(약한 방어선)이 담당한다.
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
    apikey: SUPABASE_ANON_KEY,
  }
  if (CLIENT_TOKEN) headers['x-bot-token'] = CLIENT_TOKEN
  return headers
}

export interface ChatStreamParams {
  provider: Provider
  model: string
  systemPrompt: string
  history: { role: MessageRole; content: string }[]
  userMessage: string
  useRag: boolean
  ragDocumentIds: string[]
  signal?: AbortSignal
  onDelta: (delta: string) => void
  onContext?: (context: ChatContextChunk[]) => void
}

export async function streamChat(params: ChatStreamParams): Promise<void> {
  const res = await fetch(`${FUNCTIONS_BASE}/bot-chat`, {
    method: 'POST',
    headers: functionHeaders(),
    signal: params.signal,
    body: JSON.stringify({
      provider: params.provider,
      model: params.model,
      systemPrompt: params.systemPrompt,
      history: params.history,
      userMessage: params.userMessage,
      useRag: params.useRag,
      ragDocumentIds: params.ragDocumentIds,
    }),
  })

  if (!res.ok || !res.body) {
    const text = await res.text().catch(() => '')
    throw new Error(`bot-chat 호출 실패 (${res.status}): ${text}`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

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
      if (payload === '[DONE]') continue
      try {
        const json = JSON.parse(payload)
        if (json.delta) params.onDelta(json.delta)
        if (json.context) params.onContext?.(json.context)
        if (json.error) throw new Error(json.error)
      } catch {
        // 파싱 실패 라인은 무시
      }
    }
  }
}

export async function embedTexts(texts: string[]): Promise<number[][]> {
  const res = await fetch(`${FUNCTIONS_BASE}/bot-embed`, {
    method: 'POST',
    headers: functionHeaders(),
    body: JSON.stringify({ texts }),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`bot-embed 호출 실패 (${res.status}): ${text}`)
  }
  const json = await res.json()
  return json.embeddings
}
