import { useMemo, useState } from 'react'
import { ChatPage } from './features/chat/ChatPage'
import { ConversationList } from './features/chat/ConversationList'
import { useConversations } from './features/chat/useConversations'
import { DocumentsPanel } from './features/documents/DocumentsPanel'
import { PromptLibrary } from './features/prompts/PromptLibrary'
import { SetupGuide } from './features/setup/SetupGuide'
import { supabase } from './lib/supabaseClient'
import type { ConversationMode, PromptCategory, PromptRow } from './lib/types'

type SidebarTab = 'conversations' | 'documents' | 'prompts' | 'setup'

const CATEGORY_TO_MODE: Record<PromptCategory, ConversationMode> = {
  general: 'general',
  qa: 'qa',
  summary: 'summary',
  report: 'report',
  custom: 'general',
}

function App() {
  const { conversations, create, update, remove } = useConversations()
  const [activeId, setActiveId] = useState<string | null>(null)
  const [tab, setTab] = useState<SidebarTab>('conversations')

  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeId) ?? null,
    [conversations, activeId],
  )

  const handleCreate = async () => {
    const c = await create({})
    setActiveId(c.id)
    setTab('conversations')
  }

  const handleUsePrompt = async (prompt: PromptRow) => {
    const c = await create({
      title: prompt.title,
      mode: CATEGORY_TO_MODE[prompt.category],
      system_prompt: prompt.content,
    })
    await supabase.from('bot_prompts').update({ usage_count: prompt.usage_count + 1 }).eq('id', prompt.id)
    setActiveId(c.id)
    setTab('conversations')
  }

  const handleToggleDoc = (docId: string) => {
    if (!activeConversation) return
    const has = activeConversation.rag_document_ids.includes(docId)
    const next = has
      ? activeConversation.rag_document_ids.filter((id) => id !== docId)
      : [...activeConversation.rag_document_ids, docId]
    update(activeConversation.id, { rag_document_ids: next, use_rag: next.length > 0 ? true : activeConversation.use_rag })
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-tabs">
          <button className={tab === 'conversations' ? 'active' : ''} onClick={() => setTab('conversations')}>
            대화
          </button>
          <button className={tab === 'documents' ? 'active' : ''} onClick={() => setTab('documents')}>
            문서
          </button>
          <button className={tab === 'prompts' ? 'active' : ''} onClick={() => setTab('prompts')}>
            프롬프트
          </button>
          <button className={tab === 'setup' ? 'active' : ''} onClick={() => setTab('setup')}>
            설정 방법
          </button>
        </div>
        {tab === 'conversations' && (
          <ConversationList
            conversations={conversations}
            activeId={activeId}
            onSelect={setActiveId}
            onCreate={handleCreate}
            onDelete={async (id) => {
              await remove(id)
              if (id === activeId) setActiveId(null)
            }}
            onRename={(id, title) => update(id, { title })}
          />
        )}
        {tab === 'documents' && (
          <DocumentsPanel
            selectedIds={activeConversation?.rag_document_ids ?? []}
            onToggleSelected={handleToggleDoc}
          />
        )}
        {tab === 'prompts' && <PromptLibrary onUsePrompt={handleUsePrompt} />}
      </aside>
      <main className="main-area">
        {tab === 'setup' ? (
          <SetupGuide />
        ) : (
          <ChatPage conversation={activeConversation} onUpdateConversation={(patch) => activeConversation && update(activeConversation.id, patch)} />
        )}
      </main>
    </div>
  )
}

export default App
