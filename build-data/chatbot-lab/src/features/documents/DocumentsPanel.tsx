import { useRef } from 'react'
import { useDocuments } from './useDocuments'

const STATUS_LABEL: Record<string, string> = {
  processing: '처리중…',
  ready: '준비완료',
  failed: '실패',
}

interface Props {
  selectedIds: string[]
  onToggleSelected: (id: string) => void
}

export function DocumentsPanel({ selectedIds, onToggleSelected }: Props) {
  const { documents, uploading, upload, remove } = useDocuments()
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFiles = async (files: FileList | null) => {
    if (!files) return
    for (const file of Array.from(files)) {
      await upload(file)
    }
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div className="panel documents-panel">
      <div className="panel-header">
        <h2>문서</h2>
        <button className="btn-secondary" onClick={() => inputRef.current?.click()}>
          + 업로드
        </button>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.xlsx,.xls,.txt,.md"
          multiple
          hidden
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      {Object.entries(uploading).map(([key, progress]) => (
        <div key={key} className="doc-item doc-item--uploading">
          <span>{progress.stage === 'parsing' && '텍스트 추출 중…'}</span>
          <span>{progress.stage === 'embedding' && `임베딩 중 (${progress.detail})`}</span>
          <span>{progress.stage === 'saving' && '저장 중…'}</span>
          <span>{progress.stage === 'failed' && `실패: ${progress.detail}`}</span>
        </div>
      ))}

      {documents.length === 0 && Object.keys(uploading).length === 0 && (
        <p className="empty-hint">PDF·엑셀·워드 파일을 업로드하면 채팅에서 참고 문서로 쓸 수 있습니다.</p>
      )}

      <ul className="doc-list">
        {documents.map((doc) => (
          <li key={doc.id} className={`doc-item doc-item--${doc.status}`}>
            <label>
              <input
                type="checkbox"
                disabled={doc.status !== 'ready'}
                checked={selectedIds.includes(doc.id)}
                onChange={() => onToggleSelected(doc.id)}
              />
              <span className="doc-name" title={doc.filename}>
                {doc.filename}
              </span>
            </label>
            <span className="doc-meta">
              {STATUS_LABEL[doc.status]}
              {doc.status === 'ready' && ` · 청크 ${doc.chunk_count}`}
            </span>
            <button className="btn-icon" title="삭제" onClick={() => remove(doc.id)}>
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
