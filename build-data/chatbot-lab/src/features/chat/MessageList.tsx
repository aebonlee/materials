import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { ChatContextChunk, Conversation, Message } from '../../lib/types'
import { exportConversationAsDocx, exportMessageAsMarkdown } from './exportDocx'

interface Props {
  conversation: Conversation
  messages: Message[]
  streamingText: string
  streamingContext: ChatContextChunk[]
  sending: boolean
}

function ContextChips({ context }: { context: ChatContextChunk[] | null }) {
  if (!context || context.length === 0) return null
  return (
    <details className="context-chips">
      <summary>참고 문서 발췌 {context.length}건</summary>
      <ul>
        {context.map((c) => (
          <li key={c.id}>
            청크#{c.chunk_index} · 유사도 {(c.similarity * 100).toFixed(0)}%
            <blockquote>{c.content.slice(0, 200)}{c.content.length > 200 ? '…' : ''}</blockquote>
          </li>
        ))}
      </ul>
    </details>
  )
}

export function MessageList({ conversation, messages, streamingText, streamingContext, sending }: Props) {
  return (
    <div className="message-list">
      {messages.length === 0 && !sending && (
        <div className="empty-hint chat-empty">
          <p>{conversation.system_prompt || '무엇이든 물어보세요.'}</p>
        </div>
      )}
      {messages.map((m) => (
        <div key={m.id} className={`message message--${m.role}`}>
          <div className="message-role">{m.role === 'user' ? '나' : m.role === 'assistant' ? 'AI' : '시스템'}</div>
          <div className="message-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
          </div>
          <ContextChips context={m.context} />
          {m.role === 'assistant' && (
            <div className="message-actions">
              <button className="btn-icon" onClick={() => navigator.clipboard.writeText(m.content)}>
                복사
              </button>
              <button className="btn-icon" onClick={() => exportMessageAsMarkdown(m)}>
                .md 저장
              </button>
            </div>
          )}
        </div>
      ))}
      {sending && (
        <div className="message message--assistant">
          <div className="message-role">AI</div>
          <div className="message-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{streamingText || '…'}</ReactMarkdown>
          </div>
          <ContextChips context={streamingContext} />
        </div>
      )}
      {messages.length > 0 && (
        <div className="conversation-export">
          <button className="btn-secondary" onClick={() => exportConversationAsDocx(conversation, messages)}>
            대화 전체를 보고서(.docx)로 내보내기
          </button>
        </div>
      )}
    </div>
  )
}
