import { useCallback, useEffect, useState } from 'react'
import { supabase } from '../../lib/supabaseClient'
import type { DocumentRow } from '../../lib/types'
import { ingestDocument, type IngestProgress } from './ingestDocument'

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentRow[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState<Record<string, IngestProgress>>({})

  const refresh = useCallback(async () => {
    setLoading(true)
    const { data } = await supabase
      .from('bot_documents')
      .select('*')
      .order('created_at', { ascending: false })
    setDocuments(data ?? [])
    setLoading(false)
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  const upload = useCallback(
    async (file: File) => {
      const key = `${file.name}-${file.size}-${Date.now()}`
      setUploading((prev) => ({ ...prev, [key]: { stage: 'parsing' } }))
      try {
        await ingestDocument(file, (p) => {
          setUploading((prev) => ({ ...prev, [key]: p }))
        })
      } finally {
        await refresh()
        setUploading((prev) => {
          const next = { ...prev }
          delete next[key]
          return next
        })
      }
    },
    [refresh],
  )

  const remove = useCallback(
    async (id: string) => {
      await supabase.from('bot_documents').delete().eq('id', id)
      await refresh()
    },
    [refresh],
  )

  return { documents, loading, uploading, upload, remove, refresh }
}
