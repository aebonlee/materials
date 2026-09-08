import type { Paragraph as DocxParagraph } from 'docx'
import type { Conversation, Message } from '../../lib/types'

function messageToParagraphs(
  { Paragraph, TextRun }: typeof import('docx'),
  message: Message,
): DocxParagraph[] {
  const speaker = message.role === 'user' ? '나' : 'AI'
  const lines = message.content.split('\n')
  return [
    new Paragraph({
      spacing: { before: 200 },
      children: [new TextRun({ text: `${speaker}`, bold: true })],
    }),
    ...lines.map((line) => new Paragraph({ children: [new TextRun(line)] })),
  ]
}

export async function exportConversationAsDocx(conversation: Conversation, messages: Message[]) {
  const docx = await import('docx')
  const { Document, HeadingLevel, Packer, Paragraph, TextRun } = docx

  const doc = new Document({
    sections: [
      {
        children: [
          new Paragraph({
            heading: HeadingLevel.TITLE,
            children: [new TextRun(conversation.title)],
          }),
          new Paragraph({
            children: [
              new TextRun({
                text: `생성일: ${new Date(conversation.created_at).toLocaleString('ko-KR')}`,
                italics: true,
                size: 18,
              }),
            ],
          }),
          ...messages.flatMap((m) => messageToParagraphs(docx, m)),
        ],
      },
    ],
  })

  const blob = await Packer.toBlob(doc)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${conversation.title || '대화'}.docx`
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

export function exportMessageAsMarkdown(message: Message) {
  const blob = new Blob([message.content], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `응답-${new Date(message.created_at).getTime()}.md`
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}
