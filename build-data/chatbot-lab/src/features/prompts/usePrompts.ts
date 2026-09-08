import { useCallback, useEffect, useState } from 'react'
import { supabase } from '../../lib/supabaseClient'
import type { PromptCategory, PromptRow } from '../../lib/types'

export function usePrompts() {
  const [prompts, setPrompts] = useState<PromptRow[]>([])
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    const { data } = await supabase
      .from('bot_prompts')
      .select('*')
      .order('is_pinned', { ascending: false })
      .order('usage_count', { ascending: false })
      .order('updated_at', { ascending: false })
    setPrompts(data ?? [])
    setLoading(false)
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  const create = useCallback(
    async (input: { title: string; content: string; category: PromptCategory }) => {
      await supabase.from('bot_prompts').insert(input)
      await refresh()
    },
    [refresh],
  )

  const update = useCallback(
    async (id: string, patch: Partial<Pick<PromptRow, 'title' | 'content' | 'category' | 'is_pinned'>>) => {
      await supabase.from('bot_prompts').update(patch).eq('id', id)
      await refresh()
    },
    [refresh],
  )

  const remove = useCallback(
    async (id: string) => {
      await supabase.from('bot_prompts').delete().eq('id', id)
      await refresh()
    },
    [refresh],
  )

  const markUsed = useCallback(async (id: string, currentCount: number) => {
    await supabase.from('bot_prompts').update({ usage_count: currentCount + 1 }).eq('id', id)
  }, [])

  return { prompts, loading, create, update, remove, markUsed, refresh }
}
