import { useState } from 'react'
import type { PromptCategory, PromptRow } from '../../lib/types'
import { usePrompts } from './usePrompts'

const CATEGORY_LABEL: Record<PromptCategory, string> = {
  general: '일반',
  qa: '문서 Q&A',
  summary: '요약',
  report: '보고서',
  custom: '커스텀',
}

interface Props {
  onUsePrompt: (prompt: PromptRow) => void
}

export function PromptLibrary({ onUsePrompt }: Props) {
  const { prompts, create, update, remove } = usePrompts()
  const [editing, setEditing] = useState<PromptRow | null>(null)
  const [creating, setCreating] = useState(false)

  return (
    <div className="panel prompts-panel">
      <div className="panel-header">
        <h2>프롬프트 라이브러리</h2>
        <button className="btn-secondary" onClick={() => setCreating(true)}>
          + 새 프롬프트
        </button>
      </div>

      {creating && (
        <PromptForm
          initial={{ title: '', content: '', category: 'custom' }}
          onCancel={() => setCreating(false)}
          onSave={async (v) => {
            await create(v)
            setCreating(false)
          }}
        />
      )}

      <ul className="prompt-list">
        {prompts.map((p) =>
          editing?.id === p.id ? (
            <PromptForm
              key={p.id}
              initial={p}
              onCancel={() => setEditing(null)}
              onSave={async (v) => {
                await update(p.id, v)
                setEditing(null)
              }}
            />
          ) : (
            <li key={p.id} className="prompt-item">
              <div className="prompt-item-header">
                <span className="prompt-category">{CATEGORY_LABEL[p.category]}</span>
                <strong>{p.title}</strong>
                {p.is_pinned && <span title="고정됨">📌</span>}
              </div>
              <p className="prompt-content-preview">{p.content}</p>
              <div className="prompt-actions">
                <button className="btn-primary" onClick={() => onUsePrompt(p)}>
                  이 프롬프트로 대화 시작
                </button>
                <button className="btn-icon" onClick={() => setEditing(p)}>
                  편집
                </button>
                <button className="btn-icon" onClick={() => update(p.id, { is_pinned: !p.is_pinned })}>
                  {p.is_pinned ? '고정 해제' : '고정'}
                </button>
                <button className="btn-icon" onClick={() => remove(p.id)}>
                  삭제
                </button>
              </div>
              <span className="prompt-usage">사용 {p.usage_count}회</span>
            </li>
          ),
        )}
      </ul>
    </div>
  )
}

function PromptForm({
  initial,
  onSave,
  onCancel,
}: {
  initial: { title: string; content: string; category: PromptCategory }
  onSave: (v: { title: string; content: string; category: PromptCategory }) => void
  onCancel: () => void
}) {
  const [title, setTitle] = useState(initial.title)
  const [content, setContent] = useState(initial.content)
  const [category, setCategory] = useState<PromptCategory>(initial.category)

  return (
    <li className="prompt-item prompt-item--editing">
      <input
        className="input"
        placeholder="프롬프트 제목"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <select className="input" value={category} onChange={(e) => setCategory(e.target.value as PromptCategory)}>
        {Object.entries(CATEGORY_LABEL).map(([k, v]) => (
          <option key={k} value={k}>
            {v}
          </option>
        ))}
      </select>
      <textarea
        className="input"
        rows={4}
        placeholder="시스템 프롬프트 내용"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <div className="prompt-actions">
        <button
          className="btn-primary"
          disabled={!title.trim() || !content.trim()}
          onClick={() => onSave({ title: title.trim(), content: content.trim(), category })}
        >
          저장
        </button>
        <button className="btn-icon" onClick={onCancel}>
          취소
        </button>
      </div>
    </li>
  )
}
