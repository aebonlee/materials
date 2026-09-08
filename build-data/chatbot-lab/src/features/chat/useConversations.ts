import { useCallback, useEffect, useState } from 'react'
import { supabase } from '../../lib/supabaseClient'
import type { Conversation, ConversationMode, Provider } from '../../lib/types'

export function useConversations() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    const { data } = await supabase
      .from('bot_conversations')
      .select('*')
      .order('updated_at', { ascending: false })
    setConversations(data ?? [])
    setLoading(false)
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  const create = useCallback(
    async (input: {
      title?: string
      mode?: ConversationMode
      system_prompt?: string
      provider?: Provider
      model?: string
    }) => {
      const { data, error } = await supabase
        .from('bot_conversations')
        .insert({
          title: input.title || '새 대화',
          mode: input.mode || 'general',
          system_prompt: input.system_prompt || '',
          provider: input.provider || 'openai',
          model: input.model || 'gpt-4.1-mini',
        })
        .select()
        .single()
      if (error || !data) throw error ?? new Error('대화 생성 실패')
      await refresh()
      return data as Conversation
    },
    [refresh],
  )

  const update = useCallback(
    async (id: string, patch: Partial<Conversation>) => {
      await supabase.from('bot_conversations').update(patch).eq('id', id)
      await refresh()
    },
    [refresh],
  )

  const remove = useCallback(
    async (id: string) => {
      await supabase.from('bot_conversations').delete().eq('id', id)
      await refresh()
    },
    [refresh],
  )

  return { conversations, loading, create, update, remove, refresh }
}
