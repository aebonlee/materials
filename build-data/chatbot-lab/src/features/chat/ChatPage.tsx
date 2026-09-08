import type { Conversation } from '../../lib/types'
import { ChatHeader } from './ChatHeader'
import { MessageInput } from './MessageInput'
import { MessageList } from './MessageList'
import { useMessages } from './useMessages'

interface Props {
  conversation: Conversation | null
  onUpdateConversation: (patch: Partial<Conversation>) => void
}

export function ChatPage({ conversation, onUpdateConversation }: Props) {
  const { messages, sending, streamingText, streamingContext, error, send, stop } = useMessages(conversation)

  if (!conversation) {
    return (
      <div className="chat-page chat-page--empty">
        <p className="empty-hint">왼쪽에서 대화를 선택하거나 새 대화를 시작하세요.</p>
      </div>
    )
  }

  return (
    <div className="chat-page">
      <ChatHeader
        conversation={conversation}
        onUpdate={onUpdateConversation}
        selectedDocCount={conversation.rag_document_ids.length}
      />
      <MessageList
        conversation={conversation}
        messages={messages}
        streamingText={streamingText}
        streamingContext={streamingContext}
        sending={sending}
      />
      {error && <div className="error-banner">{error}</div>}
      <MessageInput disabled={false} sending={sending} onSend={send} onStop={stop} />
    </div>
  )
}
