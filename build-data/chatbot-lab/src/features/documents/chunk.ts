// 문자 수 기준 청크 분할 (임베딩 모델 토큰 한도를 넉넉히 피하기 위한 근사치). 문단 경계를 우선 존중한다.
const CHUNK_SIZE = 1000
const CHUNK_OVERLAP = 150

export function chunkText(text: string): string[] {
  const normalized = text.replace(/\r\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim()
  if (!normalized) return []

  const paragraphs = normalized.split(/\n\n+/)
  const chunks: string[] = []
  let current = ''

  for (const paragraph of paragraphs) {
    if ((current + '\n\n' + paragraph).length <= CHUNK_SIZE) {
      current = current ? `${current}\n\n${paragraph}` : paragraph
      continue
    }
    if (current) chunks.push(current)

    if (paragraph.length <= CHUNK_SIZE) {
      current = paragraph
    } else {
      // 문단 자체가 너무 길면 강제로 자른다
      for (let i = 0; i < paragraph.length; i += CHUNK_SIZE - CHUNK_OVERLAP) {
        chunks.push(paragraph.slice(i, i + CHUNK_SIZE))
      }
      current = ''
    }
  }
  if (current) chunks.push(current)

  return chunks.filter((c) => c.trim().length > 0)
}
