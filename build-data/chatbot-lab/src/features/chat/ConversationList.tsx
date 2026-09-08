import { useState } from 'react'
import type { Conversation } from '../../lib/types'

interface Props {
  conversations: Conversation[]
  activeId: string | null
  onSelect: (id: string) => void
  onCreate: () => void
  onDelete: (id: string) => void
  onRename: (id: string, title: string) => void
}

export function ConversationList({ conversations, activeId, onSelect, onCreate, onDelete, onRename }: Props) {
  const [renamingId, setRenamingId] = useState<string | null>(null)
  const [draftTitle, setDraftTitle] = useState('')

  return (
    <div className="panel conversation-panel">
      <div className="panel-header">
        <h2>대화</h2>
        <button className="btn-secondary" onClick={onCreate}>
          + 새 대화
        </button>
      </div>
      <ul className="conversation-list">
        {conversations.map((c) => (
          <li key={c.id} className={`conversation-item ${c.id === activeId ? 'active' : ''}`}>
            {renamingId === c.id ? (
              <input
                className="input"
                autoFocus
                value={draftTitle}
                onChange={(e) => setDraftTitle(e.target.value)}
                onBlur={() => {
                  if (draftTitle.trim()) onRename(c.id, draftTitle.trim())
                  setRenamingId(null)
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') e.currentTarget.blur()
                  if (e.key === 'Escape') setRenamingId(null)
                }}
              />
            ) : (
              <button className="conversation-title-btn" onClick={() => onSelect(c.id)}>
                <span className="conversation-title">{c.title}</span>
                <span className="conversation-meta">
                  {c.provider === 'openai' ? 'OpenAI' : 'Solar'} · {c.model}
                </span>
              </button>
            )}
            <div className="conversation-actions">
              <button
                className="btn-icon"
                title="이름 변경"
                onClick={() => {
                  setRenamingId(c.id)
                  setDraftTitle(c.title)
                }}
              >
                ✎
              </button>
              <button className="btn-icon" title="삭제" onClick={() => onDelete(c.id)}>
                ✕
              </button>
            </div>
          </li>
        ))}
        {conversations.length === 0 && <p className="empty-hint">아직 대화가 없습니다. 새 대화를 시작해보세요.</p>}
      </ul>
    </div>
  )
}
