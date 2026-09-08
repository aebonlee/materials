export type Provider = 'openai' | 'solar' | 'anthropic' | 'gemini'
export type ConversationMode = 'general' | 'qa' | 'summary' | 'report'
export type MessageRole = 'system' | 'user' | 'assistant'
export type PromptCategory = 'general' | 'qa' | 'summary' | 'report' | 'custom'
export type DocumentStatus = 'processing' | 'ready' | 'failed'
export type DocumentFileType = 'pdf' | 'docx' | 'xlsx' | 'txt'

export interface Conversation {
  id: string
  title: string
  mode: ConversationMode
  system_prompt: string
  provider: Provider
  model: string
  use_rag: boolean
  rag_document_ids: string[]
  created_at: string
  updated_at: string
}

export interface ChatContextChunk {
  id: string
  document_id: string
  chunk_index: number
  content: string
  similarity: number
}

export interface Message {
  id: string
  conversation_id: string
  role: MessageRole
  content: string
  context: ChatContextChunk[] | null
  created_at: string
}

export interface DocumentRow {
  id: string
  filename: string
  file_type: DocumentFileType
  char_count: number
  chunk_count: number
  status: DocumentStatus
  error_message: string | null
  created_at: string
}

export interface PromptRow {
  id: string
  title: string
  content: string
  category: PromptCategory
  is_pinned: boolean
  usage_count: number
  created_at: string
  updated_at: string
}
