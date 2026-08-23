const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export async function uploadDocument(file: File) {
  const form = new FormData(); form.append('file', file)
  const r = await fetch(`${API}/upload`, { method: 'POST', body: form })
  const data = await r.json(); if (!r.ok) throw new Error(data.detail || 'Upload failed')
  return data
}

export async function summarize(document_id: string, length: string) {
  const r = await fetch(`${API}/summarize`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({document_id, length}) })
  const data = await r.json(); if (!r.ok) throw new Error(data.detail || 'Summary failed')
  return data
}

export async function chat(document_id: string, question: string) {
  const r = await fetch(`${API}/chat`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({document_id, question}) })
  const data = await r.json(); if (!r.ok) throw new Error(data.detail || 'Chat failed')
  return data
}
