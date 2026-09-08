import { useCallback, useEffect, useRef, useState } from 'react'
import { supabase } from '../../lib/supabaseClient'
import { streamChat } from '../../lib/edgeFunctions'
import type { ChatContextChunk, Conversation, Message } from '../../lib/types'

export function useMessages(conversation: Conversation | null) {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [streamingText, setStreamingText] = useState('')
  const [streamingContext, setStreamingContext] = useState<ChatContextChunk[]>([])
  const [sending, setSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const abortRef = useRef<AbortController | null>(null)

  const refresh = useCallback(async () => {
    if (!conversation) {
      setMessages([])
      return
    }
    setLoading(true)
    const { data } = await supabase
      .from('bot_messages')
      .select('*')
      .eq('conversation_id', conversation.id)
      .order('created_at', { ascending: true })
    setMessages(data ?? [])
    setLoading(false)
  }, [conversation])

  useEffect(() => {
    refresh()
  }, [refresh])

  const send = useCallback(
    async (userText: string) => {
      if (!conversation || sending) return
      setError(null)
      setSending(true)
      setStreamingText('')
      setStreamingContext([])

      const { data: userMsg } = await supabase
        .from('bot_messages')
        .insert({ conversation_id: conversation.id, role: 'user', content: userText })
        .select()
        .single()
      if (userMsg) setMessages((prev) => [...prev, userMsg])

      const history = messages.map((m) => ({ role: m.role, content: m.content }))
      const controller = new AbortController()
      abortRef.current = controller

      let fullText = ''
      let fullContext: ChatContextChunk[] = []
      try {
        await streamChat({
          provider: conversation.provider,
          model: conversation.model,
          systemPrompt: conversation.system_prompt,
          history,
          userMessage: userText,
          useRag: conversation.use_rag,
          ragDocumentIds: conversation.rag_document_ids,
          signal: controller.signal,
          onDelta: (delta) => {
            fullText += delta
            setStreamingText(fullText)
          },
          onContext: (ctx) => {
            fullContext = ctx
            setStreamingContext(ctx)
          },
        })
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err))
      }

      if (fullText.trim()) {
        const { data: assistantMsg } = await supabase
          .from('bot_messages')
          .insert({
            conversation_id: conversation.id,
            role: 'assistant',
            content: fullText,
            context: fullContext.length > 0 ? fullContext : null,
          })
          .select()
          .single()
        if (assistantMsg) setMessages((prev) => [...prev, assistantMsg])
        await supabase.from('bot_conversations').update({ updated_at: new Date().toISOString() }).eq('id', conversation.id)
      }

      setStreamingText('')
      setStreamingContext([])
      setSending(false)
      abortRef.current = null
    },
    [conversation, messages, sending],
  )

  const stop = useCallback(() => {
    abortRef.current?.abort()
  }, [])

  return { messages, loading, sending, streamingText, streamingContext, error, send, stop, refresh }
}
