import type { Conversation, ConversationMode, Provider } from '../../lib/types'

const MODE_LABEL: Record<ConversationMode, string> = {
  general: '일반 대화',
  qa: '문서 Q&A',
  summary: '요약',
  report: '보고서 작성',
}

const MODEL_OPTIONS: Record<Provider, string[]> = {
  openai: ['gpt-4.1-mini', 'gpt-4.1', 'gpt-4o-mini', 'gpt-4o'],
  solar: ['solar-pro2', 'solar-mini'],
  // Claude — 가장 똑똑한 것이 앞, 싸고 빠른 것이 뒤
  anthropic: ['claude-opus-5', 'claude-sonnet-5', 'claude-haiku-4-5'],
  gemini: ['gemini-2.5-flash', 'gemini-2.5-pro'],
}

interface Props {
  conversation: Conversation
  onUpdate: (patch: Partial<Conversation>) => void
  selectedDocCount: number
}

export function ChatHeader({ conversation, onUpdate, selectedDocCount }: Props) {
  return (
    <div className="chat-header">
      <div className="chat-header-title">
        <h1>{conversation.title}</h1>
        <span className="mode-badge">{MODE_LABEL[conversation.mode]}</span>
      </div>
      <div className="chat-header-controls">
        <select
          className="input"
          value={conversation.provider}
          onChange={(e) => {
            const provider = e.target.value as Provider
            onUpdate({ provider, model: MODEL_OPTIONS[provider][0] })
          }}
        >
          <option value="openai">OpenAI</option>
          <option value="solar">Solar (업스테이지)</option>
          <option value="anthropic">Claude</option>
          <option value="gemini">Gemini</option>
        </select>
        <select className="input" value={conversation.model} onChange={(e) => onUpdate({ model: e.target.value })}>
          {MODEL_OPTIONS[conversation.provider].map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
        <label className="rag-toggle">
          <input
            type="checkbox"
            checked={conversation.use_rag}
            onChange={(e) => onUpdate({ use_rag: e.target.checked })}
          />
          문서 참고 {selectedDocCount > 0 ? `(${selectedDocCount}개 선택됨)` : '(왼쪽에서 문서 선택)'}
        </label>
      </div>
    </div>
  )
}
