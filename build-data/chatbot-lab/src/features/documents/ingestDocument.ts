import { supabase } from '../../lib/supabaseClient'
import { embedTexts } from '../../lib/edgeFunctions'
import type { DocumentFileType } from '../../lib/types'
import { chunkText } from './chunk'

const EMBED_BATCH_SIZE = 64

function detectFileType(file: File): DocumentFileType | null {
  const name = file.name.toLowerCase()
  if (name.endsWith('.pdf')) return 'pdf'
  if (name.endsWith('.docx')) return 'docx'
  if (name.endsWith('.xlsx') || name.endsWith('.xls')) return 'xlsx'
  if (name.endsWith('.txt') || name.endsWith('.md')) return 'txt'
  return null
}

async function extractText(file: File, type: DocumentFileType): Promise<string> {
  switch (type) {
    case 'pdf':
      return (await import('./parsePdf')).parsePdf(file)
    case 'docx':
      return (await import('./parseDocx')).parseDocx(file)
    case 'xlsx':
      return (await import('./parseXlsx')).parseXlsx(file)
    case 'txt':
      return file.text()
  }
}

export interface IngestProgress {
  stage: 'parsing' | 'embedding' | 'saving' | 'done' | 'failed'
  detail?: string
}

export async function ingestDocument(
  file: File,
  onProgress?: (p: IngestProgress) => void,
): Promise<string> {
  const fileType = detectFileType(file)
  if (!fileType) {
    throw new Error(`지원하지 않는 파일 형식입니다: ${file.name} (pdf/docx/xlsx/txt만 가능)`)
  }

  const { data: doc, error: insertErr } = await supabase
    .from('bot_documents')
    .insert({ filename: file.name, file_type: fileType, status: 'processing' })
    .select()
    .single()
  if (insertErr || !doc) throw insertErr ?? new Error('문서 레코드 생성 실패')

  try {
    onProgress?.({ stage: 'parsing' })
    const text = await extractText(file, fileType)
    const chunks = chunkText(text)
    if (chunks.length === 0) throw new Error('문서에서 텍스트를 추출하지 못했습니다.')

    onProgress?.({ stage: 'embedding', detail: `${chunks.length}개 청크` })
    const embeddings: number[][] = []
    for (let i = 0; i < chunks.length; i += EMBED_BATCH_SIZE) {
      const batch = chunks.slice(i, i + EMBED_BATCH_SIZE)
      const vectors = await embedTexts(batch)
      embeddings.push(...vectors)
      onProgress?.({ stage: 'embedding', detail: `${embeddings.length}/${chunks.length}` })
    }

    onProgress?.({ stage: 'saving' })
    const rows = chunks.map((content, idx) => ({
      document_id: doc.id,
      chunk_index: idx,
      content,
      embedding: `[${embeddings[idx].join(',')}]`,
    }))
    const { error: chunksErr } = await supabase.from('bot_document_chunks').insert(rows)
    if (chunksErr) throw chunksErr

    await supabase
      .from('bot_documents')
      .update({ status: 'ready', char_count: text.length, chunk_count: chunks.length })
      .eq('id', doc.id)

    onProgress?.({ stage: 'done' })
    return doc.id
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err)
    await supabase.from('bot_documents').update({ status: 'failed', error_message: message }).eq('id', doc.id)
    onProgress?.({ stage: 'failed', detail: message })
    throw err
  }
}
