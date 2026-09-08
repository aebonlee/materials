import * as XLSX from 'xlsx'

export async function parseXlsx(file: File): Promise<string> {
  const buffer = await file.arrayBuffer()
  const workbook = XLSX.read(buffer, { type: 'array' })
  const sheetTexts = workbook.SheetNames.map((name) => {
    const sheet = workbook.Sheets[name]
    const csv = XLSX.utils.sheet_to_csv(sheet)
    return `## 시트: ${name}\n${csv}`
  })
  return sheetTexts.join('\n\n')
}
