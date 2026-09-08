import { useState, type KeyboardEvent } from 'react'

interface Props {
  disabled: boolean
  sending: boolean
  onSend: (text: string) => void
  onStop: () => void
}

export function MessageInput({ disabled, sending, onSend, onStop }: Props) {
  const [text, setText] = useState('')

  const submit = () => {
    if (!text.trim() || disabled || sending) return
    onSend(text.trim())
    setText('')
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className="message-input">
      <textarea
        className="input"
        rows={3}
        placeholder={disabled ? '왼쪽에서 대화를 선택하거나 새로 시작하세요' : '메시지를 입력하세요 (Shift+Enter로 줄바꿈)'}
        value={text}
        disabled={disabled}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      {sending ? (
        <button className="btn-primary" onClick={onStop}>
          중지
        </button>
      ) : (
        <button className="btn-primary" disabled={disabled || !text.trim()} onClick={submit}>
          전송
        </button>
      )}
    </div>
  )
}
